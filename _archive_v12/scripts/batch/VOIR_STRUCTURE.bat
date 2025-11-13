@echo off
chcp 65001 > nul
cls
echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║              🎉 PROJET NITRITE ORDIPLUS V2.0                         ║
echo ║                    NETTOYÉ ET ORGANISÉ !                             ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo.
echo  📁 FICHIERS PRINCIPAUX (racine du projet)
echo  ═══════════════════════════════════════════════════════════════════════
echo.
dir /B *.md *.py *.bat *.txt *.spec *.zip 2>nul | find /V "NETTOYER" | find /V "ORGANISATION"
echo.
echo.
echo  📂 DOSSIERS ORGANISÉS
echo  ═══════════════════════════════════════════════════════════════════════
echo.
for /D %%d in (*) do @echo    📁 %%d
echo.
echo.
echo  🎯 ACCÈS RAPIDE
echo  ═══════════════════════════════════════════════════════════════════════
echo.
echo    [1] 📖 Lire la documentation       → README.md
echo    [2] 🚀 Lancer l'application        → python nitrite_complet.py
echo    [3] 🏗️  Créer version portable      → BUILD_PORTABLE_SIMPLE.bat
echo    [4] 📦 ZIP de distribution         → NiTrite_Portable_v2.0.zip
echo    [5] 📁 Voir les archives           → cd archives
echo    [6] 💻 Voir le code source         → cd src
echo    [7] 📚 Voir la documentation       → cd docs
echo.
echo.
echo  📊 STATISTIQUES
echo  ═══════════════════════════════════════════════════════════════════════
echo.

:: Compter les fichiers
set count=0
for %%f in (*.md *.py *.bat *.txt *.spec *.zip) do set /a count+=1
echo    ✅ Fichiers à la racine : %count%

:: Compter les dossiers
set dircount=0
for /D %%d in (*) do set /a dircount+=1
echo    ✅ Dossiers organisés : %dircount%

echo    ✅ Programmes disponibles : 240+
echo    ✅ Taille version portable : 14 MB
echo    ✅ Taux de réussite : 85-90%%
echo.
echo.
echo  ✨ PRÊT À L'EMPLOI !
echo  ═══════════════════════════════════════════════════════════════════════
echo.
echo    Le projet est maintenant propre, organisé et prêt pour :
echo    ✅ Développement
echo    ✅ Distribution
echo    ✅ Maintenance
echo.
echo.
pause
