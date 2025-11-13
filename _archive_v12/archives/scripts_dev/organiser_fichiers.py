#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de nettoyage et organisation des fichiers du projet NiTrite v.2
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Couleurs
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {text}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def nettoyer_logs():
    """Nettoie les anciens fichiers de logs"""
    print_header("NETTOYAGE DES LOGS")
    
    logs_dir = Path("logs")
    if not logs_dir.exists():
        print_info("Aucun dossier logs/ trouvé")
        return
    
    logs_supprimes = 0
    for log_file in logs_dir.glob("*.log"):
        # Garder seulement nitrite_20251105.log (aujourd'hui)
        if log_file.name not in ["nitrite_20251105.log", "nitrite.log"]:
            try:
                log_file.unlink()
                print_success(f"Supprimé: {log_file.name}")
                logs_supprimes += 1
            except Exception as e:
                print_warning(f"Impossible de supprimer {log_file.name}: {e}")
    
    print_info(f"{logs_supprimes} fichier(s) de log supprimé(s)")

def organiser_scripts():
    """Organise les scripts dans scripts/"""
    print_header("ORGANISATION DES SCRIPTS")
    
    scripts_dir = Path("scripts")
    scripts_dir.mkdir(exist_ok=True)
    
    # Scripts à déplacer
    scripts_a_deplacer = [
        "build_portable.py",
        "create_massive_database.py",
        "install_dependencies.py",
        "isoler_versions.py",
        "list_all_programs.py",
        "nettoyer_conflits.py",
        "corriger_erreur_powershell.py",
        "diagnostic_nitrite.py",
    ]
    
    deplaces = 0
    for script in scripts_a_deplacer:
        script_path = Path(script)
        if script_path.exists():
            dest = scripts_dir / script
            try:
                shutil.move(str(script_path), str(dest))
                print_success(f"Déplacé: {script} → scripts/")
                deplaces += 1
            except Exception as e:
                print_warning(f"Erreur pour {script}: {e}")
    
    print_info(f"{deplaces} script(s) déplacé(s)")

def organiser_fichiers_bat():
    """Organise les fichiers .bat"""
    print_header("ORGANISATION DES FICHIERS .BAT")
    
    # Créer dossier lanceurs
    lanceurs_dir = Path("lanceurs")
    lanceurs_dir.mkdir(exist_ok=True)
    
    # Fichiers .bat à garder à la racine
    bat_racine = [
        "BUILD_PORTABLE_COMPLET.bat",
        "DEMO_INTERACTIVE.bat",
    ]
    
    # Fichiers .bat à déplacer
    bat_a_deplacer = [
        "Lancer_NiTrite_DARK.bat",
        "Lancer_NiTrite_WINGET.bat",
        "Lancer_NiTrite_Complet.bat",
        "correction_simple.ps1",
        "corriger_nitrite_1.ps1",
        "corriger_nitrite_1_v2.ps1",
        "temp_dism.ps1",
        "Creer_Raccourci_Bureau.ps1",
    ]
    
    deplaces = 0
    for bat in bat_a_deplacer:
        bat_path = Path(bat)
        if bat_path.exists():
            dest = lanceurs_dir / bat
            try:
                shutil.move(str(bat_path), str(dest))
                print_success(f"Déplacé: {bat} → lanceurs/")
                deplaces += 1
            except Exception as e:
                print_warning(f"Erreur pour {bat}: {e}")
    
    print_info(f"{deplaces} fichier(s) .bat/.ps1 déplacé(s)")

def nettoyer_pycache():
    """Supprime les dossiers __pycache__"""
    print_header("NETTOYAGE DES __pycache__")
    
    supprimes = 0
    for pycache in Path(".").rglob("__pycache__"):
        try:
            shutil.rmtree(pycache, ignore_errors=True)
            print_success(f"Supprimé: {pycache}")
            supprimes += 1
        except Exception as e:
            print_warning(f"Erreur: {e}")
    
    print_info(f"{supprimes} dossier(s) __pycache__ supprimé(s)")

def nettoyer_spec():
    """Supprime les fichiers .spec PyInstaller"""
    print_header("NETTOYAGE DES FICHIERS .SPEC")
    
    supprimes = 0
    for spec in Path(".").glob("*.spec"):
        try:
            spec.unlink()
            print_success(f"Supprimé: {spec.name}")
            supprimes += 1
        except Exception as e:
            print_warning(f"Erreur: {e}")
    
    print_info(f"{supprimes} fichier(s) .spec supprimé(s)")

def nettoyer_build_dist():
    """Nettoie les dossiers build et dist temporaires"""
    print_header("NETTOYAGE BUILD ET DIST")
    
    for dossier in ["build", "dist"]:
        dossier_path = Path(dossier)
        if dossier_path.exists():
            try:
                shutil.rmtree(dossier_path, ignore_errors=True)
                print_success(f"Supprimé: {dossier}/")
            except Exception as e:
                print_warning(f"Erreur pour {dossier}/: {e}")

def creer_archive_backup():
    """Archive l'ancien dossier backup 1.2"""
    print_header("ARCHIVAGE DES BACKUPS")
    
    backup_dir = Path("backup 1.2")
    if backup_dir.exists():
        archives_dir = Path("archives")
        archives_dir.mkdir(exist_ok=True)
        
        dest = archives_dir / "backup_1.2_archive"
        if not dest.exists():
            try:
                shutil.move(str(backup_dir), str(dest))
                print_success(f"Archivé: backup 1.2/ → archives/backup_1.2_archive/")
            except Exception as e:
                print_warning(f"Erreur: {e}")
        else:
            print_info("Archive déjà existante")
    else:
        print_info("Aucun dossier backup 1.2/ trouvé")

def afficher_structure():
    """Affiche la structure organisée"""
    print_header("STRUCTURE FINALE DU PROJET")
    
    print(f"""
{Colors.BOLD}Structure recommandée :{Colors.RESET}

📁 Projet NiTrite v.2/
├── 🚀 {Colors.GREEN}nitrite_complet.py{Colors.RESET}          ← Script principal
├── 🚀 {Colors.GREEN}NiTrite_Standalone.py{Colors.RESET}       ← Version standalone
├── 📋 apps.catalog.csv
├── 📖 README.md
├── 📖 PACKAGE_PORTABLE_COMPLET.md
├── 📖 VALIDATION_FINALE.txt
│
├── 🔧 {Colors.YELLOW}BUILD_PORTABLE_COMPLET.bat{Colors.RESET}  ← Build portable
├── 🔧 {Colors.YELLOW}DEMO_INTERACTIVE.bat{Colors.RESET}        ← Démonstration
├── 🔧 {Colors.YELLOW}Lancer_NiTrite.bat{Colors.RESET}          ← Lanceur principal
│
├── 🛠️  {Colors.CYAN}build_portable_complet.py{Colors.RESET}   ← Script de build
├── 🧪 {Colors.CYAN}test_interface_portable.py{Colors.RESET}   ← Tests
├── 📁 {Colors.CYAN}organiser_fichiers.py{Colors.RESET}        ← Ce script
│
├── 📁 data/                        ← Données (JSON)
├── 📁 src/                         ← Code source
│   ├── gui_manager_complet.py     ← Interface complète
│   ├── config_manager.py
│   └── installer_manager.py
│
├── 📁 assets/                      ← Ressources
├── 📁 docs/                        ← Documentation
├── 📁 logs/                        ← Logs actifs uniquement
├── 📁 downloads/                   ← Téléchargements
│
├── 📁 {Colors.BLUE}scripts/{Colors.RESET}                     ← Scripts utilitaires
├── 📁 {Colors.BLUE}lanceurs/{Colors.RESET}                    ← Anciens lanceurs
├── 📁 {Colors.BLUE}archives/{Colors.RESET}                    ← Anciennes versions
│
└── 📦 {Colors.GREEN}NiTrite_Portable/{Colors.RESET}           ← Package portable prêt
    └── 📦 NiTrite_Portable_v2.0.zip  ← Archive de distribution
    """)

def main():
    """Fonction principale"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║  NiTrite v.2 - Nettoyage et Organisation                     ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    print_warning("Ce script va réorganiser les fichiers du projet.")
    reponse = input(f"\n{Colors.YELLOW}Continuer ? (O/N) : {Colors.RESET}").strip().upper()
    
    if reponse != 'O':
        print_info("Opération annulée")
        return
    
    # Exécuter les opérations
    nettoyer_logs()
    nettoyer_pycache()
    nettoyer_spec()
    nettoyer_build_dist()
    organiser_scripts()
    organiser_fichiers_bat()
    creer_archive_backup()
    
    # Afficher le résultat
    afficher_structure()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}  ✅ NETTOYAGE ET ORGANISATION TERMINÉS !{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}{'='*70}{Colors.RESET}\n")
    
    print_info("Le projet est maintenant bien organisé et prêt à l'emploi !")

if __name__ == "__main__":
    main()
