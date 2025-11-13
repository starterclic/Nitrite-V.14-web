"""
Script de validation complète des correctifs Spybot et Base de données portable
"""

import sys
from pathlib import Path
import json

# Configuration des chemins
project_root = Path(__file__).resolve().parent.parent.parent  # scripts/tests/ -> racine
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from src.portable_database import PortableDatabase


def test_spybot_config():
    """Teste la configuration de Spybot dans programs.json"""
    print("\n" + "="*70)
    print("TEST 1: VÉRIFICATION CONFIGURATION SPYBOT")
    print("="*70)
    
    programs_json = project_root / "data" / "programs.json"
    
    try:
        with open(programs_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Chercher Spybot
        spybot = None
        for category, programs in data.items():
            if isinstance(programs, dict):
                for prog_name, prog_info in programs.items():
                    if "Spybot" in prog_name:
                        spybot = prog_info
                        print(f"\n✅ Trouvé: {prog_name}")
                        print(f"   Catégorie: {category}")
                        break
            if spybot:
                break
        
        if not spybot:
            print("❌ Spybot non trouvé dans programs.json")
            return False
        
        # Vérifications
        checks = {
            "URL mise à jour": "SpybotSD2-latest.exe" in spybot.get('download_url', ''),
            "Arguments /NOCANCEL": "/NOCANCEL" in spybot.get('install_args', ''),
            "Arguments /TASKS": "/TASKS" in spybot.get('install_args', ''),
            "Winget ID présent": 'winget_id' in spybot,
            "Winget ID correct": spybot.get('winget_id', '') == 'SaferNetworking.SpybotSearchAndDestroy',
            "Admin requis": spybot.get('admin_required', False) == True
        }
        
        print("\n📋 Résultats des vérifications:")
        all_passed = True
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}")
            if not result:
                all_passed = False
        
        if all_passed:
            print("\n🎉 SUCCÈS: Configuration Spybot correcte!")
            return True
        else:
            print("\n⚠️ ATTENTION: Certaines vérifications ont échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_database_creation():
    """Teste la création de la base de données"""
    print("\n" + "="*70)
    print("TEST 2: CRÉATION ET STRUCTURE BASE DE DONNÉES")
    print("="*70)
    
    db_path = project_root / "portable_apps.db"
    
    try:
        # Créer la base de données
        db = PortableDatabase(
            db_path=str(db_path),
            apps_folder=str(project_root / "downloads")
        )
        
        print(f"\n✅ Base de données créée: {db_path}")
        
        # Vérifier les tables
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['applications', 'metadata', 'categories', 'execution_history']
        
        print("\n📋 Tables créées:")
        all_tables_ok = True
        for table in expected_tables:
            if table in tables:
                print(f"   ✅ {table}")
            else:
                print(f"   ❌ {table} (manquante)")
                all_tables_ok = False
        
        conn.close()
        
        if all_tables_ok:
            print("\n🎉 SUCCÈS: Structure de la base correcte!")
            return True
        else:
            print("\n⚠️ ATTENTION: Certaines tables manquent")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_database_operations():
    """Teste les opérations de base de données"""
    print("\n" + "="*70)
    print("TEST 3: OPÉRATIONS BASE DE DONNÉES")
    print("="*70)
    
    db_path = project_root / "portable_apps.db"
    
    try:
        db = PortableDatabase(
            db_path=str(db_path),
            apps_folder=str(project_root / "downloads")
        )
        
        # Test 1: Ajout d'une application test
        print("\n📝 Test ajout d'application...")
        
        # Créer un fichier exe fictif pour le test
        test_exe = project_root / "downloads" / "test_app.exe"
        if not test_exe.exists():
            test_exe.write_text("Test")
        
        app_id = db.add_application(
            name="Test Application",
            executable_path=str(test_exe),
            category="Test",
            description="Application de test",
            version="1.0.0",
            is_portable=True
        )
        
        if app_id:
            print(f"   ✅ Application ajoutée (ID: {app_id})")
        else:
            print("   ❌ Échec de l'ajout")
            return False
        
        # Test 2: Recherche
        print("\n🔍 Test recherche...")
        results = db.search_applications("Test")
        if results:
            print(f"   ✅ Recherche réussie ({len(results)} résultats)")
        else:
            print("   ❌ Aucun résultat")
            return False
        
        # Test 3: Récupération
        print("\n📥 Test récupération...")
        app = db.get_application(name="Test Application")
        if app:
            print(f"   ✅ Application récupérée: {app['name']}")
        else:
            print("   ❌ Application non trouvée")
            return False
        
        # Test 4: Mise à jour
        print("\n✏️ Test mise à jour...")
        success = db.update_application(
            name="Test Application",
            version="1.0.1",
            notes="Version mise à jour"
        )
        if success:
            print("   ✅ Mise à jour réussie")
        else:
            print("   ❌ Échec de la mise à jour")
            return False
        
        # Test 5: Statistiques
        print("\n📊 Test statistiques...")
        stats = db.get_statistics()
        if stats and stats.get('total_apps', 0) > 0:
            print(f"   ✅ Statistiques générées ({stats['total_apps']} apps)")
        else:
            print("   ⚠️ Aucune statistique")
        
        # Test 6: Suppression
        print("\n🗑️ Test suppression...")
        success = db.delete_application(name="Test Application")
        if success:
            print("   ✅ Suppression réussie")
        else:
            print("   ❌ Échec de la suppression")
            return False
        
        # Nettoyer
        if test_exe.exists():
            test_exe.unlink()
        
        print("\n🎉 SUCCÈS: Toutes les opérations fonctionnent!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_import_export():
    """Teste l'import/export JSON"""
    print("\n" + "="*70)
    print("TEST 4: IMPORT/EXPORT JSON")
    print("="*70)
    
    db_path = project_root / "portable_apps.db"
    
    try:
        db = PortableDatabase(
            db_path=str(db_path),
            apps_folder=str(project_root / "downloads")
        )
        
        # Test export
        print("\n📤 Test export...")
        export_path = project_root / "test_export.json"
        success = db.export_to_json(str(export_path))
        
        if success and export_path.exists():
            print(f"   ✅ Export réussi: {export_path}")
            
            # Vérifier le contenu
            with open(export_path, 'r', encoding='utf-8') as f:
                export_data = json.load(f)
            
            print(f"   📊 {len(export_data)} catégories exportées")
            
            # Nettoyer
            export_path.unlink()
            
            print("\n🎉 SUCCÈS: Import/Export fonctionnels!")
            return True
        else:
            print("   ❌ Échec de l'export")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_integrity_check():
    """Teste la vérification d'intégrité"""
    print("\n" + "="*70)
    print("TEST 5: VÉRIFICATION D'INTÉGRITÉ")
    print("="*70)
    
    db_path = project_root / "portable_apps.db"
    
    try:
        db = PortableDatabase(
            db_path=str(db_path),
            apps_folder=str(project_root / "downloads")
        )
        
        print("\n🔐 Vérification d'intégrité...")
        issues = db.verify_integrity()
        
        if issues:
            print(f"\n⚠️ {len(issues)} problèmes détectés:")
            for issue in issues[:5]:  # Afficher max 5
                print(f"   - {issue['app']}: {issue['issue']}")
        else:
            print("\n✅ Aucun problème détecté - Base intègre")
        
        print("\n🎉 SUCCÈS: Vérification d'intégrité fonctionnelle!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Fonction principale de validation"""
    print("\n" + "="*70)
    print(" VALIDATION COMPLÈTE - CORRECTIFS SPYBOT ET BASE DE DONNÉES")
    print("="*70)
    print(f"\n📁 Projet: {project_root}")
    
    # Liste des tests
    tests = [
        ("Configuration Spybot", test_spybot_config),
        ("Création base de données", test_database_creation),
        ("Opérations CRUD", test_database_operations),
        ("Import/Export JSON", test_import_export),
        ("Vérification intégrité", test_integrity_check)
    ]
    
    results = []
    
    # Exécuter tous les tests
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Erreur lors du test '{test_name}': {e}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "="*70)
    print(" RÉSUMÉ DES TESTS")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{len(tests)} tests réussis")
    
    if failed == 0:
        print("\n🎉🎉🎉 TOUS LES TESTS SONT PASSÉS! 🎉🎉🎉")
        print("\n✅ Les correctifs Spybot et la base de données sont opérationnels")
    else:
        print(f"\n⚠️ {failed} test(s) échoué(s) - Vérifiez les logs ci-dessus")
    
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
