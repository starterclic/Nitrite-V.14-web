"""
Script de test pour vérifier l'installation via Winget
Teste 3 programmes légers pour validation
"""

import logging
from src.winget_manager import WingetManager

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_winget_installation():
    """Teste l'installation de programmes via Winget"""
    
    print("\n" + "="*70)
    print("🧪 TEST D'INSTALLATION WINGET")
    print("="*70)
    
    # Créer le gestionnaire
    wm = WingetManager()
    
    if not wm.winget_available:
        print("\n❌ Winget n'est pas disponible sur ce système")
        print("📥 Installez 'App Installer' depuis le Microsoft Store")
        return False
    
    print(f"\n✅ Winget disponible")
    print(f"📊 {wm.get_program_count()} programmes dans la base de données")
    
    # Programmes de test (légers et rapides)
    test_programs = [
        "7-Zip",           # ~1.5 MB, très rapide
        "Notepad++",       # ~4 MB, rapide
        "Sumatra PDF",     # ~5 MB, rapide
    ]
    
    print(f"\n📦 Programmes de test sélectionnés :")
    for prog in test_programs:
        print(f"   • {prog}")
    
    print("\n⚠️  NOTE: Ces programmes seront RÉELLEMENT installés sur votre système")
    response = input("\n❓ Continuer le test ? (o/n) : ").lower()
    
    if response != 'o':
        print("\n❌ Test annulé")
        return False
    
    # Callback de log
    def log_cb(msg):
        print(msg)
        logger.info(msg)
    
    # Callback de progression
    def prog_cb(percent):
        pass  # On affiche juste le log
    
    print("\n" + "="*70)
    print("🚀 DÉBUT DU TEST D'INSTALLATION")
    print("="*70 + "\n")
    
    # Installation
    success_count = 0
    fail_count = 0
    
    for i, program_name in enumerate(test_programs, 1):
        print(f"\n[{i}/{len(test_programs)}] Test de: {program_name}")
        print("-" * 70)
        
        # Trouver le programme
        program_info = None
        for category_programs in wm.programs_db.values():
            if program_name in category_programs:
                program_info = category_programs[program_name]
                break
        
        if not program_info:
            print(f"❌ Programme '{program_name}' non trouvé dans la base")
            fail_count += 1
            continue
        
        # Installer
        success = wm.install_program(program_name, program_info, prog_cb, log_cb)
        
        if success:
            print(f"✅ {program_name} installé avec succès !")
            success_count += 1
        else:
            print(f"❌ Échec de l'installation de {program_name}")
            fail_count += 1
        
        print("-" * 70)
    
    # Résultats finaux
    print("\n" + "="*70)
    print("📊 RÉSULTATS DU TEST")
    print("="*70)
    print(f"✅ Réussis: {success_count}/{len(test_programs)}")
    print(f"❌ Échoués: {fail_count}/{len(test_programs)}")
    
    if success_count == len(test_programs):
        print("\n🎉 SUCCÈS TOTAL ! Tous les programmes sont installés correctement")
        print("✅ Winget fonctionne parfaitement avec NiTrite")
        return True
    elif success_count > 0:
        print(f"\n⚠️  SUCCÈS PARTIEL : {success_count}/{len(test_programs)} programmes installés")
        return True
    else:
        print("\n❌ ÉCHEC COMPLET : Aucun programme installé")
        return False


def verify_installations():
    """Vérifie que les programmes sont bien installés"""
    print("\n" + "="*70)
    print("🔍 VÉRIFICATION DES INSTALLATIONS")
    print("="*70)
    
    import subprocess
    
    test_programs = [
        ("7-Zip", "7zip.7zip"),
        ("Notepad++", "Notepad++.Notepad++"),
        ("Sumatra PDF", "SumatraPDF.SumatraPDF"),
    ]
    
    for prog_name, winget_id in test_programs:
        try:
            result = subprocess.run(
                ['winget', 'list', '--id', winget_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if winget_id in result.stdout:
                print(f"✅ {prog_name} : INSTALLÉ")
            else:
                print(f"❌ {prog_name} : NON TROUVÉ")
                
        except Exception as e:
            print(f"⚠️  {prog_name} : Erreur de vérification - {e}")


if __name__ == "__main__":
    try:
        # Test d'installation
        success = test_winget_installation()
        
        if success:
            # Vérification
            print("\n⏳ Vérification des installations...")
            verify_installations()
        
        print("\n" + "="*70)
        print("✅ Test terminé")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
    except Exception as e:
        logger.exception("Erreur pendant le test")
        print(f"\n❌ Erreur : {e}")
