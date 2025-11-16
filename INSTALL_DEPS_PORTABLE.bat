@echo off
REM ====================================================================
REM NiTriTe V13.0 - Installation des Dépendances (Mode Portable)
REM ====================================================================
REM
REM Ce script installe toutes les dépendances nécessaires pour BUILDER
REM l'application en mode portable. Ces dépendances seront EMBARQUÉES
REM dans l'exe final, donc rien ne sera installé sur le PC du client.
REM
REM IMPORTANT: Exécuter sur la machine de DÉVELOPPEMENT uniquement
REM ====================================================================

echo.
echo ========================================
echo  NiTriTe V13 - Installation Portable
echo ========================================
echo.
echo Ce script va installer les dependances pour le BUILD.
echo Ces dependances seront EMBARQUEES dans l'exe final.
echo.
echo RIEN ne sera installe sur le PC du client final !
echo.
pause

REM Vérifier Python
echo.
echo [1/4] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo.
    echo Telecharger Python 3.8+ depuis: https://www.python.org/downloads/
    echo IMPORTANT: Cocher "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)
python --version
echo OK - Python detecte

REM Vérifier pip
echo.
echo [2/4] Verification de pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: pip n'est pas disponible
    echo Installation de pip...
    python -m ensurepip --default-pip
)
python -m pip --version
echo OK - pip detecte

REM Mettre à jour pip
echo.
echo [3/4] Mise a jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances
echo.
echo [4/4] Installation des dependances depuis requirements.txt...
echo.
echo Les modules suivants seront installes:
echo   - PyInstaller    (pour creer l'exe)
echo   - Pillow         (gestion des images)
echo   - requests       (telechargements HTTP)
echo   - pywin32        (API Windows)
echo   - psutil         (infos systeme)
echo   - urllib3        (networking)
echo   - certifi        (certificats SSL)
echo   - tqdm           (barres de progression)
echo   - colorama       (couleurs terminal)
echo.
echo Ces modules seront EMBARQUES dans l'exe final.
echo Taille totale embarquee: ~35-50 MB
echo.
pause

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERREUR: L'installation a echoue
    echo.
    echo Solutions possibles:
    echo   1. Verifier votre connexion Internet
    echo   2. Desactiver temporairement l'antivirus
    echo   3. Executer en tant qu'administrateur
    echo   4. Installer manuellement: pip install pyinstaller pillow requests pywin32
    echo.
    pause
    exit /b 1
)

REM Vérification finale
echo.
echo ========================================
echo  Verification des modules installes
echo ========================================
echo.

echo Verification PyInstaller...
python -c "import PyInstaller; print(f'  OK - PyInstaller {PyInstaller.__version__}')" 2>nul
if errorlevel 1 (
    echo   ERREUR - PyInstaller non trouve
    set HAS_ERROR=1
)

echo Verification Pillow...
python -c "import PIL; print(f'  OK - Pillow {PIL.__version__}')" 2>nul
if errorlevel 1 (
    echo   ERREUR - Pillow non trouve
    set HAS_ERROR=1
)

echo Verification requests...
python -c "import requests; print(f'  OK - requests {requests.__version__}')" 2>nul
if errorlevel 1 (
    echo   ERREUR - requests non trouve
    set HAS_ERROR=1
)

echo Verification pywin32...
python -c "import win32api; print('  OK - pywin32')" 2>nul
if errorlevel 1 (
    echo   ATTENTION - pywin32 non trouve (optionnel pour le build)
)

echo Verification urllib3...
python -c "import urllib3; print(f'  OK - urllib3 {urllib3.__version__}')" 2>nul

echo Verification certifi...
python -c "import certifi; print('  OK - certifi')" 2>nul

if defined HAS_ERROR (
    echo.
    echo ATTENTION: Certains modules critiques ne sont pas installes
    echo Le build risque d'echouer
    echo.
    echo Reinstallez manuellement:
    echo   pip install pyinstaller pillow requests
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  INSTALLATION TERMINEE AVEC SUCCES
echo ========================================
echo.
echo Vous pouvez maintenant lancer le build:
echo   python build_v13.py
echo.
echo Cela va creer un exe PORTABLE avec toutes les
echo dependances embarquees (rien sur le PC client).
echo.
echo Fichier final: dist\NiTriTe_V13_Modern.exe
echo Taille: ~35-50 MB (tout en un seul fichier)
echo.
echo Consultez README.md pour plus d'infos.
echo.
pause
