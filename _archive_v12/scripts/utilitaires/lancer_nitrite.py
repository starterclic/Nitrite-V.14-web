"""
NiTrite v.2 - LANCEMENT FINAL
Interface ultra-visible avec 80+ applications
Installation automatique et silencieuse
"""

import tkinter as tk
import sys
import os
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'  # scripts/utilitaires/ -> racine))

def main():
    """Lance NiTrite v.2 avec interface ultra-visible"""
    
    print("=" * 60)
    print("🚀 NITRITE v.2 - INSTALLATEUR AUTOMATIQUE")
    print("=" * 60)
    print("✨ Interface ultra-visible avec 80+ applications")
    print("🔄 Installation automatique et silencieuse")
    print("🚫 Rejet automatique des offres publicitaires")
    print("=" * 60)
    
    try:
        # Import des modules
        from config_manager import ConfigManager
        from installer_manager import InstallerManager
        from gui_manager_maxvisibility import NiTriteGUIMaxVisibility
        
        # Créer la fenêtre principale
        root = tk.Tk()
        root.title("🎯 NiTrite v.2 - Installateur Automatique Ultra-Visible")
        
        # MAXIMISER la fenêtre pour visibilité maximale
        root.state('zoomed')
        root.configure(bg='#ffffff')
        
        # Initialiser les gestionnaires
        print("🔧 Initialisation des gestionnaires...")
        config_manager = ConfigManager()
        
        # Charger la base de données massive
        massive_db_path = Path(__file__).parent.parent / 'data'  # scripts/utilitaires/ -> racine / 'programs_massive.json'
        if massive_db_path.exists():
            print("📂 Chargement de 80+ applications...")
            config_manager.load_programs_from_file(str(massive_db_path))
            programs_count = config_manager.get_programs_count()
            print(f"✅ {programs_count} applications chargées")
        else:
            print("⚠️ Utilisation de la configuration par défaut")
        
        installer_manager = InstallerManager(config_manager)
        
        # Créer l'interface ultra-visible
        print("🎨 Création de l'interface ultra-visible...")
        gui = NiTriteGUIMaxVisibility(root, installer_manager, config_manager)
        
        print("🎯 Interface prête ! Fenêtre maximisée pour visibilité optimale")
        print("📱 Utilisez les boutons de sélection rapide pour choisir vos programmes")
        print("🔄 L'installation sera entièrement automatique")
        print("=" * 60)
        
        # Message de bienvenue dans l'interface
        welcome_text = f"""
🎉 BIENVENUE DANS NITRITE v.2 !

✨ {config_manager.get_programs_count()} APPLICATIONS DISPONIBLES
🎯 INTERFACE ULTRA-VISIBLE ACTIVÉE
🔄 INSTALLATION AUTOMATIQUE
🚫 REJET AUTOMATIQUE DES PUBLICITÉS

👆 UTILISEZ LES BOUTONS CI-DESSUS POUR SÉLECTIONNER VOS PROGRAMMES
⚡ SÉLECTION RAPIDE DISPONIBLE PAR CATÉGORIE
🚀 CLIQUEZ SUR 'INSTALLER' QUAND VOUS ÊTES PRÊT
        """
        
        # Démarrer l'interface
        root.mainloop()
        
        print("✅ Application fermée normalement")
        
    except ImportError as e:
        print(f"❌ ERREUR : Module manquant : {e}")
        print("💡 Assurez-vous que tous les fichiers sont présents")
        input("Appuyez sur Entrée pour fermer...")
        
    except Exception as e:
        print(f"❌ ERREUR FATALE : {e}")
        print("📝 Consultez les logs pour plus de détails")
        input("Appuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()