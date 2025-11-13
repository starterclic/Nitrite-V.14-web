"""
Script de test pour NiTrite v.2
Vérifie le bon fonctionnement de l'application
"""

import sys
import os
from pathlib import Path
import unittest
import tempfile
import json

# Ajouter le dossier parent au chemin Python
sys.path.append(str(Path(__file__).parent.parent.parent  # scripts/tests/ -> racine))

def test_imports():
    """Test des imports des modules"""
    print("🔍 Test des imports...")
    
    try:
        from src.config_manager import ConfigManager
        print("  ✅ ConfigManager importé")
    except Exception as e:
        print(f"  ❌ Erreur ConfigManager: {e}")
        return False
    
    try:
        from src.dependency_manager import DependencyManager
        print("  ✅ DependencyManager importé")
    except Exception as e:
        print(f"  ❌ Erreur DependencyManager: {e}")
        return False
    
    try:
        from src.installer_manager import InstallerManager
        print("  ✅ InstallerManager importé")
    except Exception as e:
        print(f"  ❌ Erreur InstallerManager: {e}")
        return False
    
    try:
        from src.gui_manager import NiTriteGUI
        print("  ✅ NiTriteGUI importé")
    except Exception as e:
        print(f"  ❌ Erreur NiTriteGUI: {e}")
        return False
    
    return True

def test_config_manager():
    """Test du gestionnaire de configuration"""
    print("\n🔍 Test du ConfigManager...")
    
    try:
        from src.config_manager import ConfigManager
        
        # Créer un gestionnaire temporaire
        config = ConfigManager()
        
        # Test de chargement
        config.load_config()
        print("  ✅ Configuration chargée")
        
        # Test de sauvegarde
        config.set('test_key', 'test_value')
        config.save_config()
        print("  ✅ Configuration sauvegardée")
        
        # Test de la base de données
        programs = config.load_programs_database()
        if programs:
            print(f"  ✅ Base de données chargée ({len(programs)} programmes)")
        else:
            print("  ⚠️  Base de données vide ou non trouvée")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur ConfigManager: {e}")
        return False

def test_dependency_manager():
    """Test du gestionnaire de dépendances"""
    print("\n🔍 Test du DependencyManager...")
    
    try:
        from src.dependency_manager import DependencyManager
        
        dep_manager = DependencyManager()
        
        # Test de vérification des packages
        for package in ['os', 'sys', 'json']:  # Packages standards
            if dep_manager.is_package_available(package):
                print(f"  ✅ Package {package} disponible")
            else:
                print(f"  ❌ Package {package} non disponible")
        
        # Test d'informations
        info = dep_manager.get_dependency_info()
        print(f"  ℹ️  Dépendances requises: {len(info['required_packages'])}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur DependencyManager: {e}")
        return False

def test_installer_manager():
    """Test du gestionnaire d'installations"""
    print("\n🔍 Test de l'InstallerManager...")
    
    try:
        from src.installer_manager import InstallerManager
        
        installer = InstallerManager()
        
        # Test de chargement de la configuration
        installer.load_programs_config()
        if installer.programs_config:
            print(f"  ✅ Configuration chargée ({len(installer.programs_config)} programmes)")
            
            # Tester quelques vérifications
            for program_id in list(installer.programs_config.keys())[:3]:
                program_info = installer.programs_config[program_id]
                is_installed = installer.is_program_installed(program_info)
                status = "installé" if is_installed else "non installé"
                print(f"  ℹ️  {program_info['name']}: {status}")
        else:
            print("  ⚠️  Aucune configuration de programmes")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur InstallerManager: {e}")
        return False

def test_files_structure():
    """Test de la structure des fichiers"""
    print("\n🔍 Test de la structure des fichiers...")
    
    required_files = [
        'nitrite_installer.py',
        'src/gui_manager.py',
        'src/installer_manager.py',
        'src/dependency_manager.py',
        'src/config_manager.py',
        'data/config.json',
        'data/programs.json',
        'README.md'
    ]
    
    required_dirs = [
        'src',
        'data',
        'downloads',
        'logs',
        'assets',
        'dependencies'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} manquant")
            all_good = False
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ manquant")
            all_good = False
    
    return all_good

def test_programs_database():
    """Test de la base de données des programmes"""
    print("\n🔍 Test de la base de données des programmes...")
    
    try:
        programs_file = Path('data/programs.json')
        if not programs_file.exists():
            print("  ❌ Fichier programs.json non trouvé")
            return False
        
        with open(programs_file, 'r', encoding='utf-8') as f:
            programs = json.load(f)
        
        print(f"  ✅ {len(programs)} programmes dans la base")
        
        # Vérifier quelques programmes
        categories = {}
        for prog_id, prog_info in programs.items():
            category = prog_info.get('category', 'Non défini')
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
            
            # Vérifier les champs requis
            required_fields = ['name', 'download_url', 'install_type']
            for field in required_fields:
                if field not in prog_info:
                    print(f"  ⚠️  {prog_id}: champ '{field}' manquant")
        
        print("  📊 Catégories:")
        for cat, count in categories.items():
            print(f"    • {cat}: {count} programmes")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 NiTrite v.2 - Tests de fonctionnement")
    print("=" * 50)
    
    tests = [
        ("Structure des fichiers", test_files_structure),
        ("Imports des modules", test_imports),
        ("Base de données programmes", test_programs_database),
        ("ConfigManager", test_config_manager),
        ("DependencyManager", test_dependency_manager),
        ("InstallerManager", test_installer_manager)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📋 Résumé des tests:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Score: {passed}/{len(results)} tests réussis")
    
    if passed == len(results):
        print("🎉 Tous les tests sont passés! L'application devrait fonctionner correctement.")
    elif passed >= len(results) * 0.8:
        print("⚠️  La plupart des tests sont passés. Quelques problèmes mineurs détectés.")
    else:
        print("❌ Plusieurs tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🚀 Vous pouvez maintenant lancer NiTrite v.2:")
        print("   • Double-cliquez sur 'Lancer_NiTrite.bat'")
        print("   • Ou exécutez: python nitrite_installer.py")
    else:
        print("\n🔧 Corrigez les erreurs avant de lancer l'application.")
    
    input("\nAppuyez sur Entrée pour continuer...")