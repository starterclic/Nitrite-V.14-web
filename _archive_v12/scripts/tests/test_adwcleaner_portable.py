"""
Test pour vérifier que ADW Cleaner fonctionne en mode portable
"""
import json
from pathlib import Path

def test_adwcleaner_config():
    """Vérifie la configuration d'ADW Cleaner"""
    
    print("\n" + "="*70)
    print("  TEST CONFIGURATION ADW CLEANER PORTABLE")
    print("="*70 + "\n")
    
    # Charger la configuration
    config_path = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / "data" / "programs.json"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Chercher ADW Cleaner
    adwcleaner = None
    for category, programs in data.items():
        if "AdwCleaner" in programs:
            adwcleaner = programs["AdwCleaner"]
            break
        if "AdwCleaner Portable" in programs:
            adwcleaner = programs["AdwCleaner Portable"]
            break
    
    if not adwcleaner:
        print("❌ ADW Cleaner non trouvé dans la configuration !")
        return False
    
    print("📋 CONFIGURATION TROUVÉE :\n")
    
    # Vérifications
    checks = {
        "Description portable": ("portable" in adwcleaner.get("description", "").lower(), 
                                adwcleaner.get("description", "")),
        "portable = true": (adwcleaner.get("portable") == True, 
                           adwcleaner.get("portable")),
        "install_args = 'portable'": (adwcleaner.get("install_args") == "portable", 
                                      adwcleaner.get("install_args")),
        "cleanup_folder": (adwcleaner.get("cleanup_folder") == "Outils de nettoyage", 
                          adwcleaner.get("cleanup_folder")),
        "admin_required = false": (adwcleaner.get("admin_required") == False, 
                                   adwcleaner.get("admin_required")),
        "URL disponible": (bool(adwcleaner.get("download_url")), 
                          adwcleaner.get("download_url", "")[:60] + "..."),
        "WinGet ID": (bool(adwcleaner.get("winget_id")), 
                     adwcleaner.get("winget_id", "")),
    }
    
    all_ok = True
    for check_name, (passed, value) in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check_name:25s} : {value}")
        if not passed:
            all_ok = False
    
    print("\n" + "="*70)
    
    if all_ok:
        print("✅ CONFIGURATION CORRECTE - ADW CLEANER EN MODE PORTABLE !")
        print("\n📂 Comportement attendu :")
        print("   1. Téléchargement du fichier .exe")
        print("   2. Copie dans: Bureau/Outils de nettoyage/")
        print("   3. Création d'un raccourci sur le bureau")
        print("   4. AUCUNE installation système")
    else:
        print("❌ PROBLÈMES DÉTECTÉS DANS LA CONFIGURATION !")
    
    print("="*70 + "\n")
    
    return all_ok

if __name__ == "__main__":
    success = test_adwcleaner_config()
    exit(0 if success else 1)
