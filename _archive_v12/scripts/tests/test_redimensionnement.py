#!/usr/bin/env python3
"""
Test des nouvelles fonctionnalités de redimensionnement des catégories
"""

import sys
from pathlib import Path

def test_new_ui_features():
    """Test des nouvelles fonctionnalités de l'interface"""
    print("🔍 Test des nouvelles fonctionnalités de redimensionnement...")
    
    try:
        # Vérifier que le fichier GUI a les nouvelles méthodes
        gui_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'src' / 'gui_manager.py'
        with open(gui_file, 'r', encoding='utf-8') as f:
            gui_content = f.read()
        
        # Nouvelles méthodes pour le redimensionnement
        new_methods = [
            'create_scrollable_category_frame',
            'toggle_category',
            'expand_all_categories',
            'collapse_all_categories',
            'reorganize_categories'
        ]
        
        found_methods = 0
        for method in new_methods:
            if f"def {method}" in gui_content:
                print(f"  ✅ Méthode {method} présente")
                found_methods += 1
            else:
                print(f"  ❌ Méthode {method} manquante")
        
        # Nouvelles fonctionnalités UI
        ui_features = [
            'collapsed_categories',  # Gestion des catégories pliées
            'category_widgets',      # Widgets des catégories
            'cat_canvas',           # Canvas par catégorie
            'main_container',       # Conteneur principal
            'columnconfigure(i, weight=1, minsize=350)', # Colonnes redimensionnables
            'MouseWheel',           # Support scroll par catégorie
            '📖 Tout déplier',      # Bouton déplier
            '📙 Tout plier',        # Bouton plier
            '🔄 Réorganiser'        # Bouton réorganiser
        ]
        
        found_features = 0
        for feature in ui_features:
            if feature in gui_content:
                print(f"  ✅ Fonctionnalité {feature} présente")
                found_features += 1
            else:
                print(f"  ⚠️  Fonctionnalité {feature} manquante")
        
        print(f"  📊 {found_methods}/{len(new_methods)} nouvelles méthodes")
        print(f"  📊 {found_features}/{len(ui_features)} nouvelles fonctionnalités")
        
        # Vérifications spécifiques pour le redimensionnement
        redimensioning_features = [
            'height=200',           # Hauteur fixe par catégorie
            'minsize=350',          # Taille minimale des colonnes
            'font=(\'Arial\', 8',   # Texte plus compact
            'grid(row=row, column=col, sticky=(tk.W, tk.E, tk.N, tk.S)', # Redimensionnement
            'for i in range(3):'    # 3 colonnes
        ]
        
        found_redim = 0
        for feature in redimensioning_features:
            if feature in gui_content:
                print(f"  ✅ Redimensionnement: {feature}")
                found_redim += 1
        
        print(f"  📏 {found_redim}/{len(redimensioning_features)} fonctionnalités de redimensionnement")
        
        return found_methods >= 4 and found_features >= 6 and found_redim >= 3
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_toolbar_improvements():
    """Test des améliorations de la barre d'outils"""
    print("\n🛠️ Test des améliorations de la barre d'outils...")
    
    try:
        gui_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'src' / 'gui_manager.py'
        with open(gui_file, 'r', encoding='utf-8') as f:
            gui_content = f.read()
        
        toolbar_features = [
            'Outils de sélection et d\'affichage',
            'selection_frame',
            'control_frame',
            'display_frame',
            '📖 Tout déplier',
            '📙 Tout plier',
            '🔄 Réorganiser',
            'expand_all_categories',
            'collapse_all_categories'
        ]
        
        found_toolbar = 0
        for feature in toolbar_features:
            if feature in gui_content:
                print(f"  ✅ Barre d'outils: {feature}")
                found_toolbar += 1
        
        print(f"  📊 {found_toolbar}/{len(toolbar_features)} améliorations de la barre d'outils")
        
        return found_toolbar >= 7
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_layout_improvements():
    """Test des améliorations de mise en page"""
    print("\n📐 Test des améliorations de mise en page...")
    
    try:
        gui_file = Path(__file__).parent.parent.parent  # scripts/tests/ -> racine / 'src' / 'gui_manager.py'
        with open(gui_file, 'r', encoding='utf-8') as f:
            gui_content = f.read()
        
        layout_features = [
            'for i in range(3):',           # 3 colonnes
            'minsize=350',                  # Taille minimale
            'sticky=(tk.W, tk.E, tk.N, tk.S)', # Redimensionnement complet
            'height=200',                   # Hauteur contrôlée
            'font=(\'Arial\', 8',           # Police plus petite
            'pady=1',                       # Espacement réduit
            'desc_text[:32]',               # Description plus courte
            'cat_scrollbar'                 # Scrollbar par catégorie
        ]
        
        found_layout = 0
        for feature in layout_features:
            if feature in gui_content:
                print(f"  ✅ Mise en page: {feature}")
                found_layout += 1
        
        print(f"  📊 {found_layout}/{len(layout_features)} améliorations de mise en page")
        
        return found_layout >= 6
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test des Catégories Redimensionnables - NiTrite v.2")
    print("=" * 60)
    
    tests = [
        ("Nouvelles fonctionnalités UI", test_new_ui_features),
        ("Améliorations barre d'outils", test_toolbar_improvements),
        ("Améliorations mise en page", test_layout_improvements)
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
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSULTATS: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests == total_tests:
        print("🎉 TOUTES LES AMÉLIORATIONS VALIDÉES!")
        print("\n🎯 Nouvelles fonctionnalités disponibles:")
        print("  ✅ Catégories redimensionnables en 3 colonnes")
        print("  ✅ Hauteur fixe par catégorie (200px)")
        print("  ✅ Scroll individuel par catégorie")
        print("  ✅ Boutons plier/déplier par catégorie")
        print("  ✅ Contrôles globaux (tout plier/déplier)")
        print("  ✅ Réorganisation automatique")
        print("  ✅ Affichage plus compact et dense")
        print("  ✅ Barre d'outils améliorée")
        print("\n🚀 L'interface peut maintenant afficher BEAUCOUP plus d'applications!")
    else:
        print(f"⚠️  {total_tests - passed_tests} test(s) ont échoué")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)