#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des checkboxes - Détecte les programmes non comptabilisés
"""

import sys
import json
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path.cwd() / 'src'))

def test_programs_loaded():
    """Teste quels programmes sont chargés"""
    print("=" * 70)
    print("TEST DES PROGRAMMES CHARGÉS")
    print("=" * 70)
    
    # Charger programs.json
    programs_file = Path("data/programs.json")
    with open(programs_file, 'r', encoding='utf-8') as f:
        programs = json.load(f)
    
    total_in_json = 0
    categories_info = {}
    
    for category, progs in programs.items():
        count = len(progs)
        total_in_json += count
        categories_info[category] = count
        print(f"📁 {category}: {count} programmes")
    
    print(f"\n📊 TOTAL dans programs.json: {total_in_json} programmes")
    
    # Vérifier les programmes avec is_command
    commands_count = 0
    normal_programs = 0
    
    for category, progs in programs.items():
        for prog_name, prog_info in progs.items():
            if prog_info.get('is_command', False):
                commands_count += 1
            else:
                normal_programs += 1
    
    print(f"\n🔧 Commandes système: {commands_count}")
    print(f"📦 Programmes normaux: {normal_programs}")
    print(f"✅ TOTAL: {commands_count + normal_programs}")
    
    # Détecter les programmes qui pourraient poser problème
    print(f"\n⚠️  PROGRAMMES AVEC CARACTÈRES SPÉCIAUX:")
    special_chars_progs = []
    for category, progs in programs.items():
        for prog_name in progs.keys():
            # Vérifier les caractères spéciaux
            if any(char in prog_name for char in ['&', '+', '#', '@', '(', ')', '[', ']']):
                special_chars_progs.append((category, prog_name))
    
    if special_chars_progs:
        for cat, prog in special_chars_progs[:10]:
            print(f"  • [{cat}] {prog}")
        if len(special_chars_progs) > 10:
            print(f"  ... et {len(special_chars_progs) - 10} autres")
    else:
        print("  Aucun")
    
    # Vérifier les commandes vs programmes
    print(f"\n🔍 ANALYSE DES COMMANDES:")
    for category, progs in programs.items():
        commands_in_cat = sum(1 for p in progs.values() if p.get('is_command', False))
        if commands_in_cat > 0:
            print(f"  • {category}: {commands_in_cat} commande(s)")

if __name__ == "__main__":
    test_programs_loaded()
