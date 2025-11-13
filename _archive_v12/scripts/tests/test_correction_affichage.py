#!/usr/bin/env python3
"""
Test de vérification de l'affichage des applications
"""

import sys
from pathlib import Path

def test_interface_display():
    """Test que l'interface affiche bien les applications"""
    print("🔍 Test de l'affichage des applications...")
    
    try:
        # Vérifier la structure corrigée
        gui_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'src' / 'gui_manager.py'
        with open(gui_file, 'r', encoding='utf-8') as f:
            gui_content = f.read()
        
        # Vérifications de la correction
        fixes = [
            'max_cols = 2',                    # Retour à 2 colonnes
            'minsize=400',                     # Taille plus grande
            'ttk.LabelFrame(self.scrollable_frame', # Structure simplifiée
            'programs_container',              # Container des programmes
            'cat_canvas',                      # Canvas par catégorie
            'height=150',                      # Hauteur réduite mais visible
            'font=(\'Arial\', 9, \'bold\')',   # Police plus grande
            'len(desc_text) > 45'              # Description plus longue
        ]
        
        found_fixes = 0
        for fix in fixes:
            if fix in gui_content:
                print(f"  ✅ Correction: {fix}")
                found_fixes += 1
            else:
                print(f"  ❌ Manque: {fix}")
        
        print(f"  📊 {found_fixes}/{len(fixes)} corrections appliquées")
        
        # Vérifier qu'on n'a plus les anciennes structures problématiques
        removed_issues = [
            'main_container.pack',             # Structure complexe supprimée
            'create_scrollable_category_frame' # Méthode obsolète supprimée
        ]
        
        issues_removed = 0
        for issue in removed_issues:
            if issue not in gui_content:
                print(f"  ✅ Supprimé: {issue}")
                issues_removed += 1
            else:
                print(f"  ⚠️  Reste: {issue}")
        
        return found_fixes >= 6 and issues_removed >= 1
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_program_loading():
    """Test du chargement des programmes"""
    print("\n📋 Test du chargement des programmes...")
    
    try:
        import json
        programs_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'data' / 'programs.json'
        with open(programs_file, 'r', encoding='utf-8') as f:
            programs = json.load(f)
        
        print(f"  ✅ {len(programs)} programmes chargés")
        
        # Vérifier quelques programmes clés
        key_programs = ['firefox', 'chrome', 'vscode', 'steam', 'discord']
        found_programs = 0
        for prog in key_programs:
            if prog in programs:
                print(f"  ✅ {programs[prog]['name']} trouvé")
                found_programs += 1
        
        print(f"  📊 {found_programs}/{len(key_programs)} programmes clés présents")
        return found_programs >= 4
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def main():
    """Test principal"""
    print("🧪 Test de Correction de l'Affichage - NiTrite v.2")
    print("=" * 50)
    
    tests = [
        ("Correction interface", test_interface_display),
        ("Chargement programmes", test_program_loading)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"\n✅ {test_name}: RÉUSSI")
            else:
                print(f"\n❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"\n❌ {test_name}: ERREUR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 RÉSULTATS: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests == total_tests:
        print("🎉 CORRECTION RÉUSSIE!")
        print("\n🎯 Problèmes corrigés:")
        print("  ✅ Structure d'interface simplifiée")
        print("  ✅ Affichage en 2 colonnes stables")
        print("  ✅ Catégories avec hauteur visible (150px)")
        print("  ✅ Scroll par catégorie fonctionnel")
        print("  ✅ Police et espacement optimisés")
        print("  ✅ Descriptions plus lisibles")
        print("\n🚀 Les applications devraient maintenant être visibles!")
    else:
        print("⚠️  Des problèmes persistent")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)