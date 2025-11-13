@echo off
:: NiTriTe V.13 - Web Version Launcher
:: Lance le serveur web et ouvre le navigateur

title NiTriTe V.13 - Web Version

echo ====================================
echo   NiTriTe V.13 - Version Web
echo ====================================
echo.
echo Demarrage du serveur web...
echo.

:: Install Flask dependencies if needed
pip install flask flask-cors psutil >nul 2>&1

:: Start the web server
echo Serveur web demarre sur http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

:: Open browser
start http://localhost:5000

:: Run backend
python web_backend.py

pause
