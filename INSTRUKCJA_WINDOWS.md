# 🚀 DEPLOYMENT CUPRA HUB - INSTRUKCJA DLA WINDOWS

## 📋 KROK PO KROKU (20 minut)

---

## KROK 1️⃣ - Rozpakuj ZIP

1. Pobierz **cupra-project-READY-TO-DEPLOY.zip**
2. Rozpakuj go na Desktop lub gdzie chcesz
3. Powinna być taka struktura:
```
C:\Users\wikim\Desktop\cupra-project\
├── index.html
├── goliath_v11.py
├── server.py
├── requirements.txt
├── Procfile
└── ... (reszta plików)
```

---

## KROK 2️⃣ - Zainstaluj Git (jeśli nie masz)

1. Idź na https://git-scm.com/download/win
2. Pobierz i zainstaluj (next, next, finish)
3. **Restart komputera** (ważne!)
4. Otwórz Command Prompt (WIN + R → cmd → Enter)

---

## KROK 3️⃣ - Stwórz GitHub Repository

1. Idź na https://github.com/new
2. Wypełnij:
   - **Repository name:** `cupra-hub`
   - **Description:** "CUPRA Inventory Management System"
   - **Public** ✅ (ważne!)
   - **Add .gitignore:** NIE zaznaczaj
   - **Add README:** NIE zaznaczaj
3. Klikni **Create repository** ✅

---

## KROK 4️⃣ - Push plików na GitHub (WINDOWS CMD)

### 4a. Otwórz Command Prompt w folderze z projektem

Idź do: `C:\Users\wikim\Desktop\cupra-project\`

Klikni w tym folderze na adres (gdzie pisze ścieżka) i wpisz `cmd`:

```
C:\Users\wikim\Desktop\cupra-project>
```

### 4b. Inicjalizuj Git repo

Wpisz (copy-paste do cmd):

```
git init
```

Powinna być odpowiedź:
```
Initialized empty Git repository in C:\Users\wikim\Desktop\cupra-project\.git\
```

### 4c. Dodaj GitHub

Wpisz (zamiast S1KOR__ wpisz Twój login):

```
git remote add origin https://github.com/S1KOR__/cupra-hub.git
```

Sprawdzenie:
```
git remote -v
```

Powinna być:
```
origin  https://github.com/S1KOR__/cupra-hub.git (fetch)
origin  https://github.com/S1KOR__/cupra-hub.git (push)
```

### 4d. Dodaj wszystkie pliki

```
git add .
```

### 4e. Commit

```
git commit -m "Initial commit - CUPRA Hub v2.0"
```

### 4f. Push na GitHub

```
git branch -M main
git push -u origin main
```

**Jeśli poprosi Ci się na login:**
```
Username: S1KOR__
Password: [wklej token - patrz poniżej]
```

---

## 🔐 KROK 5️⃣ - GitHub Token (jeśli poprosi na hasło)

1. Idź na https://github.com/settings/tokens
2. Klikni **Generate new token** → **Generate new token (classic)**
3. Zaznacz opcje:
   - ☑️ repo
   - ☑️ workflow
4. Klikni **Generate token**
5. **SKOPIUJ TOKEN** (pojawi się raz!)
6. Wróć do cmd → w promptzie na "Password:" → wklej token
7. Enter ✅

---

## KROK 6️⃣ - Deployment na Railway.app

1. Idź na https://railway.app
2. **Sign up** (możesz przez GitHub)
3. Klikni **+ New Project**
4. Wybierz **Deploy from GitHub repo**
5. **Connect GitHub** (jeśli poprosi)
6. Szukaj `cupra-hub` i wybierz
7. Railway automatycznie:
   - Pobiera repo
   - Czyta Procfile
   - Instaluje requirements.txt
   - Startuje server.py

**Czekaj 3-5 minut** ⏳

Jak skończy → powinien być ✅ **Deployment successful**

---

## KROK 7️⃣ - Pobierz publiczny URL

W Railway dashboard:
1. Klikni na projekt **cupra-hub**
2. Idź do **Settings** (lub szukaj w menu)
3. Szukaj **Domains** lub **Public URL**
4. Powinna być coś jak:
   ```
   https://cupra-hub-production.up.railway.app
   ```
5. **SKOPIUJ TEN URL!** ✅

---

## KROK 8️⃣ - Testowanie

### Test 1: Strona główna

Otwórz przeglądarkę i idź na:
```
https://cupra-hub-production.up.railway.app
```

Powinna się załadować **strona CUPRA HUB** z listą aut 🎉

### Test 2: Sprawdzenie schedulera

Idź na:
```
https://cupra-hub-production.up.railway.app/api/status
```

Powinna być odpowiedź (JSON):
```json
{
  "status": "running",
  "uptime": "2 minutes",
  "next_scrape": "2026-03-15 06:00:00 UTC"
}
```

✅ **Jeśli widzisz to = WSZYSTKO DZIAŁA!**

---

## 🎯 Co się będzie działo:

```
🕕 06:00 UTC KAŻDEGO DNIA:
   ↓
   Scraper automatycznie się uruchomi
   ↓
   Przeskanuje otomoto.pl (29 dealerów CUPRA)
   ↓
   Aktualizuje data.json
   ↓
   Strona przeładowuje się
   ↓
   Wszyscy widzą świeże dane 🎉

🔄 Reszta dnia:
   Strona dostępna 24/7
   Czeka na następny scrape
```

---

## 🆘 PROBLEMY?

### ❌ Git command not found

**Przyczyna:** Git nie zainstalowany lub nie restartujesz komputera

**Rozwiązanie:**
1. Pobierz Git: https://git-scm.com/download/win
2. Zainstaluj
3. **Restart komputera**
4. Otwórz nowy Command Prompt

---

### ❌ fatal: 'origin' does not appear...

**Przyczyna:** Git repo nie zainicjalizowany

**Rozwiązanie:**
W Command Prompt:
```
git init
git remote add origin https://github.com/S1KOR__/cupra-hub.git
```

---

### ❌ Railway mówi "BUILD FAILED"

1. W Railway klikni projekt
2. Idź do **Logs**
3. Szukaj `ERROR` w logach
4. Pokaż mi ten błąd na Tasklet

---

### ❌ Strona ładuje się ale bez danych

- Czekaj aż scraper się uruchomi (06:00 UTC dzisiaj/jutro)
- Lub sprawdź Railway logs czy scraper się uruchomił

---

### ❌ /api/status zwraca błąd 404

**Przyczyna:** Server.py się nie uruchomił poprawnie

**Sprawdzenie:**
1. W Railway klikni projekt
2. Idź do **Logs**
3. Szukaj `Running on` lub `Listening`
4. Jeśli błąd → pokaż mi logs

---

## ✅ CHECKLIST - Czy wszystko OK?

- [ ] Git zainstalowany
- [ ] GitHub repo `cupra-hub` istnieje
- [ ] Pliki pushnuty na GitHub (widać w GitHub)
- [ ] Railway deployment successful (zielony ✅)
- [ ] Strona ładuje się na Railway URL
- [ ] /api/status zwraca JSON
- [ ] Scheduler pokazuje `next_scrape`

---

## 🎉 GOTOWE!

Twoja strona CUPRA HUB jest teraz **ONLINE 24/7** 🚀

**Publiczny URL:** (dostaniesz z Railway w KROK 7)

**Scraper:** Automatycznie każdego dnia o 06:00 UTC

**Koszt:** Zupełnie FREE (Railway free tier)

---

## 📞 Problemy?

Pisz na Tasklet - będę czekać! 🎯
