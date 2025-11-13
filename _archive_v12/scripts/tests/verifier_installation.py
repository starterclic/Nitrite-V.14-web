#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Vérification d'Installation - NiTrite v2.0
=====================================================

Vérifie que tous les composants de NiTrite sont correctement installés
et prêts à l'emploi.
"""

import sys
from pathlib import Path
import json

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Affiche un en-tête"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")


def check_passed(text):
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")


def check_failed(text):
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")


def check_warning(text):
    """Affiche un avertissement"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")


def check_info(text):
    """Affiche une information"""
    print(f"   {text}")


def check_python_version():
    """Vérifie la version de Python"""
    print_header("1. Vérification de Python")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 8:
        check_passed(f"Python {version_str}")
        return True
    else:
        check_failed(f"Python {version_str} (requis: 3.8+)")
        return False


def check_required_modules():
    """Vérifie les modules Python requis"""
    print_header("2. Vérification des Modules Python")

    required_modules = {
        'requests': 'Téléchargement HTTP',
        'PIL': 'Traitement d\'images (Pillow)',
        'tkinter': 'Interface graphique',
        'sqlite3': 'Base de données',
        'json': 'Configuration JSON',
        'pathlib': 'Gestion des chemins'
    }

    all_ok = True
    for module, description in required_modules.items():
        try:
            __import__(module)
            check_passed(f"{module:15} - {description}")
        except ImportError:
            check_failed(f"{module:15} - {description}")
            all_ok = False

    return all_ok


def check_project_structure():
    """Vérifie la structure du projet"""
    print_header("3. Vérification de la Structure du Projet")

    project_root = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine

    required_items = {
        'Fichiers': [
            'nitrite_complet.py',
            'lancer_nitrite.py',
            'lancer_portable.py',
            'requirements.txt',
            'GUIDE_UTILISATION.md',
            'LANCER_NITRITE.bat',
            'LANCER_PORTABLE.bat'
        ],
        'Dossiers': [
            'src',
            'data',
            'tests',
            'docs',
            'scripts'
        ]
    }

    all_ok = True

    for item_type, items in required_items.items():
        print(f"\n{item_type}:")
        for item in items:
            path = project_root / item
            if path.exists():
                check_passed(f"{item}")
            else:
                check_failed(f"{item} - MANQUANT")
                all_ok = False

    return all_ok


def check_data_files():
    """Vérifie les fichiers de données"""
    print_header("4. Vérification des Fichiers de Données")

    project_root = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine
    data_dir = project_root / 'data'

    all_ok = True

    # Vérifier config.json
    config_file = data_dir / 'config.json'
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            required_keys = ['app_version', 'language', 'max_concurrent_downloads']
            missing_keys = [key for key in required_keys if key not in config]

            if not missing_keys:
                check_passed(f"config.json - Valide")
                check_info(f"Version: {config.get('app_version')}")
                check_info(f"Langue: {config.get('language')}")
            else:
                check_warning(f"config.json - Clés manquantes: {', '.join(missing_keys)}")
                all_ok = False
        except json.JSONDecodeError:
            check_failed(f"config.json - JSON invalide")
            all_ok = False
    else:
        check_failed(f"config.json - MANQUANT")
        all_ok = False

    # Vérifier programs.json
    programs_file = data_dir / 'programs.json'
    if programs_file.exists():
        try:
            with open(programs_file, 'r', encoding='utf-8') as f:
                programs = json.load(f)

            program_count = sum(len(cat) for cat in programs.values() if isinstance(cat, dict))
            check_passed(f"programs.json - Valide")
            check_info(f"Nombre de programmes: {program_count}")
        except json.JSONDecodeError:
            check_failed(f"programs.json - JSON invalide")
            all_ok = False
    else:
        check_failed(f"programs.json - MANQUANT")
        all_ok = False

    return all_ok


def check_source_modules():
    """Vérifie les modules source"""
    print_header("5. Vérification des Modules Source")

    project_root = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine
    src_dir = project_root / 'src'

    required_modules = [
        'config_manager.py',
        'installer_manager.py',
        'gui_manager.py',
        'winget_manager.py',
        'portable_database.py',
        'elevation_helper.py'
    ]

    all_ok = True
    for module in required_modules:
        module_path = src_dir / module
        if module_path.exists():
            # Vérifier la syntaxe
            try:
                import py_compile
                py_compile.compile(str(module_path), doraise=True)
                check_passed(f"{module} - Syntaxe OK")
            except py_compile.PyCompileError as e:
                check_failed(f"{module} - Erreur de syntaxe: {e}")
                all_ok = False
        else:
            check_failed(f"{module} - MANQUANT")
            all_ok = False

    return all_ok


def check_tests():
    """Vérifie les tests"""
    print_header("6. Vérification des Tests")

    project_root = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine
    tests_dir = project_root / 'tests'

    if not tests_dir.exists():
        check_warning("Dossier tests/ manquant")
        return False

    test_files = list(tests_dir.glob('test_*.py'))

    if test_files:
        check_passed(f"{len(test_files)} fichier(s) de test trouvé(s)")
        for test_file in test_files:
            check_info(f"  - {test_file.name}")
        return True
    else:
        check_warning("Aucun fichier de test trouvé")
        return False


def run_quick_tests():
    """Exécute des tests rapides"""
    print_header("7. Exécution de Tests Rapides")

    try:
        # Test d'import des modules principaux
        sys.path.insert(0, str(Path(__file__).parent.parent.parent  # scripts/tests/ -> racine))

        from src.config_manager import ConfigManager
        check_passed("Import de ConfigManager")

        from src.installer_manager import InstallerManager
        check_passed("Import de InstallerManager")

        from src.portable_database import PortableDatabase
        check_passed("Import de PortableDatabase")

        # Test de création d'un ConfigManager
        config = ConfigManager()
        if config.config.get('app_version') == '2.0.0':
            check_passed("ConfigManager fonctionnel")
        else:
            check_warning("ConfigManager: version inattendue")

        return True
    except Exception as e:
        check_failed(f"Erreur lors des tests: {e}")
        return False


def main():
    """Fonction principale"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🔍 Vérification d'Installation - NiTrite v2.0           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    results = []

    results.append(("Python", check_python_version()))
    results.append(("Modules", check_required_modules()))
    results.append(("Structure", check_project_structure()))
    results.append(("Données", check_data_files()))
    results.append(("Modules Source", check_source_modules()))
    results.append(("Tests", check_tests()))
    results.append(("Tests Rapides", run_quick_tests()))

    # Résumé final
    print_header("Résumé")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{Colors.GREEN}✅ OK{Colors.RESET}" if result else f"{Colors.RED}❌ ÉCHEC{Colors.RESET}"
        print(f"{name:20} {status}")

    print()
    print(f"{Colors.BOLD}Score: {passed}/{total}{Colors.RESET}")

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Tous les tests sont passés !{Colors.RESET}")
        print(f"{Colors.GREEN}NiTrite est prêt à l'emploi.{Colors.RESET}")
        print(f"\n{Colors.BLUE}Pour lancer l'application:{Colors.RESET}")
        print(f"  python lancer_nitrite.py")
        print(f"  ou")
        print(f"  LANCER_NITRITE.bat")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Certains tests ont échoué.{Colors.RESET}")
        print(f"{Colors.YELLOW}Corrigez les erreurs avant de lancer l'application.{Colors.RESET}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Vérification interrompue{Colors.RESET}")
        sys.exit(1)
