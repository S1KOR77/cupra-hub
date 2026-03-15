# 📦 CUPRA HUB v2.0 — Setup Guide

## Co się zmieniło?

### Było:
```
❌ Server działa tylko na Twoim komputerze
❌ Trzeba ręcznie uruchamiać scraper
❌ Jeśli wyłączysz PC = strona offline
❌ Data.json ręczna aktualizacja
```

### Teraz:
```
✅ Server zawsze online na Railway.app (cloud)
✅ Scraper uruchamia się automatycznie co dzień (06:00 UTC)
✅ Strona dostępna 24/7
✅ Data.json auto-updateje się codziennie
✅ Brak zależności od Twojego komputera
```

## 📁 Pliki które dodałem:

| Plik | Co robi |
|------|---------|
| `server.py` | **Enhanced** - wbudowany scheduler + logging |
| `requirements.txt` | Zależności (requests, openpyxl, APScheduler) |
| `Procfile` | Instrukcja dla Railway jak uruchomić |
| `runtime.txt` | Python v3.11 |
| `DEPLOYMENT.md` | Instrukcje wdrażania krok po kroku |
| `.gitignore` | Pliki które się nie pushują do GitHub |

## 🚀 Jak wdrożyć (3 kroki):

### Opcja A: Automatycznie (Najłatwiej)

**TL;DR - Wyślij mi:**
- ✅ GitHub login
- ✅ Email do GitHub
- ✅ Czy lubisz godzinę 06:00 UTC czy inna?

Ja się zajmę całym deployment'em.

### Opcja B: Sam deployment (30 minut)

Jeśli masz GitHub konto:
1. Utwórz repo: `cupra-hub`
2. Push te pliki tam
3. Idź do railway.app i connectuj repo
4. Deploy! 🎉

**Patrz `DEPLOYMENT.md` dla szczegółów**

## 🎯 Co się będzie dziać co dzień?

```
06:00 UTC (codziennie):
  ↓
  Server uruchamia scraper
  ↓
  Scraper scrapuje 29 dealerów Otomoto
  ↓
  Liczy marże, rabatyidealnie
  ↓
  Zapisuje nowe auta do data.json
  ↓
  Strona refresh'uje dane automatycznie
  ↓
  ✨ Dane zawsze aktualne!
```

## 💾 Edycja rabatów

**Stare:**
```
Edytujesz w settings.json lokalnie
→ Refreshujesz stronę na swoim PC
```

**Nowe:**
```
Edytujesz settings.json w GitHub
→ Git push
→ Railway automatycznie wdrażaRedeploy
→ Wszyscy widzą nowe rabaty w ~2 minuty
```

## 🔧 Problemy?

**Scraper się nie uruchomił?**
- ✅ Check Logs na Railway dashboard
- ✅ Sprawdzić czy Otomoto nie zmienił struktury strony
- ✅ Czasami Otomoto rate-limituje - to OK, retry'uje

**Strona nie się updatowuje?**
- ✅ Sprawdź czy `data.json` jest recent (patrz timestamp)
- ✅ Jeśli > 24h stare = scraper się nie uruchomił

**Railway pokazuje błąd?**
- ✅ Sprawdzić czy requirements.txt ma Python 3.11+
- ✅ Sprawdzić czy Procfile jest OK

## 📊 Szczegóły techniczne

### Server (HTTP):
- Port: Dynamiczny (Railway przydzela)
- Handler: SimpleHTTPRequestHandler + custom API endpoints
- Routing:
  - `GET /` → `index.html` (frontend)
  - `GET /api/data` → `data.json` (auta)
  - `GET /api/settings` → `settings.json` (rabaty)
  - `POST /api/settings` → Zapisz zmiany rabatów
  - `GET /api/status` → Status servera

### Scheduler:
- **Engine**: APScheduler (BackgroundScheduler)
- **Trigger**: Cron - codziennie o 06:00 UTC
- **Job**: `run_scraper()` → subprocess `goliath_v11.py`
- **Timeout**: 3600s (1 godzina)
- **Logging**: `logger.info()` → Railway logs

### Scraper (goliath_v11.py):
- **Działanie**: Przeskanuj wszystkie 29 salonów CUPRA
- **Dane**: Otomoto inventory
- **Wyjście**: `data.json` (auta) + `CUPRA_INVENTORY.xlsx` (Excel)
- **Smart Cache**: Nie rescrapuje auta które są OK (marża w normie)

## 🎨 Co następnie?

Po wdrażaniu (ostateczny polish):
1. Instant app (nowoczesny UI zamiast HTML)
2. Dark mode improvements
3. Responsive design
4. Mobile app?

## 📞 Pytania?

Jeśli coś nie jasne - pytaj! 🎯

---

**Status:** Ready for deployment ✅
**Cost:** Free tier Railway (~1-2 USD/miesiąc) 💰
**Uptime:** 24/7 ✨
