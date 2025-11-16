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

echo ✅ Python détecté
echo.

REM Vérifier PyInstaller
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installation de PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ Erreur lors de l'installation de PyInstaller
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller installé
echo.

REM Vérifier les dépendances
echo 📦 Vérification des dépendances...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)

echo ✅ Dépendances installées
echo.

REM Nettoyer les anciens builds
echo 🧹 Nettoyage des anciens builds...
if exist build rmdir /s /q build
if exist dist\NiTriTe_Web_V13.exe del /q dist\NiTriTe_Web_V13.exe
echo ✅ Nettoyage terminé
echo.

REM Build avec PyInstaller
echo 🔨 Compilation en cours...
echo.
echo ⏳ Cela peut prendre 2-5 minutes...
echo.

pyinstaller --clean NiTriTe_Web_Portable.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors de la compilation
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo    ✅ BUILD TERMINÉ AVEC SUCCÈS !
echo ═══════════════════════════════════════════════════════════
echo.
echo 📁 Emplacement: dist\NiTriTe_Web_V13.exe
echo 📦 Taille:
dir dist\NiTriTe_Web_V13.exe | find "NiTriTe_Web_V13.exe"
echo.
echo ═══════════════════════════════════════════════════════════
echo    🚀 COMMENT UTILISER
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Double-cliquez sur dist\NiTriTe_Web_V13.exe
echo 2. Le navigateur s'ouvrira automatiquement
echo 3. Utilisez l'application web
echo 4. Fermez la fenêtre console pour arrêter
echo.
echo 💡 L'exécutable est TOTALEMENT PORTABLE:
echo    - Aucune installation requise
echo    - Fonctionne sur n'importe quel PC Windows
echo    - Peut être copié sur une clé USB
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM Proposer de tester
set /p test="Voulez-vous tester l'exécutable maintenant ? (O/N) : "
if /i "%test%"=="O" (
    echo.
    echo 🚀 Lancement de NiTriTe Web Portable...
    start "" "dist\NiTriTe_Web_V13.exe"
)

echo.
pause
