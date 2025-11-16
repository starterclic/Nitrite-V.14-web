@echo off
chcp 65001 >nul 2>&1
title NiTriTe V.13 - Test Version Web Portable (Sans Build)
color 0E

echo.
echo ===============================================================
echo    Test Version Web Portable (SANS COMPILATION)
echo ===============================================================
echo.
echo Ce script teste le lanceur SANS compiler en .exe
echo Utile pour verifier que tout fonctionne avant le build
echo.
echo ===============================================================
echo.

REM Verifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python non installe
    pause
    exit /b 1
)

echo [OK] Python installe
echo.

REM Installer dependances
echo [INFO] Verification des dependances...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ATTENTION] Erreur installation dependances
)
echo [OK] Dependances OK
echo.

REM Lancer directement le script Python
echo.
echo ===============================================================
echo    LANCEMENT DU TEST
echo ===============================================================
echo.
echo Le serveur va demarrer...
echo Le navigateur s'ouvrira automatiquement
echo.
echo Pour arreter: Ctrl+C ou fermez cette fenetre
echo.
echo ===============================================================
echo.

python nitrite_web_portable.py

pause
