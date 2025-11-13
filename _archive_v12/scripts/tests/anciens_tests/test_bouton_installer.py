"""
Script de test pour vérifier le fonctionnement du bouton INSTALLER
"""

import tkinter as tk
from pathlib import Path
import sys
import logging

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'  # scripts/tests/anciens_tests/ -> racine))

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Test du système"""
    logger.info("=" * 60)
    logger.info("🧪 TEST DU BOUTON INSTALLER")
    logger.info("=" * 60)
    
    try:
        # Importer les managers
        from config_manager import ConfigManager
        from installer_manager import InstallerManager
        from gui_manager_complet import create_gui_manager
        
        logger.info("✅ Modules importés avec succès")
        
        # Créer la fenêtre principale
        root = tk.Tk()
        
        # Créer les managers
        config_manager = ConfigManager()
        logger.info(f"✅ ConfigManager créé")
        
        installer_manager = InstallerManager(config_manager)
        logger.info(f"✅ InstallerManager créé")
        
        # Créer l'interface graphique
        gui = create_gui_manager(root, installer_manager, config_manager)
        logger.info(f"✅ Interface créée avec {len(gui.program_vars)} programmes")
        
        # Vérifier l'état du bouton
        logger.info(f"📊 État initial du bouton: {gui.install_button['state']}")
        logger.info(f"📊 Commande du bouton: {gui.install_button['command']}")
        
        # Tester la sélection d'un programme
        if gui.program_vars:
            first_prog = list(gui.program_vars.keys())[0]
            logger.info(f"🎯 Test de sélection: {first_prog}")
            gui.program_vars[first_prog].set(True)
            gui.update_selection_count()
            logger.info(f"📊 État après sélection: {gui.install_button['state']}")
        
        # Lancer l'application
        root.mainloop()
        
    except Exception as e:
        logger.error(f"❌ Erreur: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == "__main__":
    main()
