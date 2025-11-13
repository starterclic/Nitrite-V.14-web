"""
Gestionnaire d'installations pour NiTrite v.2
Gère le téléchargement et l'installation silencieuse des programmes
"""

import os
import subprocess
import tempfile
import zipfile
import shutil
import json
import time
import threading
import sys
from pathlib import Path
import logging
from urllib.parse import urlparse
import hashlib
import ctypes
from ctypes import wintypes

# Import conditionnel pour requests
try:
    import requests
except ImportError:
    requests = None
    logging.warning("Module 'requests' non disponible - certaines fonctionnalités seront limitées")

# Import conditionnel pour winreg
try:
    import winreg
except ImportError:
    winreg = None

# Import du module d'élévation
try:
    from .elevation_helper import run_as_admin_silent, is_admin, create_elevated_process
except ImportError:
    try:
        from elevation_helper import run_as_admin_silent, is_admin, create_elevated_process
    except ImportError:
        # Fallback si module non disponible
        def run_as_admin_silent(cmd, timeout=300):
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return (result.returncode == 0, result.returncode, result.stdout, result.stderr)
        def is_admin():
            return False
        def create_elevated_process(exe, args=None, working_dir=None):
            return False

# Import de la base de données portable
try:
    from .portable_database import PortableDatabase
except ImportError:
    try:
        from portable_database import PortableDatabase
    except ImportError:
        PortableDatabase = None

def get_windows_folder_path(csidl):
    """
    Obtient le chemin d'un dossier Windows spécial via SHGetFolderPath.
    CSIDL_DESKTOP = 0 (Bureau)
    CSIDL_PROGRAMS = 2 (Menu Démarrer\Programmes)
    """
    try:
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        result = ctypes.windll.shell32.SHGetFolderPathW(None, csidl, None, 0, buf)
        if result == 0:
            return Path(buf.value)
    except Exception as e:
        logging.warning(f"Impossible d'obtenir le chemin du dossier Windows (CSIDL {csidl}): {e}")

    # Fallback
    return Path.home() / 'Desktop'

def get_desktop_path():
    """Obtient le vrai chemin du Bureau Windows, quelle que soit la langue."""
    CSIDL_DESKTOP = 0
    return get_windows_folder_path(CSIDL_DESKTOP)

class InstallerManager:
    """Gestionnaire des installations de programmes"""

    def __init__(self, config_path=None, log_callback=None, app_dir=None):
        self.logger = logging.getLogger(__name__)
        self.log_callback = log_callback if log_callback else self._default_log
        
        self.download_dir = Path(tempfile.gettempdir()) / 'NiTrite_Downloads'
        self.download_dir.mkdir(exist_ok=True)
        
        if config_path is None:
            raise ValueError("Le chemin vers le fichier de configuration est requis.")
        
        self.config_path = Path(config_path)
        self.programs_db = self._load_config()
        
        self.stop_requested = False
        self.current_process = None
        
        # Initialiser la base de données portable
        if PortableDatabase and app_dir:
            try:
                self.app_dir = Path(app_dir)
                db_path = self.app_dir / "portable_apps.db"
                self.portable_db = PortableDatabase(
                    db_path=str(db_path),
                    apps_folder=str(self.download_dir)
                )
                self.log_callback(f"✅ Base de données portable initialisée: {db_path}", "info")
            except Exception as e:
                self.log_callback(f"⚠️ Impossible d'initialiser la base de données portable: {e}", "warning")
                self.portable_db = None
        else:
            self.portable_db = None
            if not PortableDatabase:
                self.log_callback("⚠️ Module PortableDatabase non disponible", "warning")

    def _default_log(self, message, level="info"):
        """Callback de log par défaut si aucun n'est fourni."""
        log_func = getattr(self.logger, level, self.logger.info)
        log_func(message)

    def _load_config(self):
        """Charge la configuration des programmes depuis le fichier JSON."""
        try:
            if not self.config_path.exists():
                self.log_callback(f"Fichier de configuration non trouvé: {self.config_path}", "error")
                return {}
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                categorized_programs = json.load(f)
            
            # Aplatir la structure pour un accès facile
            all_programs = {}
            for category, programs in categorized_programs.items():
                if isinstance(programs, dict):
                    for program_name, program_info in programs.items():
                        # Ajouter la catégorie et le nom pour référence future
                        program_info['category'] = category
                        program_info['name'] = program_name
                        all_programs[program_name] = program_info
            
            self.log_callback(f"Configuration chargée: {len(all_programs)} programmes", "info")
            return all_programs
        except Exception as e:
            self.log_callback(f"Erreur lors du chargement de la configuration: {e}", "error")
            return {}

    def get_programs_db(self):
        """Retourne la base de données des programmes."""
        return self.programs_db

    def install_programs_threaded(self, program_list, progress_callback):
        """Lance l'installation dans un thread séparé."""
        thread = threading.Thread(
            target=self.install_programs,
            args=(program_list, progress_callback)
        )
        thread.daemon = True
        thread.start()

    def install_programs(self, program_list, progress_callback, completion_callback=None, success_list=None, failed_list=None):
        """
        Installe une liste de programmes.
        
        Args:
            program_list: Liste des noms de programmes à installer
            progress_callback: Fonction appelée pour mettre à jour la progression (progress, message)
            completion_callback: Fonction appelée à la fin (success)
        """
        self.stop_requested = False
        total_programs = len(program_list)
        success_count = 0
        
        # Listes pour tracking (si fournies depuis GUI)
        if success_list is None:
            success_list = []
        if failed_list is None:
            failed_list = []
        
        self.log_callback("🚀 Début de l'installation...", "info")
        
        for i, program_name in enumerate(program_list):
            if self.stop_requested:
                self.log_callback("⚠️ Installation arrêtée par l'utilisateur.", "warning")
                if completion_callback:
                    completion_callback(False)
                return
            
            progress = (i / total_programs) * 100
            progress_callback(progress, f"Installation de {program_name}...")

            program_info = self.programs_db.get(program_name, {})
            success, error_reason, method = self.install_single_program(program_name)

            if success:
                success_count += 1
                # Ajouter aux installations réussies
                success_list.append({
                    'name': program_name,
                    'category': program_info.get('category', 'N/A'),
                    'method': method if method else 'Unknown'
                })
            else:
                # Ajouter aux installations échouées
                if not self.stop_requested:
                    self.log_callback(f"❌ Échec de l'installation de {program_name}", "error")
                    failed_list.append({
                        'name': program_name,
                        'category': program_info.get('category', 'N/A'),
                        'reason': error_reason if error_reason else 'Installation échouée'
                    })
            
            time.sleep(1)
        
        if not self.stop_requested:
            progress_callback(100, "Installation terminée")
            self.log_callback(f"✅ Toutes les installations sont terminées. ({success_count}/{total_programs} réussies)", "success")
            if completion_callback:
                completion_callback(True)
        else:
            if completion_callback:
                completion_callback(False)

    def install_single_program(self, program_name):
        """
        Installe un programme spécifique avec une logique corrigée.

        Returns:
            tuple: (success, error_reason, method) où:
                - success (bool): True si installation réussie
                - error_reason (str): Raison de l'échec si applicable, None sinon
                - method (str): Méthode utilisée ('Direct', 'WinGet', 'Portable', 'Already Installed')
        """
        if program_name not in self.programs_db:
            self.log_callback(f"Programme '{program_name}' non trouvé.", "error")
            return False, "Programme non trouvé dans la base de données", None

        program_info = self.programs_db[program_name]
        self.log_callback(f"Début de l'installation de {program_name}", "info")
        self.log_callback(f"📋 Config: portable={program_info.get('portable', False)}, install_args={program_info.get('install_args', '')}, winget_id={program_info.get('winget_id', 'None')}, download_url={program_info.get('download_url', 'None')}", "info")

        # LOGIQUE CORRIGÉE POUR LES PORTABLES
        is_portable = program_info.get('portable', False)
        install_args = program_info.get('install_args', '')
        if is_portable or install_args == 'portable':
            self.log_callback(f"🌀 Traitement de l'application portable: {program_name}", "info")
            installer_path = self._download_program(program_info)
            if installer_path:
                success = self.execute_installation(installer_path, program_info)
                if success:
                    return True, None, "Portable"
                else:
                    return False, "Échec de l'exécution de l'installateur portable", None
            else:
                self.log_callback(f"❌ Échec du téléchargement pour l'application portable {program_name}", "error")
                return False, "Échec du téléchargement", None

        # Logique pour les programmes non-portables
        if self.is_program_installed(program_info):
            self.log_callback(f"{program_name} est déjà installé.", "info")
            return True, None, "Already Installed"

        # Stratégie 1: Téléchargement direct
        download_url = program_info.get('download_url', '').strip()
        if download_url:
            self.log_callback("🔄 Tentative via téléchargement direct...", "info")
            installer_path = self._download_program(program_info)
            if installer_path:
                if self.execute_installation(installer_path, program_info):
                    self.log_callback(f"✅ {program_name} installé avec succès via téléchargement direct.", "success")
                    return True, None, "Direct"
                self.log_callback("⚠️ Échec de l'installation après téléchargement.", "warning")

        # Stratégie 2: Winget (en fallback)
        winget_id = program_info.get('winget_id')
        self.log_callback(f"🔍 Vérification WinGet ID: {winget_id}", "info")
        if winget_id:
            self.log_callback(f"🔄 Tentative via winget avec ID: {winget_id}...", "info")
            if self.install_via_winget(winget_id, program_info):
                self.log_callback(f"✅ {program_name} installé avec succès via winget.", "success")
                return True, None, "WinGet"
            self.log_callback("⚠️ Échec de l'installation via winget.", "warning")

            # Stratégie 2b: Essayer les IDs WinGet alternatifs si présents
            fallback_ids = program_info.get('winget_fallback_ids', [])
            if fallback_ids:
                for idx, fallback_id in enumerate(fallback_ids, 1):
                    self.log_callback(f"🔄 Tentative {idx} avec WinGet ID alternatif: {fallback_id}...", "info")
                    if self.install_via_winget(fallback_id, program_info):
                        self.log_callback(f"✅ {program_name} installé avec succès via winget (ID alternatif).", "success")
                        return True, None, "WinGet (Fallback)"
                    self.log_callback(f"⚠️ Échec avec ID alternatif {fallback_id}.", "warning")

        self.log_callback(f"❌ Échec de toutes les méthodes d'installation pour {program_name}", "error")
        return False, "Toutes les méthodes d'installation ont échoué", None

    def _download_program(self, program_info, max_retries=3):
        """
        Télécharge un programme depuis son URL avec retry automatique.

        Args:
            program_info: Dictionnaire contenant les infos du programme
            max_retries: Nombre maximum de tentatives (défaut: 3)

        Returns:
            str: Chemin du fichier téléchargé ou None si échec
        """
        if not requests:
            self.log_callback("Le module 'requests' est manquant.", "error")
            return None

        download_url = program_info.get('download_url', '')
        if not download_url:
            self.log_callback("URL de téléchargement manquante", "error")
            return None

        filename = program_info.get('filename', os.path.basename(urlparse(download_url).path))
        if not filename:
            filename = f"download_{int(time.time())}"

        file_path = self.download_dir / filename

        # Retry avec backoff exponentiel
        for attempt in range(1, max_retries + 1):
            try:
                if attempt > 1:
                    delay = 2 ** (attempt - 1)  # 2s, 4s, 8s
                    self.log_callback(f"⏳ Nouvelle tentative dans {delay}s... (tentative {attempt}/{max_retries})", "info")
                    time.sleep(delay)

                self.log_callback(f"📥 Téléchargement de {filename}... (tentative {attempt}/{max_retries})", "info")
                timeout = program_info.get('download_timeout', 60)  # 60s par défaut
                response = requests.get(download_url, stream=True, timeout=timeout)
                response.raise_for_status()

                # Téléchargement avec progression
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # Filtrer les chunks vides
                            f.write(chunk)

                self.log_callback(f"✅ Téléchargement terminé: {file_path}", "success")
                return str(file_path)

            except requests.exceptions.Timeout as e:
                self.log_callback(f"⏱️ Timeout lors du téléchargement (tentative {attempt}/{max_retries}): {e}", "warning")
            except requests.exceptions.ConnectionError as e:
                self.log_callback(f"🔌 Erreur de connexion (tentative {attempt}/{max_retries}): {e}", "warning")
            except requests.exceptions.RequestException as e:
                self.log_callback(f"⚠️ Erreur réseau (tentative {attempt}/{max_retries}): {e}", "warning")
            except Exception as e:
                self.log_callback(f"❌ Erreur inattendue lors du téléchargement: {e}", "error")
                self.logger.exception(e)
                return None

        # Toutes les tentatives ont échoué
        self.log_callback(f"❌ Échec du téléchargement après {max_retries} tentatives", "error")
        return None

    def execute_installation(self, installer_path, program_info):
        """
        Exécute l'installation ou la copie du programme.
        
        Args:
            installer_path: Chemin vers l'installateur
            program_info: Informations du programme
            
        Returns:
            bool: True si l'installation a réussi
        """
        is_portable = program_info.get('portable', False)
        install_args = program_info.get('install_args', '')

        if is_portable or install_args == 'portable':
            portable_folder = program_info.get('cleanup_folder', 'Programmes Portables')
            desktop_path = get_desktop_path()
            portable_dir = desktop_path / portable_folder
            portable_dir.mkdir(parents=True, exist_ok=True)
            
            dest_file = portable_dir / Path(installer_path).name
            shutil.copy2(installer_path, dest_file)
            self.log_callback(f"✅ Fichier portable copié dans: {portable_dir}", "success")
            
            # Ajouter à la base de données portable
            if self.portable_db:
                try:
                    app_id = self.portable_db.add_application(
                        name=program_info.get('name', Path(installer_path).stem),
                        executable_path=str(dest_file),
                        display_name=program_info.get('name', Path(installer_path).stem),
                        category=program_info.get('category', 'Non classé'),
                        description=program_info.get('description', ''),
                        download_url=program_info.get('download_url', ''),
                        is_portable=True,
                        install_args=str(install_args),
                        admin_required=program_info.get('admin_required', False),
                        notes=program_info.get('note', ''),
                        essential=program_info.get('essential', False),
                        winget_id=program_info.get('winget_id', '')
                    )
                    if app_id:
                        self.log_callback(f"💾 Application ajoutée à la base de données (ID: {app_id})", "info")
                except Exception as e:
                    self.log_callback(f"⚠️ Erreur lors de l'ajout à la BDD: {e}", "warning")
            
            if dest_file.suffix.lower() == '.exe':
                self.create_desktop_shortcut(str(dest_file), program_info['name'])
            return True

        # Convertir install_args en liste si c'est une chaîne
        if isinstance(install_args, str):
            install_args = install_args.split() if install_args else []
        elif not isinstance(install_args, list):
            install_args = []
        
        # Vérifier que l'installateur existe
        if not os.path.exists(installer_path):
            self.log_callback(f"Fichier installateur non trouvé: {installer_path}", "error")
            return False
        
        # Timeout d'installation
        timeout = program_info.get('install_timeout', 300)  # 5 minutes par défaut
        admin_required = program_info.get('admin_required', True)  # Par défaut OUI
        
        # Construire la commande d'installation
        if program_info.get('install_type', '').lower() == 'msi':
            base_cmd = ['msiexec', '/i', installer_path, '/quiet', '/norestart']
            if install_args:
                base_cmd.extend(install_args)
        elif program_info.get('install_type', '').lower() == 'zip':
            return self.extract_zip_program(installer_path, program_info)
        else:
            base_cmd = [installer_path] + install_args
        
        self.log_callback(f"🔧 Commande: {' '.join(base_cmd)}")
        
        # Essayer d'abord SANS privilèges administrateur
        if not admin_required:
            self.log_callback("🔓 Tentative d'installation sans privilèges administrateur...")
            success = self._execute_command_normal(base_cmd, timeout)
            if success:
                return True
            self.log_callback("⚠️ Échec sans privilèges admin, tentative avec élévation...", "warning")
        
        # Méthode 1: PowerShell avec élévation
        self.log_callback("🔐 Exécution avec privilèges administrateur (PowerShell)...")
        success = self._execute_command_elevated_ps(base_cmd, timeout)
        if success:
            return True
            
        # Méthode 2: Runas si PowerShell échoue
        self.log_callback("🔐 Tentative avec runas...", "warning")
        success = self._execute_command_elevated_runas(base_cmd, timeout)
        if success:
            return True
        
        # Méthode 3: Dernier recours - sans élévation
        self.log_callback("🔓 Dernier recours - exécution sans élévation...", "warning")
        return self._execute_command_normal(base_cmd, timeout)
        
    def _execute_command_normal(self, cmd, timeout):
        """Exécute une commande sans privilèges administrateur"""
        try:
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = subprocess.SW_HIDE
            
            env = os.environ.copy()
            env['WINGET_DISABLE_INTERACTIVITY'] = '1'
            env['NITRITE_INSTALLATION'] = '1'
            
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startup_info,
                env=env,
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            )
            
            stdout, stderr = self.current_process.communicate(timeout=timeout)
            return_code = self.current_process.returncode
            
            if return_code == 0:
                self.log_callback("✅ Installation réussie (mode normal)", "success")
                return True
            else:
                error_msg = stderr.decode('utf-8', errors='ignore')
                if "access denied" in error_msg.lower() or "privilège" in error_msg.lower():
                    self.log_callback("⚠️ Privilèges insuffisants", "warning")
                else:
                    self.log_callback(f"❌ Erreur (code {return_code}): {error_msg[:200]}", "error")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_callback("⏱️ Timeout installation (mode normal)", "warning")
            try:
                self.current_process.terminate()
                time.sleep(2)
                if self.current_process.poll() is None:
                    self.current_process.kill()
            except Exception:
                pass
            return False
        except Exception as e:
            self.log_callback(f"❌ Erreur exécution normale: {e}", "error")
            return False
    
    def _execute_command_elevated_ps(self, cmd, timeout):
        """Exécute une commande avec privilèges administrateur via PowerShell et élévation automatique"""
        try:
            self.log_callback("🔐 Demande d'élévation automatique...", "info")
            
            # Méthode 1: Utiliser le helper d'élévation pour bypass UAC si possible
            success, returncode, stdout, stderr = run_as_admin_silent(cmd, timeout)
            
            if success or returncode == 0:
                self.log_callback("✅ Installation réussie (élévation automatique)", "success")
                return True
            
            # Méthode 2 (fallback): PowerShell traditionnel avec -Verb RunAs
            self.log_callback("🔄 Tentative PowerShell standard...", "info")
            escaped_cmd = cmd[0]
            if len(cmd) > 1:
                args_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd[1:])
                ps_cmd = f'Start-Process "{escaped_cmd}" -ArgumentList "{args_str}" -Verb RunAs -Wait -WindowStyle Hidden'
            else:
                ps_cmd = f'Start-Process "{escaped_cmd}" -Verb RunAs -Wait -WindowStyle Hidden'
            
            result = subprocess.run(
                ["powershell.exe", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                self.log_callback("✅ Installation réussie (PowerShell admin)", "success")
                return True
            else:
                error_msg = result.stderr
                if "cancelled by the user" in error_msg.lower():
                    self.log_callback("⚠️ Installation annulée par l'utilisateur", "warning")
                else:
                    self.log_callback(f"❌ Erreur PowerShell: {error_msg[:200]}", "error")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_callback("⏱️ Timeout installation (PowerShell)", "warning")
            return False
        except Exception as e:
            self.log_callback(f"❌ Erreur PowerShell: {e}", "error")
            return False
    
    def _execute_command_elevated_runas(self, cmd, timeout):
        """Exécute une commande avec privilèges administrateur via runas"""
        try:
            # Créer un fichier batch temporaire
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as f:
                f.write('@echo off\n')
                f.write(' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd))
                f.write('\n')
                batch_file = f.name
            
            try:
                # Exécuter avec runas
                runas_cmd = ['runas', '/user:Administrator', batch_file]
                result = subprocess.run(
                    runas_cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                if result.returncode == 0:
                    self.log_callback("✅ Installation réussie (runas)", "success")
                    return True
                else:
                    self.log_callback(f"❌ Erreur runas: {result.stderr[:200]}", "error")
                    return False
                    
            finally:
                # Nettoyer le fichier batch
                try:
                    os.remove(batch_file)
                except Exception:
                    pass
                    
        except Exception as e:
            self.log_callback(f"❌ Erreur runas: {e}", "error")
            return False
    
    def extract_zip_program(self, zip_path, program_info):
        """
        Extrait un programme depuis un fichier ZIP
        
        Args:
            zip_path: Chemin vers le fichier ZIP
            program_info: Informations du programme
            
        Returns:
            bool: True si l'extraction a réussi
        """
        try:
            extract_path = program_info.get('extract_path', 'C:\\Program Files')
            program_folder = program_info.get('program_folder', program_info['name'])
            
            full_extract_path = Path(extract_path) / program_folder
            
            self.log_callback(f"Extraction vers {full_extract_path}")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(full_extract_path)
            
            # Créer un raccourci si spécifié
            if 'executable' in program_info:
                self.create_desktop_shortcut(
                    full_extract_path / program_info['executable'],
                    program_info['name']
                )
            
            return True
            
        except Exception as e:
            self.log_callback(f"Erreur lors de l'extraction: {e}", "error")
            return False
    
    def create_desktop_shortcut(self, target_path, name):
        """Crée un raccourci sur le bureau"""
        try:
            import win32com.client
            
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, f"{name}.lnk")
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = str(target_path)
            shortcut.WorkingDirectory = str(target_path.parent)
            shortcut.save()
            
            self.log_callback(f"Raccourci créé: {shortcut_path}")
            
        except Exception as e:
            self.log_callback(f"Impossible de créer le raccourci: {e}", "warning")
    
    def is_program_installed(self, program_info):
        """
        Vérifie si un programme est déjà installé avec méthodes multiples
        
        Args:
            program_info: Informations du programme
            
        Returns:
            bool: True si le programme est installé
        """
        try:
            program_name = program_info.get('name', '')
            
            # Méthode 1: Vérification via winget si ID disponible
            if 'winget_id' in program_info:
                if self.check_winget_installation(program_info['winget_id']):
                    self.logger.info(f"✅ {program_name} détecté via winget")
                    return True
            
            # Méthode 2: Vérifier via le registre Windows
            if 'registry_key' in program_info:
                if self.check_registry_installation(program_info['registry_key']):
                    self.logger.info(f"✅ {program_name} détecté via registre")
                    return True
            
            # Méthode 3: Vérifier l'existence d'un fichier
            if 'check_file' in program_info:
                if Path(program_info['check_file']).exists():
                    self.logger.info(f"✅ {program_name} détecté via fichier")
                    return True
            
            # Méthode 4: Vérifier via une commande
            if 'check_command' in program_info:
                if self.check_command_installation(program_info['check_command']):
                    self.logger.info(f"✅ {program_name} détecté via commande")
                    return True
            
            # Méthode 5: Vérification automatique dans les dossiers communs
            if self.check_common_installation_paths(program_info):
                self.logger.info(f"✅ {program_name} détecté dans dossiers standards")
                return True
            
            # Méthode 6: Vérification via le registre des programmes installés
            if self.check_installed_programs_registry(program_info):
                self.logger.info(f"✅ {program_name} détecté dans la liste des programmes")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification d'installation: {e}")
            return False
    
    def check_winget_installation(self, winget_id):
        """Vérifie l'installation via winget list"""
        try:
            result = subprocess.run(
                ['winget', 'list', '--id', winget_id],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                # Vérifier si le programme est vraiment dans la liste
                output = result.stdout.lower()
                return winget_id.lower() in output and "no installed package found" not in output
                
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            self.logger.debug(f"Erreur vérification winget pour {winget_id}: {e}")
        
        return False
    
    def check_common_installation_paths(self, program_info):
        """Vérifie les dossiers d'installation communs"""
        try:
            program_name = program_info.get('name', '')
            if not program_name:
                return False
            
            # Nettoyer le nom du programme pour la recherche
            clean_name = program_name.replace(' ', '').replace('-', '').replace('_', '').lower()
            
            # Dossiers à vérifier
            search_paths = [
                Path("C:/Program Files"),
                Path("C:/Program Files (x86)"),
                Path(os.path.expanduser("~/AppData/Local")),
                Path(os.path.expanduser("~/AppData/Roaming")),
                Path("C:/Users/Public/Desktop"),
                Path(os.path.expanduser("~/Desktop"))
            ]
            
            for search_path in search_paths:
                if not search_path.exists():
                    continue
                
                try:
                    # Rechercher des dossiers contenant le nom du programme
                    for item in search_path.iterdir():
                        if item.is_dir():
                            item_name = item.name.replace(' ', '').replace('-', '').replace('_', '').lower()
                            if clean_name in item_name or item_name in clean_name:
                                # Vérifier s'il y a des exécutables
                                exe_files = list(item.glob("*.exe"))
                                if exe_files:
                                    self.logger.debug(f"Programme trouvé dans: {item}")
                                    return True
                except (PermissionError, OSError):
                    continue  # Ignorer les erreurs d'accès
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Erreur vérification dossiers communs: {e}")
            return False
    
    def check_installed_programs_registry(self, program_info):
        """Vérifie le registre des programmes installés Windows"""
        try:
            if not winreg:
                return False
            
            program_name = program_info.get('name', '')
            if not program_name:
                return False
            
            # Clés de registre à vérifier
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            ]
            
            clean_program_name = program_name.lower().replace(' ', '').replace('-', '')
            
            for hkey, path in registry_paths:
                try:
                    with winreg.OpenKey(hkey, path) as key:
                        i = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    try:
                                        display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                        clean_display_name = display_name.lower().replace(' ', '').replace('-', '')
                                        
                                        if (clean_program_name in clean_display_name or 
                                            clean_display_name in clean_program_name):
                                            return True
                                            
                                    except FileNotFoundError:
                                        pass  # DisplayName n'existe pas
                                i += 1
                            except OSError:
                                break  # Plus de sous-clés
                                
                except (OSError, WindowsError):
                    continue  # Erreur d'accès à cette clé
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Erreur vérification registre programmes: {e}")
            return False
    
    def check_registry_installation(self, registry_path):
        """Vérifie l'installation via le registre Windows"""
        try:
            key_parts = registry_path.split('\\')
            root_key = getattr(winreg, key_parts[0])
            sub_key = '\\'.join(key_parts[1:])
            
            winreg.OpenKey(root_key, sub_key)
            return True
            
        except WindowsError:
            return False
    
    def check_command_installation(self, command):
        """Vérifie l'installation via une commande"""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification du programme: {e}")
            return False
    
    def install_via_winget(self, winget_id, program_info):
        """
        Installe un programme via winget
        
        Args:
            winget_id: ID winget du programme
            program_info: Informations du programme
            
        Returns:
            bool: True si l'installation a réussi
        """
        try:
            self.log_callback(f"📦 Installation via winget: {winget_id}", "info")
            
            # Construire la commande winget
            cmd = ['winget', 'install', '--id', winget_id, '--silent', '--accept-package-agreements', '--accept-source-agreements']
            self.log_callback(f"🔧 Commande WinGet: {' '.join(cmd)}", "info")
            
            # Vérifier si admin requis
            admin_required = program_info.get('admin_required', True)
            
            if admin_required:
                # Exécuter avec privilèges admin
                success, returncode, stdout, stderr = run_as_admin_silent(cmd, timeout=300)
                
                if success or returncode == 0:
                    self.log_callback(f"✅ {program_info['name']} installé via winget", "success")
                    return True
                else:
                    self.log_callback(f"❌ Erreur winget (code {returncode}):", "error")
                    self.log_callback(f"STDOUT: {stdout if stdout else '(vide)'}", "error")
                    self.log_callback(f"STDERR: {stderr if stderr else '(vide)'}", "error")
                    return False
            else:
                # Exécuter sans privilèges admin
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                if result.returncode == 0:
                    self.log_callback(f"✅ {program_info['name']} installé via winget", "success")
                    return True
                else:
                    self.log_callback(f"❌ Erreur winget (code {result.returncode}):", "error")
                    self.log_callback(f"STDOUT: {result.stdout if result.stdout else '(vide)'}", "error")
                    self.log_callback(f"STDERR: {result.stderr if result.stderr else '(vide)'}", "error")
                    return False
                    
        except subprocess.TimeoutExpired:
            self.log_callback(f"⏱️ Timeout installation winget pour {winget_id}", "warning")
            return False
        except Exception as e:
            self.log_callback(f"❌ Erreur installation winget: {e}", "error")
            return False

    def install_via_chocolatey(self, choco_id, program_info):
        """
        Installe un programme via Chocolatey

        Args:
            choco_id: ID Chocolatey du programme
            program_info: Informations du programme

        Returns:
            bool: True si l'installation a réussi
        """
        try:
            self.log_callback(f"🍫 Installation via Chocolatey: {choco_id}", "info")

            # Construire la commande chocolatey
            cmd = ['choco', 'install', choco_id, '-y', '--no-progress', '--ignore-checksums']
            self.log_callback(f"🔧 Commande Chocolatey: {' '.join(cmd)}", "info")

            # Chocolatey nécessite toujours des privilèges admin
            success, returncode, stdout, stderr = run_as_admin_silent(cmd, timeout=300)

            if success or returncode == 0:
                self.log_callback(f"✅ Installation réussie via Chocolatey", "success")
                return True
            else:
                self.log_callback(f"❌ Erreur Chocolatey (code {returncode}):", "error")
                self.log_callback(f"STDOUT: {stdout if stdout else '(vide)'}", "error")
                self.log_callback(f"STDERR: {stderr if stderr else '(vide)'}", "error")
                return False

        except subprocess.TimeoutExpired:
            self.log_callback(f"⏱️ Timeout installation Chocolatey pour {choco_id}", "warning")
            return False
        except Exception as e:
            self.log_callback(f"❌ Erreur installation Chocolatey: {e}", "error")
            return False

    def verify_file_hash(self, file_path, expected_hash):
        """
        Vérifie le hash SHA256 d'un fichier
        
        Args:
            file_path: Chemin vers le fichier
            expected_hash: Hash SHA256 attendu
            
        Returns:
            bool: True si le hash correspond
        """
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            calculated_hash = sha256_hash.hexdigest()
            return calculated_hash.lower() == expected_hash.lower()
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification du hash: {e}")
            return False
    
    def stop_installation(self):
        """Arrête l'installation en cours"""
        self.stop_requested = True
        if self.current_process:
            try:
                self.current_process.terminate()
                time.sleep(2)
                if self.current_process.poll() is None:
                    self.current_process.kill()
            except Exception as e:
                self.logger.error(f"Erreur lors de l'arrêt du processus: {e}")
        
        self.logger.info("Arrêt de l'installation demandé")
    
    def get_download_size(self, url):
        """Obtient la taille d'un fichier à télécharger"""
        try:
            response = requests.head(url, timeout=10)
            return int(response.headers.get('content-length', 0))
        except Exception as e:
            self.logger.warning(f"Impossible d'obtenir la taille du fichier: {e}")
            return 0