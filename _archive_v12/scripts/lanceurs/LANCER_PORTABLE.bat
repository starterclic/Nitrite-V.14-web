@echo off
chcp 65001 >nul 2>&1
title NiTrite OrdiPlus v3.0 - Mode Portable

REM Retourner a la racine du projet
cd /d "%~dp0\..\..\"

echo.
echo ==============================================================
echo.
echo      NiTrite OrdiPlus v3.0 - Mode Portable
echo.
echo ==============================================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe
    echo.
    pause
    exit /b 1
)

REM Lancer en mode portable (sans verification des dependances)
echo [INFO] Lancement en mode portable...
echo.
python scripts\lanceurs\lancer_portable.py

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Une erreur s'est produite
    echo [INFO] Essayez: LANCER_NITRITE.bat (avec verification des dependances)
    pause
    exit /b %errorlevel%
)

exit /b 0
