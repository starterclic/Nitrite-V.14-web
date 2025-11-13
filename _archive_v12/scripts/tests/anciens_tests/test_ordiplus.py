"""
Test pour vérifier les programmes OrdiPlus
"""
import json
import sys
from pathlib import Path

# Charger programs.json
programs_file = Path("data/programs.json")
if programs_file.exists():
    with open(programs_file, 'r', encoding='utf-8') as f:
        programs = json.load(f)
else:
    print("❌ Fichier programs.json introuvable!")
    sys.exit(1)

print("=" * 80)
print("🔍 ANALYSE DE LA CATÉGORIE 'Outils OrdiPlus'")
print("=" * 80)

# Filtrer les programmes OrdiPlus
ordiplus_programs = [p for p in programs if p.get('category') == 'Outils OrdiPlus']

print(f"\n📊 Nombre total de programmes OrdiPlus: {len(ordiplus_programs)}")
print("\n" + "=" * 80)
print("📋 LISTE DES PROGRAMMES:")
print("=" * 80)

for i, prog in enumerate(ordiplus_programs, 1):
    name = prog.get('name', 'Sans nom')
    command = prog.get('command', 'Aucune')
    is_system = prog.get('is_system_command', False)
    
    print(f"\n{i}. {name}")
    print(f"   📌 Commande: {command}")
    print(f"   🔧 Commande système: {is_system}")
    
    # Vérifier si c'est une vraie installation ou une commande
    if is_system or not command or command == "":
        print(f"   ⚠️  PROBLÈME: Pas d'installation réelle!")

print("\n" + "=" * 80)
print("🔍 RÉSUMÉ:")
print("=" * 80)

# Compter les différents types
system_commands = [p for p in ordiplus_programs if p.get('is_system_command', False)]
no_command = [p for p in ordiplus_programs if not p.get('command') or p.get('command') == ""]
installable = [p for p in ordiplus_programs if p.get('command') and not p.get('is_system_command', False)]

print(f"✅ Programmes installables: {len(installable)}")
print(f"🔧 Commandes système: {len(system_commands)}")
print(f"❌ Sans commande: {len(no_command)}")

if system_commands:
    print("\n⚠️  COMMANDES SYSTÈME (non installables):")
    for p in system_commands:
        print(f"   - {p.get('name')}")

if no_command:
    print("\n❌ SANS COMMANDE (non installables):")
    for p in no_command:
        print(f"   - {p.get('name')}")
