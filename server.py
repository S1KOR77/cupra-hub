#!/usr/bin/env python3
"""
CUPRA HUB — HTTP Server + Auto Scraper v2.1
Serwuje pliki statyczne + API do odczytu/zapisu ustawień.
Automatycznie uruchamia scraper co dzień o 06:00 UTC.
Endpoint /run-scraper do ręcznego uruchomienia.
"""
import http.server
import json
import os
import sys
import time
import threading
import logging
import subprocess
from urllib.parse import urlparse, parse_qs
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

PORT = int(os.environ.get('PORT', 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Track scraper state
scraper_state = {
    'running': False,
    'last_run': None,
    'last_status': None,
    'last_duration': None,
}
scraper_lock = threading.Lock()


class CupraHandler(http.server.SimpleHTTPRequestHandler):
    """Handler z API endpointami."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/settings':
            self._serve_json_file('settings.json')
        elif parsed.path == '/api/data':
            self._serve_json_file('data.json')
        elif parsed.path == '/api/status':
            self._send_json({
                'status': 'ok',
                'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'data_exists': os.path.exists(os.path.join(BASE_DIR, 'data.json')),
                'settings_exists': os.path.exists(os.path.join(BASE_DIR, 'settings.json')),
                'server_version': '2.1-railway',
                'scraper': scraper_state,
            })
        elif parsed.path == '/run-scraper':
            self._trigger_scraper()
        elif parsed.path == '/' or parsed.path == '':
            self.path = '/index.html'
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/settings':
            self._save_json_file('settings.json')
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
        if scraper_state['running']:
            self._send_json({
                'status': 'already_running',
                'message': 'Scraper jest już uruchomiony',
                'started_at': scraper_state.get('last_run', '')
            })
            return

        # Start in background thread
        thread = threading.Thread(target=run_scraper, daemon=True)
        thread.start()
        self._send_json({
            'status': 'started',
            'message': 'Scraper uruchomiony w tle',
            'time': time.strftime('%Y-%m-%d %H:%M:%S')
        })

    def _serve_json_file(self, filename):
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(filepath):
            self._send_json({'error': f'{filename} nie znaleziony'}, 404)
            return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._send_json(data)
        except Exception as e:
            self._send_json({'error': str(e)}, 500)

    def _save_json_file(self, filename):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            filepath = os.path.join(BASE_DIR, filename)

            # Backup
            if os.path.exists(filepath):
                backup = filepath + '.backup'
                with open(filepath, 'r', encoding='utf-8') as f:
                    old_data = f.read()
                with open(backup, 'w', encoding='utf-8') as f:
                    f.write(old_data)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self._send_json({'status': 'saved', 'file': filename, 'time': time.strftime('%Y-%m-%d %H:%M:%S')})
        except Exception as e:
            self._send_json({'error': str(e)}, 500)

    def _send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._add_cors_headers()
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _add_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, format, *args):
        # Log only errors
        if '404' in str(args) or '500' in str(args):
            super().log_message(format, *args)


def run_scraper():
    """Uruchom scraper (goliath_v11.py)."""
    with scraper_lock:
        if scraper_state['running']:
            logger.info("⚠️ Scraper already running, skipping")
            return
        scraper_state['running'] = True
        scraper_state['last_run'] = time.strftime('%Y-%m-%d %H:%M:%S')

    start = time.time()
    try:
        logger.info("🔄 Uruchamianie scrapera CUPRA...")
        result = subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, 'goliath_v11.py')],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        duration = round(time.time() - start, 1)
        scraper_state['last_duration'] = f"{duration}s"

        if result.returncode == 0:
            scraper_state['last_status'] = 'success'
            logger.info(f"✅ Scraper zakończył się pomyślnie ({duration}s)")
            logger.info(result.stdout[-1000:] if result.stdout else "No output")
        else:
            scraper_state['last_status'] = 'error'
            logger.error(f"❌ Scraper failed ({duration}s): {result.stderr[-1000:]}")
            if result.stdout:
                logger.error(f"stdout: {result.stdout[-500:]}")
    except subprocess.TimeoutExpired:
        scraper_state['last_status'] = 'timeout'
        logger.error("❌ Scraper timeout (>1h)")
    except Exception as e:
        scraper_state['last_status'] = 'exception'
        logger.error(f"❌ Scraper error: {str(e)}")
    finally:
        scraper_state['running'] = False


def schedule_scraper():
    """Skonfiguruj scheduler do codziennego scrapowania o 06:00 UTC."""
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        run_scraper,
        'cron',
        hour=6,
        minute=0,
        timezone='UTC',
        id='daily_scraper'
    )
    scheduler.start()
    logger.info("⏰ Scheduler uruchomiony - scraper będzie działać codziennie o 06:00 UTC")


def main():
    # Zmień na UTF-8 na Windows
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    os.chdir(BASE_DIR)

    # Uruchom scheduler
    schedule_scraper()

    # Uruchom serwer na 0.0.0.0 (dostępny z całego internetu)
    bind_address = ('0.0.0.0', PORT)
    server = http.server.HTTPServer(bind_address, CupraHandler)

    logger.info(f"🚀 CUPRA HUB Server v2.1 uruchomiony na porcie {PORT}")
    logger.info(f"📍 Dostępny pod: http://0.0.0.0:{PORT}")
    logger.info(f"📂 Baza danych: {BASE_DIR}")
    logger.info(f"🔗 Ręczne uruchomienie: GET /run-scraper")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("⏹️ Server zatrzymany.")
        server.server_close()


if __name__ == '__main__':
    main()
