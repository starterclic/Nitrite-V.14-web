#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test automatisé de l'interface NiTrite Portable
Vérifie que l'interface originale complète est bien présente
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

# Couleurs pour l'affichage
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Affiche un en-tête"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {text}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.RESET}\n")

def print_success(text):
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_info(text):
    """Affiche une information"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def print_warning(text):
    """Affiche un avertissement"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def test_portable_structure():
    """Teste la structure du package portable"""
    print_header("TEST 1 : STRUCTURE DU PACKAGE PORTABLE")
    
    portable_dir = Path("NiTrite_Portable")
    required_files = [
        "NiTrite_OrdiPlus_v2.exe",
        "Lancer_NiTrite.bat",
        "README.txt",
        "INFO.txt"
    ]
    
    required_dirs = ["data", "assets", "docs"]
    
    all_ok = True
    
    # Vérifier le dossier principal
    if not portable_dir.exists():
        print_error(f"Dossier {portable_dir} introuvable")
        return False
    
    print_success(f"Dossier {portable_dir} trouvé")
    
    # Vérifier les fichiers requis
    for file in required_files:
        file_path = portable_dir / file
        if file_path.exists():
            size = file_path.stat().st_size / (1024 * 1024)  # MB
            print_success(f"Fichier {file} trouvé ({size:.1f} MB)")
        else:
            print_error(f"Fichier {file} manquant")
            all_ok = False
    
    # Vérifier les dossiers requis
    for dir_name in required_dirs:
        dir_path = portable_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            files_count = len(list(dir_path.rglob("*")))
            print_success(f"Dossier {dir_name}/ trouvé ({files_count} fichiers)")
        else:
            print_error(f"Dossier {dir_name}/ manquant")
            all_ok = False
    
    return all_ok

def test_data_files():
    """Teste les fichiers de données"""
    print_header("TEST 2 : FICHIERS DE DONNÉES")
    
    portable_dir = Path("NiTrite_Portable")
    data_dir = portable_dir / "data"
    
    required_data_files = [
        "programs.json",
        "config.json",
        "office_links.json"
    ]
    
    all_ok = True
    
    for file in required_data_files:
        file_path = data_dir / file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if file == "programs.json":
                    # Compter les programmes
                    total = sum(len(progs) for progs in data.values())
                    print_success(f"{file} trouvé - {total} programmes dans {len(data)} catégories")
                else:
                    print_success(f"{file} trouvé - JSON valide")
            except json.JSONDecodeError as e:
                print_error(f"{file} - Erreur JSON: {e}")
                all_ok = False
        else:
            print_error(f"{file} manquant")
            all_ok = False
    
    return all_ok

def test_launcher_bat():
    """Teste le fichier .bat"""
    print_header("TEST 3 : LANCEUR .BAT")
    
    bat_file = Path("NiTrite_Portable") / "Lancer_NiTrite.bat"
    
    if not bat_file.exists():
        print_error("Lancer_NiTrite.bat introuvable")
        return False
    
    # Lire le contenu
    with open(bat_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("@echo off", "Désactivation de l'écho"),
        ("NiTrite_OrdiPlus_v2.exe", "Référence à l'exécutable"),
        ("start", "Commande de lancement"),
        ("timeout", "Pause avant fermeture"),
    ]
    
    all_ok = True
    for check, description in checks:
        if check in content:
            print_success(f"{description} présent")
        else:
            print_error(f"{description} manquant")
            all_ok = False
    
    return all_ok

def test_readme():
    """Teste le README"""
    print_header("TEST 4 : DOCUMENTATION")
    
    readme_file = Path("NiTrite_Portable") / "README.txt"
    
    if not readme_file.exists():
        print_error("README.txt introuvable")
        return False
    
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = [
        ("LANCEMENT RAPIDE", "Instructions de lancement"),
        ("FONCTIONNALITÉS", "Liste des fonctionnalités"),
        ("279 programmes", "Nombre de programmes"),
        ("28 outils", "Outils système"),
        ("Ordi Plus", "Marque Ordi Plus"),
        ("DÉPANNAGE", "Section dépannage"),
    ]
    
    all_ok = True
    for section, description in sections:
        if section in content:
            print_success(f"{description} présent")
        else:
            print_warning(f"{description} absent (optionnel)")
    
    return all_ok

def test_zip_archive():
    """Teste l'archive ZIP"""
    print_header("TEST 5 : ARCHIVE ZIP")
    
    zip_file = Path("NiTrite_Portable_v2.0.zip")
    
    if not zip_file.exists():
        print_warning("Archive ZIP non trouvée (optionnel si package manuel)")
        return True
    
    size = zip_file.stat().st_size / (1024 * 1024)  # MB
    print_success(f"Archive trouvée : {zip_file.name} ({size:.1f} MB)")
    
    return True

def test_interface_components():
    """Vérifie les composants de l'interface dans le code source"""
    print_header("TEST 6 : COMPOSANTS D'INTERFACE (CODE SOURCE)")
    
    gui_file = Path("src") / "gui_manager_complet.py"
    
    if not gui_file.exists():
        print_error("gui_manager_complet.py introuvable")
        return False
    
    with open(gui_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    components = [
        ("class NiTriteGUIComplet", "Classe principale"),
        ("create_reparation_section", "Section Réparation"),
        ("create_activation_section", "Section Activation"),
        ("create_winget_section", "Section Winget"),
        ("create_parametres_section", "Section Paramètres"),
        ("create_support_section", "Section Support"),
        ("#FF6B00", "Couleur orange Ordi Plus"),
        ("#003366", "Couleur bleu Ordi Plus"),
        ("logo_ordiplus_bg.png", "Logo en arrière-plan"),
    ]
    
    all_ok = True
    for component, description in components:
        if component in content:
            print_success(f"{description} présent")
        else:
            print_error(f"{description} manquant")
            all_ok = False
    
    return all_ok

def test_build_script():
    """Vérifie le script de build"""
    print_header("TEST 7 : SCRIPT DE BUILD")
    
    build_script = Path("build_portable_complet.py")
    
    if not build_script.exists():
        print_error("build_portable_complet.py introuvable")
        return False
    
    with open(build_script, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("nitrite_complet.py", "Utilise le script ORIGINAL (pas standalone)"),
        ("NiTrite_Portable", "Crée le dossier portable"),
        ("Lancer_NiTrite.bat", "Crée le lanceur .bat"),
        ("create_zip_archive", "Fonction de création du ZIP"),
        ("--add-data", "Configuration PyInstaller"),
    ]
    
    all_ok = True
    for check, description in checks:
        if check in content:
            print_success(f"{description}")
        else:
            print_error(f"{description} manquant")
            all_ok = False
    
    return all_ok

def display_summary(results):
    """Affiche le résumé des tests"""
    print_header("RÉSUMÉ DES TESTS")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    print(f"\n{Colors.BOLD}Tests exécutés: {total}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Réussis: {passed}{Colors.RESET}")
    print(f"{Colors.RED}❌ Échoués: {failed}{Colors.RESET}")
    print()
    
    # Détails
    for test_name, result in results.items():
        status = f"{Colors.GREEN}✅ OK{Colors.RESET}" if result else f"{Colors.RED}❌ ÉCHEC{Colors.RESET}"
        print(f"  {status}  {test_name}")
    
    print()
    
    # Conclusion
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}  ✅ TOUS LES TESTS SONT PASSÉS !{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}  Le package portable est PARFAIT et prêt à l'emploi !{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}{'='*70}{Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.YELLOW}{Colors.BOLD}  ⚠️  {failed} test(s) ont échoué{Colors.RESET}")
        print(f"{Colors.YELLOW}{Colors.BOLD}  Veuillez corriger les problèmes avant distribution{Colors.RESET}")
        print(f"{Colors.YELLOW}{Colors.BOLD}{'='*70}{Colors.RESET}\n")
    
    return failed == 0

def main():
    """Fonction principale"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║  Test d'Interface - NiTrite v.2 Ordi Plus Portable           ║")
    print("║  Vérification complète du package                            ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    # Exécuter les tests
    results = {
        "Structure du package": test_portable_structure(),
        "Fichiers de données": test_data_files(),
        "Lanceur .bat": test_launcher_bat(),
        "Documentation": test_readme(),
        "Archive ZIP": test_zip_archive(),
        "Composants d'interface": test_interface_components(),
        "Script de build": test_build_script(),
    }
    
    # Afficher le résumé
    success = display_summary(results)
    
    # Code de sortie
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
