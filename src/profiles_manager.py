#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Profils d'Installation
Permet de créer et gérer des profils prédéfinis pour différents cas d'usage
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set
import logging

# Import du module de chemins portables pour mode 100% portable
try:
    from .portable_paths import get_portable_config_dir
except ImportError:
    from portable_paths import get_portable_config_dir

logger = logging.getLogger(__name__)


class ProfilesManager:
    """Gestionnaire de profils d'installation prédéfinis"""

    # Profils prédéfinis
    PREDEFINED_PROFILES = {
        "🎮 Gaming Station": {
            "description": "Configuration optimale pour un PC gaming",
            "applications": [
                "Steam", "Epic Games Store", "Battle.net", "Discord",
                "OBS Studio", "MSI Afterburner", "GeForce Experience",
                "7-Zip", "WinRAR", "VLC Media Player", "Spotify",
                "Google Chrome", "TeamSpeak", "Razer Synapse"
            ],
            "icon": "🎮",
            "color": "#7c4dff"
        },
        "💼 Bureau Professionnel": {
            "description": "Suite complète pour environnement de bureau",
            "applications": [
                "Microsoft Office", "LibreOffice", "Adobe Acrobat Reader",
                "Google Chrome", "Mozilla Firefox", "7-Zip",
                "VLC Media Player", "Microsoft Teams", "Zoom",
                "Slack", "Notepad++", "WinRAR", "TeamViewer"
            ],
            "icon": "💼",
            "color": "#0066cc"
        },
        "💻 Développeur": {
            "description": "Environnement de développement complet",
            "applications": [
                "Visual Studio Code", "Git", "GitHub Desktop",
                "Node.js", "Python", "Docker Desktop",
                "Postman", "FileZilla", "PuTTY", "WinSCP",
                "Notepad++", "Google Chrome", "Firefox Developer Edition",
                "Windows Terminal", "Visual Studio Community"
            ],
            "icon": "💻",
            "color": "#00e676"
        },
        "🎨 Création Multimédia": {
            "description": "Outils de création photo, vidéo et audio",
            "applications": [
                "Adobe Photoshop", "GIMP", "Inkscape", "Blender",
                "Audacity", "OBS Studio", "DaVinci Resolve",
                "VLC Media Player", "HandBrake", "Paint.NET",
                "Krita", "Adobe Premiere Pro", "FL Studio"
            ],
            "icon": "🎨",
            "color": "#ff6b00"
        },
        "🏫 Étudiant": {
            "description": "Pack essentiel pour étudiants",
            "applications": [
                "Microsoft Office", "LibreOffice", "Adobe Acrobat Reader",
                "Google Chrome", "Zoom", "Microsoft Teams",
                "Notepad++", "7-Zip", "VLC Media Player",
                "Spotify", "Discord", "Dropbox", "OneDrive"
            ],
            "icon": "🏫",
            "color": "#ffd600"
        },
        "🔧 Maintenance Technique": {
            "description": "Outils pour techniciens informatique",
            "applications": [
                "CCleaner", "Malwarebytes", "CrystalDiskInfo",
                "HWiNFO", "CPU-Z", "GPU-Z", "MSI Afterburner",
                "Rufus", "Ventoy", "7-Zip", "WinRAR",
                "TeamViewer", "AnyDesk", "PuTTY", "WinSCP",
                "Notepad++", "Google Chrome"
            ],
            "icon": "🔧",
            "color": "#ff1744"
        },
        "🏠 Maison/Famille": {
            "description": "Applications essentielles pour usage domestique",
            "applications": [
                "Google Chrome", "VLC Media Player", "Spotify",
                "WhatsApp", "Skype", "Zoom", "7-Zip",
                "Adobe Acrobat Reader", "LibreOffice", "GIMP",
                "Dropbox", "OneDrive", "Malwarebytes"
            ],
            "icon": "🏠",
            "color": "#00b0ff"
        },
        "⚡ Installation Express": {
            "description": "Pack minimal pour démarrage rapide",
            "applications": [
                "Google Chrome", "7-Zip", "VLC Media Player",
                "Adobe Acrobat Reader", "Notepad++", "Microsoft Office"
            ],
            "icon": "⚡",
            "color": "#ff8533"
        },
        "🎬 Home Cinema": {
            "description": "Configuration pour PC média/entertainment",
            "applications": [
                "VLC Media Player", "Kodi", "Plex Media Player",
                "Spotify", "Netflix", "Disney+", "YouTube",
                "HandBrake", "MPC-HC", "K-Lite Codec Pack",
                "Audacity", "iTunes"
            ],
            "icon": "🎬",
            "color": "#e91e63"
        },
        "🌐 Télétravail": {
            "description": "Outils essentiels pour travail à distance",
            "applications": [
                "Microsoft Teams", "Zoom", "Slack", "Discord",
                "TeamViewer", "AnyDesk", "Google Chrome",
                "Microsoft Office", "OneDrive", "Dropbox",
                "Notepad++", "Adobe Acrobat Reader", "7-Zip",
                "VLC Media Player"
            ],
            "icon": "🌐",
            "color": "#9c27b0"
        }
    }

    def __init__(self, config_dir=None):
        """Initialiser le gestionnaire de profils"""
        if config_dir is None:
            # MODE PORTABLE: Utiliser le dossier à côté de l'exe
            # Au lieu de C:\Users\[User]\.nitrite\profiles (NON portable)
            # On utilise [ExeDir]\config\profiles (PORTABLE)
            config_dir = get_portable_config_dir() / 'profiles'
        else:
            config_dir = Path(config_dir)

        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Profils stockés dans: {self.config_dir} (mode portable)")

        self.profiles_file = self.config_dir / 'profiles.json'
        self.favorites_file = self.config_dir / 'favorites.json'
        self.history_file = self.config_dir / 'history.json'

        # Charger les données
        self.custom_profiles = self._load_custom_profiles()
        self.favorites = self._load_favorites()
        self.history = self._load_history()

    def _load_custom_profiles(self) -> Dict:
        """Charger les profils personnalisés"""
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erreur lors du chargement des profils : {e}")
        return {}

    def _save_custom_profiles(self):
        """Sauvegarder les profils personnalisés"""
        try:
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.custom_profiles, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des profils : {e}")

    def _load_favorites(self) -> Set[str]:
        """Charger les applications favorites"""
        if self.favorites_file.exists():
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            except Exception as e:
                logger.error(f"Erreur lors du chargement des favoris : {e}")
        return set()

    def _save_favorites(self):
        """Sauvegarder les favoris"""
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.favorites), f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des favoris : {e}")

    def _load_history(self) -> List[Dict]:
        """Charger l'historique des installations"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erreur lors du chargement de l'historique : {e}")
        return []

    def _save_history(self):
        """Sauvegarder l'historique"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history[-100:], f, indent=2, ensure_ascii=False)  # Garder les 100 derniers
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de l'historique : {e}")

    def get_all_profiles(self) -> Dict:
        """Obtenir tous les profils (prédéfinis + personnalisés)"""
        all_profiles = self.PREDEFINED_PROFILES.copy()
        all_profiles.update(self.custom_profiles)
        return all_profiles

    def get_profile_apps(self, profile_name: str) -> List[str]:
        """Obtenir la liste des applications d'un profil"""
        all_profiles = self.get_all_profiles()
        if profile_name in all_profiles:
            return all_profiles[profile_name].get('applications', [])
        return []

    def create_profile(self, name: str, description: str, applications: List[str],
                      icon: str = "📦", color: str = "#ff6b00"):
        """Créer un nouveau profil personnalisé"""
        self.custom_profiles[name] = {
            "description": description,
            "applications": applications,
            "icon": icon,
            "color": color
        }
        self._save_custom_profiles()
        logger.info(f"Profil créé : {name}")

    def delete_profile(self, name: str) -> bool:
        """Supprimer un profil personnalisé"""
        if name in self.custom_profiles:
            del self.custom_profiles[name]
            self._save_custom_profiles()
            logger.info(f"Profil supprimé : {name}")
            return True
        return False

    def add_favorite(self, app_name: str):
        """Ajouter une application aux favoris"""
        self.favorites.add(app_name)
        self._save_favorites()
        logger.info(f"Favori ajouté : {app_name}")

    def remove_favorite(self, app_name: str):
        """Retirer une application des favoris"""
        self.favorites.discard(app_name)
        self._save_favorites()
        logger.info(f"Favori retiré : {app_name}")

    def is_favorite(self, app_name: str) -> bool:
        """Vérifier si une application est favorite"""
        return app_name in self.favorites

    def get_favorites(self) -> Set[str]:
        """Obtenir toutes les applications favorites"""
        return self.favorites.copy()

    def add_to_history(self, app_name: str, success: bool = True):
        """Ajouter une installation à l'historique"""
        from datetime import datetime

        entry = {
            "app": app_name,
            "timestamp": datetime.now().isoformat(),
            "success": success
        }
        self.history.append(entry)
        self._save_history()

    def get_history(self, limit: int = 20) -> List[Dict]:
        """Obtenir l'historique récent"""
        return self.history[-limit:]

    def get_most_installed(self, limit: int = 10) -> List[tuple]:
        """Obtenir les applications les plus installées"""
        from collections import Counter

        # Compter les occurrences
        app_counts = Counter(entry['app'] for entry in self.history if entry.get('success', False))

        # Retourner les plus fréquents
        return app_counts.most_common(limit)

    def clear_history(self):
        """Effacer l'historique"""
        self.history.clear()
        self._save_history()
        logger.info("Historique effacé")

    def export_profile(self, profile_name: str, export_path: str) -> bool:
        """Exporter un profil vers un fichier JSON"""
        all_profiles = self.get_all_profiles()
        if profile_name not in all_profiles:
            return False

        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "name": profile_name,
                    "data": all_profiles[profile_name]
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Profil exporté : {profile_name} -> {export_path}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'export du profil : {e}")
            return False

    def import_profile(self, import_path: str) -> bool:
        """Importer un profil depuis un fichier JSON"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            name = data.get('name')
            profile_data = data.get('data')

            if name and profile_data:
                self.custom_profiles[name] = profile_data
                self._save_custom_profiles()
                logger.info(f"Profil importé : {name}")
                return True
        except Exception as e:
            logger.error(f"Erreur lors de l'import du profil : {e}")
        return False


class SystemScanner:
    """Scanner de système pour détecter les applications manquantes"""

    def __init__(self):
        """Initialiser le scanner"""
        self.logger = logging.getLogger(__name__)

    def get_installed_apps(self) -> Set[str]:
        """Obtenir la liste des applications installées sur le système"""
        installed = set()

        try:
            # Scanner le registre Windows (méthode 1)
            installed.update(self._scan_registry())

            # Scanner Program Files (méthode 2)
            installed.update(self._scan_program_files())

            # Scanner avec WinGet (méthode 3)
            installed.update(self._scan_winget())

        except Exception as e:
            self.logger.error(f"Erreur lors du scan des applications : {e}")

        return installed

    def _scan_registry(self) -> Set[str]:
        """Scanner le registre Windows pour les applications installées"""
        installed = set()

        if not hasattr(os, 'name') or os.name != 'nt':
            return installed

        try:
            import winreg

            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]

            for hkey, path in registry_paths:
                try:
                    key = winreg.OpenKey(hkey, path)
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey = winreg.OpenKey(key, subkey_name)
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                installed.add(name)
                            except:
                                pass
                            winreg.CloseKey(subkey)
                        except:
                            pass
                    winreg.CloseKey(key)
                except:
                    pass

        except Exception as e:
            self.logger.warning(f"Erreur lors du scan du registre : {e}")

        return installed

    def _scan_program_files(self) -> Set[str]:
        """Scanner les dossiers Program Files"""
        installed = set()

        program_paths = [
            Path(os.environ.get('ProgramFiles', 'C:\\Program Files')),
            Path(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')),
            Path(os.environ.get('LocalAppData', '')) / 'Programs'
        ]

        for path in program_paths:
            if path.exists():
                try:
                    for item in path.iterdir():
                        if item.is_dir():
                            installed.add(item.name)
                except Exception as e:
                    self.logger.warning(f"Erreur lors du scan de {path} : {e}")

        return installed

    def _scan_winget(self) -> Set[str]:
        """Scanner avec WinGet list"""
        installed = set()

        try:
            import subprocess
            result = subprocess.run(
                ['winget', 'list'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines[2:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if parts:
                            installed.add(parts[0])

        except Exception as e:
            self.logger.warning(f"Erreur lors du scan WinGet : {e}")

        return installed

    def find_missing_apps(self, desired_apps: List[str], programs_data: Dict) -> List[str]:
        """Trouver les applications manquantes par rapport à une liste désirée"""
        installed = self.get_installed_apps()
        installed_lower = {app.lower() for app in installed}

        missing = []
        for app_name in desired_apps:
            # Vérifier si l'app est installée (recherche insensible à la casse)
            if app_name.lower() not in installed_lower:
                # Vérifier aussi les variantes du nom
                found = False
                for installed_name in installed_lower:
                    if app_name.lower() in installed_name or installed_name in app_name.lower():
                        found = True
                        break

                if not found:
                    missing.append(app_name)

        return missing

    def suggest_apps_for_profile(self, profile_name: str, programs_data: Dict,
                                profiles_manager: ProfilesManager) -> List[str]:
        """Suggérer les applications manquantes pour un profil"""
        profile_apps = profiles_manager.get_profile_apps(profile_name)
        return self.find_missing_apps(profile_apps, programs_data)
