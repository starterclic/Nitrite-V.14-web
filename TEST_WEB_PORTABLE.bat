@echo off
chcp 65001 >nul 2>&1
title NiTriTe V.13 - Test Version Web Portable (Sans Build)
color 0E

echo.
echo ═══════════════════════════════════════════════════════════
echo    🧪 Test Version Web Portable (SANS COMPILATION)
echo ═══════════════════════════════════════════════════════════
echo.
echo Ce script teste le lanceur SANS compiler en .exe
echo Utile pour vérifier que tout fonctionne avant le build
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non installé
    pause
    exit /b 1
)

echo ✅ Python installé
echo.

REM Installer dépendances
echo 📦 Vérification des dépendances...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ⚠️  Erreur installation dépendances
)
echo ✅ Dépendances OK
echo.

REM Lancer directement le script Python
echo.
echo ═══════════════════════════════════════════════════════════
echo    🚀 LANCEMENT DU TEST
echo ═══════════════════════════════════════════════════════════
echo.
echo Le serveur va démarrer...
echo Le navigateur s'ouvrira automatiquement
echo.
echo Pour arrêter: Ctrl+C ou fermez cette fenêtre
echo.
echo ═══════════════════════════════════════════════════════════
echo.

python nitrite_web_portable.py

pause
