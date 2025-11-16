#!/usr/bin/env python3
"""
NiTriTe V.13 - Lanceur Web Portable
Lance le serveur Flask et ouvre automatiquement le navigateur
"""

import os
import sys
import time
import webbrowser
import threading
import logging
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_resource_path(relative_path):
    """Obtenir le chemin absolu vers une ressource (compatible PyInstaller)"""
    try:
        # PyInstaller crée un dossier temp et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def open_browser():
    """Ouvre le navigateur après un délai"""
    time.sleep(2)  # Attendre que le serveur démarre
    logger.info("🌐 Ouverture du navigateur...")
    webbrowser.open('http://localhost:5000')

def main():
    """Point d'entrée principal"""
    print("=" * 70)
    print("   🚀 NiTriTe V.13 - Version Web Portable")
    print("=" * 70)
    print()
    print("📦 Initialisation...")

    # Vérifier que les dossiers nécessaires existent
    web_dir = get_resource_path('web')
    if not os.path.exists(web_dir):
        print(f"❌ Erreur: Le dossier 'web' n'existe pas: {web_dir}")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

    print(f"✅ Dossier web trouvé: {web_dir}")

    # Importer Flask et démarrer le serveur
    try:
        from flask import Flask, send_from_directory
        from flask_cors import CORS
        import platform

        logger.info("✅ Flask importé avec succès")

        # Initialiser l'application Flask
        app = Flask(__name__, static_folder=web_dir, static_url_path='')
        CORS(app)

        @app.route('/')
        def index():
            """Servir la page principale"""
            return send_from_directory(web_dir, 'index.html')

        # Importer les routes du backend
        print("📡 Chargement du backend API...")

        # Changer de répertoire vers le dossier de base pour les imports
        original_dir = os.getcwd()
        if hasattr(sys, '_MEIPASS'):
            os.chdir(sys._MEIPASS)

        try:
            # Importer et enregistrer toutes les routes
            import web_backend

            # Copier toutes les routes du web_backend vers notre app
            for rule in web_backend.app.url_map.iter_rules():
                if rule.endpoint != 'static':
                    try:
                        view_func = web_backend.app.view_functions[rule.endpoint]
                        app.add_url_rule(
                            rule.rule,
                            endpoint=rule.endpoint,
                            view_func=view_func,
                            methods=rule.methods
                        )
                    except Exception as e:
                        logger.debug(f"Impossible d'ajouter la route {rule.endpoint}: {e}")

            logger.info("✅ Routes API chargées")

        except Exception as e:
            logger.warning(f"⚠️  Backend API non disponible: {e}")
            logger.info("ℹ️  L'application fonctionnera en mode frontend uniquement")

        finally:
            os.chdir(original_dir)

        print()
        print("=" * 70)
        print("   ✅ Serveur prêt !")
        print("=" * 70)
        print()
        print("🌐 URL: http://localhost:5000")
        print()
        print("📝 Le navigateur va s'ouvrir automatiquement...")
        print("⚠️  Pour arrêter le serveur: Fermez cette fenêtre")
        print()
        print("=" * 70)

        # Ouvrir le navigateur dans un thread séparé
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Démarrer le serveur Flask
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False
        )

    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("\nDépendances manquantes. Installez-les avec:")
        print("pip install -r requirements.txt")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        logger.exception("Erreur détaillée:")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du serveur...")
        print("Au revoir ! 👋")
        sys.exit(0)
