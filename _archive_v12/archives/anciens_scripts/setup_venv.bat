@echo off
chcp 65001 > nul
title Configuration Environnement Virtuel - NiTrite v.2.5
color 0B

echo.
echo ═══════════════════════════════════════════════════════════
echo    🔧 CONFIGURATION ENVIRONNEMENT VIRTUEL NITRITE
echo ═══════════════════════════════════════════════════════════
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ❌ ERREUR: Python n'est pas installé
    echo.
    echo 📥 Installer Python depuis: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version
echo.

REM Vérifier si l'environnement virtuel existe déjà
if exist "venv_nitrite" (
    echo ⚠️  Environnement virtuel existant détecté
    echo.
    choice /C ON /M "Voulez-vous le recréer (O) ou garder l'existant (N)"
    if errorlevel 2 goto :skip_creation
    if errorlevel 1 goto :recreate_venv
)

:recreate_venv
echo.
echo 🗑️  Suppression de l'ancien environnement...
if exist "venv_nitrite" rmdir /s /q venv_nitrite
echo.

echo 📦 Création de l'environnement virtuel...
python -m venv venv_nitrite

if errorlevel 1 (
    color 0C
    echo ❌ Erreur lors de la création de l'environnement virtuel
    echo.
    pause
    exit /b 1
)

echo ✅ Environnement virtuel créé
echo.

:skip_creation
echo 🔄 Activation de l'environnement virtuel...
call venv_nitrite\Scripts\activate.bat

if errorlevel 1 (
    color 0C
    echo ❌ Erreur lors de l'activation
    pause
    exit /b 1
)

echo ✅ Environnement activé
echo.

echo 📥 Mise à jour de pip...
python -m pip install --upgrade pip --quiet

echo.
echo 📦 Installation des dépendances NiTrite...
echo.

echo    → Installation de pywin32...
pip install pywin32 --quiet
if errorlevel 1 (
    echo    ⚠️  Erreur avec pywin32
) else (
    echo    ✅ pywin32 installé
)

echo    → Installation de winshell...
pip install winshell --quiet
if errorlevel 1 (
    echo    ⚠️  Erreur avec winshell
) else (
    echo    ✅ winshell installé
)

echo    → Installation de requests...
pip install requests --quiet
if errorlevel 1 (
    echo    ⚠️  Erreur avec requests
) else (
    echo    ✅ requests installé
)

echo.
echo ═══════════════════════════════════════════════════════════
echo    ✅ CONFIGURATION TERMINÉE
echo ═══════════════════════════════════════════════════════════
echo.
echo 📦 Dépendances installées dans: venv_nitrite\
echo.
echo 🚀 Pour lancer NiTrite, utilisez:
echo    Lancer_NiTrite_VEnv.bat
echo.
echo 💡 Avantages de l'environnement virtuel:
echo    ✅ Dépendances isolées du système
echo    ✅ Pas d'impact sur autres applications Python
echo    ✅ Facile à supprimer (dossier venv_nitrite)
echo.
echo ═══════════════════════════════════════════════════════════
echo.

pause
