@echo off
chcp 65001 > nul
echo ════════════════════════════════════════════════════════════
echo    🧹 NETTOYAGE ET ORGANISATION DU PROJET NITRITE
echo ════════════════════════════════════════════════════════════
echo.

:: Créer les dossiers d'organisation
echo [1/5] Création des dossiers d'organisation...
if not exist "archives\scripts_dev" mkdir "archives\scripts_dev"
if not exist "archives\builds_anciens" mkdir "archives\builds_anciens"
if not exist "archives\documentation_dev" mkdir "archives\documentation_dev"
if not exist "archives\fichiers_temporaires" mkdir "archives\fichiers_temporaires"
echo ✅ Dossiers créés

:: Déplacer les scripts de développement
echo.
echo [2/5] Archivage des scripts de développement...
move /Y analyser_tous_programmes.py "archives\scripts_dev\" 2>nul
move /Y analyzer_urls.py "archives\scripts_dev\" 2>nul
move /Y correction_automatique_complete.py "archives\scripts_dev\" 2>nul
move /Y corriger_23_warnings.py "archives\scripts_dev\" 2>nul
move /Y corriger_9_erreurs.py "archives\scripts_dev\" 2>nul
move /Y corriger_ordiplus.py "archives\scripts_dev\" 2>nul
move /Y corriger_toutes_urls.py "archives\scripts_dev\" 2>nul
move /Y corriger_urls.py "archives\scripts_dev\" 2>nul
move /Y fix_nitrite.py "archives\scripts_dev\" 2>nul
move /Y identifier_warnings.py "archives\scripts_dev\" 2>nul
move /Y nettoyer_doublons.py "archives\scripts_dev\" 2>nul
move /Y organiser_fichiers.py "archives\scripts_dev\" 2>nul
move /Y stats_final.py "archives\scripts_dev\" 2>nul
move /Y supprimer_sans_solution.py "archives\scripts_dev\" 2>nul
move /Y valider_projet.py "archives\scripts_dev\" 2>nul
move /Y verifier_toutes_urls.py "archives\scripts_dev\" 2>nul
echo ✅ Scripts de dev archivés

:: Déplacer les scripts de test
echo.
echo [3/5] Archivage des scripts de test...
if not exist "tests\anciens_tests" mkdir "tests\anciens_tests"
move /Y test_bouton_installer.py "tests\anciens_tests\" 2>nul
move /Y test_checkboxes.py "tests\anciens_tests\" 2>nul
move /Y test_installation_debug.py "tests\anciens_tests\" 2>nul
move /Y test_interface_portable.py "tests\anciens_tests\" 2>nul
move /Y test_ordiplus.py "tests\anciens_tests\" 2>nul
move /Y test_rapide_stats.py "tests\anciens_tests\" 2>nul
move /Y test_tous_programmes.py "tests\anciens_tests\" 2>nul
move /Y test_urls_ordiplus.py "tests\anciens_tests\" 2>nul
echo ✅ Scripts de test archivés

:: Déplacer les anciens builds
echo.
echo [4/5] Archivage des anciens builds...
move /Y build_portable_autonome.py "archives\builds_anciens\" 2>nul
move /Y BUILD_PORTABLE_AUTONOME_ULTIME.bat "archives\builds_anciens\" 2>nul
move /Y BUILD_PORTABLE_COMPLET.bat "archives\builds_anciens\" 2>nul
move /Y build_portable_complet.py "archives\builds_anciens\" 2>nul
move /Y BUILD_PORTABLE_COMPLETE.bat "archives\builds_anciens\" 2>nul
move /Y NiTrite_Portable\ "archives\builds_anciens\" 2>nul
move /Y NiTrite_Portable_Complet\ "archives\builds_anciens\" 2>nul
move /Y NiTrite_Portable_Complet.zip "archives\builds_anciens\" 2>nul
echo ✅ Anciens builds archivés

:: Déplacer la documentation de développement
echo.
echo [5/5] Archivage de la documentation de développement...
move /Y CORRECTION_BOUTON_INSTALLER.md "archives\documentation_dev\" 2>nul
move /Y CORRECTION_COMPLETE_RAPPORT.md "archives\documentation_dev\" 2>nul
move /Y CORRECTION_INSTALLATIONS.md "archives\documentation_dev\" 2>nul
move /Y MISE_A_JOUR_AUTOMATIQUE_URLS.md "archives\documentation_dev\" 2>nul
move /Y NETTOYAGE_EFFECTUÉ.txt "archives\documentation_dev\" 2>nul
move /Y NETTOYAGE_TERMINE.md "archives\documentation_dev\" 2>nul
move /Y BUILD_REUSSI.md "archives\documentation_dev\" 2>nul
move /Y RECAPITULATIF_FINAL.md "archives\documentation_dev\" 2>nul
move /Y LIRE_ICI.txt "archives\documentation_dev\" 2>nul
echo ✅ Documentation archivée

:: Nettoyer les fichiers temporaires
echo.
echo [BONUS] Nettoyage des fichiers temporaires...
del /Q debug.log 2>nul
del /Q python-installer.exe 2>nul
del /Q install_dependencies.bat 2>nul
del /Q install_winget.bat 2>nul
del /Q DEMO_INTERACTIVE.bat 2>nul
echo ✅ Fichiers temporaires supprimés

:: Nettoyer les dossiers build et dist
echo.
echo [BONUS] Nettoyage des dossiers de build...
if exist "build" (
    rmdir /S /Q "build" 2>nul
    echo ✅ Dossier build supprimé
)
if exist "dist" (
    rmdir /S /Q "dist" 2>nul
    echo ✅ Dossier dist supprimé
)

echo.
echo ════════════════════════════════════════════════════════════
echo    ✅ NETTOYAGE TERMINÉ !
echo ════════════════════════════════════════════════════════════
echo.
echo 📁 STRUCTURE FINALE DU PROJET :
echo.
echo    NiTrite v.2/
echo    ├── 🚀 BUILD_PORTABLE_SIMPLE.bat    (Build portable)
echo    ├── 📄 nitrite_complet.py           (Application principale)
echo    ├── 📋 requirements.txt             (Dépendances)
echo    ├── ⚙️ NiTrite_OrdiPlus_v2.spec    (Config PyInstaller)
echo    │
echo    ├── 📦 NiTrite_Portable_Simple/     (Version portable)
echo    ├── 📦 NiTrite_Portable_v2.0.zip    (Distribution)
echo    │
echo    ├── 📁 src/                         (Code source)
echo    ├── 📁 data/                        (Base de données)
echo    ├── 📁 tests/                       (Tests)
echo    ├── 📁 docs/                        (Documentation)
echo    │
echo    ├── 📁 archives/                    (Fichiers archivés)
echo    │   ├── scripts_dev/
echo    │   ├── builds_anciens/
echo    │   ├── documentation_dev/
echo    │   └── ...
echo    │
echo    └── 📖 README_PROJET.md             (Documentation)
echo.
echo ════════════════════════════════════════════════════════════
pause
