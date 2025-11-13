#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Vérification du Nombre d'Applications - NiTrite v2.0
==============================================================

Vérifie et affiche le nombre exact d'applications dans programs.json
"""

import json
from pathlib import Path

def main():
    """Vérifie le nombre d'applications"""
    print("\n" + "="*70)
    print("🔍 Vérification du nombre d'applications - NiTrite v2.0")
    print("="*70 + "\n")

    # Lire le fichier programs.json
    project_root = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine
    programs_file = project_root / 'data' / 'programs.json'

    if not programs_file.exists():
        print("❌ ERREUR: Le fichier programs.json n'existe pas!")
        print(f"   Chemin recherché: {programs_file}")
        return 1

    try:
        with open(programs_file, 'r', encoding='utf-8') as f:
            programs = json.load(f)

        # Compter les programmes par catégorie
        total = 0
        categories_avec_10_plus = 0

        print("📊 Programmes par catégorie:\n")
        print(f"{'Catégorie':<35} {'Nombre':>10}")
        print("-" * 70)

        for category, apps in sorted(programs.items()):
            if isinstance(apps, dict):
                count = len(apps)
                total += count

                # Marquer les catégories avec 10+ programmes
                marker = "✅" if count >= 10 else "  "
                print(f"{marker} {category:<33} {count:>10}")

                if count >= 10:
                    categories_avec_10_plus += 1

        print("-" * 70)
        print(f"\n{'TOTAL:':^35} {total:>10} programmes\n")
        print(f"📈 Catégories avec 10+ programmes: {categories_avec_10_plus}/{len(programs)}")

        # Verdict
        print("\n" + "="*70)
        if total == 304:
            print("✅ SUCCÈS: 304 applications détectées (version complète v2.0)")
            print("   Tous les ajouts ont été correctement appliqués!")
        elif total == 241:
            print("⚠️  ATTENTION: 241 applications détectées (ancienne version)")
            print("   Vous n'avez pas la dernière version!")
            print("\n   Solutions:")
            print("   1. Récupérez les dernières modifications:")
            print("      git pull origin claude/analyze-and-fix-app-011CUxUDqMVYZBmahuMZqLZf")
            print("\n   2. Ou téléchargez à nouveau le projet depuis GitHub")
        else:
            print(f"⚠️  Version inattendue: {total} applications")
        print("="*70 + "\n")

        return 0

    except json.JSONDecodeError as e:
        print(f"❌ ERREUR: Le fichier programs.json est invalide!")
        print(f"   Détails: {e}")
        return 1
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
