================================================================================
  NiTriTe V13.0 - Guide de Build Rapide
================================================================================

POUR BUILDER L'APPLICATION PORTABLE :
======================================

Option 1 - Double-clic (le plus simple)
---------------------------------------
  1. Double-cliquez sur BUILD.bat
  2. Attendez 5-10 minutes
  3. Récupérez le ZIP dans dist/

Option 2 - Ligne de commande
-----------------------------
  1. Ouvrez CMD ou PowerShell dans ce dossier
  2. Tapez : python build_v13.py
  3. Attendez 5-10 minutes
  4. Récupérez le ZIP dans dist/

RÉSULTAT
========
  dist/NiTriTe_V13_Portable_YYYYMMDD.zip
  └── Contient l'exe portable prêt à distribuer

PRÉREQUIS
=========
  - Windows 10/11 (x64)
  - Python 3.8 ou supérieur
  - Connexion Internet (pour télécharger les dépendances)
  - 5-10 minutes de patience

LE SCRIPT FAIT TOUT AUTOMATIQUEMENT
====================================
  ✓ Vérifie Python 3.8+
  ✓ Installe PyInstaller, Pillow, requests, pywin32, etc.
  ✓ Nettoie les anciens builds
  ✓ Compile l'exe portable (35-50 MB)
  ✓ Crée le package ZIP

  Aucune action manuelle requise !

DOCUMENTATION DÉTAILLÉE
========================
  BUILD_SIMPLE.md          - Guide ultra-simple en 1 commande
  BUILD_QUICK_START.md     - Guide 3 étapes détaillé
  GUIDE_BUILD_WINDOWS.md   - Guide complet avancé
  MODE_PORTABLE.md         - Tout sur le mode portable

EN CAS DE PROBLÈME
==================
  1. Vérifiez que Python est dans le PATH
     python --version

  2. Vérifiez votre connexion Internet

  3. Désactivez temporairement l'antivirus

  4. Consultez BUILD_SIMPLE.md section "Dépannage"

  5. Essayez manuellement :
     pip install -r requirements.txt
     python build_v13.py

SUPPORT
=======
  Consultez la documentation dans les fichiers MD
  Tous les guides sont dans le dossier racine

================================================================================
Version : 13.0
Build : Automatique avec installation des dépendances
Mode : 100% Portable (rien sur le PC client)
================================================================================
