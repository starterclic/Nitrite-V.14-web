#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation pour programs_expanded.json
Vérifie l'intégrité, la cohérence et les statistiques du fichier
"""

import json
import os
from collections import Counter

def validate_programs_json(file_path):
    """Valide le fichier programs.json et affiche les statistiques"""

    print("=" * 80)
    print(" " * 20 + "VALIDATION DE PROGRAMS_EXPANDED.JSON")
    print("=" * 80)
    print()

    # 1. Vérifier que le fichier existe
    if not os.path.exists(file_path):
        print(f"❌ ERREUR : Fichier introuvable : {file_path}")
        return False

    print(f"✅ Fichier trouvé : {file_path}")
    file_size = os.path.getsize(file_path)
    print(f"   Taille : {file_size:,} bytes ({file_size / 1024:.2f} KB)")
    print()

    # 2. Vérifier que c'est un JSON valide
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON valide et chargé avec succès")
        print()
    except json.JSONDecodeError as e:
        print(f"❌ ERREUR JSON : {e}")
        return False
    except Exception as e:
        print(f"❌ ERREUR de lecture : {e}")
        return False

    # 3. Statistiques générales
    print("-" * 80)
    print("STATISTIQUES GÉNÉRALES")
    print("-" * 80)

    total_programs = 0
    total_categories = len(data)
    programs_per_category = {}

    for category, programs in data.items():
        count = len(programs)
        total_programs += count
        programs_per_category[category] = count

    print(f"📊 Nombre de catégories : {total_categories}")
    print(f"📦 Nombre total d'applications : {total_programs}")
    print(f"📈 Moyenne par catégorie : {total_programs / total_categories:.1f}")
    print()

    # 4. Vérifier les objectifs
    print("-" * 80)
    print("VÉRIFICATION DES OBJECTIFS")
    print("-" * 80)

    issues = []

    # Objectif 1 : Plus de 500 applications
    if total_programs >= 500:
        print(f"✅ Objectif 500+ applications : ATTEINT ({total_programs} apps)")
    else:
        print(f"❌ Objectif 500+ applications : NON ATTEINT ({total_programs} apps)")
        issues.append(f"Manque {500 - total_programs} applications")

    # Objectif 2 : 30+ apps par catégorie (sauf exceptions)
    categories_below_target = []
    for category, count in programs_per_category.items():
        if category in ['Outils OrdiPlus', 'Pack Office']:
            target = 10
        else:
            target = 30

        if count < target:
            categories_below_target.append((category, count, target))

    if not categories_below_target:
        print(f"✅ Toutes les catégories atteignent leur objectif")
    else:
        print(f"❌ {len(categories_below_target)} catégories sous l'objectif :")
        for cat, count, target in categories_below_target:
            print(f"   - {cat} : {count}/{target} (manque {target - count})")
            issues.append(f"{cat} manque {target - count} apps")

    print()

    # 5. Détails par catégorie
    print("-" * 80)
    print("DÉTAILS PAR CATÉGORIE")
    print("-" * 80)
    print()

    for category in sorted(programs_per_category.keys()):
        count = programs_per_category[category]
        if category in ['Outils OrdiPlus', 'Pack Office']:
            target = 10
        else:
            target = 30

        status = "✅" if count >= target else "❌"
        print(f"{status} {category:35s} : {count:3d} / {target:2d} applications")

    print()

    # 6. Vérification des métadonnées
    print("-" * 80)
    print("VÉRIFICATION DES MÉTADONNÉES")
    print("-" * 80)

    required_fields = ['description', 'category']
    optional_fields = ['download_url', 'install_args', 'winget_id', 'admin_required',
                      'portable', 'cleanup_folder', 'essential']

    programs_without_description = 0
    programs_without_category = 0
    programs_with_winget = 0
    programs_portable = 0
    total_apps_checked = 0

    for category, programs in data.items():
        for app_name, app_data in programs.items():
            total_apps_checked += 1

            if 'description' not in app_data or not app_data['description']:
                programs_without_description += 1

            if 'category' not in app_data or not app_data['category']:
                programs_without_category += 1

            if 'winget_id' in app_data and app_data['winget_id']:
                programs_with_winget += 1

            if app_data.get('portable', False):
                programs_portable += 1

    print(f"📋 Applications vérifiées : {total_apps_checked}")
    print(f"✅ Avec description : {total_apps_checked - programs_without_description}")
    print(f"✅ Avec catégorie : {total_apps_checked - programs_without_category}")
    print(f"🔧 Avec WinGet ID : {programs_with_winget}")
    print(f"💼 Applications portables : {programs_portable}")

    if programs_without_description > 0:
        print(f"⚠️  Sans description : {programs_without_description}")
        issues.append(f"{programs_without_description} apps sans description")

    if programs_without_category > 0:
        print(f"❌ Sans catégorie : {programs_without_category}")
        issues.append(f"{programs_without_category} apps sans catégorie")

    print()

    # 7. Vérification des doublons
    print("-" * 80)
    print("VÉRIFICATION DES DOUBLONS")
    print("-" * 80)

    all_program_names = []
    for category, programs in data.items():
        for app_name in programs.keys():
            all_program_names.append(app_name)

    name_counts = Counter(all_program_names)
    duplicates = {name: count for name, count in name_counts.items() if count > 1}

    if not duplicates:
        print("✅ Aucun doublon trouvé")
    else:
        print(f"❌ {len(duplicates)} programmes en doublon :")
        for name, count in duplicates.items():
            print(f"   - {name} : {count} occurrences")
            issues.append(f"Doublon : {name}")

    print()

    # 8. Résumé final
    print("=" * 80)
    print("RÉSUMÉ DE LA VALIDATION")
    print("=" * 80)

    if not issues:
        print()
        print(" " * 30 + "✅ VALIDATION RÉUSSIE ✅")
        print()
        print(f"   • {total_programs} applications validées")
        print(f"   • {total_categories} catégories complètes")
        print(f"   • {programs_with_winget} IDs WinGet disponibles")
        print(f"   • Toutes les catégories atteignent leur objectif")
        print(f"   • Aucun doublon détecté")
        print(f"   • Structure JSON correcte")
        print()
        print(" " * 25 + "Le fichier est prêt à l'emploi ! 🚀")
        print()
        return True
    else:
        print()
        print(f"⚠️  VALIDATION AVEC {len(issues)} PROBLÈME(S) ⚠️")
        print()
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print()
        return False

if __name__ == "__main__":
    # Utiliser un chemin relatif pour la portabilité
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    file_path = os.path.join(project_root, "data", "programs_expanded.json")

    # Alternative : utiliser programs.json si c'est celui-là qui est utilisé
    if not os.path.exists(file_path):
        file_path = os.path.join(project_root, "data", "programs.json")

    success = validate_programs_json(file_path)

    print("=" * 80)
    if success:
        print("Validation terminée avec succès !")
    else:
        print("Validation terminée avec des avertissements")
    print("=" * 80)
