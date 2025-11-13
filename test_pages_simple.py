#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple des pages avancées
"""

import sys
import os

# Ajouter src au path
sys.path.insert(0, 'src')

print("="*60)
print("TEST DES PAGES AVANCÉES - Mode Fallback")
print("="*60)
print()

# Simuler les dépendances manquantes
print("1. Test des imports...")
print()

try:
    from gui_modern_v13 import ModernColors, bind_mousewheel
    print("✅ ModernColors importé")
except Exception as e:
    print(f"❌ Erreur ModernColors: {e}")
    sys.exit(1)

try:
    from advanced_pages import (
        UpdatesPage, BackupPage, OptimizationsPage,
        DiagnosticPage, SettingsPage, ThemeManager
    )
    print("✅ Toutes les pages importées")
except Exception as e:
    print(f"❌ Erreur import pages: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("2. Vérification des classes...")
print()

# Vérifier que les classes ont des méthodes
pages_classes = {
    'UpdatesPage': UpdatesPage,
    'BackupPage': BackupPage,
    'OptimizationsPage': OptimizationsPage,
    'DiagnosticPage': DiagnosticPage,
    'SettingsPage': SettingsPage,
}

for name, cls in pages_classes.items():
    methods = [m for m in dir(cls) if not m.startswith('_')]
    print(f"  {name}: {len(methods)} méthodes publiques")

    # Vérifier __init__
    if hasattr(cls, '__init__'):
        print(f"    ✅ __init__ présent")

    # Vérifier _create_widgets
    if hasattr(cls, '_create_widgets'):
        print(f"    ✅ _create_widgets présent")
    else:
        print(f"    ❌ _create_widgets MANQUANT!")

print()
print("3. Test création d'une page (UpdatesPage)...")
print()

try:
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre

    # Données simulées
    programs_data = {
        "Test Category": {
            "Test App": {
                "description": "Test application",
                "category": "Test"
            }
        }
    }

    # Créer la page
    page = UpdatesPage(root, programs_data)

    # Vérifier que la page a des enfants (widgets)
    children = page.winfo_children()
    print(f"✅ UpdatesPage créée avec {len(children)} widgets enfants")

    if len(children) == 0:
        print("⚠️  PROBLÈME: La page n'a aucun widget!")
        print("   Les widgets ne se créent pas correctement")
    else:
        print("✅ La page contient des widgets - devrait s'afficher")

    root.destroy()

except ImportError as e:
    print(f"❌ tkinter non disponible: {e}")
    print("   (Normal sur ce système - testez sur Windows)")
except Exception as e:
    print(f"❌ Erreur lors création page: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*60)
print("FIN DU TEST")
print("="*60)
print()
print("DIAGNOSTIC:")
print()
print("Si tous les tests sont ✅ sauf 'tkinter non disponible':")
print("  → Le code est correct")
print("  → Testez sur Windows pour voir l'interface")
print()
print("Si UpdatesPage n'a AUCUN widget (0 widgets):")
print("  → Problème dans _create_widgets()")
print("  → La page ne se construit pas")
print()
print("Si erreur import pages:")
print("  → Fichier advanced_pages.py corrompu")
print("  → Vérifier la syntaxe Python")
