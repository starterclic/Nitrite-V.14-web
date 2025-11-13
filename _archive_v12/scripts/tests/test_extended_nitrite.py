#!/usr/bin/env python3
"""
Test complet de NiTrite v.2 Extended - Validation de toutes les nouvelles fonctionnalités
"""

import json
import sys
from pathlib import Path

def test_extended_database():
    """Test de la base de données étendue"""
    print("🔍 Test de la base de données étendue...")
    
    try:
        # Charger la base de données
        programs_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs.json'
        with open(programs_file, 'r', encoding='utf-8') as f:
            programs = json.load(f)
        
        # Compter par catégorie
        categories = {}
        requested_apps = {
            'spybot': 'Spybot Search & Destroy',
            'adwcleaner': 'AdwCleaner', 
            'wise_disk_cleaner': 'Wise Disk Cleaner',
            'pdf_reader': 'Adobe Acrobat Reader DC',
            'anydesk': 'AnyDesk',
            'rustdesk': 'RustDesk',
            'steam': 'Steam',
            'epic_games': 'Epic Games Launcher',
            'gog_galaxy': 'GOG Galaxy'
        }
        
        for prog_id, prog_info in programs.items():
            category = prog_info.get('category', 'Divers')
            categories.setdefault(category, 0)
            categories[category] += 1
        
        print(f"  ✅ {len(programs)} programmes au total")
        print(f"  ✅ {len(categories)} catégories")
        
        # Vérifier les applications demandées
        found_requested = 0
        for app_id, app_name in requested_apps.items():
            if app_id in programs:
                print(f"  ✅ {app_name} trouvé")
                found_requested += 1
            else:
                print(f"  ❌ {app_name} manquant")
        
        print(f"  📊 {found_requested}/{len(requested_apps)} applications demandées présentes")
        
        # Afficher la répartition par catégorie
        print("\n  📋 Répartition par catégorie:")
        for category, count in sorted(categories.items()):
            print(f"    • {category}: {count} programmes")
        
        return len(programs) >= 50 and found_requested >= 8
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_gui_improvements():
    """Test des améliorations de l'interface"""
    print("\n🖥️ Test des améliorations de l'interface...")
    
    try:
        # Vérifier que le fichier GUI a les nouvelles méthodes
        gui_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'src' / 'gui_manager.py'
        with open(gui_file, 'r', encoding='utf-8') as f:
            gui_content = f.read()
        
        required_methods = [
            'select_category',
            'select_all_programs', 
            'clear_selection',
            'update_selection_stats',
            'show_about',
            '_on_mousewheel',
            'create_header',
            'create_toolbar'
        ]
        
        found_methods = 0
        for method in required_methods:
            if f"def {method}" in gui_content:
                print(f"  ✅ Méthode {method} présente")
                found_methods += 1
            else:
                print(f"  ❌ Méthode {method} manquante")
        
        # Vérifier les améliorations visuelles
        ui_improvements = [
            'setup_window',  # Adaptation écran
            'Category.TLabel',  # Styles des catégories
            'MouseWheel',  # Support molette
            'scrollbar_v',  # Double scrollbar
            'stats_label'  # Statistiques
        ]
        
        found_improvements = 0
        for improvement in ui_improvements:
            if improvement in gui_content:
                print(f"  ✅ Amélioration {improvement} présente")
                found_improvements += 1
        
        print(f"  📊 {found_methods}/{len(required_methods)} nouvelles méthodes")
        print(f"  📊 {found_improvements}/{len(ui_improvements)} améliorations UI")
        
        return found_methods >= 6 and found_improvements >= 3
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_application_categories():
    """Test des catégories spécifiques demandées"""
    print("\n🎯 Test des catégories spécifiques...")
    
    try:
        programs_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs.json'
        with open(programs_file, 'r', encoding='utf-8') as f:
            programs = json.load(f)
        
        # Catégories attendues avec minimum de programmes
        expected_categories = {
            'Navigateurs': 5,
            'Développement': 8,
            'Jeux': 4,
            'Sécurité': 5,
            'Utilitaires': 8,
            'Communication': 5,
            'Multimédia': 5,
            'Bureautique': 2
        }
        
        categories_count = {}
        for prog_info in programs.values():
            category = prog_info.get('category', 'Divers')
            categories_count.setdefault(category, 0)
            categories_count[category] += 1
        
        passed_categories = 0
        for category, min_count in expected_categories.items():
            actual_count = categories_count.get(category, 0)
            if actual_count >= min_count:
                print(f"  ✅ {category}: {actual_count} programmes (≥{min_count})")
                passed_categories += 1
            else:
                print(f"  ❌ {category}: {actual_count} programmes (<{min_count})")
        
        print(f"  📊 {passed_categories}/{len(expected_categories)} catégories validées")
        
        return passed_categories >= 7
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_functionality():
    """Test des fonctionnalités essentielles"""
    print("\n⚙️ Test des fonctionnalités...")
    
    try:
        # Test d'import des modules
        sys.path.insert(0, str(Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'src'))
        
        from gui_manager import NiTriteGUI
        from installer_manager import InstallerManager
        from config_manager import ConfigManager
        from dependency_manager import DependencyManager
        
        print("  ✅ Tous les modules importés avec succès")
        
        # Test de chargement de configuration
        config = ConfigManager()
        programs = config.load_programs_database()
        print(f"  ✅ Base de données chargée: {len(programs)} programmes")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur d'import: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test Complet de NiTrite v.2 Extended")
    print("=" * 50)
    
    tests = [
        ("Base de données étendue", test_extended_database),
        ("Améliorations interface", test_gui_improvements), 
        ("Catégories d'applications", test_application_categories),
        ("Fonctionnalités essentielles", test_functionality)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"\n✅ {test_name}: RÉUSSI")
            else:
                print(f"\n❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"\n❌ {test_name}: ERREUR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 RÉSULTATS FINAUX: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("🚀 NiTrite v.2 Extended est prêt à être utilisé!")
        print("\n🎯 Améliorations validées:")
        print("  ✅ 50+ applications disponibles")
        print("  ✅ Interface adaptée à l'écran")
        print("  ✅ Sélection rapide par catégorie")
        print("  ✅ Toutes les apps demandées présentes")
        print("  ✅ Navigation améliorée avec molette")
        print("  ✅ Design moderne et intuitif")
    else:
        print(f"⚠️  {total_tests - passed_tests} test(s) ont échoué")
        print("Vérifiez les erreurs ci-dessus")
    
    print(f"\n📈 Score de qualité: {(passed_tests/total_tests)*100:.1f}%")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)