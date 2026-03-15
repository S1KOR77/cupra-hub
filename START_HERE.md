# 🎯 START HERE - CUPRA HUB v2.0

## 👋 Witaj S1KOR__!

Masz gotowy projekt CUPRA HUB do wdrażania na Internet! 🚀

---

## 📁 Co jest w tym folderze?

```
cupra-project/
├── 🎯 START_HERE.md ← TY TUTAJ (czytaj to!)
├── 📖 INSTRUKCJA_DEPLOYMENT_S1KOR.md ← GŁÓWNA INSTRUKCJA (step-by-step)
├── ⚙️  DEPLOY_COMMANDS.sh ← Gotowe komendy (copy-paste)
├── 💻 server.py ← Server z wbudowanym schedulerem
├── 🐍 goliath_v11.py ← Scraper (auto-uruchamia się codziennie)
├── 📄 index.html ← Twoja ładna strona
├── 📊 data.json ← Auta (auto-updateja się)
├── ⚙️  settings.json ← Rabaty (edytujesz tu)
├── 📦 requirements.txt ← Zależności Python
├── 🚂 Procfile ← Instrukcja dla Railway
├── 🔧 runtime.txt ← Python 3.11
└── .gitignore ← Co się nie pushuje na GitHub
```

---

## 🎬 Szybki start (3 minuty)

### ✅ Co masz gotowe:
- ✅ Scraper (goliath_v11.py) - działa
- ✅ Strona (index.html) - piękna
- ✅ Server (server.py) - ma scheduler wbudowany
- ✅ Wszystkie config pliki (requirements, Procfile, itp.)

### 🎯 Co musisz zrobić:
1. **Przeczytaj:** `INSTRUKCJA_DEPLOYMENT_S1KOR.md`
2. **Uruchom:** Komendy z `DEPLOY_COMMANDS.sh` (copy-paste)
3. **Wdrażaj:** Railway.app (link w instrukcji)
4. **Testuj:** Strona będzie dostępna online
5. **Świetnie!** Scraper będzie się uruchamiać codziennie o 06:00 UTC

---

## 📖 GŁÓWNA INSTRUKCJA

Wszystko jest w:
### **👉 INSTRUKCJA_DEPLOYMENT_S1KOR.md**

**Zawiera:**
- KROK 1️⃣ - GitHub setup
- KROK 2️⃣ - Push plików
- KROK 3️⃣ - Railway deployment
- KROK 4️⃣ - Test
- Troubleshooting

---

## ⚡ Tldr; (super szybko)

1. **GitHub:** Nowe repo `cupra-hub` (public)
2. **Git:** `git init` + `git push -u origin main`
3. **Railway:** Connect repo → Auto-deploy
4. **Test:** Otwórz URL strony
5. **Done!** Strona online 24/7 ✅

---

## 🤖 Co się będzie działo automatycznie?

```
Każdego dnia o 06:00 UTC (codziennie):

  🕕 06:00 → Scheduler uruchamia scraper
    ↓
  🔄 Scraper scanuje 29 dealerów Otomoto
    ↓
  💾 Aktualizuje data.json
    ↓
  🌐 Strona odświeża dane
    ↓
  ✨ Wszyscy widzą świeże auta!

  Resztę dnia: Strona dostępna 24/7
```

---

## 🎯 Jakie URL'e będą dostępne:

```
🏠 Strona:        https://cupra-hub-production.up.railway.app/
📊 API auta:      https://cupra-hub-production.up.railway.app/api/data
⚙️  API rabaty:   https://cupra-hub-production.up.railway.app/api/settings
📡 Status:        https://cupra-hub-production.up.railway.app/api/status
```

---

## 💡 Edycja rabatów bez restarta servera

1. Otwórz GitHub: `github.com/S1KOR__/cupra-hub`
2. Klikni na `settings.json` → Edit ✏️
3. Zmień wartości (np. `discount_multiplier`)
4. Commit
5. Railway automatycznie redeploy'uje (~1 minuta)
6. ✅ Nowe rabaty są live!

---

## 🆘 Jeśli będą problemy:

### Gdzie szukać pomocy:
1. **Błędy GitHub/Git:** Patrz sekcja "Problemy?" w instrukcji
2. **Błędy Railway:** Sprawdź `Logs` w Railway dashboard
3. **Scraper się nie uruchomia:** Check Railway logs (APScheduler)
4. **Strona nie ładuje się:** Sprawdź czy deployment jest successful ✅

### Jeśli stuck:
- Skopiuj **pełny tekst błędu** z Logs
- Napisz mi na Tasklet
- Najlepiej ze screenshotem

---

## 📊 Techniczne detale (dla dociekliwych)

| Komponent | Rola | Autoryzacja |
|-----------|------|-------------|
| **server.py** | HTTP server + Scheduler | Biegnie na Railway |
| **goliath_v11.py** | Web scraper (Otomoto) | Uruchamia się codziennie |
| **APScheduler** | Cron scheduler | Built-in w server.py |
| **data.json** | Database aut | Auto-updateja się |
| **index.html** | Frontend | Ładuje się z /api/data |
| **Railway** | Cloud hosting | 24/7 uptime |

---

## 💰 Koszt

| Resource | Koszt | Notes |
|----------|-------|-------|
| Railway (free) | $0 | Do 500h/miesiąc, wystarczy |
| GitHub | $0 | Public repo FREE |
| Domain | $0 | railway.app subdomain FREE |
| **TOTAL** | **$0** | 🎉 Zupełnie darmowe! |

---

## ✅ Checklist przed deployment'em

- [ ] Masz konto GitHub (S1KOR__)
- [ ] Git zainstalowany na komputerze
- [ ] Przeczytałeś `INSTRUKCJA_DEPLOYMENT_S1KOR.md`
- [ ] Masz gotowe komendy z `DEPLOY_COMMANDS.sh`
- [ ] Masz konto Railway.app

---

## 🚀 Jesteś gotów?

→ Otwórz: **INSTRUKCJA_DEPLOYMENT_S1KOR.md**

Tam masz wszystko krok po kroku. Follow i będzie dobrze! 🎯

---

## 📞 Pytania?

Czekam na Tasklet! Pisz swobodnie jeśli coś niejasne 🤖

---

**Status:** ✅ Wszystko gotowe
**Czas deployment'u:** 15-20 minut
**Komplikacja:** Niska (3/10) - głównie klikanie buttons
**Rezultat:** Strona online 24/7 🎉
