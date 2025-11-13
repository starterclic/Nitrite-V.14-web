
"""
Script d'isolation pour éviter les conflits entre NiTrite 1.0 et NiTrite v.2
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_running_nitrite_processes():
    """Vérifie les processus NiTrite en cours"""
    print("🔍 Vérification des processus NiTrite...")
    
    try:
        # Vérifier PowerShell avec NiTrite
        result = subprocess.run([
            'powershell', '-Command', 
            'Get-Process | Where-Object {$_.ProcessName -like "*powershell*" -and $_.MainWindowTitle -like "*NiTrite*"}'
        ], capture_output=True, text=True, timeout=5)
        
        if result.stdout.strip():
            print("⚠️  NiTrite 1.0 (PowerShell) détecté en cours d'exécution")
            return True
        else:
            print("✅ Aucun processus NiTrite 1.0 détecté")
            return False
            
    except Exception as e:
        print(f"ℹ️  Vérification des processus: {e}")
        return False

def stop_nitrite_1_processes():
    """Arrête les processus NiTrite 1.0"""
    print("🛑 Arrêt des processus NiTrite 1.0...")
    
    try:
        subprocess.run([
            'powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -like "*NiTrite*"} | Stop-Process -Force'
        ], capture_output=True, text=True, timeout=10)
        
        print("✅ Processus NiTrite 1.0 arrêtés")
        time.sleep(2)
        
    except Exception as e:
        print(f"⚠️  Arrêt partiel des processus: {e}")

def set_nitrite_v2_environment():
    """Configure l'environnement pour NiTrite v.2"""
    print("⚙️  Configuration de l'environnement NiTrite v.2...")
    
    # Variables d'environnement pour éviter les conflits
    os.environ['NITRITE_VERSION'] = '2.0'
    os.environ['NITRITE_MODE'] = 'PYTHON'
    os.environ['POWERSHELL_NITRITE_DISABLED'] = '1'
    
    print("✅ Environnement configuré pour NiTrite v.2")

def launch_nitrite_v2():
    """Lance NiTrite v.2 en mode isolé"""
    print("🚀 Lancement de NiTrite v.2...")
    
    try:
        current_dir = Path(__file__).parent.parent  # scripts/utilitaires/ -> racine
        nitrite_script = current_dir / 'nitrite_installer.py'
        
        if nitrite_script.exists():
            subprocess.run([sys.executable, str(nitrite_script)])
        else:
            print("❌ Script NiTrite v.2 non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

def main():
    """Fonction principale d'isolation"""
    print("🔧 NiTrite - Script d'isolation des versions")
    print("=" * 50)
    
    # Vérifier et arrêter NiTrite 1.0 si nécessaire
    if check_running_nitrite_processes():
        response = input("Voulez-vous arrêter NiTrite 1.0 pour lancer NiTrite v.2 ? (o/n): ")
        if response.lower() == 'o':
            stop_nitrite_1_processes()
    
    # Configurer l'environnement
    set_nitrite_v2_environment()
    
    # Lancer NiTrite v.2
    launch_nitrite_v2()

if __name__ == "__main__":
    main()
