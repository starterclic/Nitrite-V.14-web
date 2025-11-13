"""
Script d'installation automatique des dépendances pour NiTrite v.2
"""

import subprocess
import sys
import os

def install_dependencies():
    """Installe les dépendances requises"""
    
    dependencies = [
        'requests>=2.28.0',
        'Pillow>=9.0.0'
    ]
    
    # Sur Windows, ajouter pywin32
    if os.name == 'nt':
        dependencies.append('pywin32>=304')
    
    print("🔧 Installation des dépendances pour NiTrite v.2...")
    print("=" * 50)
    
    for dep in dependencies:
        print(f"📦 Installation de {dep}...")
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', dep
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"  ✅ {dep} installé avec succès")
            else:
                print(f"  ❌ Erreur lors de l'installation de {dep}")
                print(f"     Erreur: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"  ⏰ Timeout lors de l'installation de {dep}")
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    print("\n✅ Installation terminée!")
    print("🚀 Vous pouvez maintenant lancer NiTrite v.2")

if __name__ == "__main__":
    install_dependencies()
    input("\nAppuyez sur Entrée pour continuer...")