import http.server
import socketserver
import json
import os
import shutil
import subprocess
import threading
import time
from urllib.parse import urlparse, parse_qs
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get('PORT', 8080))

# ─────────── Railway Volume ───────────
# Na Railway: ustaw zmienną środowiskową VOLUME_PATH=/data
# i dodaj Volume zamontowany pod /data w dashboardzie Railway.
# Lokalnie: pliki zostają w BASE_DIR (brak zmian).
VOLUME_PATH = os.environ.get('VOLUME_PATH', BASE_DIR)


def pf(filename):
    """Zwraca pełną ścieżkę do trwałego pliku danych (na Volume)."""
    return os.path.join(VOLUME_PATH, filename)


def migrate_to_volume():
    """Przy pierwszym uruchomieniu kopiuje istniejące pliki do Volume."""
    if VOLUME_PATH == BASE_DIR:
        return
    os.makedirs(VOLUME_PATH, exist_ok=True)
    for fn in ['data.json', 'settings.json', 'manual_overrides.json']:
        src = os.path.join(BASE_DIR, fn)
        dst = pf(fn)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f'[volume] Migracja {fn} → {VOLUME_PATH}')


# ─────────── scraper log buffer ───────────
SCRAPER_LOGS = []
SCRAPER_RUNNING = False
SCRAPER_LOCK = threading.Lock()
MAX_LOG_LINES = 500

def log_append(msg):
    ts = datetime.utcnow().strftime('%H:%M:%S')
    line = f'[{ts}] {msg}'
    with SCRAPER_LOCK:
        SCRAPER_LOGS.append(line)
        if len(SCRAPER_LOGS) > MAX_LOG_LINES:
            SCRAPER_LOGS.pop(0)

def run_scraper_background():
    global SCRAPER_RUNNING
    with SCRAPER_LOCK:
        if SCRAPER_RUNNING:
            return False
        SCRAPER_RUNNING = True
    SCRAPER_LOGS.clear()
    log_append('🚀 Scraper uruchomiony')

    def worker():
        global SCRAPER_RUNNING
        try:
            script = os.path.join(BASE_DIR, 'goliath_v11.py')
            proc = subprocess.Popen(
                ['python3', '-u', script],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, cwd=BASE_DIR
            )
            for line in proc.stdout:
                log_append(line.rstrip())
            proc.wait()
            log_append(f'✅ Scraper zakończony (kod: {proc.returncode})')

            # Skopiuj data.json z BASE_DIR na Volume (jeśli różne ścieżki)
            if VOLUME_PATH != BASE_DIR:
                src = os.path.join(BASE_DIR, 'data.json')
                dst = pf('data.json')
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    log_append(f'💾 data.json skopiowany na Volume ({VOLUME_PATH})')

        except Exception as e:
            log_append(f'❌ Błąd: {e}')
        finally:
            with SCRAPER_LOCK:
                SCRAPER_RUNNING = False

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return True


class CupraHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # suppress default access log

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path in ('/', '/index.html'):
            self._serve_file('index.html', 'text/html')
        elif parsed.path == '/api/data':
            self._serve_json_file(pf('data.json'))
        elif parsed.path == '/api/logs':
            with SCRAPER_LOCK:
                running = SCRAPER_RUNNING
                lines = list(SCRAPER_LOGS)
            self._send_json({'running': running, 'logs': lines})
        elif parsed.path == '/api/settings':
            self._serve_json_file(pf('settings.json'))
        elif parsed.path == '/api/overrides':
            self._serve_json_file(pf('manual_overrides.json'))
        else:
            self.send_error(404, 'Not found')

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/settings':
            self._save_settings()
        elif parsed.path == '/api/overrides':
            self._save_override()
        elif parsed.path == '/api/overrides/delete':
            self._delete_override()
        elif parsed.path == '/api/overrides/clear':
            self._clear_overrides()
        elif parsed.path == '/run-scraper':
            self._trigger_scraper()
        else:
            self.send_error(404, 'Not found')

    def do_OPTIONS(self):
        self.send_response(200)
        self._add_cors_headers()
        self.end_headers()

    def _trigger_scraper(self):
        """Ręczne uruchomienie scrapera."""
        started = run_scraper_background()
        if started:
            self._send_json({'status': 'started', 'message': 'Scraper uruchomiony'})
        else:
            self._send_json({'status': 'already_running', 'message': 'Scraper już działa'})

    def _serve_file(self, filename, content_type):
        filepath = os.path.join(BASE_DIR, filename)
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(data))
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self._add_cors_headers()
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_error(404, f'{filename} not found')

    def _serve_json_file(self, filepath):
        """Serwuje plik JSON pod podaną pełną ścieżką."""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(data))
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self._add_cors_headers()
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            # Return empty JSON for optional files
            empty = b'{}'
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(empty))
            self._add_cors_headers()
            self.end_headers()
            self.wfile.write(empty)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Cache-Control', 'no-store')
        self._add_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _add_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _save_settings(self):
        """Zapisz settings.json na Volume."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            os.makedirs(VOLUME_PATH, exist_ok=True)
            with open(pf('settings.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self._send_json({'success': True})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)

    def _save_override(self):
        """Zapisz nadpisanie ceny dla konkretnego samochodu na Volume."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            otomoto_id = str(data.get('otomoto_id', '')).strip()
            if not otomoto_id:
                self._send_json({'error': 'Brak otomoto_id'}, 400)
                return

            os.makedirs(VOLUME_PATH, exist_ok=True)
            filepath = pf('manual_overrides.json')
            overrides = {}
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    overrides = json.load(f)

            entry = {}
            if data.get('sale_price') is not None:
                entry['sale_price'] = float(data['sale_price'])
            if data.get('catalog_price') is not None:
                entry['catalog_price'] = float(data['catalog_price'])
            if data.get('dealer_cost') is not None:
                entry['dealer_cost'] = float(data['dealer_cost'])
            if data.get('discount') is not None:
                entry['discount'] = float(data['discount'])
            if data.get('anomaly_resolved') is not None:
                entry['anomaly_resolved'] = bool(data['anomaly_resolved'])

            if entry:
                overrides[otomoto_id] = entry
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(overrides, f, ensure_ascii=False, indent=2)

            self._send_json({'success': True, 'saved': entry})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)

    def _delete_override(self):
        """Usuń nadpisanie dla konkretnego samochodu z Volume."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            otomoto_id = str(data.get('otomoto_id', '')).strip()
            if not otomoto_id:
                self._send_json({'error': 'Brak otomoto_id'}, 400)
                return

            filepath = pf('manual_overrides.json')
            overrides = {}
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    overrides = json.load(f)
            overrides.pop(otomoto_id, None)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(overrides, f, ensure_ascii=False, indent=2)

            self._send_json({'success': True})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)

    def _clear_overrides(self):
        """Wyczyść wszystkie nadpisania cen na Volume."""
        try:
            os.makedirs(VOLUME_PATH, exist_ok=True)
            with open(pf('manual_overrides.json'), 'w', encoding='utf-8') as f:
                json.dump({}, f)
            self._send_json({'success': True})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)


def auto_start_scraper():
    """Uruchom scraper przy starcie serwera jeśli brak świeżych danych."""
    data_file = pf('data.json')
    # Fallback: sprawdź też BASE_DIR (dla lokalnego developmentu)
    if not os.path.exists(data_file) and VOLUME_PATH != BASE_DIR:
        data_file = os.path.join(BASE_DIR, 'data.json')

    should_run = True
    if os.path.exists(data_file):
        age = time.time() - os.path.getmtime(data_file)
        if age < 3600:  # < 1 godzina
            should_run = False
            print(f'[auto-start] data.json ma {int(age/60)} min — pomijam start scrapera')
    if should_run:
        print('[auto-start] Uruchamiam scraper automatycznie...')
        run_scraper_background()


if __name__ == '__main__':
    print(f'[server] CUPRA Hub v2.4 — port {PORT}')
    print(f'[server] VOLUME_PATH={VOLUME_PATH}')
    migrate_to_volume()
    auto_start_scraper()
    with socketserver.TCPServer(('', PORT), CupraHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f'[server] Nasłuchuję na :{PORT}')
        httpd.serve_forever()
