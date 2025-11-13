#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Identifier et supprimer les programmes sans solution
"""

import json
from datetime import datetime

def supprimer_programmes_sans_solution():
    """Supprime les programmes sans URL ni winget_id"""
    
    with open('data/programs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Sauvegarder l'original
    backup_name = f"data/programs.json.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    programmes_supprimes = []
    
    print("\n" + "="*80)
    print("          🗑️  SUPPRESSION DES PROGRAMMES SANS SOLUTION          ")
    print("="*80 + "\n")
    
    for category_name, programs in data.items():
        programmes_a_retirer = []
        
        for prog_name, prog_data in programs.items():
            url = prog_data.get('download_url', '')
            winget_id = prog_data.get('winget_id', '')
            
            # Vérifier si le programme n'a ni URL ni winget_id
            if (not url or url == "winget") and not winget_id:
                programmes_a_retirer.append(prog_name)
                programmes_supprimes.append(f"{prog_name} [{category_name}]")
                print(f"🗑️  {prog_name:<40} [{category_name}]")
        
        # Supprimer les programmes identifiés
        for prog_name in programmes_a_retirer:
            del programs[prog_name]
    
    # Sauvegarder les modifications
    with open('data/programs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Sauvegarde: {backup_name}")
    
    print("\n" + "="*80)
    print(f"          ✅ {len(programmes_supprimes)} PROGRAMME(S) SUPPRIMÉ(S)          ")
    print("="*80)
    
    if programmes_supprimes:
        print("\n📋 PROGRAMMES SUPPRIMÉS:")
        for prog in programmes_supprimes:
            print(f"   • {prog}")
    
    print(f"\n🔄 Reconstruisez le package: python build_portable_complet.py")

if __name__ == "__main__":
    supprimer_programmes_sans_solution()
