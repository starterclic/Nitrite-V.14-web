"""
Script pour corriger les URLs cassées dans programs.json
"""
import json
from pathlib import Path

def corriger_urls():
    """Corrige les URLs 404 dans programs.json"""
    
    programs_file = Path('data/programs.json')
    
    with open(programs_file, 'r', encoding='utf-8') as f:
        programs = json.load(f)
    
    # Corrections d'URLs
    corrections = {
        # Adobe Acrobat Reader DC - URL mise à jour
        ("Outils OrdiPlus", "Adobe Acrobat Reader DC"): {
            "download_url": "https://get.adobe.com/reader/download/?installer=Reader_DC_2024_fr_FR.exe&os=Windows%2010&browser_type=KHTML&browser_dist=Chrome&d=McAfee_Security_Scan_Plus_PC1_CPDWN_CDS_BS_&dualoffer=false",
            "install_args": "/sAll /rs",
            "admin_required": True
        },
        
        # Mozilla Firefox - URL corrigée
        ("Outils OrdiPlus", "Mozilla Firefox"): {
            "download_url": "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=fr",
            "install_args": "/S",
            "admin_required": True
        },
        
        # Office 2007 - Utiliser winget à la place
        ("Outils OrdiPlus", "Office 2007"): {
            "download_url": "",
            "winget_id": "Microsoft.Office",
            "admin_required": True,
            "note": "Installation via winget - Microsoft Office"
        },
        
        # RustDesk Portable - URL corrigée (latest release)
        ("Outils OrdiPlus", "RustDesk Portable"): {
            "download_url": "https://github.com/rustdesk/rustdesk/releases/download/1.3.2/rustdesk-1.3.2-x86_64.exe",
            "install_args": "portable",
            "portable": True,
            "admin_required": False
        },
        
        # Spybot Search & Destroy - URL corrigée
        ("Outils OrdiPlus", "Spybot Search & Destroy"): {
            "download_url": "https://download.spybot.info/SpybotSD-2.9.82.0-setup.exe",
            "install_args": "/VERYSILENT /NORESTART",
            "admin_required": True
        },
        
        # Wise Disk Cleaner - URL corrigée
        ("Outils OrdiPlus", "Wise Disk Cleaner"): {
            "download_url": "https://downloads.wisecleaner.com/soft/WDCFree.exe",
            "install_args": "/VERYSILENT /NORESTART",
            "admin_required": True
        },
        
        # AdwCleaner - Ajouter admin_required
        ("Outils OrdiPlus", "AdwCleaner"): {
            "admin_required": True
        },
        
        # Malwarebytes - Ajouter admin_required
        ("Outils OrdiPlus", "Malwarebytes"): {
            "admin_required": True
        },
        
        # VLC Media Player - Ajouter admin_required
        ("Outils OrdiPlus", "VLC Media Player"): {
            "admin_required": True
        },
    }
    
    # Appliquer les corrections
    for (category, program_name), updates in corrections.items():
        if category in programs and program_name in programs[category]:
            print(f"✅ Correction de {category} -> {program_name}")
            for key, value in updates.items():
                programs[category][program_name][key] = value
                print(f"   - {key}: {value}")
        else:
            print(f"⚠️  Programme non trouvé: {category} -> {program_name}")
    
    # Sauvegarder
    with open(programs_file, 'w', encoding='utf-8') as f:
        json.dump(programs, f, indent=4, ensure_ascii=False)
    
    print("\n✅ Fichier programs.json mis à jour!")

if __name__ == "__main__":
    print("=" * 80)
    print("🔧 CORRECTION DES URLs CASSÉES")
    print("=" * 80)
    
    corriger_urls()
    
    print("\n" + "=" * 80)
    print("✅ Corrections terminées!")
    print("   Reconstruisez le package: python build_portable_complet.py")
    print("=" * 80)
