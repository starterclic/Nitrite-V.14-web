@echo off
chcp 65001 > nul
cls
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║        🔍 VÉRIFICATION AVANT BUILD - NiTrite v2.0             ║
echo ║           Version Portable Autonome                           ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.

echo [1/6] 📋 Vérification des fichiers sources...
echo.

if exist "nitrite_complet.py" (
    echo    ✅ nitrite_complet.py
) else (
    echo    ❌ nitrite_complet.py MANQUANT!
    goto :error
)

if exist "NiTrite_OrdiPlus_v2.spec" (
    echo    ✅ NiTrite_OrdiPlus_v2.spec
) else (
    echo    ❌ NiTrite_OrdiPlus_v2.spec MANQUANT!
    goto :error
)

if exist "build_exe.py" (
    echo    ✅ build_exe.py
) else (
    echo    ❌ build_exe.py MANQUANT!
    goto :error
)

echo.
echo [2/6] 📁 Vérification des dossiers requis...
echo.

if exist "data" (
    echo    ✅ Dossier data/
    if exist "data\programs.json" (
        echo       ✅ programs.json trouvé
    ) else (
        echo       ⚠️  programs.json manquant (optionnel)
    )
) else (
    echo    ❌ Dossier data/ MANQUANT!
    goto :error
)

if exist "src" (
    echo    ✅ Dossier src/
    if exist "src\gui_manager.py" (
        echo       ✅ gui_manager.py trouvé
    ) else (
        echo       ❌ gui_manager.py MANQUANT!
        goto :error
    )
    if exist "src\installer_manager.py" (
        echo       ✅ installer_manager.py trouvé
    ) else (
        echo       ❌ installer_manager.py MANQUANT!
        goto :error
    )
) else (
    echo    ❌ Dossier src/ MANQUANT!
    goto :error
)

if exist "assets" (
    echo    ✅ Dossier assets/ (optionnel)
) else (
    echo    ⚠️  Dossier assets/ manquant (l'app fonctionnera sans logo)
    mkdir assets 2>nul
    echo    📁 Dossier assets/ créé
)

echo.
echo [3/6] 🐍 Vérification de Python...
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo    ✅ Python installé
) else (
    echo    ❌ Python NON installé!
    echo.
    echo    💡 Installez Python depuis python.org
    goto :error
)

echo.
echo [4/6] 📦 Vérification de PyInstaller...
echo.

python -c "import PyInstaller; print(f'   ✅ PyInstaller {PyInstaller.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo    ❌ PyInstaller NON installé!
    echo.
    echo    💡 Pour installer: pip install pyinstaller
    goto :error
)

echo.
echo [5/6] 📚 Vérification des dépendances Python...
echo.

python -c "import tkinter; print('   ✅ tkinter')" 2>nul || echo    ❌ tkinter manquant!
python -c "import requests; print('   ✅ requests')" 2>nul || echo    ⚠️  requests manquant (sera embarqué)
python -c "import PIL; print('   ✅ Pillow (PIL)')" 2>nul || echo    ⚠️  Pillow manquant (sera embarqué)
python -c "import win32com.client; print('   ✅ pywin32')" 2>nul || echo    ⚠️  pywin32 manquant (sera embarqué)

echo.
echo [6/6] 💾 Vérification de l'espace disque...
echo.
echo    💾 Espace requis: ~500 MB pour la compilation
echo    📦 Taille finale exe: ~27 MB
echo.

echo ════════════════════════════════════════════════════════════════
echo.
echo ✅ TOUTES LES VÉRIFICATIONS SONT PASSÉES !
echo.
echo 🚀 Vous pouvez maintenant lancer la compilation :
echo    BUILD_AUTONOME.bat
echo.
echo ════════════════════════════════════════════════════════════════
echo.
pause
goto :end

:error
echo.
echo ════════════════════════════════════════════════════════════════
echo ❌ ERREUR - Des fichiers sont manquants!
echo ════════════════════════════════════════════════════════════════
echo.
echo 💡 Corrigez les erreurs ci-dessus avant de continuer.
echo.
pause
exit /b 1

:end