#!/bin/bash
# CUPRA HUB Deployment Commands
# Skopiuj i uruchom po kolei w terminalu

echo "🚀 CUPRA HUB Deployment Script"
echo "================================"
echo ""

# KROK 1: Sprawdzenie czy Git jest zainstalowany
echo "📋 KROK 1: Sprawdzanie Git..."
git --version
if [ $? -ne 0 ]; then
    echo "❌ Git nie zainstalowany! Pobierz z https://git-scm.com/"
    exit 1
fi
echo "✅ Git OK"
echo ""

# KROK 2: Inicjalizacja Git repo
echo "📋 KROK 2: Inicjalizacja Git repo..."
git init
echo "✅ Git repo initialized"
echo ""

# KROK 3: Dodanie remote (GitHub)
echo "📋 KROK 3: Dodawanie GitHub remote..."
echo "Edytuj poniższe komenda - zmień S1KOR__ na swoją nazwę GitHub:"
echo ""
echo "git remote add origin https://github.com/S1KOR__/cupra-hub.git"
echo ""
echo "⚠️  ZATRZYMAJ! Skopiuj powyższą komendę, zmień S1KOR__ na swoją nazwę GitHub, i uruchom ją"
echo ""

# Po zapauzowaniu - sprawdzenie
echo "📋 KROK 4: Sprawdzanie remote..."
git remote -v
echo "✅ Remote added"
echo ""

# KROK 5: Push na GitHub
echo "📋 KROK 5: Push plików na GitHub..."
git add .
git commit -m "Initial commit - CUPRA Hub v2.0"
git branch -M main
git push -u origin main

echo ""
echo "✅ PUSH COMPLETE!"
echo ""
echo "================================"
echo "🎉 GOTOWE DO DEPLOYMENT'U!"
echo "================================"
echo ""
echo "Teraz idź na Railway.app i:"
echo "1. Zaloguj się (GitHub)"
echo "2. New Project → Deploy from GitHub"
echo "3. Wybierz cupra-hub"
echo "4. Czekaj na deployment"
echo "5. Pobierz URL i testuj!"
echo ""
echo "Pytania? Czekam! 🤖"
