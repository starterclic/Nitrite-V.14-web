"""
Test de l'interface NiTrite v.2 avec maximum de visibilité
Vérifie que l'application se lance et affiche bien tous les programmes
"""

import sys
import time
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'src'))

def test_config_manager():
    """Test du gestionnaire de configuration"""
    print("🔧 Test du ConfigManager...")
    
    try:
        from config_manager import ConfigManager
        config = ConfigManager()
        
        # Charger la base de données massive
        massive_db_path = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs_massive.json'
        if massive_db_path.exists():
            print(f"📂 Chargement de {massive_db_path}")
            result = config.load_programs_from_file(str(massive_db_path))
            if result:
                print("✅ Base de données massive chargée avec succès")
            else:
                print("❌ Échec du chargement de la base de données massive")
                return False
        else:
            print("⚠️ Fichier programs_massive.json non trouvé")
            return False
        
        # Vérifier les programmes
        programs = config.get_programs()
        total_programs = config.get_programs_count()
        
        print(f"📊 Nombre total de programmes : {total_programs}")
        print(f"📋 Catégories disponibles : {list(programs.keys())}")
        
        # Afficher quelques programmes de chaque catégorie
        for category, category_programs in programs.items():
            print(f"   {category}: {len(category_programs)} programme(s)")
            if isinstance(category_programs, dict):
                # Afficher les 3 premiers programmes
                for i, program_name in enumerate(list(category_programs.keys())[:3]):
                    print(f"      - {program_name}")
                if len(category_programs) > 3:
                    print(f"      ... et {len(category_programs) - 3} autres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du ConfigManager : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_installer_manager():
    """Test du gestionnaire d'installation"""
    print("\n⚙️ Test de l'InstallerManager...")
    
    try:
        from config_manager import ConfigManager
        from installer_manager import InstallerManager
        
        config = ConfigManager()
        installer = InstallerManager(config)
        
        print("✅ InstallerManager initialisé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de l'InstallerManager : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_components():
    """Test des composants de l'interface"""
    print("\n🎨 Test des composants GUI...")
    
    try:
        import tkinter as tk
        from config_manager import ConfigManager
        from installer_manager import InstallerManager
        from gui_manager_maxvisibility import NiTriteGUIMaxVisibility
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre pour le test
        
        # Initialiser les managers
        config = ConfigManager()
        massive_db_path = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs_massive.json'
        if massive_db_path.exists():
            config.load_programs_from_file(str(massive_db_path))
        
        installer = InstallerManager(config)
        
        # Créer l'interface
        gui = NiTriteGUIMaxVisibility(root, installer, config)
        
        # Vérifier que l'interface a bien chargé les programmes
        programs_count = len(gui.program_vars)
        print(f"✅ Interface créée avec {programs_count} programmes")
        
        # Nettoyer
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de l'interface : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_massive_database():
    """Test spécifique de la base de données massive"""
    print("\n📊 Test de la base de données massive...")
    
    try:
        import json
        massive_db_path = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs_massive.json'
        
        if not massive_db_path.exists():
            print("❌ Fichier programs_massive.json non trouvé")
            return False
        
        with open(massive_db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Fichier JSON valide")
        
        total_apps = 0
        for category, apps in data.items():
            if isinstance(apps, dict):
                category_count = len(apps)
                total_apps += category_count
                print(f"   {category}: {category_count} applications")
                
                # Vérifier quelques applications
                for app_name, app_info in list(apps.items())[:2]:
                    if 'download_url' in app_info and 'install_args' in app_info:
                        print(f"      ✅ {app_name} - configuration complète")
                    else:
                        print(f"      ⚠️ {app_name} - configuration incomplète")
        
        print(f"📈 Total : {total_apps} applications dans la base de données")
        
        if total_apps >= 80:
            print("🎯 Objectif de 80+ applications atteint !")
            return True
        else:
            print(f"⚠️ Seulement {total_apps} applications (objectif: 80+)")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de la base de données : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test de NiTrite v.2 - Maximum Visibilité")
    print("=" * 50)
    
    tests = [
        ("Base de données massive", test_massive_database),
        ("ConfigManager", test_config_manager),
        ("InstallerManager", test_installer_manager),
        ("Composants GUI", test_gui_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Test : {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
        
        if result:
            print(f"✅ {test_name} : RÉUSSI")
        else:
            print(f"❌ {test_name} : ÉCHEC")
    
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"{test_name:<25} : {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"📊 Résultat final : {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont réussis ! L'application est prête.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)