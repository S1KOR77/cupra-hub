# GOLIATH v13 — CHANGELOG

## 🐛 Naprawione krytyczne bugi

### 1. `return []` zamiast `return [], 0` (linia 508)
**Problem:** `_extract_ads_from_json()` zwracał `[]` gdy brak `__NEXT_DATA__`, a `collect()` próbował rozpakować do `ads, total = ...` → **crash dla każdego dealera bez JSON**.
**Fix:** Zmieniono na `return [], 0`.

### 2. Merge z cache nigdy nie działał (linia 1842)
**Problem:** JSON był zapisywany jako tablica `[{...}, {...}]`, ale merge szukał `old_data.get("cars", [])` — klucz "cars" nie istniał, więc **auta z cache znikały** po każdym uruchomieniu.
**Fix:** `cached_items = old_data if isinstance(old_data, list) else old_data.get("cars", [])`

### 3. Brak `beautifulsoup4` w requirements.txt
**Problem:** Scraper importuje `from bs4 import BeautifulSoup` ale pakiet nie był w requirements → **crash na Railway**.
**Fix:** Dodano `beautifulsoup4==4.12.3` do requirements.txt.

### 4. Opis ucięty do 500 znaków
**Problem:** `clean_desc[:500]` obcinał opis PRZED szukaniem ceny katalogowej w opisie.
**Fix:** Zwiększono limit do 2000 znaków.

## 📈 Ulepszenia

### 5. Agresywny kalkulator marży (-1% do 7%)
**Problem:** Marże poza zakresem oznaczane jako ANOMALIA bez próby dopasowania.
**Fix:** Nowy 6-krokowy algorytm:
1. Sprawdź bazową marżę (bez rabatu)
2. Zastosuj pełny rabat
3. EV → zawsze rabat
4. Próbuj różne korekty VGP (6-20%)
5. Korekta + rabat łącznie
6. Fallback — wybierz najbliższą do zakresu

### 6. Multi-strategy zbieranie linków
**Fix:** 3 warstwy parsowania:
1. `__NEXT_DATA__` JSON (najszybsze i najdokładniejsze)
2. BeautifulSoup fallback (gdy JSON daje <3 wyniki)
3. Regex fallback (ostatnia deska ratunku)

### 7. Server v2.1 — endpoint `/run-scraper`
- GET/POST `/run-scraper` → ręczne uruchomienie scrapera
- GET `/api/status` → status scrapera (running/last_run/last_status)
- Thread-safe — nie uruchomi dwóch scraperów jednocześnie

## 📦 Pliki do wdrożenia na Railway

| Plik | Opis |
|------|------|
| `goliath_v11.py` | Główny scraper z poprawkami |
| `server.py` | Serwer HTTP z `/run-scraper` |
| `requirements.txt` | Z dodanym beautifulsoup4 |

## ⚡ Test wydajności

MOTORPOL WROCŁAW: **69 linków** (vs poprzednio ~6 per page × 3 strony = 18)
→ 3.8× więcej aut dzięki poprawionemu parsowaniu!
