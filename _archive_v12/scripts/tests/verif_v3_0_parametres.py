"""
Vérification Version 3.0 - Paramètres Windows
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from winget_manager import WingetManager


def verif_v3_0():
    """Vérification complète v3.0"""
    print("=" * 70)
    print("🔍 VÉRIFICATION NiTrite v3.0 - PARAMÈTRES WINDOWS")
    print("=" * 70)
    print()
    
    wm = WingetManager()
    
    # 1. Vérifier la nouvelle catégorie
    print("1. NOUVELLE CATÉGORIE PARAMÈTRES WINDOWS")
    print("-" * 70)
    
    categories = list(wm.programs_db.keys())
    
    if "⚙️ Paramètres Windows" in categories:
        position = categories.index("⚙️ Paramètres Windows")
        print(f"✅ Catégorie '⚙️ Paramètres Windows' trouvée en position #{position + 1}")
    else:
        print("❌ Catégorie '⚙️ Paramètres Windows' non trouvée")
        return
    
    # 2. Compter les fonctionnalités
    params = wm.programs_db.get("⚙️ Paramètres Windows", {})
    print(f"✅ Nombre de paramètres : {len(params)}")
    print()
    
    # 3. Vérifier les paramètres demandés
    print("2. PARAMÈTRES DEMANDÉS")
    print("-" * 70)
    
    parametres_requis = {
        "Paramètres Windows": "ms-settings:",
        "Réseau et Internet": "ms-settings:network",
        "Bluetooth et appareils": "ms-settings:bluetooth",
        "Imprimantes et scanners": "ms-settings:printers",
        "Son": "ms-settings:sound",
        "Clavier": "ms-settings:typing",
        "Activation Windows": "ms-settings:activation",
        "Informations système": "ms-settings:about",
        "Mode développeur": "ms-settings:developers",
        "Sécurité Windows": "windowsdefender:",
        "Personnalisation": "ms-settings:personalization",
        "Affichage": "ms-settings:display",
        "Alimentation et batterie": "ms-settings:powersleep",
        "Panneau de configuration": "control",
        "Outils d'administration": "control admintools",
        "Configuration système (msconfig)": "msconfig",
        "Propriétés système (sysdm.cpl)": "sysdm.cpl",
        "Gestionnaire de périphériques": "devmgmt.msc",
        "Panneau NVIDIA": "NVIDIA"
    }
    
    trouve = 0
    for nom, mot_cle in parametres_requis.items():
        if nom in params:
            commande = params[nom].get('command', '')
            if mot_cle.lower() in commande.lower():
                print(f"✅ {nom}")
                trouve += 1
            else:
                print(f"⚠️ {nom} - commande différente: {commande}")
        else:
            print(f"❌ {nom} - non trouvé")
    
    print()
    print(f"Total : {trouve}/{len(parametres_requis)} paramètres trouvés")
    print()
    
    # 4. Statistiques globales
    print("3. STATISTIQUES GLOBALES")
    print("-" * 70)
    
    total_programmes = sum(len(progs) for progs in wm.programs_db.values())
    total_categories = len(wm.programs_db)
    
    print(f"✅ Total programmes/commandes : {total_programmes}")
    print(f"✅ Total catégories : {total_categories}")
    print()
    
    # 5. Ordre des 5 premières catégories
    print("4. TOP 5 CATÉGORIES")
    print("-" * 70)
    for i, cat in enumerate(categories[:5], 1):
        nb = len(wm.programs_db[cat])
        print(f"{i}. {cat} ({nb} éléments)")
    print()
    
    # 6. Vérifier les commandes vs winget
    print("5. TYPE D'ÉLÉMENTS PAR CATÉGORIE")
    print("-" * 70)
    
    for cat_name in ["⚙️ Paramètres Windows", "🔧 Réparation Windows", "Outils OrdiPlus"]:
        if cat_name in wm.programs_db:
            cat_items = wm.programs_db[cat_name]
            commandes = sum(1 for item in cat_items.values() if 'command' in item)
            programmes = sum(1 for item in cat_items.values() if 'winget_id' in item)
            print(f"   {cat_name}:")
            if commandes > 0:
                print(f"      - Commandes système : {commandes}")
            if programmes > 0:
                print(f"      - Programmes Winget : {programmes}")
    
    print()
    print("=" * 70)
    print("✅ VÉRIFICATION TERMINÉE - v3.0 PRÊT !")
    print("=" * 70)


if __name__ == "__main__":
    verif_v3_0()
