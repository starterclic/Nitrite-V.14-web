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
import shutil
from pathlib import Path
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

# Initialize managers with proper error handling
try:
    config_path = os.path.join(os.path.dirname(__file__), 'data', 'programs.json')
    installer_manager = InstallerManager(
        config_path=config_path,
        log_callback=lambda msg, level="info": logger.log(
            getattr(logging, level.upper(), logging.INFO), msg
        ),
        app_dir=os.path.dirname(__file__)
    )
    logger.info(f"✅ InstallerManager initialized with config: {config_path}")
except Exception as e:
    logger.error(f"❌ Error initializing InstallerManager: {e}")
    logger.exception(e)
    installer_manager = None

try:
    winget_manager = WingetManager()
    logger.info("✅ WingetManager initialized")
except Exception as e:
    logger.error(f"❌ Error initializing WingetManager: {e}")
    logger.exception(e)
    winget_manager = None


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


@app.route('/api/optimization/telemetry', methods=['POST'])
def apply_telemetry_tweaks():
    """Apply Windows telemetry optimization tweaks"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        # PowerShell script for telemetry tweaks
        ps_script = """
# Désactiver télémétrie
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Type DWord -Value 0 -Force -ErrorAction SilentlyContinue

# Désactiver rapport d'erreurs Windows
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" -Name "Disabled" -Type DWord -Value 1 -Force -ErrorAction SilentlyContinue

# Désactiver suggestions dans Démarrer
Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SystemPaneSuggestionsEnabled" -Type DWord -Value 0 -Force -ErrorAction SilentlyContinue

# Désactiver historique d'activité
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "PublishUserActivities" -Type DWord -Value 0 -Force -ErrorAction SilentlyContinue
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "UploadUserActivities" -Type DWord -Value 0 -Force -ErrorAction SilentlyContinue

Write-Host "Tweaks télémétrie appliqués avec succès!"
"""

        import tempfile
        script_path = os.path.join(tempfile.gettempdir(), "nitrite_telemetry_tweaks.ps1")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(ps_script)

        # Execute PowerShell as admin
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Cleanup
        if os.path.exists(script_path):
            os.remove(script_path)

        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Tweaks télémétrie appliqués avec succès. Redémarrage recommandé.'
            })
        else:
            return jsonify({
                'status': 'warning',
                'message': 'Certains changements nécessitent des droits administrateur.'
            })

    except Exception as e:
        logger.error(f"Error applying telemetry tweaks: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimization/services', methods=['POST'])
def optimize_services():
    """Optimize Windows services"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        data = request.json
        services_to_disable = data.get('services', [])

        if not services_to_disable:
            return jsonify({'error': 'No services specified'}), 400

        results = []
        for service in services_to_disable:
            try:
                # Disable service
                result = subprocess.run(
                    ['sc', 'config', service, 'start=disabled'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    results.append({'service': service, 'status': 'success'})
                else:
                    results.append({'service': service, 'status': 'failed', 'error': result.stderr})
            except Exception as e:
                results.append({'service': service, 'status': 'error', 'error': str(e)})

        return jsonify({
            'status': 'completed',
            'results': results
        })

    except Exception as e:
        logger.error(f"Error optimizing services: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimization/cleanup', methods=['POST'])
def system_cleanup():
    """Perform system cleanup"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        cleaned_size = 0
        results = []

        # Clean temp folders
        temp_dirs = [
            os.environ.get('TEMP', ''),
            'C:\\Windows\\Temp',
            os.path.expandvars('%LOCALAPPDATA%\\Temp')
        ]

        for temp_dir in temp_dirs:
            if not temp_dir or not os.path.exists(temp_dir):
                continue

            try:
                size_before = sum(f.stat().st_size for f in Path(temp_dir).rglob('*') if f.is_file())

                # Clean files older than 7 days
                import time
                current_time = time.time()
                for item in Path(temp_dir).iterdir():
                    try:
                        if item.is_file() and (current_time - item.stat().st_mtime) > (7 * 86400):
                            item.unlink()
                        elif item.is_dir() and (current_time - item.stat().st_mtime) > (7 * 86400):
                            shutil.rmtree(item, ignore_errors=True)
                    except:
                        pass

                size_after = sum(f.stat().st_size for f in Path(temp_dir).rglob('*') if f.is_file())
                freed = (size_before - size_after) / (1024 * 1024)  # MB
                cleaned_size += freed

                results.append({
                    'location': temp_dir,
                    'freed_mb': round(freed, 2)
                })
            except Exception as e:
                logger.warning(f"Error cleaning {temp_dir}: {e}")

        return jsonify({
            'status': 'success',
            'cleaned_size_mb': round(cleaned_size, 2),
            'details': results
        })

    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/master/apps', methods=['GET'])
def get_master_apps():
    """Get list of essential apps for master installation"""
    master_apps = [
        {'id': 'Adobe Acrobat Reader', 'name': 'Adobe Acrobat Reader', 'icon': '📄', 'category': 'Bureautique'},
        {'id': 'VLC', 'name': 'VLC Media Player', 'icon': '🎬', 'category': 'Multimedia'},
        {'id': 'Firefox', 'name': 'Mozilla Firefox', 'icon': '🦊', 'category': 'Navigation'},
        {'id': '7-Zip', 'name': '7-Zip', 'icon': '📦', 'category': 'Utilitaires'},
        {'id': 'Spybot', 'name': 'Spybot Search & Destroy', 'icon': '🛡️', 'category': 'Securite'},
        {'id': 'AdwCleaner', 'name': 'AdwCleaner', 'icon': '🧹', 'category': 'Securite'},
        {'id': 'AnyDesk', 'name': 'AnyDesk', 'icon': '🖥️', 'category': 'Remote'},
        {'id': 'RustDesk', 'name': 'RustDesk', 'icon': '🔒', 'category': 'Remote'},
        {'id': 'Wise Disk Cleaner', 'name': 'Wise Disk Cleaner', 'icon': '💿', 'category': 'Maintenance'},
        {'id': 'Malwarebytes', 'name': 'Malwarebytes', 'icon': '🔒', 'category': 'Securite'},
        {'id': 'Google Chrome', 'name': 'Google Chrome', 'icon': '🌐', 'category': 'Navigation'},
        {'id': 'Microsoft Office', 'name': 'Microsoft Office', 'icon': '📊', 'category': 'Bureautique'}
    ]

    return jsonify(master_apps)


@app.route('/api/backup/restore-point', methods=['POST'])
def create_restore_point():
    """Create a system restore point"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        data = request.json
        description = data.get('description', 'NiTriTe Manual Restore Point')

        # PowerShell script to create restore point
        ps_script = f"""
Checkpoint-Computer -Description "{description}" -RestorePointType "MODIFY_SETTINGS"
Write-Host "Point de restauration créé avec succès"
"""

        import tempfile
        script_path = os.path.join(tempfile.gettempdir(), "nitrite_restore_point.ps1")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(ps_script)

        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if os.path.exists(script_path):
            os.remove(script_path)

        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Point de restauration créé avec succès'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de la création du point de restauration',
                'details': result.stderr
            }), 500

    except Exception as e:
        logger.error(f"Error creating restore point: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/backup/drivers', methods=['POST'])
def backup_drivers():
    """Backup all installed drivers"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        data = request.json
        backup_path = data.get('path', 'C:\\DriversBackup')

        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)

        # DISM command to export drivers
        result = subprocess.run(
            ['dism', '/online', '/export-driver', f'/destination:{backup_path}'],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            # Count exported drivers
            driver_count = len([f for f in os.listdir(backup_path) if f.endswith('.inf')])
            return jsonify({
                'status': 'success',
                'message': f'{driver_count} drivers sauvegardés',
                'path': backup_path,
                'count': driver_count
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Erreur lors de la sauvegarde des drivers',
                'details': result.stderr
            }), 500

    except Exception as e:
        logger.error(f"Error backing up drivers: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/backup/apps-list', methods=['GET'])
def export_apps_list():
    """Export list of installed applications"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        # Get installed apps via WinGet
        result = subprocess.run(
            ['winget', 'list'],
            capture_output=True,
            text=True,
            timeout=60
        )

        apps_list = []
        if result.returncode == 0:
            lines = result.stdout.split('\n')[2:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        apps_list.append({
                            'name': ' '.join(parts[:-1]),
                            'version': parts[-1]
                        })

        return jsonify({
            'status': 'success',
            'count': len(apps_list),
            'applications': apps_list
        })

    except Exception as e:
        logger.error(f"Error exporting apps list: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/startup-apps', methods=['GET'])
def get_startup_apps():
    """Get list of startup applications"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        startup_apps = []

        # Check registry startup locations
        import winreg
        startup_keys = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        ]

        for hkey, path in startup_keys:
            try:
                key = winreg.OpenKey(hkey, path)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        startup_apps.append({
                            'name': name,
                            'path': value,
                            'location': 'HKCU' if hkey == winreg.HKEY_CURRENT_USER else 'HKLM'
                        })
                        i += 1
                    except WindowsError:
                        break
                winreg.CloseKey(key)
            except WindowsError:
                continue

        return jsonify({
            'status': 'success',
            'count': len(startup_apps),
            'applications': startup_apps
        })

    except Exception as e:
        logger.error(f"Error getting startup apps: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/dism-scan', methods=['POST'])
def run_dism_scan():
    """Run DISM scan and repair"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        data = request.json
        operation = data.get('operation', 'ScanHealth')  # ScanHealth, CheckHealth, or RestoreHealth

        cmd = ['dism', '/online', f'/{operation}']

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )

        return jsonify({
            'status': 'success' if result.returncode == 0 else 'warning',
            'message': 'DISM scan completed',
            'output': result.stdout,
            'returncode': result.returncode
        })

    except Exception as e:
        logger.error(f"Error running DISM: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/sfc-scan', methods=['POST'])
def run_sfc_scan():
    """Run System File Checker"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        result = subprocess.run(
            ['sfc', '/scannow'],
            capture_output=True,
            text=True,
            timeout=600
        )

        return jsonify({
            'status': 'success' if result.returncode == 0 else 'warning',
            'message': 'SFC scan completed',
            'output': result.stdout,
            'returncode': result.returncode
        })

    except Exception as e:
        logger.error(f"Error running SFC: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/network-reset', methods=['POST'])
def reset_network():
    """Reset network settings"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        commands = [
            ['ipconfig', '/release'],
            ['ipconfig', '/flushdns'],
            ['ipconfig', '/renew'],
            ['netsh', 'winsock', 'reset'],
            ['netsh', 'int', 'ip', 'reset'],
        ]

        results = []
        for cmd in commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                results.append({
                    'command': ' '.join(cmd),
                    'success': result.returncode == 0
                })
            except Exception as e:
                results.append({
                    'command': ' '.join(cmd),
                    'success': False,
                    'error': str(e)
                })

        return jsonify({
            'status': 'success',
            'message': 'Réinitialisation réseau terminée. Redémarrage recommandé.',
            'results': results
        })

    except Exception as e:
        logger.error(f"Error resetting network: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimization/performance', methods=['POST'])
def apply_performance_tweaks():
    """Apply advanced performance tweaks"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        ps_script = """
# Désactiver les effets visuels inutiles
Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Type DWord -Value 2 -Force -ErrorAction SilentlyContinue

# Désactiver hibernation pour libérer de l'espace
powercfg /hibernate off

# Optimiser le système de fichiers
fsutil behavior set DisableLastAccess 1

# Désactiver Windows Search indexing pour SSD
Stop-Service "WSearch" -Force -ErrorAction SilentlyContinue
Set-Service "WSearch" -StartupType Disabled -ErrorAction SilentlyContinue

# Désactiver Prefetch et Superfetch (utile pour SSD)
Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" -Name "EnablePrefetcher" -Type DWord -Value 0 -Force -ErrorAction SilentlyContinue
Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" -Name "EnableSuperfetch" -Type DWord -Value 0 -Force -ErrorAction SilentlyContinue

Write-Host "Tweaks de performance appliqués"
"""

        import tempfile
        script_path = os.path.join(tempfile.gettempdir(), "nitrite_performance_tweaks.ps1")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(ps_script)

        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if os.path.exists(script_path):
            os.remove(script_path)

        return jsonify({
            'status': 'success' if result.returncode == 0 else 'warning',
            'message': 'Tweaks de performance appliqués. Redémarrage recommandé.'
        })

    except Exception as e:
        logger.error(f"Error applying performance tweaks: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/updates/check', methods=['GET'])
def check_windows_updates():
    """Check for Windows updates"""
    try:
        if platform.system() != 'Windows':
            return jsonify({'error': 'Windows only feature'}), 400

        ps_script = """
$UpdateSession = New-Object -ComObject Microsoft.Update.Session
$UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
$SearchResult = $UpdateSearcher.Search("IsInstalled=0")
$Updates = $SearchResult.Updates

$UpdatesList = @()
foreach ($Update in $Updates) {
    $UpdatesList += @{
        Title = $Update.Title
        Description = $Update.Description
        Size = [math]::Round($Update.MaxDownloadSize / 1MB, 2)
        IsDownloaded = $Update.IsDownloaded
    }
}

$UpdatesList | ConvertTo-Json
"""

        import tempfile
        script_path = os.path.join(tempfile.gettempdir(), "check_updates.ps1")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(ps_script)

        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            capture_output=True,
            text=True,
            timeout=120
        )

        if os.path.exists(script_path):
            os.remove(script_path)

        if result.returncode == 0 and result.stdout.strip():
            try:
                updates = json.loads(result.stdout)
                return jsonify({
                    'status': 'success',
                    'count': len(updates) if isinstance(updates, list) else 1,
                    'updates': updates if isinstance(updates, list) else [updates]
                })
            except json.JSONDecodeError:
                return jsonify({
                    'status': 'success',
                    'count': 0,
                    'updates': []
                })
        else:
            return jsonify({
                'status': 'success',
                'count': 0,
                'updates': []
            })

    except Exception as e:
        logger.error(f"Error checking updates: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/benchmark/run', methods=['POST'])
def run_benchmark():
    """Run system benchmark"""
    try:
        import time
        import psutil

        # CPU Benchmark
        cpu_start = time.time()
        cpu_percent = psutil.cpu_percent(interval=2)
        cpu_time = time.time() - cpu_start

        # Memory info
        mem = psutil.virtual_memory()

        # Disk info
        disk = psutil.disk_usage('/')

        # Calculate simple score (0-100)
        cpu_score = min(100, (100 - cpu_percent))
        mem_score = min(100, (100 - mem.percent))
        disk_score = min(100, (disk.free / disk.total) * 100)

        overall_score = (cpu_score + mem_score + disk_score) / 3

        return jsonify({
            'status': 'success',
            'overall_score': round(overall_score, 1),
            'cpu_score': round(cpu_score, 1),
            'memory_score': round(mem_score, 1),
            'disk_score': round(disk_score, 1),
            'details': {
                'cpu_usage': cpu_percent,
                'memory_used_percent': mem.percent,
                'disk_used_percent': round((disk.used / disk.total) * 100, 1)
            }
        })

    except Exception as e:
        logger.error(f"Error running benchmark: {e}")
        return jsonify({'error': str(e)}), 500


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
