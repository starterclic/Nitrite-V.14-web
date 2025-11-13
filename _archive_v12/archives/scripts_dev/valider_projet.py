#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation complète du projet NiTrite v.2
Vérifie tous les aspects du projet de A à Z
"""

import sys
import json
from pathlib import Path
import subprocess

# Couleurs
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text:^70}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def test_structure():
    """Teste la structure du projet"""
    print_header("TEST 1: STRUCTURE DU PROJET")
    
    required_dirs = {
        "src": "Code source",
        "data": "Fichiers de données",
        "assets": "Ressources visuelles",
        "docs": "Documentation",
        "tests": "Tests unitaires",
        "logs": "Fichiers de logs"
    }
    
    all_ok = True
    for dir_name, desc in required_dirs.items():
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            file_count = len(list(dir_path.rglob('*')))
            print_success(f"{desc} ({dir_name}/) - {file_count} fichiers")
        else:
            print_error(f"{desc} ({dir_name}/) - MANQUANT")
            all_ok = False
    
    return all_ok

def test_source_files():
    """Teste les fichiers source"""
    print_header("TEST 2: FICHIERS SOURCE")
    
    required_files = {
        "src/gui_manager_complet.py": "Interface graphique complète",
        "src/installer_manager.py": "Gestionnaire d'installation",
        "src/config_manager.py": "Gestionnaire de configuration",
        "nitrite_complet.py": "Lanceur principal",
        "build_portable_complet.py": "Script de build"
    }
    
    all_ok = True
    for file_path, desc in required_files.items():
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size / 1024
            print_success(f"{desc} - {size:.1f} KB")
        else:
            print_error(f"{desc} - MANQUANT")
            all_ok = False
    
    return all_ok

def test_data_files():
    """Teste les fichiers de données"""
    print_header("TEST 3: FICHIERS DE DONNÉES")
    
    all_ok = True
    
    # Test programs.json
    programs_file = Path("data/programs.json")
    if programs_file.exists():
        try:
            with open(programs_file, 'r', encoding='utf-8') as f:
                programs = json.load(f)
            total_programs = sum(len(progs) for progs in programs.values())
            print_success(f"programs.json - {total_programs} programmes dans {len(programs)} catégories")
        except json.JSONDecodeError as e:
            print_error(f"programs.json - Erreur JSON: {e}")
            all_ok = False
    else:
        print_error("programs.json - MANQUANT")
        all_ok = False
    
    # Test config.json
    config_file = Path("data/config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print_success("config.json - Valide")
        except json.JSONDecodeError as e:
            print_error(f"config.json - Erreur JSON: {e}")
            all_ok = False
    else:
        print_warning("config.json - Optionnel, non trouvé")
    
    return all_ok

def test_code_quality():
    """Teste la qualité du code"""
    print_header("TEST 4: QUALITÉ DU CODE")
    
    issues = []
    
    # Vérifier les except: nus (mauvaise pratique)
    print_info("Vérification des gestionnaires d'exceptions...")
    src_files = list(Path("src").rglob("*.py"))
    
    for src_file in src_files:
        try:
            content = src_file.read_text(encoding='utf-8')
            # Chercher "except:" sans spécification
            if "except:" in content and "except Exception" not in content:
                # Vérifier si ce n'est pas un faux positif
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if line.strip() == "except:" or line.strip().startswith("except:"):
                        issues.append(f"{src_file.name}:{i} - except: nu (non spécifique)")
        except Exception as e:
            print_warning(f"Impossible de lire {src_file}: {e}")
    
    if not issues:
        print_success("Aucun problème de gestion d'exceptions trouvé")
    else:
        for issue in issues[:5]:  # Afficher max 5
            print_warning(issue)
        if len(issues) > 5:
            print_info(f"... et {len(issues) - 5} autres problèmes")
    
    return len(issues) == 0

def test_imports():
    """Teste les imports Python"""
    print_header("TEST 5: IMPORTS PYTHON")
    
    sys.path.insert(0, str(Path.cwd() / 'src'))
    
    modules_to_test = [
        ("config_manager", "ConfigManager"),
        ("installer_manager", "InstallerManager"),
        ("gui_manager_complet", "NiTriteGUIComplet"),
    ]
    
    all_ok = True
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                print_success(f"{module_name}.{class_name} - OK")
            else:
                print_error(f"{module_name}.{class_name} - Classe non trouvée")
                all_ok = False
        except ImportError as e:
            print_error(f"{module_name} - Erreur d'import: {e}")
            all_ok = False
        except Exception as e:
            print_warning(f"{module_name} - Avertissement: {e}")
    
    return all_ok

def test_dependencies():
    """Teste les dépendances Python"""
    print_header("TEST 6: DÉPENDANCES PYTHON")
    
    required_packages = [
        "tkinter",
        "PIL",
        "requests",
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} - Installé")
        except ImportError:
            print_error(f"{package} - MANQUANT")
            all_ok = False
    
    return all_ok

def test_portable_package():
    """Teste le package portable"""
    print_header("TEST 7: PACKAGE PORTABLE")
    
    portable_dir = Path("NiTrite_Portable")
    if not portable_dir.exists():
        print_warning("Package portable non trouvé - Exécutez build_portable_complet.py")
        return True  # Pas une erreur critique
    
    required_items = {
        "NiTrite_OrdiPlus_v2.exe": "Exécutable principal",
        "Lancer_NiTrite.bat": "Lanceur .bat",
        "data": "Dossier de données",
        "README.txt": "Documentation"
    }
    
    all_ok = True
    for item, desc in required_items.items():
        item_path = portable_dir / item
        if item_path.exists():
            if item_path.is_file():
                size = item_path.stat().st_size / (1024 * 1024)
                print_success(f"{desc} - {size:.1f} MB")
            else:
                file_count = len(list(item_path.rglob('*')))
                print_success(f"{desc} - {file_count} fichiers")
        else:
            print_error(f"{desc} - MANQUANT")
            all_ok = False
    
    return all_ok

def test_documentation():
    """Teste la documentation"""
    print_header("TEST 8: DOCUMENTATION")
    
    doc_files = [
        "README.md",
        "README_PROJET.md",
        "CORRECTION_BOUTON_INSTALLER.md"
    ]
    
    found = 0
    for doc_file in doc_files:
        if Path(doc_file).exists():
            print_success(f"{doc_file}")
            found += 1
        else:
            print_warning(f"{doc_file} - Non trouvé")
    
    print_info(f"{found}/{len(doc_files)} fichiers de documentation trouvés")
    return found > 0

def run_all_tests():
    """Exécute tous les tests"""
    print(f"\n{Colors.BOLD}{Colors.WHITE}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║        VALIDATION COMPLÈTE - NITRITE V.2 ORDI PLUS          ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    tests = [
        ("Structure du projet", test_structure),
        ("Fichiers source", test_source_files),
        ("Fichiers de données", test_data_files),
        ("Qualité du code", test_code_quality),
        ("Imports Python", test_imports),
        ("Dépendances", test_dependencies),
        ("Package portable", test_portable_package),
        ("Documentation", test_documentation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Erreur pendant {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print_header("RÉSUMÉ DES TESTS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.END} - {test_name}")
    
    print(f"\n{Colors.BOLD}Score: {passed}/{total} tests réussis{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TOUS LES TESTS SONT PASSÉS !{Colors.END}")
        print(f"{Colors.GREEN}Le projet est prêt pour la distribution.{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}⚠️  Certains tests ont échoué.{Colors.END}")
        print(f"{Colors.YELLOW}Veuillez corriger les problèmes avant la distribution.{Colors.END}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrompus par l'utilisateur{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Erreur fatale: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
