"""
Version améliorée de NiTrite v.2 avec gestion des conflits
Gère les interférences avec WinGet et autres installateurs
"""

import sys
import os
import subprocess
import time
import psutil
from pathlib import Path

def check_running_installers():
    """Vérifie si d'autres installateurs sont en cours"""
    installer_processes = ['winget', 'chocolatey', 'ninite', 'msiexec', 'setup', 'installer']
    
    running_installers = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = proc.info['name'].lower()
            for installer in installer_processes:
                if installer in proc_name:
                    running_installers.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return running_installers

def kill_conflicting_processes():
    """Arrête les processus qui peuvent causer des conflits"""
    print("🔧 Vérification des processus conflictuels...")
    
    conflicts = check_running_installers()
    if conflicts:
        print("⚠️  Processus d'installation détectés:")
        for proc in conflicts:
            print(f"  - {proc['name']} (PID: {proc['pid']})")
        
        response = input("Voulez-vous arrêter ces processus ? (o/n): ")
        if response.lower() == 'o':
            for proc in conflicts:
                try:
                    p = psutil.Process(proc['pid'])
                    p.terminate()
                    print(f"  ✅ Processus {proc['name']} arrêté")
                except:
                    print(f"  ❌ Impossible d'arrêter {proc['name']}")
            
            # Attendre un peu
            time.sleep(2)
    else:
        print("✅ Aucun processus conflictuel détecté")

def disable_winget_interference():
    """Désactive temporairement les interférences de WinGet"""
    print("🔧 Gestion des interférences WinGet...")
    
    try:
        # Vérifier si WinGet est en cours
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq winget.exe'], 
                              capture_output=True, text=True)
        
        if 'winget.exe' in result.stdout:
            print("⚠️  WinGet détecté en cours d'exécution")
            print("  Recommandation: Attendez la fin de WinGet avant de continuer")
            input("  Appuyez sur Entrée quand WinGet est terminé...")
        else:
            print("✅ WinGet non actif")
            
    except Exception as e:
        print(f"ℹ️  Impossible de vérifier WinGet: {e}")

def setup_safe_environment():
    """Configure un environnement sûr pour l'installation"""
    print("🛡️  Configuration de l'environnement sécurisé...")
    
    # Variables d'environnement pour éviter les conflits
    os.environ['WINGET_DISABLE_INTERACTIVITY'] = '1'
    os.environ['NITRITE_SAFE_MODE'] = '1'
    
    # Priorité du processus
    try:
        import psutil
        current_process = psutil.Process()
        current_process.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
        print("✅ Priorité du processus augmentée")
    except:
        print("ℹ️  Impossible de modifier la priorité")

def main():
    """Lanceur sécurisé pour NiTrite v.2"""
    print("🚀 NiTrite v.2 - Lanceur sécurisé")
    print("="*50)
    
    # Vérifications préliminaires
    kill_conflicting_processes()
    disable_winget_interference()
    setup_safe_environment()
    
    print("\n✅ Environment préparé, lancement de NiTrite v.2...")
    time.sleep(1)
    
    # Lancer l'application principale
    try:
        current_dir = Path(__file__).parent.parent  # scripts/utilitaires/ -> racine
        os.chdir(current_dir)
        
        # Importer et lancer l'application
        sys.path.insert(0, str(current_dir))
        
        # Import de l'application principale
        exec(open('nitrite_installer.py').read())
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()