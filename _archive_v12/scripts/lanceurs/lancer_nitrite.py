#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur NiTrite v3.0 - Avec Gestion Automatique des Dépendances
===============================================================

Ce script vérifie et installe automatiquement toutes les dépendances
requises avant de lancer l'application.

Usage:
    python lancer_nitrite.py [--no-check]

Options:
    --no-check    Sauter la vérification des dépendances
"""

import sys
import subprocess
import os
from pathlib import Path
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DependencyManager:
    """Gestionnaire de dépendances pour NiTrite"""

    REQUIRED_PACKAGES = [
        'requests>=2.31.0',
        'urllib3>=2.0.0',
        'certifi>=2023.0.0',
        'packaging>=23.0',
        'Pillow>=10.0.0',
        'tqdm>=4.66.0',
        'colorama>=0.4.6',
        'psutil>=5.9.0'
    ]

    WINDOWS_PACKAGES = [
        'pywin32>=306'
    ]

    def __init__(self):
        self.python_exe = sys.executable
        self.project_root = Path(__file__).parent.parent.parent  # scripts/lanceurs/ -> racine

    def check_python_version(self) -> bool:
        """Vérifie que la version de Python est compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            logger.error(f"❌ Python 3.8+ requis (version actuelle: {version.major}.{version.minor})")
            return False
        logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True

    def check_package_installed(self, package_name: str) -> bool:
        """Vérifie si un package est installé"""
        try:
            # Extraire le nom du package (sans version)
            pkg_name = package_name.split('>=')[0].split('==')[0].strip()
            __import__(pkg_name.lower().replace('-', '_'))
            return True
        except ImportError:
            return False

    def install_package(self, package: str) -> bool:
        """Installe un package via pip"""
        try:
            logger.info(f"📦 Installation de {package}...")
            result = subprocess.run(
                [self.python_exe, '-m', 'pip', 'install', package],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                logger.info(f"✅ {package} installé avec succès")
                return True
            else:
                logger.error(f"❌ Échec de l'installation de {package}")
                logger.error(result.stderr)
                return False

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'installation de {package}: {e}")
            return False

    def check_and_install_dependencies(self) -> bool:
        """Vérifie et installe toutes les dépendances"""
        logger.info("="*60)
        logger.info("🔍 Vérification des dépendances...")
        logger.info("="*60)

        packages_to_install = []

        # Vérifier les packages requis
        for package in self.REQUIRED_PACKAGES:
            pkg_name = package.split('>=')[0].strip()
            if not self.check_package_installed(pkg_name):
                packages_to_install.append(package)

        # Vérifier les packages Windows
        if sys.platform == 'win32':
            for package in self.WINDOWS_PACKAGES:
                pkg_name = package.split('>=')[0].strip()
                if not self.check_package_installed(pkg_name):
                    packages_to_install.append(package)

        if not packages_to_install:
            logger.info("✅ Toutes les dépendances sont installées")
            return True

        logger.info(f"📦 {len(packages_to_install)} package(s) à installer")

        # Mettre à jour pip
        logger.info("🔄 Mise à jour de pip...")
        subprocess.run(
            [self.python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'],
            capture_output=True,
            timeout=120
        )

        # Installer les packages manquants
        all_success = True
        for package in packages_to_install:
            if not self.install_package(package):
                all_success = False

        return all_success

    def verify_data_files(self) -> bool:
        """Vérifie que les fichiers de données existent"""
        logger.info("🔍 Vérification des fichiers de données...")

        required_files = [
            'data/config.json',
            'data/programs.json',
            'src/gui_manager.py',
            'src/installer_manager.py',
            'src/winget_manager.py'
        ]

        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                logger.error(f"❌ Fichier manquant: {file_path}")

        if missing_files:
            logger.error(f"❌ {len(missing_files)} fichier(s) manquant(s)")
            return False

        logger.info("✅ Tous les fichiers de données sont présents")
        return True


def launch_nitrite():
    """Lance l'application NiTrite"""
    try:
        logger.info("="*60)
        logger.info("🚀 Lancement de NiTrite v3.0")
        logger.info("="*60)

        # Importer et lancer
        project_root = Path(__file__).parent.parent.parent  # scripts/lanceurs/ -> racine
        sys.path.insert(0, str(project_root))

        # Import du module principal
        import nitrite_complet

        # Lancer l'application
        nitrite_complet.main()

    except KeyboardInterrupt:
        logger.info("\n⚠️ Application interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erreur lors du lancement: {e}", exc_info=True)
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)


def main():
    """Fonction principale"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🚀 NiTrite OrdiPlus v3.0 - Lanceur                ║
║                                                              ║
║     Installation automatique de 304 programmes Windows     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # Vérifier si on doit skip la vérification des dépendances
    skip_check = '--no-check' in sys.argv

    # Créer le gestionnaire de dépendances
    dep_manager = DependencyManager()

    # Vérifier la version de Python
    if not dep_manager.check_python_version():
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

    # Vérifier les fichiers de données
    if not dep_manager.verify_data_files():
        logger.error("❌ Fichiers de données manquants")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

    # Vérifier et installer les dépendances
    if not skip_check:
        if not dep_manager.check_and_install_dependencies():
            logger.error("❌ Échec de l'installation des dépendances")
            logger.info("\nVous pouvez:")
            logger.info("  1. Réessayer: python lancer_nitrite.py")
            logger.info("  2. Installer manuellement: pip install -r requirements.txt")
            input("\nAppuyez sur Entrée pour quitter...")
            sys.exit(1)
    else:
        logger.info("⏭️ Vérification des dépendances ignorée")

    # Lancer l'application
    launch_nitrite()


if __name__ == "__main__":
    main()
