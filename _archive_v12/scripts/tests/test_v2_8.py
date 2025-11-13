"""
Test des nouvelles fonctionnalités NiTrite v2.8
- Outils OrdiPlus en première position
- Couleur orange vif
- Commandes de réparation Windows
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent  # scripts/tests/ -> racine))

from src.winget_manager import WingetManager


def test_ordre_categories():
    """Test que Outils OrdiPlus est en première position"""
    print("\n" + "="*70)
    print("TEST 1: Ordre des catégories")
    print("="*70)
    
    wm = WingetManager()
    categories = list(wm.programs_db.keys())
    
    print(f"\n✅ Nombre total de catégories: {len(categories)}")
    print(f"\n📋 Top 5 des catégories:\n")
    
    for i, cat in enumerate(categories[:5], 1):
        if i == 1:
            marker = "🟠" if cat == "Outils OrdiPlus" else "❌"
        elif i == 2:
            marker = "🔧" if "Réparation" in cat else "📁"
        else:
            marker = "📁"
        
        print(f"  {i}. {marker} {cat}")
    
    # Vérification
    assert categories[0] == "Outils OrdiPlus", "❌ Outils OrdiPlus n'est pas en première position!"
    print("\n✅ TEST RÉUSSI: Outils OrdiPlus est bien en première position")
    
    assert "Réparation" in categories[1], "❌ Réparation Windows n'est pas en deuxième position!"
    print("✅ TEST RÉUSSI: Réparation Windows est bien en deuxième position")


def test_couleur_ordiplus():
    """Test que Outils OrdiPlus a la couleur orange"""
    print("\n" + "="*70)
    print("TEST 2: Couleur Outils OrdiPlus")
    print("="*70)
    
    wm = WingetManager()
    ordiplus = wm.programs_db.get("Outils OrdiPlus", {})
    
    print(f"\n✅ Nombre de programmes dans Outils OrdiPlus: {len(ordiplus)}")
    
    # Vérifier la couleur sur quelques programmes
    programs_with_color = 0
    for prog_name, prog_info in list(ordiplus.items())[:3]:
        color = prog_info.get("color", "NON DÉFINIE")
        print(f"\n  📦 {prog_name}")
        print(f"     Couleur: {color}")
        
        if color == "#FF6600":
            programs_with_color += 1
    
    assert programs_with_color > 0, "❌ Aucun programme avec la couleur orange!"
    print(f"\n✅ TEST RÉUSSI: {programs_with_color} programmes ont la couleur orange vif (#FF6600)")


def test_commandes_reparation():
    """Test des commandes de réparation Windows"""
    print("\n" + "="*70)
    print("TEST 3: Commandes de réparation Windows")
    print("="*70)
    
    wm = WingetManager()
    repair_commands = wm.get_repair_commands()
    
    print(f"\n✅ Nombre de commandes de réparation: {len(repair_commands)}")
    
    # Commandes attendues
    expected_commands = [
        "DISM - Vérifier l'état",
        "DISM - Scanner l'image",
        "DISM - Réparer l'image",
        "SFC - Vérifier fichiers système",
        "Réparer les bases de registre",
    ]
    
    print("\n🔧 Commandes disponibles:\n")
    for i, (cmd_name, cmd_info) in enumerate(repair_commands.items(), 1):
        admin = "✅" if cmd_info.get("admin_required") else "❌"
        print(f"  {i}. {cmd_name}")
        print(f"     Admin requis: {admin}")
        print(f"     Commande: {cmd_info.get('command', 'N/A')[:60]}...")
    
    # Vérifications
    for expected in expected_commands:
        assert expected in repair_commands, f"❌ Commande manquante: {expected}"
    
    print(f"\n✅ TEST RÉUSSI: Toutes les commandes principales sont présentes")


def test_detection_commandes():
    """Test de la détection des commandes de réparation"""
    print("\n" + "="*70)
    print("TEST 4: Détection automatique des commandes")
    print("="*70)
    
    wm = WingetManager()
    
    # Test avec une commande de réparation
    test_repair = "DISM - Vérifier l'état"
    is_repair = wm.is_repair_command(test_repair)
    
    print(f"\n🔍 Test: '{test_repair}'")
    print(f"   Détecté comme commande de réparation: {'✅ OUI' if is_repair else '❌ NON'}")
    
    assert is_repair, f"❌ La commande '{test_repair}' n'est pas détectée comme réparation!"
    
    # Test avec un programme normal
    test_program = "Mozilla Firefox"
    is_repair_prog = wm.is_repair_command(test_program)
    
    print(f"\n🔍 Test: '{test_program}'")
    print(f"   Détecté comme commande de réparation: {'❌ OUI (ERREUR)' if is_repair_prog else '✅ NON'}")
    
    assert not is_repair_prog, f"❌ Le programme '{test_program}' est détecté à tort comme réparation!"
    
    print("\n✅ TEST RÉUSSI: Détection automatique fonctionne correctement")


def test_structure_commande():
    """Test de la structure d'une commande de réparation"""
    print("\n" + "="*70)
    print("TEST 5: Structure des commandes de réparation")
    print("="*70)
    
    wm = WingetManager()
    repair_commands = wm.get_repair_commands()
    
    # Prendre la première commande
    cmd_name = list(repair_commands.keys())[0]
    cmd_info = repair_commands[cmd_name]
    
    print(f"\n📋 Analyse de: '{cmd_name}'")
    print(f"\n   Structure:")
    
    # Vérifier les champs requis
    required_fields = ["command", "description", "category", "admin_required"]
    
    for field in required_fields:
        has_field = field in cmd_info
        value = cmd_info.get(field, "N/A")
        status = "✅" if has_field else "❌"
        
        print(f"   {status} {field}: {value}")
        
        assert has_field, f"❌ Champ manquant: {field}"
    
    print("\n✅ TEST RÉUSSI: Structure des commandes est correcte")


def test_compte_total():
    """Test du compte total de programmes"""
    print("\n" + "="*70)
    print("TEST 6: Comptage total")
    print("="*70)
    
    wm = WingetManager()
    
    total_count = wm.get_program_count()
    categories_count = len(wm.programs_db)
    
    print(f"\n📊 Statistiques:")
    print(f"   Total de programmes/commandes: {total_count}")
    print(f"   Nombre de catégories: {categories_count}")
    
    # Détail par catégorie
    print(f"\n📋 Détail des principales catégories:")
    
    for i, (cat_name, cat_programs) in enumerate(list(wm.programs_db.items())[:5], 1):
        marker = "🟠" if cat_name == "Outils OrdiPlus" else "🔧" if "Réparation" in cat_name else "📁"
        print(f"   {i}. {marker} {cat_name}: {len(cat_programs)} éléments")
    
    assert total_count >= 238, f"❌ Nombre de programmes insuffisant: {total_count} < 238"
    assert categories_count >= 39, f"❌ Nombre de catégories insuffisant: {categories_count} < 39"
    
    print(f"\n✅ TEST RÉUSSI: {total_count} programmes/commandes dans {categories_count} catégories")


def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  🧪 TESTS NiTrite v2.8 - OUTILS ORDIPLUS + RÉPARATION WINDOWS  ".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    tests = [
        test_ordre_categories,
        test_couleur_ordiplus,
        test_commandes_reparation,
        test_detection_commandes,
        test_structure_commande,
        test_compte_total,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ ÉCHEC: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            failed += 1
    
    # Résumé
    print("\n" + "="*70)
    print("RÉSUMÉ DES TESTS")
    print("="*70)
    print(f"\n✅ Tests réussis: {passed}/{len(tests)}")
    print(f"❌ Tests échoués: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS! 🎉")
        print("\n✅ NiTrite v2.8 est prêt:")
        print("   - Outils OrdiPlus en première position ✅")
        print("   - Couleur orange vif ✅")
        print("   - Commandes de réparation Windows ✅")
        print("   - Détection automatique ✅")
        print("   - Structure correcte ✅")
        return 0
    else:
        print("\n⚠️ Certains tests ont échoué")
        return 1


if __name__ == "__main__":
    exit(run_all_tests())
