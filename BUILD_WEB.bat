@echo off
chcp 65001 >nul 2>&1
title NiTriTe V.13 - Build Version Web Portable
color 0A

echo.
echo ═══════════════════════════════════════════════════════════
echo    🚀 NiTriTe V.13 - Build Version Web Portable
echo ═══════════════════════════════════════════════════════════
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo.
    echo Installez Python depuis https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python détecté:
python --version
echo.

REM Vérifier que nous sommes dans le bon dossier
if not exist "nitrite_web_portable.py" (
    echo ❌ Erreur: nitrite_web_portable.py non trouvé
    echo.
    echo Assurez-vous d'exécuter ce script depuis le dossier du projet
    pause
    exit /b 1
)

if not exist "NiTriTe_Web_Portable.spec" (
    echo ❌ Erreur: NiTriTe_Web_Portable.spec non trouvé
    pause
    exit /b 1
)

if not exist "web_backend.py" (
    echo ❌ Erreur: web_backend.py non trouvé
    pause
    exit /b 1
)

if not exist "web\" (
    echo ❌ Erreur: Dossier web\ non trouvé
    pause
    exit /b 1
)

echo ✅ Tous les fichiers nécessaires sont présents
echo.

REM Installer/vérifier PyInstaller
echo 📦 Vérification de PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 📥 Installation de PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ Erreur lors de l'installation de PyInstaller
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller est installé
echo.

REM Installer les dépendances
echo 📦 Installation/vérification des dépendances...
echo.
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ⚠️  Avertissement: Certaines dépendances n'ont pas pu être installées
    echo Tentative de continuer quand même...
) else (
    echo ✅ Dépendances installées
)
echo.

REM Nettoyer les anciens builds
echo 🧹 Nettoyage des anciens builds...
if exist "build\" (
    rmdir /s /q "build"
    echo    - Dossier build\ supprimé
)
if exist "dist\NiTriTe_Web_V13.exe" (
    del /q "dist\NiTriTe_Web_V13.exe"
    echo    - Ancien .exe supprimé
)
echo ✅ Nettoyage terminé
echo.

REM Build avec PyInstaller
echo.
echo ═══════════════════════════════════════════════════════════
echo    🔨 COMPILATION EN COURS
echo ═══════════════════════════════════════════════════════════
echo.
echo ⏳ Cela peut prendre 2-5 minutes...
echo ⏳ Ne fermez pas cette fenêtre !
echo.

pyinstaller --clean --noconfirm NiTriTe_Web_Portable.spec

if %errorlevel% neq 0 (
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo    ❌ ERREUR LORS DE LA COMPILATION
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo Vérifiez les messages d'erreur ci-dessus.
    echo.
    echo Solutions possibles:
    echo  - Réinstallez PyInstaller: pip install --upgrade pyinstaller
    echo  - Vérifiez que tous les modules sont installés: pip install -r requirements.txt
    echo  - Essayez en tant qu'administrateur
    echo.
    pause
    exit /b 1
)

REM Vérifier que l'exe a été créé
if not exist "dist\NiTriTe_Web_V13.exe" (
    echo.
    echo ❌ L'exécutable n'a pas été créé
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo    ✅ BUILD TERMINÉ AVEC SUCCÈS !
echo ═══════════════════════════════════════════════════════════
echo.
echo 📁 Emplacement: dist\NiTriTe_Web_V13.exe
echo.
echo 📊 Taille du fichier:
dir dist\NiTriTe_Web_V13.exe | find "NiTriTe_Web_V13.exe"
echo.
echo ═══════════════════════════════════════════════════════════
echo    🚀 COMMENT UTILISER
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Double-cliquez sur dist\NiTriTe_Web_V13.exe
echo 2. Le serveur Flask démarre automatiquement
echo 3. Le navigateur s'ouvre sur http://127.0.0.1:5000
echo 4. Utilisez l'application web normalement
echo 5. Fermez la fenêtre console pour arrêter
echo.
echo 💡 L'exécutable est TOTALEMENT PORTABLE:
echo    ✔️  Aucune installation Python requise
echo    ✔️  Fonctionne sur n'importe quel PC Windows 10/11
echo    ✔️  Peut être copié sur une clé USB
echo    ✔️  Serveur Flask + interface web tout-en-un
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM Proposer de tester
set /p test="Voulez-vous tester l'exécutable maintenant ? (O/N) : "
if /i "%test%"=="O" (
    echo.
    echo 🚀 Lancement de NiTriTe Web Portable...
    echo.
    echo ⚠️  Une nouvelle fenêtre va s'ouvrir
    echo ⚠️  Le navigateur s'ouvrira automatiquement
    echo.
    start "" "dist\NiTriTe_Web_V13.exe"
    echo.
    echo ✅ Application lancée !
    echo.
)

echo.
echo 👍 Build terminé avec succès !
echo.
pause
