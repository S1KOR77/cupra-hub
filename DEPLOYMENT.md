# 🚀 CUPRA HUB — Deployment na Railway.app (Bezpłatnie)

## Co to Railway?
Railway to **cloud hosting** — Twoja aplikacja będzie dostępna 24/7 z publicznym URL, niezależnie od Twojego komputera.

## Krok po kroku:

### 1️⃣ Przygotowanie repo GitHub
```bash
# Jeśli nie masz repo, utwórz je:
# https://github.com/new

# Sklonuj lokalna wersję
git clone https://github.com/TWOJ_LOGIN/cupra-hub.git
cd cupra-hub

# Skopiuj pliki z tego folderu
# (wszystkie pliki: server.py, goliath_v11.py, settings.json, data.json, index.html, requirements.txt, Procfile, runtime.txt)

git add .
git commit -m "Initial CUPRA HUB deployment"
git push origin main
```

### 2️⃣ Połącz Railway z repo
1. Idź do: https://railway.app/
2. Kliknij **"New Project"**
3. Wybierz **"Deploy from GitHub"**
4. Zaloguj się GitHub i wybierz repo `cupra-hub`
5. Railway automatycznie wydetektuje `Procfile` i zainstaluje zależności

### 3️⃣ Czekaj na deploy
Railway będzie:
- ✅ Instalować zależności z `requirements.txt`
- ✅ Uruchamiać `python server.py` (z `Procfile`)
- ✅ Przydzielić publiczny URL

### 4️⃣ Sprawdź status
Po ~2-3 minutach:
- Pokaże się URL: `https://cupra-hub-xxxxx.up.railway.app/`
- Strona powinna być dostępna!

### 5️⃣ Scheduler — Codzienne scrapowanie
Server automatycznie będzie:
- ⏰ Uruchamiać scraper **codziennie o 06:00 UTC**
- 📊 Aktualizować `data.json`
- 🔄 Reloadować danymi stronę

Możesz zmienić godzinę w `server.py` (linia ~168):
```python
scheduler.add_job(
    run_scraper,
    'cron',
    hour=6,      # ← Zmień na inną godzinę (0-23)
    minute=0,
    timezone='UTC',
    id='daily_scraper'
)
```

## 📝 Zmiana rabatów

Edytuj `settings.json` w repo:
1. Modyfikuj rabaty w `settings.json`
2. Commituj: `git push origin main`
3. Railway automatycznie redeploy'uje się w ~1-2 minuty

## 🔧 Debugging

Jeśli scraper nie działa:
1. Idź do: https://railway.app/project (Twój projekt)
2. Kliknij **"Deployments"** → ostatni deploy
3. Popatrz na **Logs**

## Koszt
- **Free tier Railway**: 5 USD credytów na miesiąc (dla Ciebie więcej niż wystarczy)
- Tym projektem zużyjesz ~1-2 USD/miesiąc
- ✅ Praktycznie bezpłatnie

## 🎯 Podsumowanie
- ✅ Aplikacja online 24/7
- ✅ Scraper codziennie (06:00 UTC)
- ✅ Dane się auto-updateją
- ✅ Brak zależności od Twojego komputera
- ✅ Edytowanie rabatów poprzez GitHub
- ✅ Bezpłatnie

Powodzenia! 🚀
