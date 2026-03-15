# 🚀 DEPLOYMENT CUPRA HUB NA RAILWAY.APP
## Instrukcja dla S1KOR__ (GitHub: S1KOR__)

---

## 📋 KROK PO KROKU (15 minut)

### KROK 1️⃣ - Stworzenie GitHub Repository

1. Idź na https://github.com/new
2. Wypełnij:
   - **Repository name:** `cupra-hub`
   - **Description:** "CUPRA Inventory Management System"
   - **Public** (ważne! Railway musi mieć dostęp)
   - **Add a README file:** NIE zaznaczaj
   - **Add .gitignore:** Już mamy
3. Klikni **Create repository** ✅

---

### KROK 2️⃣ - Push plików na GitHub

Otwórz terminal/cmd i wejdź w folder z projektem:

```bash
cd /agent/home/cupra-project
```

Lub gdzieś gdzie masz pliki (twój folder CUPRA HUB).

Teraz wykonaj:

```bash
# Inicjalizuj Git repo
git init

# Dodaj GitHub jako remote
git remote add origin https://github.com/S1KOR__/cupra-hub.git

# Sprawdzić
git remote -v
```

Powinna być odpowiedź:
```
origin  https://github.com/S1KOR__/cupra-hub.git (fetch)
origin  https://github.com/S1KOR__/cupra-hub.git (push)
```

Teraz push wszystkich plików:

```bash
# Dodaj wszystkie pliki
git add .

# Commit
git commit -m "Initial commit - CUPRA Hub v2.0"

# Push na main branch
git branch -M main
git push -u origin main
```

**Jeśli poprosi Ci się na login:**
```
Username: S1KOR__
Password: [token dostępu - patrz poniżej]
```

#### 🔐 Jeśli GitHub poprosi o token zamiast hasła:

1. Idź na https://github.com/settings/tokens
2. **Generate new token (classic)**
3. Zaznacz: `repo`, `workflow`
4. **Generate token**
5. **Skopiuj token** (pokaże się tylko raz!)
6. W terminalu zamiast hasła - wklej token

---

### KROK 3️⃣ - Deployment na Railway

1. Idź na https://railway.app
2. **Sign up / Login** (GitHub login OK)
3. Klikni **+ New Project**
4. Wybierz **Deploy from GitHub repo**
5. **Connect GitHub** (jeśli będzie pytać o permission)
6. Wyszukaj i wybierz **cupra-hub**
7. Railway zautomatyzuje build

**Czekaj ~3-5 minut** ⏳

Jak skończy build → powinien pokazać ✅ **Deployment successful**

---

### KROK 4️⃣ - Pobierz publiczny URL

1. W Railway dashboard, idź do **Settings**
2. Szukaj **Domains** lub **Public URL**
3. Powinna być taka rzecz:
   ```
   https://cupra-hub-production.up.railway.app
   ```
4. **Skopiuj ten URL** ✅

---

### KROK 5️⃣ - Testowanie

Otwórz przeglądarkę i wejdź na:

```
https://cupra-hub-production.up.railway.app
```

Powinna się załadować **strona CUPRA HUB** z autami! 🎉

Teraz sprawdzamy czy scheduler działa:

```
https://cupra-hub-production.up.railway.app/api/status
```

Powinna być odpowiedź (JSON):
```json
{
  "status": "running",
  "uptime": "2 minutes",
  "next_scrape": "2026-03-15 06:00:00 UTC",
  "last_scrape": "2026-03-14 06:00:00 UTC"
}
```

✅ Jeśli widzisz to = **Wszystko działa!**

---

## 📅 Co się będzie działo:

```
🕕 06:00 UTC KAŻDEGO DNIA:
   ↓
   Scraper się automatycznie uruchomi
   ↓
   Przeskanuje otomoto.pl (29 dealerów CUPRA)
   ↓
   Aktualizuje data.json
   ↓
   Strona na Railway przeładowuje się
   ↓
   Wszyscy widzą świeże dane 🎉

🔄 Reszta dnia:
   Strona jest zawsze dostępna 24/7
   Czeka na następny scrape
```

---

## 🎛️ Edycja rabatów bez restarta

1. Idź na GitHub: `https://github.com/S1KOR__/cupra-hub`
2. Klikni na plik **settings.json**
3. Klikni ✏️ (Edit)
4. Edytuj rabaty:
   ```json
   "discount_multiplier": 1.15
   ```
5. **Commit changes**
6. Railway automatycznie wdraża (restart ~1 minuta)
7. Strona wyświetla nowe rabaty ✅

---

## 🆘 Problemy?

### ❌ GitHub push nie działa
```
fatal: 'origin' does not appear to be a Git repository
```
**Rozwiązanie:** 
Otwórz folder gdzie masz pliki i powtórz KROK 2️⃣

---

### ❌ Railway mówi "BUILD FAILED"
1. Klikni **View Logs** w Railway
2. Szukaj `ERROR` w logach
3. 90% problemy:
   - Brakuje pliku `Procfile`
   - Brakuje `requirements.txt`
   - Python wersja (powinno być 3.11+)

**Jeśli widzisz błąd** - skopiuj tekst błędu i daj mi znać! 📋

---

### ❌ Strona ładuje się ale bez danych
- Czekaj aż scraper się uruchomi (06:00 UTC)
- Lub klikni **Run Scraper** w Railway logs

---

### ❌ Scraper się nie uruchomia o 06:00
1. Idź do Railway Dashboard
2. Sprawdzić **Logs** → szukaj `APScheduler` lub `scraper`
3. Jeśli błąd → pokaż mi w logach

---

## 📊 URL'e które będą dostępne:

```
🏠 Strona główna:
https://cupra-hub-production.up.railway.app/

📊 API - Lista aut (JSON):
https://cupra-hub-production.up.railway.app/api/data

⚙️ API - Rabaty (JSON):
https://cupra-hub-production.up.railway.app/api/settings

📡 Status servera:
https://cupra-hub-production.up.railway.app/api/status
```

---

## ✅ Checklist - Czy wszystko OK?

- [ ] GitHub repo `cupra-hub` istnieje
- [ ] Pliki pushnuty na GitHub
- [ ] Railway deployment successful (zielony checkmark)
- [ ] Strona ładuje się
- [ ] `/api/status` zwraca JSON
- [ ] Scheduler pokazuje `next_scrape` na 06:00 UTC
- [ ] Data.json aktualizuje się codziennie

---

## 🎉 GOTOWE!

Twoja strona CUPRA HUB jest teraz **ONLINE 24/7** 🚀

**Publiczny URL:** (dostaniesz z Railway)

**Scraper:** Automatycznie każdego dnia o 06:00 UTC

**Koszt:** FREE tier Railway (do 500 uptime hours/miesiąc)

---

## 📞 Jeśli będą problemy:

Pisz mi - znowu będę w Tasklet czekać 🎯

---

**Status:** ✅ Ready to deploy
**Czas deployment'u:** ~15 minut
**Komplikacja:** Niska (3/10)
