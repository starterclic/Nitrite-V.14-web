"""
Test rapide v3.0.1 - Exécution des commandes système
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from winget_manager import WingetManager


def test_commandes_systeme():
    """Test des commandes système"""
    print("=" * 70)
    print("🔍 TEST v3.0.1 - EXÉCUTION COMMANDES SYSTÈME")
    print("=" * 70)
    print()
    
    wm = WingetManager()
    
    # 1. Test détection commandes système
    print("1. DÉTECTION COMMANDES SYSTÈME")
    print("-" * 70)
    
    test_items = [
        ("Mozilla Firefox", False, "Programme Winget"),
        ("DISM - Vérifier l'état", True, "Commande réparation"),
        ("Paramètres Windows", True, "Commande paramètres"),
        ("Réseau et Internet", True, "Commande paramètres"),
        ("Google Chrome", False, "Programme Winget"),
    ]
    
    for item_name, expected, description in test_items:
        is_cmd = wm.is_system_command(item_name)
        status = "✅" if is_cmd == expected else "❌"
        print(f"{status} {item_name:30s} → {'Commande' if is_cmd else 'Programme':10s} ({description})")
    
    print()
    
    # 2. Test méthode run_system_command existe
    print("2. MÉTHODES DISPONIBLES")
    print("-" * 70)
    
    has_run_system = hasattr(wm, 'run_system_command')
    has_is_system = hasattr(wm, 'is_system_command')
    
    print(f"{'✅' if has_run_system else '❌'} Méthode run_system_command() : {'Présente' if has_run_system else 'MANQUANTE'}")
    print(f"{'✅' if has_is_system else '❌'} Méthode is_system_command()  : {'Présente' if has_is_system else 'MANQUANTE'}")
    
    print()
    
    # 3. Compter les commandes système
    print("3. STATISTIQUES COMMANDES SYSTÈME")
    print("-" * 70)
    
    total_commandes = 0
    par_categorie = {}
    
    for cat_name, items in wm.programs_db.items():
        nb_commandes = sum(1 for item in items.values() if 'command' in item)
        if nb_commandes > 0:
            par_categorie[cat_name] = nb_commandes
            total_commandes += nb_commandes
    
    print(f"Total commandes système : {total_commandes}")
    print()
    print("Répartition par catégorie :")
    for cat, nb in par_categorie.items():
        print(f"  - {cat:30s} : {nb} commandes")
    
    print()
    print("=" * 70)
    
    if has_run_system and has_is_system:
        print("✅ TOUT EST PRÊT - Les commandes système vont s'exécuter !")
    else:
        print("❌ PROBLÈME - Méthodes manquantes")
    
    print("=" * 70)


if __name__ == "__main__":
    test_commandes_systeme()
