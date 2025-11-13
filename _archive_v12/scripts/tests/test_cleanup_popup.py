"""
Test du popup de nettoyage
"""

import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from cleanup_manager import NiTriteCleanup


def test_cleanup_popup():
    """Test du popup de nettoyage"""
    
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    
    try:
        cleanup = NiTriteCleanup()
        items = cleanup.get_cleanup_items()
        total_size = cleanup.get_total_size()
        
        print("=" * 70)
        print("🧹 TEST POPUP NETTOYAGE")
        print("=" * 70)
        print()
        print(f"Éléments détectés : {len(items)}")
        print(f"Taille totale : {total_size} Mo")
        print()
        
        if len(items) == 0:
            print("❌ Aucun élément à nettoyer détecté !")
            print("   → Le popup ne s'affichera pas (normal)")
        else:
            print("✅ Éléments détectés :")
            for name, path, size in items:
                print(f"   - {name:30s} ({size} Mo)")
            print()
            print("→ Le popup devrait s'afficher")
        
        print()
        print("=" * 70)
        print("Tentative d'affichage du popup...")
        print("=" * 70)
        
        # Tester si le popup peut s'afficher
        response = messagebox.askyesno(
            "Test",
            f"Le popup de nettoyage fonctionne !\n\n"
            f"{len(items)} élément(s) détecté(s)\n"
            f"Taille totale : {total_size} Mo"
        )
        
        if response:
            print("✅ Utilisateur a cliqué OUI")
        else:
            print("❌ Utilisateur a cliqué NON")
            
    except Exception as e:
        print(f"❌ ERREUR : {e}")
        import traceback
        traceback.print_exc()
    
    root.destroy()


if __name__ == "__main__":
    test_cleanup_popup()
