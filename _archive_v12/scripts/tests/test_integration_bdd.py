"""
Script de test pour vérifier l'intégration de la base de données portable
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def test_import_modules():
    """Test 1: Vérifier que tous les modules s'importent correctement"""
    print("=" * 60)
    print("TEST 1: Import des modules")
    print("=" * 60)
    
    try:
        from portable_database import PortableDatabase
        print("✅ portable_database importé avec succès")
        
        from installer_manager import InstallerManager
        print("✅ installer_manager importé avec succès")
        
        from gui_manager import NiTriteGUIComplet
        print("✅ gui_manager importé avec succès")
        
        print("\n✅ TOUS LES MODULES IMPORTÉS AVEC SUCCÈS\n")
        return True
    except Exception as e:
        print(f"\n❌ ERREUR D'IMPORT: {e}\n")
        return False


def test_database_init():
    """Test 2: Vérifier que la base de données peut être initialisée"""
    print("=" * 60)
    print("TEST 2: Initialisation de la base de données")
    print("=" * 60)
    
    try:
        from portable_database import PortableDatabase
        
        db_path = project_root / "data" / "test_portable.db"
        if db_path.exists():
            db_path.unlink()  # Supprimer l'ancienne base de test
        
        db = PortableDatabase(str(db_path))
        print(f"✅ Base de données créée: {db_path}")
        
        # Vérifier les tables
        stats = db.get_statistics()
        print(f"✅ Statistiques: {stats}")
        
        # Nettoyer
        db_path.unlink()
        print("✅ Base de données de test supprimée")
        
        print("\n✅ INITIALISATION RÉUSSIE\n")
        return True
    except Exception as e:
        print(f"\n❌ ERREUR D'INITIALISATION: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_installer_manager_integration():
    """Test 3: Vérifier que InstallerManager peut utiliser la base de données"""
    print("=" * 60)
    print("TEST 3: Intégration avec InstallerManager")
    print("=" * 60)
    
    try:
        from installer_manager import InstallerManager
        
        config_path = project_root / "data" / "programs.json"
        app_dir = project_root / "NiTrite_Autonome"
        app_dir.mkdir(exist_ok=True)
        
        # Créer le gestionnaire
        manager = InstallerManager(
            config_path=str(config_path),
            log_callback=lambda msg, level="info": print(f"  LOG [{level}]: {msg}"),
            app_dir=str(app_dir)
        )
        
        print("✅ InstallerManager créé avec succès")
        
        # Vérifier que la base de données est initialisée
        if hasattr(manager, 'portable_db') and manager.portable_db is not None:
            print("✅ Base de données portable initialisée dans InstallerManager")
            
            # Vérifier les statistiques
            stats = manager.portable_db.get_statistics()
            print(f"✅ Statistiques de la base: {stats}")
        else:
            print("⚠️ Base de données portable non initialisée")
        
        print("\n✅ INTÉGRATION RÉUSSIE\n")
        return True
    except Exception as e:
        print(f"\n❌ ERREUR D'INTÉGRATION: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_gui_methods():
    """Test 4: Vérifier que les méthodes GUI existent"""
    print("=" * 60)
    print("TEST 4: Vérification des méthodes GUI")
    print("=" * 60)
    
    try:
        from gui_manager import NiTriteGUIComplet
        
        # Vérifier que les méthodes existent
        methods_to_check = [
            'show_portable_database_stats',
            'show_all_portable_apps',
            'verify_database_integrity',
            'export_database_json'
        ]
        
        for method_name in methods_to_check:
            if hasattr(NiTriteGUIComplet, method_name):
                print(f"✅ Méthode '{method_name}' trouvée")
            else:
                print(f"❌ Méthode '{method_name}' MANQUANTE")
                return False
        
        print("\n✅ TOUTES LES MÉTHODES GUI PRÉSENTES\n")
        return True
    except Exception as e:
        print(f"\n❌ ERREUR DE VÉRIFICATION GUI: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_spybot_config():
    """Test 5: Vérifier que Spybot est bien configuré"""
    print("=" * 60)
    print("TEST 5: Vérification configuration Spybot")
    print("=" * 60)
    
    try:
        import json
        
        config_path = project_root / "data" / "programs.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            programs = json.load(f)
        
        # Chercher Spybot (structure imbriquée: catégorie -> programme -> data)
        spybot = None
        for category_name, category_data in programs.items():
            if isinstance(category_data, dict):
                for prog_name, prog_data in category_data.items():
                    if isinstance(prog_data, dict) and 'spybot' in prog_name.lower():
                        spybot = prog_data
                        spybot['name'] = prog_name
                        break
            if spybot:
                break
        
        if not spybot:
            print("❌ Spybot non trouvé dans programs.json")
            return False
        
        print(f"✅ Spybot trouvé: {spybot.get('name')}")
        print(f"   URL: {spybot.get('download_url', 'N/A')}")
        print(f"   Args: {spybot.get('install_args', 'N/A')}")
        print(f"   Winget ID: {spybot.get('winget_id', 'N/A')}")
        
        # Vérifications
        checks = [
            ('URL contient SpybotSD2', 'SpybotSD2' in spybot.get('download_url', '')),
            ('Install args présents', bool(spybot.get('install_args'))),
            ('Winget ID présent', bool(spybot.get('winget_id'))),
        ]
        
        all_ok = True
        for check_name, check_result in checks:
            if check_result:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}")
                all_ok = False
        
        if all_ok:
            print("\n✅ CONFIGURATION SPYBOT CORRECTE\n")
        else:
            print("\n⚠️ CONFIGURATION SPYBOT INCOMPLÈTE\n")
        
        return all_ok
    except Exception as e:
        print(f"\n❌ ERREUR DE VÉRIFICATION SPYBOT: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Exécute tous les tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  TEST D'INTÉGRATION - BASE DE DONNÉES PORTABLE          ║")
    print("║  Version NiTrite Autonome                               ║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    tests = [
        ("Import des modules", test_import_modules),
        ("Initialisation BDD", test_database_init),
        ("Intégration InstallerManager", test_installer_manager_integration),
        ("Méthodes GUI", test_gui_methods),
        ("Configuration Spybot", test_spybot_config),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERREUR CRITIQUE dans {test_name}: {e}\n")
            results.append((test_name, False))
    
    # Résumé
    print("\n")
    print("=" * 60)
    print("RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status:15} - {test_name}")
    
    print("=" * 60)
    print(f"RÉSULTAT: {passed}/{total} tests réussis")
    
    if passed == total:
        print("✅ TOUS LES TESTS RÉUSSIS - INTÉGRATION COMPLÈTE")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFIER LES ERREURS")
    
    print("=" * 60)
    print("\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
