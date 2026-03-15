@echo off
chcp 65001 >nul 2>&1
title CUPRA HUB v11 - Dashboard + Scraper
cd /d "%~dp0"

set "PYTHONIOENCODING=utf-8"
set "PYTHONLEGACYWINDOWSSTDIO=utf-8"
set "PYTHONUTF8=1"

echo.
echo   ===================================================
echo     CUPRA HUB v11 - Uruchamianie...
echo   ===================================================
echo.

REM === Sprawdz Python ===
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [BLAD] Python nie znaleziony!
    echo   Zainstaluj Python z https://python.org
    pause
    exit /b 1
)

REM === Sprawdz wymagane pakiety ===
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo   Instaluje wymagane pakiety...
    python -m pip install requests openpyxl --quiet
)

REM === Uruchom serwer HTTP w tle ===
echo   [1/3] Uruchamiam serwer HTTP na porcie 8080...
start /b "" python server.py >nul 2>&1

REM === Poczekaj az serwer wstanie ===
timeout /t 2 /nobreak >nul

REM === Otworz przegladarke ===
echo   [2/3] Otwieram dashboard w przegladarce...
start "" "http://localhost:8080"

REM === Uruchom scraper ===
echo   [3/3] Uruchamiam scraper...
echo.
echo   ===================================================
echo     Scraper pracuje - dane odswiezaja sie na stronie
echo     co 5 sekund automatycznie.
echo     NIE ZAMYKAJ tego okna!
echo   ===================================================
echo.

python goliath_v11.py

echo.
echo   ===================================================
echo     Skanowanie zakonczone!
echo     Dashboard nadal dziala na http://localhost:8080
echo     Zamknij to okno aby zatrzymac serwer.
echo   ===================================================
echo.
pause
