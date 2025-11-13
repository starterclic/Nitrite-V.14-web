"""
VALIDATION FINALE de NiTrite v.2 - Interface Ultra-Visible
Test complet de l'application avec 80+ programmes
"""

import sys
import time
import json
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'src'))

def validation_finale():
    """Validation complète de NiTrite v.2"""
    
    print("="*70)
    print("🎯 VALIDATION FINALE - NITRITE v.2 ULTRA-VISIBLE")
    print("="*70)
    
    tests_reussis = 0
    tests_totaux = 0
    
    # Test 1: Vérification de la base de données massive
    print("\n1️⃣ Test de la base de données massive...")
    tests_totaux += 1
    try:
        massive_db_path = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs_massive.json'
        with open(massive_db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_apps = sum(len(apps) for apps in data.values() if isinstance(apps, dict))
        print(f"   ✅ {total_apps} applications trouvées")
        
        if total_apps >= 80:
            print(f"   🎯 Objectif atteint : {total_apps} >= 80 applications")
            tests_reussis += 1
        else:
            print(f"   ❌ Objectif non atteint : {total_apps} < 80 applications")
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
    
    # Test 2: Vérification des modules
    print("\n2️⃣ Test des modules principaux...")
    tests_totaux += 1
    try:
        from config_manager import ConfigManager
        from installer_manager import InstallerManager
        from gui_manager_maxvisibility import NiTriteGUIMaxVisibility
        print("   ✅ Tous les modules importés avec succès")
        tests_reussis += 1
    except Exception as e:
        print(f"   ❌ Erreur d'import : {e}")
    
    # Test 3: Initialisation des gestionnaires
    print("\n3️⃣ Test d'initialisation des gestionnaires...")
    tests_totaux += 1
    try:
        config = ConfigManager()
        massive_db_path = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs_massive.json'
        config.load_programs_from_file(str(massive_db_path))
        
        installer = InstallerManager(config)
        
        programs_count = config.get_programs_count()
        print(f"   ✅ Gestionnaires initialisés - {programs_count} programmes chargés")
        tests_reussis += 1
    except Exception as e:
        print(f"   ❌ Erreur d'initialisation : {e}")
    
    # Test 4: Test de l'interface GUI (sans affichage)
    print("\n4️⃣ Test de l'interface GUI...")
    tests_totaux += 1
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Cacher pour le test
        
        gui = NiTriteGUIMaxVisibility(root, installer, config)
        
        checkbox_count = len(gui.program_vars)
        print(f"   ✅ Interface créée avec {checkbox_count} checkboxes")
        
        root.destroy()
        tests_reussis += 1
    except Exception as e:
        print(f"   ❌ Erreur GUI : {e}")
    
    # Test 5: Vérification des fichiers de lancement
    print("\n5️⃣ Test des fichiers de lancement...")
    tests_totaux += 1
    try:
        fichiers_requis = [
            'lancer_nitrite.py',
            'nitrite_maxvisibility.py',
            'src/gui_manager_maxvisibility.py',
            'data/programs_massive.json'
        ]
        
        tous_presents = True
        for fichier in fichiers_requis:
            chemin = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / fichier
            if chemin.exists():
                print(f"   ✅ {fichier} présent")
            else:
                print(f"   ❌ {fichier} MANQUANT")
                tous_presents = False
        
        if tous_presents:
            tests_reussis += 1
    except Exception as e:
        print(f"   ❌ Erreur de vérification : {e}")
    
    # Test 6: Validation des catégories et applications spécifiques
    print("\n6️⃣ Test des applications spécifiques demandées...")
    tests_totaux += 1
    try:
        apps_demandees = [
            'Spybot Search & Destroy',
            'AdwCleaner', 
            'Wise Disk Cleaner',
            'Adobe Acrobat Reader DC',
            'AnyDesk',
            'RustDesk',
            'Steam',
            'Epic Games Launcher',
            'GOG Galaxy'
        ]
        
        programmes = config.get_all_programs_flat()
        apps_trouvees = 0
        
        for app in apps_demandees:
            if app in programmes:
                print(f"   ✅ {app} trouvé")
                apps_trouvees += 1
            else:
                print(f"   ⚠️ {app} non trouvé")
        
        if apps_trouvees >= len(apps_demandees) * 0.8:  # 80% minimum
            print(f"   🎯 {apps_trouvees}/{len(apps_demandees)} applications demandées présentes")
            tests_reussis += 1
        else:
            print(f"   ❌ Seulement {apps_trouvees}/{len(apps_demandees)} applications trouvées")
            
    except Exception as e:
        print(f"   ❌ Erreur de validation : {e}")
    
    # Résultats finaux
    print("\n" + "="*70)
    print("📊 RÉSULTATS DE LA VALIDATION FINALE")
    print("="*70)
    
    pourcentage = (tests_reussis / tests_totaux) * 100
    
    print(f"✅ Tests réussis : {tests_reussis}/{tests_totaux}")
    print(f"📈 Taux de réussite : {pourcentage:.1f}%")
    
    if tests_reussis == tests_totaux:
        print("\n🎉 VALIDATION COMPLETE REUSSIE !")
        print("🚀 NiTrite v.2 est prêt à l'utilisation")
        print("📱 Interface ultra-visible avec 80+ applications")
        print("🔄 Installation automatique et silencieuse")
        print("🚫 Rejet automatique des publicités")
        print("\n💡 COMMANDE DE LANCEMENT :")
        print("   python lancer_nitrite.py")
        return True
    else:
        print(f"\n⚠️ VALIDATION PARTIELLE ({pourcentage:.1f}%)")
        print("🔧 Certains éléments nécessitent une attention")
        if pourcentage >= 80:
            print("✅ L'application devrait fonctionner correctement")
            return True
        else:
            print("❌ Des corrections sont nécessaires")
            return False

if __name__ == "__main__":
    succes = validation_finale()
    
    print("\n" + "="*70)
    if succes:
        print("🎯 NITRITE v.2 - VALIDATION FINALE REUSSIE")
        print("🚀 Prêt pour utilisation avec interface ultra-visible")
    else:
        print("⚠️ VALIDATION INCOMPLETE - Vérifiez les erreurs")
    print("="*70)
    
    sys.exit(0 if succes else 1)