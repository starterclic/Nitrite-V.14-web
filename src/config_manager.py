"""
Gestionnaire de configuration pour NiTrite v.2
"""

import json
import logging
from pathlib import Path
import os
import sys

class ConfigManager:
    """Gestionnaire de configuration de l'application"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Déterminer le bon dossier data (compatible PyInstaller)
        if getattr(sys, 'frozen', False):
            # Mode exécutable : utiliser le dossier de l'exécutable
            app_dir = Path(sys.executable).parent
            # PyInstaller extrait les données dans _MEIPASS
            if hasattr(sys, '_MEIPASS'):
                # Pour lire les données embarquées
                self.data_source = Path(sys._MEIPASS) / 'data'
            else:
                self.data_source = app_dir / 'data'
            # Pour écrire les fichiers (logs, config)
            self.config_dir = app_dir / 'data'
        else:
            # Mode script : utiliser le dossier du script
            self.data_source = Path(__file__).parent.parent / 'data'
            self.config_dir = self.data_source
        
        self.config_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / 'config.json'
        self.programs_file = self.config_dir / 'programs.json'
        
        # Configuration par défaut
        self.default_config = {
            'app_version': '2.0.0',
            'language': 'fr',
            'auto_cleanup': True,
            'max_concurrent_downloads': 3,
            'download_timeout': 300,
            'install_timeout': 600,
            'verify_signatures': True,
            'create_restore_point': False,
            'log_level': 'INFO'
        }
        
        self.config = self.default_config.copy()
    
    def load_config(self):
        """Charge la configuration depuis le fichier"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # Fusionner avec la configuration par défaut
                self.config.update(loaded_config)
                self.logger.info("Configuration chargée")
            else:
                # Créer le fichier de configuration par défaut
                self.save_config()
                self.logger.info("Configuration par défaut créée")
                
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la configuration: {e}")
            self.config = self.default_config.copy()
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.logger.info("Configuration sauvegardée")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de la configuration: {e}")
    
    def get(self, key, default=None):
        """Récupère une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Définit une valeur de configuration"""
        self.config[key] = value
    
    def create_programs_database(self):
        """Crée la base de données des programmes"""
        programs_db = {
            "firefox": {
                "name": "Mozilla Firefox",
                "description": "Navigateur web open source",
                "category": "Navigateurs",
                "download_url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=fr",
                "install_args": ["/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Mozilla\\Mozilla Firefox",
                "cleanup_after_install": True
            },
            "chrome": {
                "name": "Google Chrome",
                "description": "Navigateur web de Google",
                "category": "Navigateurs",
                "download_url": "https://dl.google.com/chrome/install/chrome_installer.exe",
                "install_args": ["/silent", "/install"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Google\\Chrome",
                "cleanup_after_install": True
            },
            "vscode": {
                "name": "Visual Studio Code",
                "description": "Éditeur de code source",
                "category": "Développement",
                "download_url": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64",
                "install_args": ["/VERYSILENT", "/NORESTART", "/MERGETASKS=!runcode"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{EA457B21-F73E-494C-ACAB-524FDE069978}_is1",
                "cleanup_after_install": True
            },
            "git": {
                "name": "Git for Windows",
                "description": "Système de contrôle de version",
                "category": "Développement",
                "download_url": "https://github.com/git-for-windows/git/releases/latest/download/Git-2.42.0.2-64-bit.exe",
                "install_args": ["/VERYSILENT", "/NORESTART"],
                "install_type": "exe",
                "check_command": "git --version",
                "cleanup_after_install": True
            },
            "python": {
                "name": "Python 3.11",
                "description": "Langage de programmation Python",
                "category": "Développement",
                "download_url": "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe",
                "install_args": ["/quiet", "InstallAllUsers=1", "PrependPath=1"],
                "install_type": "exe",
                "check_command": "python --version",
                "cleanup_after_install": True
            },
            "nodejs": {
                "name": "Node.js",
                "description": "Runtime JavaScript",
                "category": "Développement",
                "download_url": "https://nodejs.org/dist/v18.18.2/node-v18.18.2-x64.msi",
                "install_args": [],
                "install_type": "msi",
                "check_command": "node --version",
                "cleanup_after_install": True
            },
            "notepadplusplus": {
                "name": "Notepad++",
                "description": "Éditeur de texte avancé",
                "category": "Développement",
                "download_url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.7/npp.8.5.7.Installer.x64.exe",
                "install_args": ["/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Notepad++",
                "cleanup_after_install": True
            },
            "libreoffice": {
                "name": "LibreOffice",
                "description": "Suite bureautique open source",
                "category": "Bureautique",
                "download_url": "https://download.libreoffice.org/libreoffice/stable/7.6.2/win/x86_64/LibreOffice_7.6.2_Win_x64.msi",
                "install_args": ["/passive", "/norestart"],
                "install_type": "msi",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\LibreOffice",
                "cleanup_after_install": True
            },
            "vlc": {
                "name": "VLC Media Player",
                "description": "Lecteur multimédia",
                "category": "Multimédia",
                "download_url": "https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe",
                "install_args": ["/L=1036", "/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\VideoLAN\\VLC",
                "cleanup_after_install": True
            },
            "pdf_reader": {
                "name": "Adobe Acrobat Reader DC",
                "description": "Lecteur de fichiers PDF",
                "category": "Bureautique",
                "download_url": "https://ardownload2.adobe.com/pub/adobe/reader/win/AcrobatDC/2300820360/AcroRdrDC2300820360_fr_FR.exe",
                "install_args": ["/sAll", "/rs", "/msi"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Adobe\\Acrobat Reader",
                "cleanup_after_install": True
            },
            "winrar": {
                "name": "WinRAR",
                "description": "Logiciel de compression",
                "category": "Utilitaires",
                "download_url": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-623fr.exe",
                "install_args": ["/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\WinRAR",
                "cleanup_after_install": True
            },
            "7zip": {
                "name": "7-Zip",
                "description": "Archiveur de fichiers open source",
                "category": "Utilitaires",
                "download_url": "https://www.7-zip.org/a/7z2301-x64.exe",
                "install_args": ["/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\7-Zip",
                "cleanup_after_install": True
            },
            "discord": {
                "name": "Discord",
                "description": "Application de communication",
                "category": "Communication",
                "download_url": "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64",
                "install_args": ["--silent"],
                "install_type": "exe",
                "check_file": "%LOCALAPPDATA%\\Discord\\Discord.exe",
                "cleanup_after_install": True
            },
            "steam": {
                "name": "Steam",
                "description": "Plateforme de jeux vidéo",
                "category": "Jeux",
                "download_url": "https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe",
                "install_args": ["/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Valve\\Steam",
                "cleanup_after_install": True
            },
            "teamviewer": {
                "name": "TeamViewer",
                "description": "Logiciel de prise de contrôle à distance",
                "category": "Utilitaires",
                "download_url": "https://download.teamviewer.com/download/TeamViewer_Setup.exe",
                "install_args": ["/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\TeamViewer",
                "cleanup_after_install": True
            },
            "malwarebytes": {
                "name": "Malwarebytes",
                "description": "Logiciel anti-malware",
                "category": "Sécurité",
                "download_url": "https://data-cdn.mbamupdates.com/web/mb4-setup-consumer/MBSetup.exe",
                "install_args": ["/VERYSILENT", "/NORESTART"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Malwarebytes",
                "cleanup_after_install": True
            },
            "ccleaner": {
                "name": "CCleaner",
                "description": "Nettoyeur de système",
                "category": "Utilitaires",
                "download_url": "https://download.ccleaner.com/ccsetup605.exe",
                "install_args": ["/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Piriform\\CCleaner",
                "cleanup_after_install": True
            },
            "putty": {
                "name": "PuTTY",
                "description": "Client SSH/Telnet",
                "category": "Développement",
                "download_url": "https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.78-installer.msi",
                "install_args": ["/quiet"],
                "install_type": "msi",
                "check_file": "C:\\Program Files\\PuTTY\\putty.exe",
                "cleanup_after_install": True
            },
            "filezilla": {
                "name": "FileZilla Client",
                "description": "Client FTP",
                "category": "Développement",
                "download_url": "https://download.filezilla-project.org/client/FileZilla_3.65.0_win64_sponsored-setup.exe",
                "install_args": ["/user=all", "/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\FileZilla Client",
                "cleanup_after_install": True
            },
            "wireshark": {
                "name": "Wireshark",
                "description": "Analyseur de protocoles réseau",
                "category": "Développement",
                "download_url": "https://1.na.dl.wireshark.org/win64/Wireshark-win64-4.0.8.exe",
                "install_args": ["/S"],
                "install_type": "exe",
                "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Wireshark",
                "cleanup_after_install": True
            }
        }
        
        try:
            with open(self.programs_file, 'w', encoding='utf-8') as f:
                json.dump(programs_db, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Base de données des programmes créée avec {len(programs_db)} programmes")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création de la base de données: {e}")
    
    def load_programs_database(self):
        """Charge la base de données des programmes"""
        try:
            # En mode PyInstaller, charger depuis le dossier embarqué
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                source_file = self.data_source / 'programs.json'
                # Si le fichier n'existe pas dans le dossier de l'exe, utiliser celui embarqué
                if not self.programs_file.exists() and source_file.exists():
                    with open(source_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    # Copier dans le dossier de l'exe pour les futures modifications
                    with open(self.programs_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    return data
            
            if not self.programs_file.exists():
                self.create_programs_database()
            
            with open(self.programs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la base de données: {e}")
            return {}
    
    def add_custom_program(self, program_id, program_info):
        """Ajoute un programme personnalisé"""
        try:
            programs_db = self.load_programs_database()
            programs_db[program_id] = program_info
            
            with open(self.programs_file, 'w', encoding='utf-8') as f:
                json.dump(programs_db, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Programme personnalisé ajouté: {program_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout du programme: {e}")
            return False
    
    def remove_program(self, program_id):
        """Supprime un programme de la base de données"""
        try:
            programs_db = self.load_programs_database()
            if program_id in programs_db:
                del programs_db[program_id]
                
                with open(self.programs_file, 'w', encoding='utf-8') as f:
                    json.dump(programs_db, f, indent=4, ensure_ascii=False)
                
                self.logger.info(f"Programme supprimé: {program_id}")
                return True
            else:
                self.logger.warning(f"Programme non trouvé: {program_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression du programme: {e}")
            return False
    
    def update_program(self, program_id, program_info):
        """Met à jour les informations d'un programme"""
        try:
            programs_db = self.load_programs_database()
            if program_id in programs_db:
                programs_db[program_id].update(program_info)
                
                with open(self.programs_file, 'w', encoding='utf-8') as f:
                    json.dump(programs_db, f, indent=4, ensure_ascii=False)
                
                self.logger.info(f"Programme mis à jour: {program_id}")
                return True
            else:
                self.logger.warning(f"Programme non trouvé: {program_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour du programme: {e}")
            return False
    
    def export_config(self, export_path):
        """Exporte la configuration vers un fichier"""
        try:
            export_data = {
                'config': self.config,
                'programs': self.load_programs_database()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Configuration exportée vers: {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'export: {e}")
            return False
    
    def import_config(self, import_path):
        """Importe la configuration depuis un fichier"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'config' in import_data:
                self.config.update(import_data['config'])
                self.save_config()
            
            if 'programs' in import_data:
                with open(self.programs_file, 'w', encoding='utf-8') as f:
                    json.dump(import_data['programs'], f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Configuration importée depuis: {import_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'import: {e}")
            return False
    
    def load_programs_from_file(self, file_path):
        """Charge les programmes depuis un fichier JSON spécifique"""
        try:
            file_path = Path(file_path)
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    programs_data = json.load(f)
                    # Sauvegarder dans le fichier programs.json local
                    with open(self.programs_file, 'w', encoding='utf-8') as f2:
                        json.dump(programs_data, f2, indent=4, ensure_ascii=False)
                    self.logger.info(f"✅ Programmes chargés depuis {file_path}")
                    self.logger.info(f"📊 {self.get_programs_count(programs_data)} programmes disponibles")
                    return True
            else:
                self.logger.warning(f"⚠️ Fichier non trouvé : {file_path}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du chargement depuis {file_path} : {e}")
            return False
    
    def get_programs(self):
        """Retourne tous les programmes organisés par catégorie"""
        return self.load_programs_database()
    
    def get_programs_count(self, programs_data=None):
        """Retourne le nombre total de programmes"""
        if programs_data is None:
            programs_data = self.load_programs_database()
        
        count = 0
        for category in programs_data.values():
            if isinstance(category, dict):
                count += len(category)
        return count
    
    def get_all_programs_flat(self):
        """Retourne tous les programmes de toutes catégories dans un dictionnaire plat"""
        programs_db = self.load_programs_database()
        all_programs = {}
        for category, programs in programs_db.items():
            if isinstance(programs, dict):
                all_programs.update(programs)
        return all_programs