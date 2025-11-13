#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Structure - NiTrite v3.0
=================================

Vérifie que tous les fichiers sont correctement placés et que
les chemins dans les scripts sont corrects.
"""

import sys
from pathlib import Path

def test_structure():
    """Test la structure du projet"""
    print("\n" + "="*70)
    print(" Test de Structure - NiTrite v3.0")
    print("="*70 + "\n")

    # Racine du projet
    project_root = Path(__file__).parent.parent.parent
    print(f"Racine du projet: {project_root}")
    print()

    errors = []
    success = []

    # Fichiers essentiels à la racine
    essential_root_files = [
        "README.md",
        "build_nitrite_v3.0_portable.py",
        "nitrite_complet.py",
        "requirements.txt",
        "LANCER.bat"
    ]

    print("[1/5] Vérification des fichiers à la racine...")
    for file in essential_root_files:
        path = project_root / file
        if path.exists():
            success.append(f"  ✅ {file}")
        else:
            errors.append(f"  ❌ {file} - MANQUANT")

    for msg in success:
        print(msg)
    for msg in errors:
        print(msg)
    print()

    # Dossiers essentiels
    essential_dirs = [
        "src",
        "data",
        "scripts",
        "scripts/lanceurs",
        "scripts/tests",
        "docs"
    ]

    print("[2/5] Vérification des dossiers...")
    errors_dir = []
    success_dir = []
    for dir_name in essential_dirs:
        path = project_root / dir_name
        if path.exists() and path.is_dir():
            success_dir.append(f"  ✅ {dir_name}/")
        else:
            errors_dir.append(f"  ❌ {dir_name}/ - MANQUANT")

    for msg in success_dir:
        print(msg)
    for msg in errors_dir:
        print(msg)
    print()

    # Lanceurs
    print("[3/5] Vérification des lanceurs...")
    lanceurs = [
        "scripts/lanceurs/LANCER_NITRITE.bat",
        "scripts/lanceurs/LANCER_PORTABLE.bat",
        "scripts/lanceurs/lancer_nitrite.py",
        "scripts/lanceurs/lancer_portable.py"
    ]

    errors_lanceurs = []
    success_lanceurs = []
    for lanceur in lanceurs:
        path = project_root / lanceur
        if path.exists():
            success_lanceurs.append(f"  ✅ {lanceur}")
        else:
            errors_lanceurs.append(f"  ❌ {lanceur} - MANQUANT")

    for msg in success_lanceurs:
        print(msg)
    for msg in errors_lanceurs:
        print(msg)
    print()

    # Data files
    print("[4/5] Vérification des fichiers de données...")
    data_files = [
        "data/programs.json",
        "data/config.json"
    ]

    errors_data = []
    success_data = []
    for file in data_files:
        path = project_root / file
        if path.exists():
            success_data.append(f"  ✅ {file}")
        else:
            errors_data.append(f"  ❌ {file} - MANQUANT")

    for msg in success_data:
        print(msg)
    for msg in errors_data:
        print(msg)
    print()

    # Test import des lanceurs
    print("[5/5] Test des imports...")
    sys.path.insert(0, str(project_root / "scripts" / "lanceurs"))

    try:
        import lancer_nitrite
        print("  ✅ lancer_nitrite.py - Import OK")
    except Exception as e:
        errors.extend(errors_dir + errors_lanceurs + errors_data)
        errors.append(f"  ❌ lancer_nitrite.py - Erreur d'import: {e}")

    try:
        import lancer_portable
        print("  ✅ lancer_portable.py - Import OK")
    except Exception as e:
        errors.extend(errors_dir + errors_lanceurs + errors_data)
        errors.append(f"  ❌ lancer_portable.py - Erreur d'import: {e}")

    print()

    # Résumé
    print("="*70)
    all_errors = errors + errors_dir + errors_lanceurs + errors_data
    if not all_errors:
        print("✅ TOUS LES TESTS SONT PASSÉS")
        print("\nLa structure du projet est correcte !")
        print("Vous pouvez lancer NiTrite avec: LANCER.bat")
        print("="*70 + "\n")
        return 0
    else:
        print(f"❌ {len(all_errors)} ERREUR(S) DÉTECTÉE(S)")
        print("\nProblèmes détectés:")
        for error in all_errors:
            print(error)
        print("="*70 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(test_structure())
