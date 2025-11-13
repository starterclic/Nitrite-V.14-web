"""
Test des installations problématiques
Malwarebytes, ADW Cleaner, Wise Disk Cleaner
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.installer_manager import InstallerManager
from src.config_manager import ConfigManager

def test_callback(message, level="info"):
    """Callback pour afficher les logs"""
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    print(f"{icons.get(level, 'ℹ️')} {message}")

def test_installation():
    """Test des 3 programmes problématiques"""
    print("=" * 70)
    print("🧪 TEST DES INSTALLATIONS PROBLÉMATIQUES")
    print("=" * 70)
    print()
    
    # Programmes à tester
    programs_to_test = [
        "Malwarebytes",
        "AdwCleaner", 
        "Wise Disk Cleaner"
    ]
    
    # Initialiser le gestionnaire
    config_manager = ConfigManager()
    installer = InstallerManager(config_manager)
    
    print(f"📦 Programmes à tester : {', '.join(programs_to_test)}")
    print()
    
    results = {}
    
    for program_name in programs_to_test:
        print(f"\n{'='*70}")
        print(f"🔍 TEST: {program_name}")
        print(f"{'='*70}\n")
        
        # Vérifier que le programme existe
        if program_name not in installer.programs_config:
            print(f"❌ Programme '{program_name}' introuvable dans la config")
            results[program_name] = "NOT_FOUND"
            continue
        
        config = installer.programs_config[program_name]
        print(f"📋 Configuration:")
        print(f"   • URL : {config.get('download_url', 'Aucune')}")
        print(f"   • WinGet ID : {config.get('winget_id', 'Aucun')}")
        print(f"   • Arguments : {config.get('install_args', 'Aucun')}")
        print(f"   • Admin requis : {config.get('admin_required', False)}")
        print()
        
        # Lancer l'installation
        try:
            success = installer.install_single_program(
                program_name,
                log_callback=test_callback,
                progress_callback=lambda p: print(f"📊 Progression : {p}%")
            )
            
            results[program_name] = "SUCCESS" if success else "FAILED"
            
            if success:
                print(f"\n✅ {program_name} installé avec succès!")
            else:
                print(f"\n❌ Échec de l'installation de {program_name}")
                
        except Exception as e:
            print(f"\n❌ Erreur lors du test de {program_name}: {e}")
            results[program_name] = f"ERROR: {e}"
        
        print()
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    print()
    
    for program, result in results.items():
        icon = "✅" if result == "SUCCESS" else "❌"
        print(f"{icon} {program}: {result}")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    print()
    print("⚠️  ATTENTION: Ce script va tenter d'installer les programmes!")
    print("⚠️  Assurez-vous d'avoir les privilèges administrateur")
    print()
    
    response = input("Continuer? (oui/non): ").strip().lower()
    
    if response in ['oui', 'o', 'yes', 'y']:
        test_installation()
    else:
        print("Test annulé.")
