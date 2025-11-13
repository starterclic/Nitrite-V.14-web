@echo off
REM ====================================================================
REM NiTriTe V13.0 - Build Automatique (Windows)
REM ====================================================================
REM
REM Ce script lance build_v13.py qui fait TOUT automatiquement :
REM   - Vérification Python 3.8+
REM   - Installation automatique des dépendances
REM   - Compilation de l'exe portable
REM   - Création du package ZIP
REM
REM Durée : 5-10 minutes (première fois)
REM Résultat : dist/NiTriTe_V13_Portable_YYYYMMDD.zip
REM
REM ====================================================================

title NiTriTe V13 - Build Automatique

REM Afficher le header
echo.
echo ====================================================================
echo  NiTriTe V13.0 - Build Automatique
echo ====================================================================
echo.
echo Ce script va construire l'exe portable avec toutes les dependances
echo Duree estimee : 5-10 minutes (premiere fois)
echo.

REM Vérifier que Python est installé
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

REM Afficher la version Python
echo Python detecte:
python --version
echo.

REM Vérifier que build_v13.py existe
if not exist "build_v13.py" (
    echo ERREUR: build_v13.py non trouve dans ce dossier
    echo.
    echo Assurez-vous d'executer ce script depuis le dossier racine du projet
    echo.
    pause
    exit /b 1
)

echo Lancement du build automatique...
echo.
echo ====================================================================
echo.

REM Lancer le script Python
python build_v13.py

REM Afficher le résultat
echo.
if errorlevel 1 (
    echo.
    echo ====================================================================
    echo  BUILD ECHOUE - Consultez les erreurs ci-dessus
    echo ====================================================================
    echo.
    echo Solutions possibles:
    echo   1. Verifier que vous etes sur Windows 10/11
    echo   2. Verifier votre connexion Internet
    echo   3. Desactiver temporairement l'antivirus
    echo   4. Consulter BUILD_SIMPLE.md pour plus d'aide
    echo.
) else (
    echo.
    echo ====================================================================
    echo  Fichier pret dans dist/
    echo ====================================================================
    echo.
    echo Vous pouvez maintenant distribuer le ZIP a vos clients !
    echo.
)

REM Pause finale déjà dans build_v13.py
REM Donc pas besoin de pause ici
