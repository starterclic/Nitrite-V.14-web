@echo off
chcp 65001 >nul 2>&1
title Vérification du Nombre d'Applications - NiTrite v2.0

echo.
echo ================================================================
echo    🔍 Vérification du nombre d'applications - NiTrite v2.0
echo ================================================================
echo.

python verifier_nombre_apps.py

echo.
echo Appuyez sur une touche pour fermer...
pause >nul
