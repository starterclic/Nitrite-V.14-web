@echo off
chcp 65001 > nul
title Suppression Environnement Virtuel - NiTrite
color 0C

echo.
echo ═══════════════════════════════════════════════════════════
echo    🗑️  SUPPRESSION ENVIRONNEMENT VIRTUEL NITRITE
echo ═══════════════════════════════════════════════════════════
echo.

if not exist "venv_nitrite" (
    color 0E
    echo ⚠️  Aucun environnement virtuel trouvé
    echo.
    pause
    exit /b 0
)

echo 📁 Environnement virtuel détecté: venv_nitrite\
echo.
echo ⚠️  ATTENTION: Cette action va supprimer:
echo    • Toutes les dépendances Python de NiTrite
echo    • L'environnement virtuel complet
echo.
echo 💡 Note: NiTrite ne sera pas supprimé, seulement l'environnement
echo.

choice /C ON /M "Êtes-vous sûr de vouloir supprimer l'environnement virtuel (O/N)"
if errorlevel 2 goto :cancel
if errorlevel 1 goto :delete

:delete
echo.
echo 🗑️  Suppression en cours...
echo.

REM Désactiver l'environnement s'il est actif
call venv_nitrite\Scripts\deactivate.bat 2>nul

REM Supprimer le dossier
rmdir /s /q venv_nitrite

if exist "venv_nitrite" (
    color 0C
    echo ❌ Erreur lors de la suppression
    echo.
    echo 💡 Fermez tous les programmes Python et réessayez
    echo.
    pause
    exit /b 1
)

color 0A
echo ✅ Environnement virtuel supprimé avec succès
echo.
echo 💡 Pour recréer l'environnement:
echo    setup_venv.bat
echo.
goto :end

:cancel
color 0E
echo.
echo ℹ️  Suppression annulée
echo.

:end
pause
