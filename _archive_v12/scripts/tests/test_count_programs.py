"""
Script de test pour compter les programmes disponibles
"""

import json
from pathlib import Path

def count_programs():
    """Compte le nombre total de programmes disponibles"""
    programs_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs.json'
    
    if not programs_file.exists():
        print("❌ Fichier programs.json non trouvé")
        return
    
    with open(programs_file, 'r', encoding='utf-8') as f:
        programs_data = json.load(f)
    
    print("=" * 60)
    print("📊 ANALYSE DES PROGRAMMES DISPONIBLES")
    print("=" * 60)
    
    total = 0
    for category, programs in programs_data.items():
        count = len(programs) if isinstance(programs, dict) else 0
        print(f"\n{category}: {count} programmes")
        total += count
        
        # Afficher les noms des programmes
        if isinstance(programs, dict):
            for i, prog_name in enumerate(programs.keys(), 1):
                print(f"  {i}. {prog_name}")
    
    print("\n" + "=" * 60)
    print(f"✅ TOTAL: {total} programmes disponibles")
    print("=" * 60)

if __name__ == "__main__":
    count_programs()
    input("\nAppuyez sur Entrée pour continuer...")
