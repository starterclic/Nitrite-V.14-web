@echo off
title NiTriTe V13 - Build Version Bureau
color 0A

echo.
echo ===============================================================
echo    NiTriTe V13 - Build Version Bureau (Tkinter)
echo ===============================================================
echo.
echo Ce script compile la version bureau en executable portable
echo Duree estimee : 2-5 minutes
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

REM Verifier que build_v13.py existe
if not exist "..\build_v13.py" (
    echo [ERREUR] build_v13.py non trouve
    echo.
    echo Assurez-vous que le fichier existe a la racine du projet
    pause
    exit /b 1
)

echo [OK] Script de build trouve
echo.

REM Verifier PyInstaller
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installation de PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [ERREUR] Impossible d'installer PyInstaller
        pause
        exit /b 1
    )
)

echo [OK] PyInstaller installe
echo.

REM Lancer le script de build
echo ===============================================================
echo    COMPILATION EN COURS
echo ===============================================================
echo.

cd ..
python build_v13.py
set BUILD_ERROR=%errorlevel%
cd batch

if %BUILD_ERROR% neq 0 (
    echo.
    echo ===============================================================
    echo    BUILD ECHOUE
    echo ===============================================================
    echo.
    echo Solutions:
    echo  - Reinstaller PyInstaller: pip install --upgrade pyinstaller
    echo  - Verifier requirements: pip install -r requirements.txt
    echo  - Consulter docs\troubleshooting.md
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================================
echo    BUILD TERMINE AVEC SUCCES !
echo ===============================================================
echo.
echo Executable cree: dist\NiTriTe_V13_Modern.exe
echo.
echo L'executable est totalement portable:
echo  - Aucune installation Python requise
echo  - Fonctionne sur Windows 10/11
echo  - Peut etre copie sur cle USB
echo.

set /p test="Voulez-vous tester l'executable maintenant ? (O/N) : "
if /i "%test%"=="O" (
    echo.
    echo [INFO] Lancement...
    start "" "..\dist\NiTriTe_V13_Modern.exe"
)

echo.
pause
