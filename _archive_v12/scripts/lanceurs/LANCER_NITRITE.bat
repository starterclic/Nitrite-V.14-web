@echo off
chcp 65001 >nul 2>&1
title NiTrite OrdiPlus v3.0 - Lanceur

REM Retourner a la racine du projet
cd /d "%~dp0\..\..\"

echo.
echo ==============================================================
echo.
echo           NiTrite OrdiPlus v3.0
echo.
echo     Installation automatique de 304 programmes Windows
echo.
echo ==============================================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo.
    echo Telechargez Python depuis: https://www.python.org/downloads/
    echo Cochez "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

REM Lancer avec le script de gestion des dependances
echo [INFO] Lancement de NiTrite...
echo.
python scripts\lanceurs\lancer_nitrite.py

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Une erreur s'est produite
    pause
    exit /b %errorlevel%
)

exit /b 0
