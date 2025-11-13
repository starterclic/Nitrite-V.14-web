"""
Correction des programmes Outils OrdiPlus qui ne fonctionnent pas
"""
import json
from datetime import datetime

programs_file = 'data/programs.json'

print("=" * 80)
print("🔧 CORRECTION DES PROGRAMMES OUTILS ORDIPLUS")
print("=" * 80)
print()

# Charger
with open(programs_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

ordiplus = data.get('Outils OrdiPlus', {})

# Corrections à apporter
corrections = {
    "AdwCleaner": {
        "download_url": "",
        "winget_id": "Malwarebytes.AdwCleaner",
        "note": "Installation via winget"
    },
    "Adobe Acrobat Reader DC": {
        "download_url": "",
        "winget_id": "Adobe.Acrobat.Reader.64-bit",
        "note": "Installation via winget"
    },
    "Malwarebytes": {
        "download_url": "https://data-cdn.mbamupdates.com/web/mb4-setup-consumer/MBSetup.exe",
        "install_args": "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-",
        "note": "URL vérifiée - Arguments corrigés"
    },
    "Wise Disk Cleaner": {
        "download_url": "https://downloads.wisecleaner.com/soft/WDCFree.exe",
        "install_args": "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-",
        "note": "Arguments corrigés pour installation silencieuse"
    },
    "Spybot Search & Destroy": {
        "download_url": "",
        "winget_id": "Safer-Networking.SpybotAntiBeacon",
        "note": "Installation via winget - URL obsolète"
    }
}

count = 0
for prog_name, fixes in corrections.items():
    if prog_name in ordiplus:
        print(f"✅ Correction: {prog_name}")
        for key, value in fixes.items():
            old_value = ordiplus[prog_name].get(key, '')
            if old_value != value:
                ordiplus[prog_name][key] = value
                print(f"   • {key}: {value if value else '(vide pour winget)'}")
                count += 1

# Sauvegarde
backup_file = f"{programs_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
with open(backup_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
print(f"\n💾 Sauvegarde: {backup_file}")

# Sauvegarder
with open(programs_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print()
print("=" * 80)
print(f"✅ {count} MODIFICATIONS APPLIQUÉES")
print("=" * 80)
print()
print("📋 RÉSUMÉ:")
print("   • AdwCleaner → Winget")
print("   • Adobe Reader → Winget")
print("   • Spybot → Winget")
print("   • Malwarebytes → Arguments corrigés")
print("   • Wise Disk Cleaner → Arguments corrigés")
print()
print("🔄 Reconstruisez le package: python build_portable_complet.py")
