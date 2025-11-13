"""
Script simplifié pour créer l'application portable NiTrite v.2 Ordi Plus
Lance le build depuis la racine du projet
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Lance le script de build"""
    
    print("🚀 Lancement du générateur d'exécutable NiTrite Ordi Plus")
    print("=" * 60)
    
    # Chemin du script de build
    build_script = Path(__file__).parent / 'scripts' / 'build_executable.py'
    
    if not build_script.exists():
        print(f"❌ Script de build non trouvé: {build_script}")
        return 1
    
    # Lancer le script de build
    try:
        result = subprocess.run([sys.executable, str(build_script)], check=False)
        return result.returncode
    except Exception as e:
        print(f"❌ Erreur lors du lancement du build: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
