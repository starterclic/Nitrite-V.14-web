@echo off
chcp 65001 > nul
cls
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║        🚀 BUILD NITRITE AUTONOME v2.0                         ║
echo ║           Version 100%% Portable - Aucune dépendance          ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo 📋 Ce script va créer :
echo    • Un exécutable .exe avec Python embarqué (~27 MB)
echo    • Un ZIP de distribution prêt à partager (~25 MB)
echo    • AUCUNE installation requise sur PC cible
echo.
echo ⏱️  Temps estimé : 5 minutes
echo.
pause
echo.
echo ════════════════════════════════════════════════════════════════
echo  🔨 DÉMARRAGE DU BUILD
echo ════════════════════════════════════════════════════════════════
echo.

python build_exe.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors du build
    echo.
    echo 💡 Assurez-vous que :
    echo    1. Python est installé
    echo    2. PyInstaller est installé : pip install pyinstaller
    echo    3. requirements.txt est à jour
    echo.
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════════
echo  ✅ BUILD TERMINÉ !
echo ════════════════════════════════════════════════════════════════
echo.
echo 📦 Fichiers créés :
echo.
echo    📂 NiTrite_Autonome\
echo       ├── NiTrite_OrdiPlus_v2.exe  (~27 MB)
echo       ├── LANCER_NITRITE.bat
echo       └── README.txt
echo.
echo    📦 NiTrite_Autonome_v2.0.zip    (~25 MB)
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 🎯 POUR TESTER :
echo    cd NiTrite_Autonome
echo    .\NiTrite_OrdiPlus_v2.exe
echo.
echo 📤 POUR DISTRIBUER :
echo    Partagez : NiTrite_Autonome_v2.0.zip
echo.
echo ✨ AVANTAGES :
echo    ✅ Aucune dépendance (Python inclus dans .exe)
echo    ✅ Fonctionne sur 100%% des PC Windows
echo    ✅ Installation : Décompresser + double-clic
echo    ✅ Portable sur clé USB
echo.
echo ════════════════════════════════════════════════════════════════
echo.
pause
