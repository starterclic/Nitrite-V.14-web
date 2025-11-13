@echo off
chcp 65001 > nul
title NiTrite v.2.5 OrdiPlus - Environnement Virtuel
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║        🚀 NITRITE v.2.5 - ÉDITION ORDIPLUS 🛠️            ║
echo ║          (Environnement Virtuel Isolé)                   ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv_nitrite" (
    color 0E
    echo ⚠️  ENVIRONNEMENT VIRTUEL NON TROUVÉ
    echo.
    echo 🔧 Configuration requise...
    echo.
    choice /C ON /M "Voulez-vous créer l'environnement virtuel maintenant (O/N)"
    if errorlevel 2 goto :no_setup
    if errorlevel 1 goto :run_setup
    
    :run_setup
    echo.
    call setup_venv.bat
    if errorlevel 1 (
        color 0C
        echo.
        echo ❌ La configuration a échoué
        pause
        exit /b 1
    )
    echo.
    
    :no_setup
    if not exist "venv_nitrite" (
        color 0C
        echo.
        echo ❌ Impossible de continuer sans environnement virtuel
        echo.
        echo 🔧 Exécutez d'abord: setup_venv.bat
        echo.
        pause
        exit /b 1
    )
)

echo ✅ Environnement virtuel trouvé
echo.

REM Activer l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call venv_nitrite\Scripts\activate.bat

if errorlevel 1 (
    color 0C
    echo ❌ Erreur lors de l'activation
    echo.
    pause
    exit /b 1
)

echo ✅ Environnement activé
echo.

REM Créer les dossiers nécessaires
if not exist "logs" mkdir logs
if not exist "downloads" mkdir downloads
if not exist "data" mkdir data

echo 📂 Dossiers vérifiés
echo.

REM Afficher les informations
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  NOUVEAUTÉS v.2.5:                                        ║
echo ║                                                           ║
echo ║  🛠️  Catégorie OrdiPlus (9 outils essentiels)            ║
echo ║  📦 Pack Office 2019/2021/2024 en français               ║
echo ║  🔐 Activation Windows/Office intégrée                   ║
echo ║  📁 Dossier "Outils de nettoyage" auto                   ║
echo ║  🎨 Interface optimisée (5 colonnes)                     ║
echo ║  🔒 Environnement virtuel isolé                          ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

echo 🚀 Lancement de NiTrite v.2.5...
echo.
echo 💡 Dépendances utilisées depuis: venv_nitrite\
echo.

REM Lancer l'application
python nitrite_complet.py

REM Désactiver l'environnement virtuel après fermeture
call venv_nitrite\Scripts\deactivate.bat 2>nul

REM Vérifier le code de sortie
if errorlevel 1 (
    color 0C
    echo.
    echo ╔═══════════════════════════════════════════════════════════╗
    echo ║  ❌ ERREUR LORS DE L'EXÉCUTION                           ║
    echo ╚═══════════════════════════════════════════════════════════╝
    echo.
    echo 📋 Consultez le fichier de log pour plus de détails:
    echo    logs\nitrite.log
    echo.
    pause
    exit /b 1
)

color 0A
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  ✅ NITRITE FERMÉ CORRECTEMENT                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo 🔒 Environnement virtuel désactivé
echo.
echo Merci d'avoir utilisé NiTrite v.2.5 OrdiPlus Edition! 🎯
echo.
pause
