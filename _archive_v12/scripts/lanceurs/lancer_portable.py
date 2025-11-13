#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur NiTrite v3.0 - Version Portable
========================================

Ce script lance NiTrite en mode portable sans vérifier les dépendances.
À utiliser avec la version compilée (.exe) ou dans un environnement
où toutes les dépendances sont déjà installées.

Usage:
    python lancer_portable.py
"""

import sys
import os
from pathlib import Path
import logging

# Configuration du logging simplifié
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PortableLauncher:
    """Lanceur portable pour NiTrite"""

    def __init__(self):
        # Le fichier est dans scripts/lanceurs/, donc remonter de 2 niveaux
        self.project_root = Path(__file__).parent.parent.parent
        self.is_frozen = getattr(sys, 'frozen', False)

    def setup_environment(self):
        """Configure l'environnement d'exécution"""
        # Ajouter le répertoire du projet au path Python
        sys.path.insert(0, str(self.project_root))
        sys.path.insert(0, str(self.project_root / 'src'))

        # Définir les variables d'environnement
        os.environ['NITRITE_PORTABLE'] = '1'
        os.environ['PYTHONIOENCODING'] = 'utf-8'

        logger.info("✅ Environnement configuré")

    def check_critical_files(self) -> bool:
        """Vérifie les fichiers critiques minimaux"""
        critical_files = [
            'nitrite_complet.py',
            'data/programs.json'
        ]

        missing = []
        for file in critical_files:
            if not (self.project_root / file).exists():
                missing.append(file)

        if missing:
            logger.error(f"❌ Fichiers critiques manquants: {', '.join(missing)}")
            return False

        return True

    def launch(self):
        """Lance l'application"""
        try:
            logger.info("🚀 Démarrage de NiTrite v3.0 (Mode Portable)")

            # Configuration de l'environnement
            self.setup_environment()

            # Vérification minimale
            if not self.check_critical_files():
                raise FileNotFoundError("Fichiers critiques manquants")

            # Import et lancement
            import nitrite_complet
            nitrite_complet.main()

        except ImportError as e:
            logger.error(f"❌ Erreur d'import: {e}")
            logger.error("\n⚠️ Des dépendances sont manquantes.")
            logger.error("Utilisez 'lancer_nitrite.py' pour les installer automatiquement.")
            raise
        except Exception as e:
            logger.error(f"❌ Erreur: {e}", exc_info=True)
            raise


def main():
    """Fonction principale"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      🚀 NiTrite OrdiPlus v3.0 - Version Portable            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    launcher = PortableLauncher()

    try:
        launcher.launch()
    except KeyboardInterrupt:
        logger.info("\n⚠️ Application interrompue")
        sys.exit(0)
    except Exception:
        logger.error("\n❌ Échec du lancement")
        logger.info("\n💡 Essayez: python lancer_nitrite.py")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)


if __name__ == "__main__":
    main()
