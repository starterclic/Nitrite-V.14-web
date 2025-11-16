@echo off
chcp 65001 >nul 2>&1
title NiTriTe V.13 - Build Version Web Portable
color 0A

echo.
echo ===============================================================
echo    NiTriTe V.13 - Build Version Web Portable
echo ===============================================================
echo.

REM Verifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo.
    echo Installez Python depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detecte:
python --version
echo.

REM Verifier que nous sommes dans le bon dossier
if not exist "nitrite_web_portable.py" (
    echo [ERREUR] nitrite_web_portable.py non trouve
    echo.
    echo Assurez-vous d'executer ce script depuis le dossier du projet
    pause
    exit /b 1
)

if not exist "NiTriTe_Web_Portable.spec" (
    echo [ERREUR] NiTriTe_Web_Portable.spec non trouve
    pause
    exit /b 1
)

if not exist "web_backend.py" (
    echo [ERREUR] web_backend.py non trouve
    pause
    exit /b 1
)

if not exist "web\" (
    echo [ERREUR] Dossier web\ non trouve
    pause
    exit /b 1
)

echo [OK] Tous les fichiers necessaires sont presents
echo.

REM Installer/verifier PyInstaller
echo [INFO] Verification de PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [INFO] Installation de PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [ERREUR] Erreur lors de l'installation de PyInstaller
        pause
        exit /b 1
    )
)

echo [OK] PyInstaller est installe
echo.

REM Installer les dependances
echo [INFO] Installation/verification des dependances...
echo.
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ATTENTION] Certaines dependances n'ont pas pu etre installees
    echo Tentative de continuer quand meme...
) else (
    echo [OK] Dependances installees
)
echo.

REM Nettoyer les anciens builds
echo [INFO] Nettoyage des anciens builds...
if exist "build\" (
    rmdir /s /q "build"
    echo    - Dossier build\ supprime
)
if exist "dist\NiTriTe_Web_V13.exe" (
    del /q "dist\NiTriTe_Web_V13.exe"
    echo    - Ancien .exe supprime
)
echo [OK] Nettoyage termine
echo.

REM Build avec PyInstaller
echo.
echo ===============================================================
echo    COMPILATION EN COURS
echo ===============================================================
echo.
echo [INFO] Cela peut prendre 2-5 minutes...
echo [INFO] Ne fermez pas cette fenetre !
echo.

pyinstaller --clean --noconfirm NiTriTe_Web_Portable.spec

if %errorlevel% neq 0 (
    echo.
    echo ===============================================================
    echo    ERREUR LORS DE LA COMPILATION
    echo ===============================================================
    echo.
    echo Verifiez les messages d'erreur ci-dessus.
    echo.
    echo Solutions possibles:
    echo  - Reinstallez PyInstaller: pip install --upgrade pyinstaller
    echo  - Verifiez les modules: pip install -r requirements.txt
    echo  - Essayez en tant qu'administrateur
    echo.
    pause
    exit /b 1
)

REM Verifier que l'exe a ete cree
if not exist "dist\NiTriTe_Web_V13.exe" (
    echo.
    echo [ERREUR] L'executable n'a pas ete cree
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================================
echo    BUILD TERMINE AVEC SUCCES !
echo ===============================================================
echo.
echo [INFO] Emplacement: dist\NiTriTe_Web_V13.exe
echo.
echo [INFO] Taille du fichier:
dir dist\NiTriTe_Web_V13.exe | find "NiTriTe_Web_V13.exe"
echo.
echo ===============================================================
echo    COMMENT UTILISER
echo ===============================================================
echo.
echo 1. Double-cliquez sur dist\NiTriTe_Web_V13.exe
echo 2. Le serveur Flask demarre automatiquement
echo 3. Le navigateur s'ouvre sur http://127.0.0.1:5000
echo 4. Utilisez l'application web normalement
echo 5. Fermez la fenetre console pour arreter
echo.
echo L'executable est TOTALEMENT PORTABLE:
echo    - Aucune installation Python requise
echo    - Fonctionne sur n'importe quel PC Windows 10/11
echo    - Peut etre copie sur une cle USB
echo    - Serveur Flask + interface web tout-en-un
echo.
echo ===============================================================
echo.

REM Proposer de tester
set /p test="Voulez-vous tester l'executable maintenant ? (O/N) : "
if /i "%test%"=="O" (
    echo.
    echo [INFO] Lancement de NiTriTe Web Portable...
    echo.
    echo [INFO] Une nouvelle fenetre va s'ouvrir
    echo [INFO] Le navigateur s'ouvrira automatiquement
    echo.
    start "" "dist\NiTriTe_Web_V13.exe"
    echo.
    echo [OK] Application lancee !
    echo.
)

echo.
echo Build termine avec succes !
echo.
pause
