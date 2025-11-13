#!/usr/bin/env python3
"""
NiTriTe V.13 - Web Backend API
Flask server for handling installations and system commands
"""

import os
import sys
import json
import subprocess
import platform
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from installer_manager import InstallerManager
from winget_manager import WingetManager

# Initialize Flask app
app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)  # Enable CORS for web interface

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize managers
installer_manager = InstallerManager()
winget_manager = WingetManager()


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('web', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'version': '13.0',
        'platform': platform.system(),
        'python_version': platform.python_version()
    })


@app.route('/api/applications', methods=['GET'])
def get_applications():
    """Get all applications from database"""
    try:
        programs_file = os.path.join(os.path.dirname(__file__), 'data', 'programs.json')

        if not os.path.exists(programs_file):
            return jsonify({'error': 'Programs database not found'}), 404

        with open(programs_file, 'r', encoding='utf-8') as f:
            programs = json.load(f)

        return jsonify(programs)

    except Exception as e:
        logger.error(f"Error loading applications: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Get system tools data"""
    try:
        from tools_data_complete import TOOLS_DATA

        return jsonify({
            'sections': [
                {
                    'id': 'activation',
                    'icon': '🔧',
                    'title': 'Activation & Téléchargements',
                    'tools': [
                        {'id': 'kms', 'name': 'Activation Windows/Office (KMS)', 'icon': '🔑'},
                        {'id': 'rufus', 'name': 'Rufus (USB Bootable)', 'icon': '💿'},
                        {'id': 'ventoy', 'name': 'Ventoy', 'icon': '📀'},
                        {'id': 'medicat', 'name': 'MediCat USB', 'icon': '🏥'},
                    ]
                },
                {
                    'id': 'repair',
                    'icon': '🔨',
                    'title': 'Réparation Système',
                    'tools': [
                        {'id': 'dism', 'name': 'DISM /RestoreHealth', 'icon': '🛠️'},
                        {'id': 'sfc', 'name': 'SFC /scannow', 'icon': '🔍'},
                        {'id': 'chkdsk', 'name': 'CHKDSK', 'icon': '💾'},
                        {'id': 'mbr', 'name': 'Réparer MBR', 'icon': '⚙️'},
                    ]
                },
                {
                    'id': 'maintenance',
                    'icon': '🧹',
                    'title': 'Maintenance & Nettoyage',
                    'tools': [
                        {'id': 'disk_cleanup', 'name': 'Nettoyage Disque', 'icon': '🗑️'},
                        {'id': 'temp_files', 'name': 'Nettoyer Fichiers Temporaires', 'icon': '📁'},
                        {'id': 'defrag', 'name': 'Défragmentation', 'icon': '📊'},
                        {'id': 'windows_update', 'name': 'Windows Update', 'icon': '🔄'},
                    ]
                },
                {
                    'id': 'diagnostics',
                    'icon': '📊',
                    'title': 'Diagnostics & Informations',
                    'tools': [
                        {'id': 'system_info', 'name': 'Informations Système', 'icon': '💻'},
                        {'id': 'device_manager', 'name': 'Gestionnaire de Périphériques', 'icon': '🔌'},
                        {'id': 'disk_manager', 'name': 'Gestion des Disques', 'icon': '💿'},
                        {'id': 'task_manager', 'name': 'Gestionnaire des Tâches', 'icon': '📈'},
                    ]
                },
                {
                    'id': 'network',
                    'icon': '🌐',
                    'title': 'Réseau & Internet',
                    'tools': [
                        {'id': 'network_reset', 'name': 'Réinitialiser Réseau', 'icon': '🔄'},
                        {'id': 'ipconfig', 'name': 'IP Configuration', 'icon': '🌍'},
                        {'id': 'dns_flush', 'name': 'Vider Cache DNS', 'icon': '🗑️'},
                        {'id': 'network_troubleshoot', 'name': 'Dépannage Réseau', 'icon': '🔧'},
                    ]
                },
                {
                    'id': 'personalization',
                    'icon': '🎨',
                    'title': 'Personnalisation Windows',
                    'tools': [
                        {'id': 'themes', 'name': 'Thèmes Windows', 'icon': '🖼️'},
                        {'id': 'wallpaper', 'name': 'Fond d\'écran', 'icon': '🌄'},
                        {'id': 'colors', 'name': 'Couleurs', 'icon': '🎨'},
                        {'id': 'taskbar', 'name': 'Barre des tâches', 'icon': '📊'},
                    ]
                },
                {
                    'id': 'security',
                    'icon': '🔒',
                    'title': 'Sécurité & Confidentialité',
                    'tools': [
                        {'id': 'defender', 'name': 'Windows Defender', 'icon': '🛡️'},
                        {'id': 'firewall', 'name': 'Pare-feu', 'icon': '🔥'},
                        {'id': 'uac', 'name': 'Contrôle Compte Utilisateur', 'icon': '👤'},
                        {'id': 'privacy', 'name': 'Paramètres Confidentialité', 'icon': '🔐'},
                    ]
                },
                {
                    'id': 'utilities',
                    'icon': '💼',
                    'title': 'Utilitaires Système',
                    'tools': [
                        {'id': 'registry', 'name': 'Éditeur de Registre', 'icon': '📝'},
                        {'id': 'services', 'name': 'Services Windows', 'icon': '⚙️'},
                        {'id': 'startup', 'name': 'Programmes Démarrage', 'icon': '🚀'},
                        {'id': 'env_vars', 'name': 'Variables d\'Environnement', 'icon': '🌍'},
                    ]
                },
            ]
        })

    except Exception as e:
        logger.error(f"Error loading tools: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Get installation profiles"""
    profiles = [
        {
            'id': 'gaming',
            'name': 'Gaming Station',
            'icon': '🎮',
            'description': 'Tout pour les joueurs : launchers, Discord, OBS, utilitaires gaming',
            'apps_count': 25
        },
        {
            'id': 'office',
            'name': 'Bureau Professionnel',
            'icon': '💼',
            'description': 'Suite bureautique complète, outils de productivité et communication',
            'apps_count': 30
        },
        {
            'id': 'dev',
            'name': 'Développeur',
            'icon': '💻',
            'description': 'IDE, Git, Docker, outils de développement et langages de programmation',
            'apps_count': 40
        },
        {
            'id': 'media',
            'name': 'Création Multimédia',
            'icon': '🎨',
            'description': 'Outils photo, vidéo, audio, design graphique et création de contenu',
            'apps_count': 35
        },
        {
            'id': 'student',
            'name': 'Étudiant',
            'icon': '🏫',
            'description': 'Applications éducatives, outils de recherche et productivité étudiante',
            'apps_count': 20
        },
        {
            'id': 'tech',
            'name': 'Maintenance Technique',
            'icon': '🔧',
            'description': 'Utilitaires système, outils de diagnostic et réparation',
            'apps_count': 45
        },
        {
            'id': 'home',
            'name': 'Maison/Famille',
            'icon': '🏠',
            'description': 'Applications familiales, multimédia et usage quotidien',
            'apps_count': 22
        },
        {
            'id': 'express',
            'name': 'Installation Express',
            'icon': '⚡',
            'description': 'Essentiels uniquement : navigateur, PDF, archiveur, antivirus',
            'apps_count': 12
        },
        {
            'id': 'cinema',
            'name': 'Home Cinema',
            'icon': '🎬',
            'description': 'Lecture multimédia, streaming, gestion de bibliothèque média',
            'apps_count': 15
        },
        {
            'id': 'remote',
            'name': 'Télétravail',
            'icon': '🌐',
            'description': 'Visioconférence, collaboration, VPN et outils de travail à distance',
            'apps_count': 18
        }
    ]

    return jsonify(profiles)


@app.route('/api/diagnostics', methods=['GET'])
def get_diagnostics():
    """Get system diagnostics"""
    try:
        import psutil

        # Get system info
        cpu_info = f"{psutil.cpu_count()} cores @ {psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else f"{psutil.cpu_count()} cores"
        ram_info = f"{psutil.virtual_memory().total / (1024**3):.1f} GB (Used: {psutil.virtual_memory().percent}%)"
        disk_info = f"{psutil.disk_usage('/').total / (1024**3):.1f} GB (Free: {psutil.disk_usage('/').free / (1024**3):.1f} GB)"

        return jsonify({
            'system': {
                'os': f"{platform.system()} {platform.release()}",
                'cpu': cpu_info,
                'ram': ram_info,
                'disk': disk_info
            },
            'status': 'Backend connecté et opérationnel'
        })

    except Exception as e:
        logger.error(f"Error getting diagnostics: {e}")
        return jsonify({
            'system': {
                'os': f"{platform.system()} {platform.release()}",
                'cpu': 'Non disponible',
                'ram': 'Non disponible',
                'disk': 'Non disponible'
            },
            'status': 'Erreur lors de la récupération des informations'
        })


@app.route('/api/install', methods=['POST'])
def install_application():
    """Install a single application"""
    try:
        data = request.json
        app_id = data.get('app_id')
        method = data.get('method', 'auto')

        logger.info(f"Installing application: {app_id} (method: {method})")

        # TODO: Implement actual installation logic
        # For now, just return success

        return jsonify({
            'status': 'success',
            'message': f'Installation de {app_id} lancée',
            'app_id': app_id,
            'method': method
        })

    except Exception as e:
        logger.error(f"Error installing application: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/install/bulk', methods=['POST'])
def install_bulk():
    """Install multiple applications"""
    try:
        data = request.json
        app_ids = data.get('app_ids', [])

        logger.info(f"Bulk installing {len(app_ids)} applications")

        # TODO: Implement bulk installation logic

        return jsonify({
            'status': 'success',
            'message': f'Installation de {len(app_ids)} applications lancée',
            'app_ids': app_ids
        })

    except Exception as e:
        logger.error(f"Error in bulk installation: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools/execute', methods=['POST'])
def execute_tool():
    """Execute a system tool"""
    try:
        data = request.json
        tool_id = data.get('tool_id')
        params = data.get('params', {})

        logger.info(f"Executing tool: {tool_id}")

        # Tool execution mapping
        tools_commands = {
            'dism': ['dism', '/online', '/cleanup-image', '/restorehealth'],
            'sfc': ['sfc', '/scannow'],
            'chkdsk': ['chkdsk', 'C:', '/F'],
            'disk_cleanup': ['cleanmgr'],
            'system_info': ['msinfo32'],
            'device_manager': ['devmgmt.msc'],
            'task_manager': ['taskmgr'],
            'registry': ['regedit'],
            'services': ['services.msc'],
        }

        if tool_id in tools_commands:
            # Execute command in background
            if platform.system() == 'Windows':
                subprocess.Popen(tools_commands[tool_id], shell=True)
                return jsonify({
                    'status': 'success',
                    'message': f'Outil {tool_id} lancé'
                })
            else:
                return jsonify({
                    'status': 'warning',
                    'message': 'Commande Windows non disponible sur cette plateforme'
                })
        else:
            return jsonify({
                'status': 'info',
                'message': f'Outil {tool_id} non implémenté'
            })

    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites', methods=['GET', 'POST', 'DELETE'])
def handle_favorites():
    """Handle favorites operations"""
    # Favorites are handled client-side via localStorage
    return jsonify({'status': 'Client-side only'})


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("NiTriTe V.13 - Web Backend Starting...")
    logger.info("=" * 60)
    logger.info(f"Platform: {platform.system()} {platform.release()}")
    logger.info(f"Python: {platform.python_version()}")
    logger.info("")
    logger.info("Starting Flask server on http://localhost:5000")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
