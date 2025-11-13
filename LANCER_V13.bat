@echo off
title NiTriTe V13.0 - Launcher
color 0E
cls

echo.
echo ================================================================================
echo                        NiTriTe V13.0 - Modern Edition
echo ================================================================================
echo.
echo    Lancement de l'interface moderne...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python 3.8+ depuis https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Vérifier si le fichier principal existe
if not exist "nitrite_v13_modern.py" (
    echo [ERREUR] Fichier nitrite_v13_modern.py introuvable
    echo.
    echo Assurez-vous d'executer ce script depuis le dossier du projet
    echo.
    pause
    exit /b 1
)

REM Lancer l'application
echo [INFO] Demarrage de NiTriTe V13...
echo.
python nitrite_v13_modern.py

REM Si erreur
if errorlevel 1 (
    echo.
    echo [ERREUR] L'application s'est terminee avec une erreur
    echo.
    pause
    exit /b 1
)

exit /b 0
