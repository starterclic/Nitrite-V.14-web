"""
Script pour nettoyer les doublons dans programs.json
Garde la première occurrence de chaque programme et supprime les autres
"""
import json
from pathlib import Path
from collections import Counter
import shutil
from datetime import datetime

def nettoyer_doublons():
    """Supprime les doublons du fichier programs.json"""
    
    programs_file = Path('data/programs.json')
    
    if not programs_file.exists():
        print("❌ Fichier programs.json introuvable!")
        return
    
    # Créer une sauvegarde
    backup_file = programs_file.with_suffix('.json.backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
    shutil.copy2(programs_file, backup_file)
    print(f"✅ Sauvegarde créée: {backup_file.name}")
    
    # Charger le fichier
    with open(programs_file, 'r', encoding='utf-8') as f:
        programs = json.load(f)
    
    print("\n" + "=" * 80)
    print("📊 ANALYSE DES DOUBLONS")
    print("=" * 80)
    
    # Analyser les doublons
    all_names = []
    program_locations = {}  # {nom: [(catégorie, info), ...]}
    
    for category, progs in programs.items():
        if isinstance(progs, dict):
            for name, info in progs.items():
                all_names.append(name)
                if name not in program_locations:
                    program_locations[name] = []
                program_locations[name].append((category, info))
    
    # Trouver les doublons
    counts = Counter(all_names)
    duplicates = {name: count for name, count in counts.items() if count > 1}
    
    if not duplicates:
        print("\n✅ Aucun doublon trouvé !")
        return
    
    print(f"\n⚠️  {len(duplicates)} programmes en doublon trouvés:")
    print()
    
    # Afficher les doublons
    for name, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True):
        print(f"  📌 {name} ({count} fois)")
        locations = program_locations[name]
        for i, (cat, info) in enumerate(locations, 1):
            marker = "✓ GARDÉ" if i == 1 else "✗ SUPPRIMÉ"
            print(f"     {marker}: {cat}")
    
    print("\n" + "=" * 80)
    print("🧹 NETTOYAGE EN COURS...")
    print("=" * 80)
    
    # Nettoyer les doublons
    seen_programs = set()
    programs_cleaned = {}
    removed_count = 0
    
    # Ordre de priorité des catégories (on garde la première occurrence selon cet ordre)
    priority_order = [
        "Outils OrdiPlus",      # Priorité maximale
        "Pack Office",
        "Navigateurs",
        "Antivirus",
        "Sécurité",
        "Bureautique",
        "Multimédia",
        "Développement",
        "Utilitaires",
        "Communication",
    ]
    
    # Trier les catégories selon la priorité
    def get_priority(category):
        try:
            return priority_order.index(category)
        except ValueError:
            return 999  # Fin de liste si pas dans priority_order
    
    sorted_categories = sorted(programs.items(), key=lambda x: get_priority(x[0]))
    
    for category, progs in sorted_categories:
        if not isinstance(progs, dict):
            programs_cleaned[category] = progs
            continue
        
        category_progs = {}
        
        for name, info in progs.items():
            if name not in seen_programs:
                # Première occurrence : on garde
                category_progs[name] = info
                seen_programs.add(name)
                print(f"  ✅ {name} → gardé dans '{category}'")
            else:
                # Doublon : on supprime
                removed_count += 1
                print(f"  🗑️  {name} → supprimé de '{category}' (doublon)")
        
        programs_cleaned[category] = category_progs
    
    # Sauvegarder le fichier nettoyé
    with open(programs_file, 'w', encoding='utf-8') as f:
        json.dump(programs_cleaned, f, indent=4, ensure_ascii=False)
    
    # Statistiques finales
    print("\n" + "=" * 80)
    print("✅ NETTOYAGE TERMINÉ !")
    print("=" * 80)
    
    total_before = sum(len(p) if isinstance(p, dict) else 0 for p in programs.values())
    total_after = sum(len(p) if isinstance(p, dict) else 0 for p in programs_cleaned.values())
    
    print(f"\n📊 STATISTIQUES:")
    print(f"  • Avant : {total_before} programmes (avec doublons)")
    print(f"  • Après : {total_after} programmes (sans doublons)")
    print(f"  • Supprimés : {removed_count} doublons")
    print(f"  • Sauvegarde : {backup_file.name}")
    
    print("\n" + "=" * 80)
    print("📋 PROGRAMMES PAR CATÉGORIE (après nettoyage):")
    print("=" * 80)
    
    for category, progs in sorted(programs_cleaned.items(), key=lambda x: len(x[1]) if isinstance(x[1], dict) else 0, reverse=True):
        if isinstance(progs, dict):
            count = len(progs)
            print(f"  {category}: {count} programmes")
    
    print("\n✅ Fichier programs.json nettoyé avec succès !")
    print(f"✅ Les checkboxes devraient maintenant compter correctement !")

if __name__ == "__main__":
    print("=" * 80)
    print("🧹 NETTOYAGE DES DOUBLONS - programs.json")
    print("=" * 80)
    
    nettoyer_doublons()
    
    print("\n" + "=" * 80)
    print("🔄 PROCHAINES ÉTAPES:")
    print("=" * 80)
    print("  1. ✅ Doublons supprimés")
    print("  2. 🔨 Reconstruire le package : python build_portable_complet.py")
    print("  3. ✅ Tester l'application : tous les programmes comptés !")
    print("=" * 80)
