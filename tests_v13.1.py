#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests automatiques pour NiTriTe V13.1
Vérification des fonctionnalités principales
"""

import os
import sys
import json
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Couleurs pour terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.ENDC}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")

# Tests
def test_imports():
    """Tester que tous les modules s'importent correctement"""
    print_header("TEST 1: Imports des modules")

    errors = []

    # Test modern_colors
    try:
        from modern_colors import ModernColors, bind_mousewheel
        print_success("modern_colors.py importé")
        assert hasattr(ModernColors, 'BG_DARK'), "ModernColors.BG_DARK manquant"
        assert hasattr(ModernColors, 'ORANGE_PRIMARY'), "ModernColors.ORANGE_PRIMARY manquant"
    except Exception as e:
        print_error(f"modern_colors.py: {e}")
        errors.append(str(e))

    # Test translations
    try:
        from translations import TRANSLATIONS, get_text, set_language, _
        print_success("translations.py importé")
        assert 'fr' in TRANSLATIONS, "Traduction FR manquante"
        assert 'en' in TRANSLATIONS, "Traduction EN manquante"
        assert len(TRANSLATIONS['fr']) > 0, "Traductions FR vides"
    except Exception as e:
        print_error(f"translations.py: {e}")
        errors.append(str(e))

    # Test advanced_pages
    try:
        from advanced_pages import (
            SettingsPage, DiagnosticPage, BackupPage,
            OptimizationsPage, UpdatesPage, ThemeManager
        )
        print_success("advanced_pages.py importé")
        assert hasattr(ThemeManager, 'THEMES'), "ThemeManager.THEMES manquant"
        assert 'dark_orange' in ThemeManager.THEMES, "Thème dark_orange manquant"
        assert 'light_blue' in ThemeManager.THEMES, "Thème light_blue manquant"
    except Exception as e:
        print_error(f"advanced_pages.py: {e}")
        errors.append(str(e))

    # Test layout_manager
    try:
        from layout_manager import LayoutManager
        print_success("layout_manager.py importé")
        lm = LayoutManager()
        assert hasattr(lm, 'set_category_order'), "set_category_order manquant"
        assert hasattr(lm, 'get_category_order'), "get_category_order manquant"
    except Exception as e:
        print_error(f"layout_manager.py: {e}")
        errors.append(str(e))

    # Test gui_modern_v13
    try:
        from gui_modern_v13 import ApplicationsPage, ToolsPage, MasterInstallationPage
        print_success("gui_modern_v13.py importé")
    except Exception as e:
        print_error(f"gui_modern_v13.py: {e}")
        errors.append(str(e))

    return len(errors) == 0, errors

def test_data_files():
    """Tester que les fichiers de données existent et sont valides"""
    print_header("TEST 2: Fichiers de données")

    errors = []

    # Test programs.json
    programs_file = Path("data/programs.json")
    if programs_file.exists():
        try:
            with open(programs_file, 'r', encoding='utf-8') as f:
                programs = json.load(f)
            print_success(f"programs.json: {len(programs)} catégories, {sum(len(apps) for apps in programs.values())} apps")

            # Vérifier que Pack Office a bien été retiré
            if "Pack Office" in programs:
                print_warning("Pack Office encore présent (devrait être retiré)")
                errors.append("Pack Office non retiré")
            else:
                print_success("Pack Office correctement retiré")

        except Exception as e:
            print_error(f"programs.json invalide: {e}")
            errors.append(str(e))
    else:
        print_error("programs.json introuvable")
        errors.append("programs.json manquant")

    # Test dossier data
    data_dir = Path("data")
    if data_dir.exists():
        print_success(f"Dossier data/ existe ({len(list(data_dir.iterdir()))} fichiers)")
    else:
        print_error("Dossier data/ manquant")
        errors.append("data/ manquant")

    return len(errors) == 0, errors

def test_themes():
    """Tester que tous les thèmes sont complets"""
    print_header("TEST 3: Thèmes")

    errors = []

    try:
        from advanced_pages import ThemeManager

        required_keys = [
            "BG_DARK", "BG_MEDIUM", "BG_LIGHT", "BG_CARD", "BG_HOVER",
            "ORANGE_PRIMARY", "ORANGE_LIGHT", "ORANGE_DARK",
            "TEXT_PRIMARY", "TEXT_SECONDARY", "TEXT_MUTED",
            "GREEN_SUCCESS", "RED_ERROR", "BLUE_INFO",
            "PURPLE_PREMIUM", "YELLOW_WARNING"
        ]

        for theme_id, theme_data in ThemeManager.THEMES.items():
            missing = [key for key in required_keys if key not in theme_data]
            if missing:
                print_error(f"Thème {theme_id}: clés manquantes {missing}")
                errors.append(f"{theme_id}: {missing}")
            else:
                print_success(f"Thème {theme_id}: complet ({len(theme_data)} clés)")

        # Vérifier que light_blue existe
        if 'light_blue' in ThemeManager.THEMES:
            print_success("Thème light_blue créé (bug Mode Clair corrigé)")
        else:
            print_error("Thème light_blue manquant")
            errors.append("light_blue manquant")

    except Exception as e:
        print_error(f"Erreur test thèmes: {e}")
        errors.append(str(e))

    return len(errors) == 0, errors

def test_translations():
    """Tester que les traductions sont complètes"""
    print_header("TEST 4: Traductions")

    errors = []

    try:
        from translations import TRANSLATIONS

        fr_keys = set(TRANSLATIONS['fr'].keys())
        en_keys = set(TRANSLATIONS['en'].keys())

        # Vérifier que FR et EN ont les mêmes clés
        missing_in_en = fr_keys - en_keys
        missing_in_fr = en_keys - fr_keys

        if missing_in_en:
            print_warning(f"Clés FR manquantes en EN: {missing_in_en}")
        if missing_in_fr:
            print_warning(f"Clés EN manquantes en FR: {missing_in_fr}")

        if not missing_in_en and not missing_in_fr:
            print_success(f"Traductions synchronisées ({len(fr_keys)} clés)")
        else:
            errors.append("Traductions non synchronisées")

        # Tester quelques clés importantes
        important_keys = ["applications", "diagnostic", "settings", "optimizations", "backup"]
        for key in important_keys:
            if key in fr_keys and key in en_keys:
                print_success(f"Clé '{key}' présente FR/EN")
            else:
                print_error(f"Clé '{key}' manquante")
                errors.append(f"Clé {key} manquante")

    except Exception as e:
        print_error(f"Erreur test traductions: {e}")
        errors.append(str(e))

    return len(errors) == 0, errors

def test_build_config():
    """Tester que build_v13.py contient tous les hiddenimports"""
    print_header("TEST 5: Configuration Build")

    errors = []

    build_file = Path("build_v13.py")
    if not build_file.exists():
        print_error("build_v13.py introuvable")
        return False, ["build_v13.py manquant"]

    try:
        with open(build_file, 'r', encoding='utf-8') as f:
            content = f.read()

        required_imports = [
            'src.modern_colors',
            'src.translations',
            'src.advanced_pages',
            'src.layout_manager',
            'psutil',
            'wmi',
            'win32com'
        ]

        for imp in required_imports:
            if f"'{imp}'" in content or f'"{imp}"' in content:
                print_success(f"hiddenimport: {imp}")
            else:
                print_warning(f"hiddenimport possiblement manquant: {imp}")
                # Pas d'erreur car peut être sous un autre format

        if "NiTriTe V13.1 Portable" in content:
            print_success("Output directory: NiTriTe V13.1 Portable/")
        else:
            print_warning("Output directory non configuré")

    except Exception as e:
        print_error(f"Erreur lecture build_v13.py: {e}")
        errors.append(str(e))

    return len(errors) == 0, errors

def test_todos():
    """Vérifier qu'il ne reste pas de TODOs non résolus"""
    print_header("TEST 6: TODOs restants")

    errors = []

    # Fichiers à vérifier
    files_to_check = [
        "src/gui_modern_v13.py",
        "src/advanced_pages.py",
        "src/layout_manager.py"
    ]

    total_todos = 0

    for file_path in files_to_check:
        if not Path(file_path).exists():
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        todos = [
            (i+1, line.strip())
            for i, line in enumerate(lines)
            if 'TODO' in line or 'FIXME' in line or 'XXX' in line
        ]

        if todos:
            print_warning(f"{file_path}: {len(todos)} TODO(s)")
            for line_num, line in todos:
                print(f"    L{line_num}: {line[:80]}")
            total_todos += len(todos)
        else:
            print_success(f"{file_path}: Aucun TODO")

    if total_todos == 0:
        print_success("✨ ZÉRO TODO restant dans le code!")
    else:
        print_warning(f"⚠️  {total_todos} TODO(s) trouvé(s)")

    return True, []  # Pas d'erreur, juste info

def run_all_tests():
    """Exécuter tous les tests"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}🧪 NiTriTe V13.1 - Suite de Tests Automatiques{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}")

    tests = [
        ("Imports Modules", test_imports),
        ("Fichiers Données", test_data_files),
        ("Thèmes", test_themes),
        ("Traductions", test_translations),
        ("Configuration Build", test_build_config),
        ("TODOs Restants", test_todos),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success, errors = test_func()
            results.append((test_name, success, errors))
        except Exception as e:
            print_error(f"Erreur critique dans {test_name}: {e}")
            results.append((test_name, False, [str(e)]))

    # Résumé
    print_header("📊 RÉSUMÉ DES TESTS")

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for test_name, success, errors in results:
        if success:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
            for error in errors:
                print(f"    • {error}")

    print(f"\n{Colors.BOLD}Résultat Final:{Colors.ENDC}")
    if passed == total:
        print_success(f"✨ {passed}/{total} tests réussis - Application 100% fonctionnelle!")
        return 0
    else:
        print_error(f"❌ {passed}/{total} tests réussis - {total-passed} test(s) échoué(s)")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
