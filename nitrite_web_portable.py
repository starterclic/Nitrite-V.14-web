#!/usr/bin/env python3
"""
NiTriTe V.13 - Lanceur Web Portable
Lance le serveur Flask et ouvre automatiquement le navigateur
Compatible PyInstaller
"""

import os
import sys
import time
import webbrowser
import threading
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_base_path():
    """Obtenir le chemin de base (compatible PyInstaller)"""
    if getattr(sys, 'frozen', False):
        # Mode PyInstaller
        return sys._MEIPASS
    else:
        # Mode développement
        return os.path.abspath(".")

def open_browser():
    """Ouvre le navigateur après un délai"""
    time.sleep(3)  # Attendre que le serveur démarre
    logger.info("🌐 Ouverture du navigateur...")
    try:
        webbrowser.open('http://127.0.0.1:5000')
    except Exception as e:
        logger.warning(f"Impossible d'ouvrir le navigateur automatiquement: {e}")
        print("\n⚠️  Ouvrez manuellement: http://127.0.0.1:5000")

def main():
    """Point d'entrée principal"""
    print("=" * 70)
    print("   🚀 NiTriTe V.13 - Version Web Portable")
    print("=" * 70)
    print()

    # Changer le répertoire de travail
    base_path = get_base_path()
    os.chdir(base_path)

    logger.info(f"📁 Répertoire de base: {base_path}")

    # Ajouter src au path
    src_path = os.path.join(base_path, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Vérifier que web_backend.py existe
    backend_file = os.path.join(base_path, 'web_backend.py')
    if not os.path.exists(backend_file):
        logger.error(f"❌ Fichier manquant: {backend_file}")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

    logger.info("✅ Fichier web_backend.py trouvé")

    # Vérifier le dossier web
    web_dir = os.path.join(base_path, 'web')
    if not os.path.exists(web_dir):
        logger.error(f"❌ Dossier web manquant: {web_dir}")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

    logger.info(f"✅ Dossier web trouvé: {web_dir}")

    print()
    print("📡 Démarrage du serveur...")
    print()

    try:
        # Importer et lancer le backend
        import web_backend

        print("=" * 70)
        print("   ✅ Serveur prêt !")
        print("=" * 70)
        print()
        print("🌐 URL: http://127.0.0.1:5000")
        print()
        print("📝 Le navigateur va s'ouvrir automatiquement...")
        print("⚠️  Pour arrêter: Fermez cette fenêtre ou Ctrl+C")
        print()
        print("=" * 70)
        print()

        # Ouvrir le navigateur dans un thread séparé
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()

        # Démarrer le serveur (bloquant)
        web_backend.main()

    except ImportError as e:
        logger.error(f"❌ Erreur d'import: {e}")
        logger.error("\nDépendances manquantes. Assurez-vous que:")
        logger.error("- Flask est installé")
        logger.error("- flask-cors est installé")
        logger.error("- Tous les modules src/ sont présents")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du serveur...")
        print("Au revoir ! 👋")
        sys.exit(0)
