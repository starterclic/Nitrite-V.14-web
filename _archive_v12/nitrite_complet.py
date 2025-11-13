"""
Lanceur NiTrite v12 Final - VERSION COMPLÈTE
Affiche TOUS les programmes disponibles (80+)
"""

# --- IMPORTS ---
import warnings
# Supprimer l'avertissement de winshell concernant les séquences d'échappement invalides
warnings.filterwarnings('ignore', category=SyntaxWarning, module='winshell')

import tkinter as tk
from tkinter import messagebox
import webbrowser
import logging
from pathlib import Path
import sys
import os
import tempfile

# --- DÉBUT BLOC CORRECTION CHEMINS ---

def get_app_dir():
    """ Obtient le répertoire de base de l'application (là où est l'exécutable). """
    if getattr(sys, 'frozen', False):
        return Path(os.path.dirname(sys.executable))
    else:
        return Path(__file__).resolve().parent

def get_bundle_dir():
    """ Obtient le répertoire des ressources (peut être _MEIPASS ou le dossier source). """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).resolve().parent

APP_DIR = get_app_dir()
BUNDLE_DIR = get_bundle_dir()
DATA_PATH = BUNDLE_DIR / "data"
ASSETS_PATH = BUNDLE_DIR / "assets"
LOGS_DIR = APP_DIR / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# --- FIN BLOC CORRECTION CHEMINS ---

# Configuration du logging avec rotation
from logging.handlers import RotatingFileHandler

# Handler rotatif: 10 MB max par fichier, 5 fichiers de backup
log_file = LOGS_DIR / 'nitrite.log'
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Handler console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configuration du logger racine
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)

# Ajout du dossier 'src' au path pour les imports
sys.path.insert(0, str(BUNDLE_DIR / 'src'))
sys.path.insert(0, str(BUNDLE_DIR))

# Imports des modules du projet
try:
    from src.winget_installer import WingetInstaller
    from src.installer_manager import InstallerManager
    from src.gui_manager import NiTriteGUIComplet
    from src.elevation_helper import auto_elevate_at_startup
except ImportError:
    try:
        from winget_installer import WingetInstaller
        from installer_manager import InstallerManager
        from gui_manager import NiTriteGUIComplet
        from elevation_helper import auto_elevate_at_startup
    except ImportError as e:
        logger.critical(f"❌ Impossible d'importer les modules nécessaires: {e}")
        messagebox.showerror("Erreur d'Importation", f"Impossible de charger un module essentiel: {e}")
        sys.exit(1)


def main():
    """Fonction principale"""
    logger.info(f"📁 Dossier de l'application (écriture): {APP_DIR}")
    logger.info(f"📦 Dossier des ressources (lecture): {BUNDLE_DIR}")
    logger.info(f"💾 Chemin des données: {DATA_PATH}")
    logger.info(f"🎨 Chemin des assets: {ASSETS_PATH}")
    logger.info(f"📝 Chemin des logs: {LOGS_DIR}")
    logger.info(f"🔍 Mode 'frozen' (exe): {getattr(sys, 'frozen', False)}")
    logger.info("="*60)
    logger.info("🚀 Démarrage de NiTrite v.2 - Version Complète")
    logger.info("="*60)

    try:
        # Initialisation de Winget
        winget = WingetInstaller()
        winget.install_winget_if_needed(callback=logger.info)

        # Charger la configuration en utilisant le chemin corrigé
        installer_manager = InstallerManager(
            config_path=DATA_PATH / "programs.json", 
            log_callback=logger.info,
            app_dir=APP_DIR  # Passer le répertoire de l'application pour la base de données
        )
        
        # Créer la fenêtre Tkinter
        root = tk.Tk()
        
        # Créer l'interface graphique complète
        gui = NiTriteGUIComplet(root, installer_manager=installer_manager)
        
        logger.info("✅ Interface graphique complète initialisée")
        logger.info(f"📊 {len(installer_manager.get_programs_db())} programmes disponibles")
        
        # Lancer l'application
        root.mainloop()

    except Exception as e:
        logger.critical(f"❌ Erreur critique inattendue: {e}", exc_info=True)
        messagebox.showerror("Erreur Critique", f"Une erreur fatale est survenue:\n\n{e}\n\nConsultez le fichier de log pour plus de détails.")
    finally:
        logging.shutdown()


if __name__ == "__main__":
    # Auto-élévation des privilèges admin au démarrage
    # L'UAC sera demandé UNE SEULE FOIS au lancement de l'application
    auto_elevate_at_startup()

    # Lancer l'application
    main()
