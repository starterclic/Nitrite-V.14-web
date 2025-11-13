#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des chemins en mode portable
Garantit que TOUS les fichiers sont stockés à côté de l'exe
RIEN dans AppData, RIEN dans le profil utilisateur
"""

import os
import sys
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def get_executable_dir() -> Path:
    """
    Obtenir le répertoire de l'exécutable

    En mode PyInstaller onefile :
    - sys.executable pointe vers le .exe
    - sys._MEIPASS existe et pointe vers le dossier temp

    En mode script Python :
    - __file__ pointe vers le script

    Returns:
        Path: Chemin absolu du dossier contenant l'exe ou le script
    """
    if getattr(sys, 'frozen', False):
        # Mode PyInstaller (exe compilé)
        # sys.executable = chemin vers l'exe
        exe_path = Path(sys.executable)
        exe_dir = exe_path.parent
        logger.debug(f"Mode PyInstaller détecté - Exe: {exe_path}")
        logger.debug(f"Dossier exe: {exe_dir}")
        return exe_dir
    else:
        # Mode script Python (développement)
        # __file__ = chemin vers ce script
        script_path = Path(__file__).resolve()
        # Remonter de src/ vers la racine
        project_root = script_path.parent.parent
        logger.debug(f"Mode script détecté - Racine: {project_root}")
        return project_root


def get_portable_config_dir() -> Path:
    """
    Obtenir le dossier de configuration portable

    Crée un dossier 'config' à côté de l'exe pour stocker :
    - Profils utilisateur
    - Favoris
    - Historique
    - Préférences

    Returns:
        Path: Chemin absolu du dossier de configuration portable
    """
    exe_dir = get_executable_dir()
    config_dir = exe_dir / 'config'

    # Créer le dossier s'il n'existe pas
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Dossier config portable: {config_dir}")
    except Exception as e:
        logger.warning(f"Impossible de créer {config_dir}: {e}")
        # Fallback: utiliser le dossier temp
        import tempfile
        config_dir = Path(tempfile.gettempdir()) / 'nitrite_config'
        config_dir.mkdir(parents=True, exist_ok=True)
        logger.warning(f"Utilisation du fallback: {config_dir}")

    return config_dir


def get_portable_data_dir() -> Path:
    """
    Obtenir le dossier de données portable

    En mode PyInstaller, les données sont dans sys._MEIPASS
    En mode script, elles sont dans le dossier data/

    Returns:
        Path: Chemin absolu du dossier de données
    """
    if getattr(sys, 'frozen', False):
        # Mode PyInstaller - données dans le bundle
        data_dir = Path(sys._MEIPASS) / 'data'
    else:
        # Mode script - données dans le dossier du projet
        data_dir = get_executable_dir() / 'data'

    logger.debug(f"Dossier data: {data_dir}")
    return data_dir


def get_portable_assets_dir() -> Path:
    """
    Obtenir le dossier assets portable

    Returns:
        Path: Chemin absolu du dossier assets
    """
    if getattr(sys, 'frozen', False):
        # Mode PyInstaller - assets dans le bundle
        assets_dir = Path(sys._MEIPASS) / 'assets'
    else:
        # Mode script - assets dans le dossier du projet
        assets_dir = get_executable_dir() / 'assets'

    logger.debug(f"Dossier assets: {assets_dir}")
    return assets_dir


def get_portable_logs_dir() -> Path:
    """
    Obtenir le dossier de logs portable

    Returns:
        Path: Chemin absolu du dossier de logs
    """
    exe_dir = get_executable_dir()
    logs_dir = exe_dir / 'logs'

    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Dossier logs: {logs_dir}")
    except Exception as e:
        logger.warning(f"Impossible de créer {logs_dir}: {e}")
        # Fallback: pas de logs
        logs_dir = None

    return logs_dir


def is_portable_mode() -> bool:
    """
    Vérifier si on est en mode portable (exe PyInstaller)

    Returns:
        bool: True si mode portable, False si mode script
    """
    return getattr(sys, 'frozen', False)


def get_portable_info() -> dict:
    """
    Obtenir les informations sur le mode portable

    Returns:
        dict: Dictionnaire avec les infos de configuration
    """
    info = {
        'mode': 'portable' if is_portable_mode() else 'script',
        'executable': sys.executable,
        'exe_dir': str(get_executable_dir()),
        'config_dir': str(get_portable_config_dir()),
        'data_dir': str(get_portable_data_dir()),
        'assets_dir': str(get_portable_assets_dir()),
        'logs_dir': str(get_portable_logs_dir()) if get_portable_logs_dir() else None,
    }

    if is_portable_mode():
        info['temp_dir'] = getattr(sys, '_MEIPASS', None)

    return info


# Fonction helper pour debug
def print_portable_info():
    """Afficher les informations de configuration portable"""
    print("\n" + "="*60)
    print("Configuration Mode Portable - NiTriTe V13")
    print("="*60)

    info = get_portable_info()
    for key, value in info.items():
        print(f"{key:15s}: {value}")

    print("="*60 + "\n")


# Test du module
if __name__ == "__main__":
    # Configurer le logging pour le test
    logging.basicConfig(level=logging.DEBUG)

    print_portable_info()

    # Vérifier que les dossiers existent
    print("\nVérification des dossiers:")
    print(f"  Config existe : {get_portable_config_dir().exists()}")
    print(f"  Data existe   : {get_portable_data_dir().exists()}")
    print(f"  Assets existe : {get_portable_assets_dir().exists()}")

    # Test d'écriture dans config
    test_file = get_portable_config_dir() / 'test.txt'
    try:
        test_file.write_text("Test mode portable", encoding='utf-8')
        print(f"\n✓ Écriture test OK: {test_file}")
        test_file.unlink()  # Supprimer le fichier de test
    except Exception as e:
        print(f"\n✗ Écriture test ÉCHEC: {e}")
