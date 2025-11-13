"""
Gestionnaire d'installation via Winget
Utilise le gestionnaire de paquets Windows officiel pour des installations fiables
"""

import subprocess
import logging
from typing import Dict, List, Optional, Callable
from pathlib import Path
import json
import sys
import os
import ctypes

logger = logging.getLogger(__name__)


def is_admin():
    """Vérifie si le script s'exécute avec des privilèges administrateur"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def request_admin_privileges():
    """Relance le script avec des privilèges administrateur"""
    if not is_admin():
        logger.info("⚡ Demande de privilèges administrateur...")
        try:
            # Relancer le script en tant qu'administrateur
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                " ".join(sys.argv),
                None,
                1
            )
            sys.exit(0)
        except Exception as e:
            logger.warning(f"⚠️ Impossible d'obtenir les privilèges admin: {e}")
            return False
    return True


class WingetManager:
    """Gestionnaire d'installation via Winget"""
    
    def __init__(self, auto_elevate=False):
        """
        Initialise le gestionnaire Winget
        
        Args:
            auto_elevate: Si True, demande automatiquement les privilèges admin si nécessaire
        """
        if auto_elevate and not is_admin():
            logger.info("🔐 Mode auto-élévation activé")
            request_admin_privileges()
        
        self.is_admin = is_admin()
        self.winget_available = self._check_winget()
        self.programs_db = self._load_winget_programs()
        
        if self.is_admin:
            logger.info("✅ Exécution avec privilèges administrateur")
        else:
            logger.info("ℹ️ Exécution en mode utilisateur standard")
        
    def _check_winget(self) -> bool:
        """Vérifie si Winget est disponible"""
        try:
            result = subprocess.run(
                ['winget', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"✅ Winget disponible: {result.stdout.strip()}")
                return True
        except Exception as e:
            logger.warning(f"⚠️ Winget non disponible: {e}")
        return False
    
    def _load_winget_programs(self) -> Dict:
        """Charge la base de données des programmes Winget"""
        programs = {
            # ===== OUTILS ORDIPLUS ===== (CATÉGORIE PRIORITAIRE)
            "Outils OrdiPlus": {
                "AnyDesk": {
                    "winget_id": "AnyDesk.AnyDesk",
                    "description": "Accès à distance et contrôle à distance",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "RustDesk": {
                    "winget_id": "RustDesk.RustDesk",
                    "description": "Alternative open source à TeamViewer",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "Spybot Search & Destroy": {
                    "winget_id": "SaferNetworking.SpybotSearchAndDestroy",
                    "description": "Anti-malware et anti-spyware",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "Malwarebytes": {
                    "winget_id": "Malwarebytes.Malwarebytes",
                    "description": "Protection contre les malwares",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "AdwCleaner": {
                    "winget_id": "Malwarebytes.AdwCleaner",
                    "description": "Suppression d'adwares et programmes indésirables",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "Wise Disk Cleaner": {
                    "winget_id": "WiseCleaner.WiseDiskCleaner",
                    "description": "Nettoyage et optimisation de disque",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "Adobe Acrobat Reader": {
                    "winget_id": "Adobe.Acrobat.Reader.64-bit",
                    "description": "Lecteur PDF Adobe Acrobat Reader",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "VLC Media Player": {
                    "winget_id": "VideoLAN.VLC",
                    "description": "Lecteur multimédia universel",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "Microsoft Office 2007": {
                    "winget_id": "Microsoft.Office",
                    "description": "Suite bureautique Microsoft Office 2007",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "Microsoft Office 2024": {
                    "winget_id": "Microsoft.Office",
                    "description": "Suite bureautique Microsoft Office 2024",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
                "Microsoft Office 2016": {
                    "winget_id": "Microsoft.Office",
                    "description": "Suite bureautique Microsoft Office 2016",
                    "category": "Outils OrdiPlus",
                    "color": "#FF6600"
                },
            },
            
            # ===== RÉPARATION WINDOWS =====
            "🔧 Réparation Windows": {
                "DISM - Vérifier l'état": {
                    "command": "DISM /Online /Cleanup-Image /CheckHealth",
                    "description": "Vérification rapide de l'état de l'image Windows",
                    "category": "🔧 Réparation Windows",
                    "admin_required": True
                },
                "DISM - Scanner l'image": {
                    "command": "DISM /Online /Cleanup-Image /ScanHealth",
                    "description": "Scan approfondi de l'image Windows (peut prendre du temps)",
                    "category": "🔧 Réparation Windows",
                    "admin_required": True
                },
                "DISM - Réparer l'image": {
                    "command": "DISM /Online /Cleanup-Image /RestoreHealth",
                    "description": "Répare l'image Windows en utilisant Windows Update",
                    "category": "🔧 Réparation Windows",
                    "admin_required": True
                },
                "DISM - Nettoyer les composants": {
                    "command": "DISM /Online /Cleanup-Image /StartComponentCleanup",
                    "description": "Nettoie les composants obsolètes et libère de l'espace",
                    "category": "🔧 Réparation Windows",
                    "admin_required": True
                },
                "DISM - Nettoyage avancé": {
                    "command": "DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase",
                    "description": "Nettoyage approfondi, supprime les sauvegardes de composants",
                    "category": "🔧 Réparation Windows",
                    "admin_required": True
                },
                "SFC - Vérifier fichiers système": {
                    "command": "sfc /scannow",
                    "description": "Scan et réparation des fichiers système corrompus",
                    "category": "🔧 Réparation Windows",
                    "admin_required": True
                },
                "Nettoyer le Windows Store": {
                    "command": "wsreset.exe",
                    "description": "Réinitialise le cache du Microsoft Store",
                    "category": "🔧 Réparation Windows",
                    "admin_required": False
                },
                "Réparer les bases de registre": {
                    "command": "DISM /Online /Cleanup-Image /RestoreHealth & sfc /scannow",
                    "description": "Réparation complète : DISM + SFC (recommandé)",
                    "category": "🔧 Réparation Windows",
                    "admin_required": True
                },
            },
            
            # ===== PARAMÈTRES WINDOWS =====
            "⚙️ Paramètres Windows": {
                "Paramètres Windows": {
                    "command": "start ms-settings:",
                    "description": "Ouvre les Paramètres Windows",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Réseau et Internet": {
                    "command": "start ms-settings:network",
                    "description": "Configuration réseau, Wi-Fi, Ethernet, VPN",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Bluetooth et appareils": {
                    "command": "start ms-settings:bluetooth",
                    "description": "Gestion Bluetooth, imprimantes, souris, clavier",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Imprimantes et scanners": {
                    "command": "start ms-settings:printers",
                    "description": "Ajouter et gérer imprimantes et scanners",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Son": {
                    "command": "start ms-settings:sound",
                    "description": "Volume, périphériques audio, mixage",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Clavier": {
                    "command": "start ms-settings:typing",
                    "description": "Paramètres du clavier et saisie",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Activation Windows": {
                    "command": "start ms-settings:activation",
                    "description": "Vérifier l'activation de Windows",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Informations système": {
                    "command": "start ms-settings:about",
                    "description": "Version Windows, spécifications, nom du PC",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Mode développeur": {
                    "command": "start ms-settings:developers",
                    "description": "Activer le mode développeur, PowerShell",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Sécurité Windows": {
                    "command": "start windowsdefender:",
                    "description": "Antivirus, pare-feu, protection",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Personnalisation": {
                    "command": "start ms-settings:personalization",
                    "description": "Thème, couleurs, arrière-plan, écran de verrouillage",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Affichage": {
                    "command": "start ms-settings:display",
                    "description": "Résolution, orientation, échelle, HDR",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Alimentation et batterie": {
                    "command": "start ms-settings:powersleep",
                    "description": "Mode veille, économiseur d'énergie",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Panneau de configuration": {
                    "command": "control",
                    "description": "Panneau de configuration classique",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Outils d'administration": {
                    "command": "control admintools",
                    "description": "Outils d'administration Windows",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Configuration système (msconfig)": {
                    "command": "msconfig",
                    "description": "Démarrage, services, options de démarrage",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": True
                },
                "Propriétés système (sysdm.cpl)": {
                    "command": "sysdm.cpl",
                    "description": "Nom ordinateur, domaine, variables d'environnement",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Gestionnaire de périphériques": {
                    "command": "devmgmt.msc",
                    "description": "Pilotes et matériel",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
                "Panneau NVIDIA": {
                    "command": "start shell:AppsFolder\\NVIDIACorp.NVIDIAControlPanel_56jybvy8sckqj!NVIDIACorp.NVIDIAControlPanel",
                    "description": "Paramètres carte graphique NVIDIA (si installée)",
                    "category": "⚙️ Paramètres Windows",
                    "admin_required": False
                },
            },
            
            # ===== NAVIGATEURS =====
            "Navigateurs": {
                "Google Chrome": {
                    "winget_id": "Google.Chrome",
                    "description": "Navigateur web de Google",
                    "category": "Navigateurs"
                },
                "Mozilla Firefox": {
                    "winget_id": "Mozilla.Firefox",
                    "description": "Navigateur web open source",
                    "category": "Navigateurs"
                },
                "Microsoft Edge": {
                    "winget_id": "Microsoft.Edge",
                    "description": "Navigateur web de Microsoft",
                    "category": "Navigateurs"
                },
                "Brave Browser": {
                    "winget_id": "Brave.Brave",
                    "description": "Navigateur axé sur la confidentialité",
                    "category": "Navigateurs"
                },
                "Opera": {
                    "winget_id": "Opera.Opera",
                    "description": "Navigateur web avec VPN intégré",
                    "category": "Navigateurs"
                },
                "Vivaldi": {
                    "winget_id": "VivaldiTechnologies.Vivaldi",
                    "description": "Navigateur hautement personnalisable",
                    "category": "Navigateurs"
                },
                "Tor Browser": {
                    "winget_id": "TorProject.TorBrowser",
                    "description": "Navigateur pour la navigation anonyme",
                    "category": "Navigateurs"
                },
                "DuckDuckGo Browser": {
                    "winget_id": "DuckDuckGo.DesktopBrowser",
                    "description": "Navigateur axé sur la confidentialité et anti-tracking",
                    "category": "Navigateurs"
                },
            },
            
            # ===== COMMUNICATION =====
            "Communication": {
                "Discord": {
                    "winget_id": "Discord.Discord",
                    "description": "Plateforme de communication pour gamers",
                    "category": "Communication"
                },
                "Slack": {
                    "winget_id": "SlackTechnologies.Slack",
                    "description": "Outil de communication d'équipe",
                    "category": "Communication"
                },
                "Microsoft Teams": {
                    "winget_id": "Microsoft.Teams",
                    "description": "Plateforme de collaboration Microsoft",
                    "category": "Communication"
                },
                "Zoom": {
                    "winget_id": "Zoom.Zoom",
                    "description": "Application de visioconférence",
                    "category": "Communication"
                },
                "Skype": {
                    "winget_id": "Microsoft.Skype",
                    "description": "Application de communication Microsoft",
                    "category": "Communication"
                },
                "Telegram Desktop": {
                    "winget_id": "Telegram.TelegramDesktop",
                    "description": "Messagerie instantanée sécurisée",
                    "category": "Communication"
                },
                "WhatsApp": {
                    "winget_id": "WhatsApp.WhatsApp",
                    "description": "Messagerie instantanée",
                    "category": "Communication"
                },
                "Signal": {
                    "winget_id": "OpenWhisperSystems.Signal",
                    "description": "Messagerie chiffrée de bout en bout",
                    "category": "Communication"
                },
            },
            
            # ===== MULTIMÉDIA =====
            "Multimédia": {
                "VLC Media Player": {
                    "winget_id": "VideoLAN.VLC",
                    "description": "Lecteur multimédia universel",
                    "category": "Multimédia"
                },
                "Spotify": {
                    "winget_id": "Spotify.Spotify",
                    "description": "Service de streaming musical",
                    "category": "Multimédia"
                },
                "Audacity": {
                    "winget_id": "Audacity.Audacity",
                    "description": "Éditeur audio open source",
                    "category": "Multimédia"
                },
                "OBS Studio": {
                    "winget_id": "OBSProject.OBSStudio",
                    "description": "Logiciel de streaming et enregistrement",
                    "category": "Multimédia"
                },
                "GIMP": {
                    "winget_id": "GIMP.GIMP",
                    "description": "Éditeur d'images open source",
                    "category": "Multimédia"
                },
                "Paint.NET": {
                    "winget_id": "dotPDN.PaintDotNet",
                    "description": "Éditeur d'images simple et puissant",
                    "category": "Multimédia"
                },
                "Inkscape": {
                    "winget_id": "Inkscape.Inkscape",
                    "description": "Éditeur de graphiques vectoriels",
                    "category": "Multimédia"
                },
                "Blender": {
                    "winget_id": "BlenderFoundation.Blender",
                    "description": "Suite de création 3D",
                    "category": "Multimédia"
                },
                "HandBrake": {
                    "winget_id": "HandBrake.HandBrake",
                    "description": "Convertisseur vidéo",
                    "category": "Multimédia"
                },
                "FFmpeg": {
                    "winget_id": "Gyan.FFmpeg",
                    "description": "Framework multimédia complet",
                    "category": "Multimédia"
                },
            },
            
            # ===== DÉVELOPPEMENT =====
            "Développement": {
                "Visual Studio Code": {
                    "winget_id": "Microsoft.VisualStudioCode",
                    "description": "Éditeur de code de Microsoft",
                    "category": "Développement"
                },
                "Git": {
                    "winget_id": "Git.Git",
                    "description": "Système de contrôle de version",
                    "category": "Développement"
                },
                "GitHub Desktop": {
                    "winget_id": "GitHub.GitHubDesktop",
                    "description": "Client Git graphique de GitHub",
                    "category": "Développement"
                },
                "Python 3.12": {
                    "winget_id": "Python.Python.3.12",
                    "description": "Langage de programmation Python",
                    "category": "Développement"
                },
                "Node.js": {
                    "winget_id": "OpenJS.NodeJS",
                    "description": "Runtime JavaScript",
                    "category": "Développement"
                },
                "Docker Desktop": {
                    "winget_id": "Docker.DockerDesktop",
                    "description": "Plateforme de conteneurisation",
                    "category": "Développement"
                },
                "Postman": {
                    "winget_id": "Postman.Postman",
                    "description": "Plateforme de test API",
                    "category": "Développement"
                },
                "Notepad++": {
                    "winget_id": "Notepad++.Notepad++",
                    "description": "Éditeur de texte avancé",
                    "category": "Développement"
                },
                "Sublime Text": {
                    "winget_id": "SublimeHQ.SublimeText.4",
                    "description": "Éditeur de texte sophistiqué",
                    "category": "Développement"
                },
                "JetBrains Toolbox": {
                    "winget_id": "JetBrains.Toolbox",
                    "description": "Gestionnaire d'IDE JetBrains",
                    "category": "Développement"
                },
                "Android Studio": {
                    "winget_id": "Google.AndroidStudio",
                    "description": "IDE pour développement Android",
                    "category": "Développement"
                },
                "FileZilla": {
                    "winget_id": "TimKosse.FileZilla.Client",
                    "description": "Client FTP open source",
                    "category": "Développement"
                },
                "PuTTY": {
                    "winget_id": "PuTTY.PuTTY",
                    "description": "Client SSH et Telnet pour Windows",
                    "category": "Développement"
                },
            },
            
            # ===== UTILITAIRES =====
            "Utilitaires": {
                "7-Zip": {
                    "winget_id": "7zip.7zip",
                    "description": "Gestionnaire d'archives",
                    "category": "Utilitaires"
                },
                "WinRAR": {
                    "winget_id": "RARLab.WinRAR",
                    "description": "Gestionnaire d'archives complet",
                    "category": "Utilitaires"
                },
                "Everything": {
                    "winget_id": "voidtools.Everything",
                    "description": "Recherche de fichiers ultra-rapide",
                    "category": "Utilitaires"
                },
                "TreeSize Free": {
                    "winget_id": "JAMSoftware.TreeSize.Free",
                    "description": "Analyse de l'espace disque",
                    "category": "Utilitaires"
                },
                "PowerToys": {
                    "winget_id": "Microsoft.PowerToys",
                    "description": "Utilitaires Windows avancés",
                    "category": "Utilitaires"
                },
                "ShareX": {
                    "winget_id": "ShareX.ShareX",
                    "description": "Outil de capture d'écran avancé",
                    "category": "Utilitaires"
                },
                "Greenshot": {
                    "winget_id": "Greenshot.Greenshot",
                    "description": "Outil de capture d'écran",
                    "category": "Utilitaires"
                },
                "Lightshot": {
                    "winget_id": "Skillbrains.Lightshot",
                    "description": "Outil de capture d'écran simple",
                    "category": "Utilitaires"
                },
                "Revo Uninstaller": {
                    "winget_id": "RevoUninstaller.RevoUninstaller",
                    "description": "Désinstalleur avancé",
                    "category": "Utilitaires"
                },
                "CCleaner": {
                    "winget_id": "Piriform.CCleaner",
                    "description": "Nettoyeur système",
                    "category": "Utilitaires"
                },
                "Rufus": {
                    "winget_id": "Rufus.Rufus",
                    "description": "Création de clés USB bootables",
                    "category": "Utilitaires"
                },
                "Speccy": {
                    "winget_id": "Piriform.Speccy",
                    "description": "Informations système détaillées",
                    "category": "Utilitaires"
                },
                "CPU-Z": {
                    "winget_id": "CPUID.CPU-Z",
                    "description": "Informations sur le processeur",
                    "category": "Utilitaires"
                },
                "GPU-Z": {
                    "winget_id": "TechPowerUp.GPU-Z",
                    "description": "Informations sur la carte graphique",
                    "category": "Utilitaires"
                },
                "HWiNFO": {
                    "winget_id": "REALiX.HWiNFO",
                    "description": "Informations matérielles complètes",
                    "category": "Utilitaires"
                },
                "Core Temp": {
                    "winget_id": "ALCPU.CoreTemp",
                    "description": "Surveillance température processeur",
                    "category": "Utilitaires"
                },
            },
            
            # ===== SÉCURITÉ =====
            "Sécurité": {
                "Malwarebytes": {
                    "winget_id": "Malwarebytes.Malwarebytes",
                    "description": "Anti-malware puissant",
                    "category": "Sécurité"
                },
                "Spybot Search & Destroy": {
                    "winget_id": "9MXJPF3M2W50",
                    "description": "Anti-spyware et protection vie privée",
                    "category": "Sécurité"
                },
                "Spybot Anti-Beacon": {
                    "winget_id": "SaferNetworking.SpybotAntiBeacon",
                    "description": "Bloque les pisteurs et télémétrie Windows",
                    "category": "Sécurité"
                },
                "Bitwarden": {
                    "winget_id": "Bitwarden.Bitwarden",
                    "description": "Gestionnaire de mots de passe open source",
                    "category": "Sécurité"
                },
                "KeePass": {
                    "winget_id": "DominikReichl.KeePass",
                    "description": "Gestionnaire de mots de passe",
                    "category": "Sécurité"
                },
                "1Password": {
                    "winget_id": "AgileBits.1Password",
                    "description": "Gestionnaire de mots de passe premium",
                    "category": "Sécurité"
                },
                "NordVPN": {
                    "winget_id": "NordVPN.NordVPN",
                    "description": "Service VPN",
                    "category": "Sécurité"
                },
                "ProtonVPN": {
                    "winget_id": "ProtonTechnologies.ProtonVPN",
                    "description": "VPN sécurisé et privé",
                    "category": "Sécurité"
                },
                "CyberGhost VPN": {
                    "winget_id": "CyberGhost.CyberGhost",
                    "description": "VPN rapide et sécurisé",
                    "category": "Sécurité"
                },
                "VeraCrypt": {
                    "winget_id": "IDRIX.VeraCrypt",
                    "description": "Chiffrement de disque",
                    "category": "Sécurité"
                },
                "AdwCleaner": {
                    "winget_id": "Malwarebytes.AdwCleaner",
                    "description": "Suppression de logiciels publicitaires et malwares",
                    "category": "Sécurité"
                },
                "Wise Disk Cleaner": {
                    "winget_id": "WiseCleaner.WiseDiskCleaner",
                    "description": "Nettoyeur de disque et optimisation sécurité",
                    "category": "Sécurité"
                },
                "Surfshark VPN": {
                    "winget_id": "Surfshark.Surfshark",
                    "description": "VPN rapide et sécurisé avec fonctions avancées",
                    "category": "Sécurité"
                },
                "Wise Data Recovery": {
                    "winget_id": "WiseCleaner.WiseDataRecovery",
                    "description": "Récupération de fichiers supprimés",
                    "category": "Sécurité"
                },
                "Wise Registry Cleaner": {
                    "winget_id": "WiseCleaner.WiseRegistryCleaner",
                    "description": "Nettoyage et optimisation du registre Windows",
                    "category": "Sécurité"
                },
            },
            
            # ===== PRODUCTIVITÉ =====
            "Productivité": {
                "Microsoft Office": {
                    "winget_id": "Microsoft.Office",
                    "description": "Suite bureautique Microsoft",
                    "category": "Productivité"
                },
                "LibreOffice": {
                    "winget_id": "TheDocumentFoundation.LibreOffice",
                    "description": "Suite bureautique open source",
                    "category": "Productivité"
                },
                "Notion": {
                    "winget_id": "Notion.Notion",
                    "description": "Espace de travail tout-en-un",
                    "category": "Productivité"
                },
                "Obsidian": {
                    "winget_id": "Obsidian.Obsidian",
                    "description": "Base de connaissances personnelle",
                    "category": "Productivité"
                },
                "Evernote": {
                    "winget_id": "Evernote.Evernote",
                    "description": "Application de prise de notes",
                    "category": "Productivité"
                },
                "Todoist": {
                    "winget_id": "Doist.Todoist",
                    "description": "Gestionnaire de tâches",
                    "category": "Productivité"
                },
                "Trello": {
                    "winget_id": "Atlassian.Trello",
                    "description": "Gestion de projets visuelle",
                    "category": "Productivité"
                },
                "Adobe Acrobat Reader": {
                    "winget_id": "Adobe.Acrobat.Reader.64-bit",
                    "description": "Lecteur PDF officiel d'Adobe",
                    "category": "Productivité"
                },
                "Foxit PDF Reader": {
                    "winget_id": "Foxit.FoxitReader",
                    "description": "Lecteur PDF rapide",
                    "category": "Productivité"
                },
                "Sumatra PDF": {
                    "winget_id": "SumatraPDF.SumatraPDF",
                    "description": "Lecteur PDF léger",
                    "category": "Productivité"
                },
                "Calibre": {
                    "winget_id": "calibre.calibre",
                    "description": "Gestionnaire de bibliothèque d'ebooks",
                    "category": "Productivité"
                },
            },
            
            # ===== CLOUD & STOCKAGE =====
            "Cloud & Stockage": {
                "Google Drive": {
                    "winget_id": "Google.GoogleDrive",
                    "description": "Stockage cloud de Google",
                    "category": "Cloud & Stockage"
                },
                "Dropbox": {
                    "winget_id": "Dropbox.Dropbox",
                    "description": "Service de stockage cloud",
                    "category": "Cloud & Stockage"
                },
                "OneDrive": {
                    "winget_id": "Microsoft.OneDrive",
                    "description": "Stockage cloud de Microsoft",
                    "category": "Cloud & Stockage"
                },
                "Nextcloud": {
                    "winget_id": "Nextcloud.NextcloudDesktop",
                    "description": "Cloud privé auto-hébergé",
                    "category": "Cloud & Stockage"
                },
                "Syncthing": {
                    "winget_id": "Syncthing.Syncthing",
                    "description": "Synchronisation de fichiers P2P",
                    "category": "Cloud & Stockage"
                },
            },
            
            # ===== GAMING =====
            "Gaming": {
                "Steam": {
                    "winget_id": "Valve.Steam",
                    "description": "Plateforme de jeux PC",
                    "category": "Gaming"
                },
                "Epic Games Launcher": {
                    "winget_id": "EpicGames.EpicGamesLauncher",
                    "description": "Lanceur de jeux Epic",
                    "category": "Gaming"
                },
                "GOG Galaxy": {
                    "winget_id": "GOG.Galaxy",
                    "description": "Client de jeux GOG",
                    "category": "Gaming"
                },
                "EA App": {
                    "winget_id": "ElectronicArts.EADesktop",
                    "description": "Plateforme de jeux EA",
                    "category": "Gaming"
                },
                "Ubisoft Connect": {
                    "winget_id": "Ubisoft.Connect",
                    "description": "Lanceur de jeux Ubisoft",
                    "category": "Gaming"
                },
                "Battle.net": {
                    "winget_id": "Blizzard.BattleNet",
                    "description": "Lanceur de jeux Blizzard",
                    "category": "Gaming"
                },
                "WeMod": {
                    "winget_id": "WeMod.WeMod",
                    "description": "Gestionnaire de cheats pour jeux solo",
                    "category": "Gaming"
                },
                "PLITCH": {
                    "winget_id": "MegaDev.PLITCH",
                    "description": "Trainer de jeux avec codes",
                    "category": "Gaming"
                },
                "Vortex": {
                    "winget_id": "NexusMods.Vortex",
                    "description": "Gestionnaire de mods pour jeux",
                    "category": "Gaming"
                },
                "MSI Afterburner": {
                    "winget_id": "Guru3D.Afterburner",
                    "description": "Overclocking carte graphique",
                    "category": "Gaming"
                },
                "RivaTuner Statistics Server": {
                    "winget_id": "Guru3D.RTSS",
                    "description": "Affichage FPS et monitoring en jeu",
                    "category": "Gaming"
                },
            },
            
            # ===== ACCÈS À DISTANCE =====
            "Accès à distance": {
                "TeamViewer": {
                    "winget_id": "TeamViewer.TeamViewer",
                    "description": "Accès et support à distance",
                    "category": "Accès à distance"
                },
                "AnyDesk": {
                    "winget_id": "AnyDeskSoftwareGmbH.AnyDesk",
                    "description": "Bureau à distance rapide",
                    "category": "Accès à distance"
                },
                "Chrome Remote Desktop": {
                    "winget_id": "Google.ChromeRemoteDesktop",
                    "description": "Accès à distance via Chrome",
                    "category": "Accès à distance"
                },
                "RustDesk": {
                    "winget_id": "RustDesk.RustDesk",
                    "description": "Bureau à distance open source",
                    "category": "Accès à distance"
                },
            },
            
            # ===== LOGICIELS MATÉRIEL =====
            "Logiciels Matériel": {
                "Corsair iCUE 5": {
                    "winget_id": "Corsair.iCUE.5",
                    "description": "Gestion périphériques Corsair (dernière version)",
                    "category": "Logiciels Matériel"
                },
                "Corsair iCUE 4": {
                    "winget_id": "Corsair.iCUE.4",
                    "description": "Gestion périphériques Corsair (version 4)",
                    "category": "Logiciels Matériel"
                },
            },
            
            # ===== STREAMING & MÉDIAS =====
            "Streaming & Médias": {
                "Plex Desktop": {
                    "winget_id": "Plex.Plex",
                    "description": "Client Plex pour Windows",
                    "category": "Streaming & Médias"
                },
                "Plexamp": {
                    "winget_id": "Plex.Plexamp",
                    "description": "Lecteur audio Plex",
                    "category": "Streaming & Médias"
                },
            },
            
            # ===== RUNTIMES & BIBLIOTHÈQUES =====
            "Runtimes & Bibliothèques": {
                "Microsoft Visual C++ 2015-2022 x64": {
                    "winget_id": "Microsoft.VCRedist.2015+.x64",
                    "description": "Bibliothèque Visual C++ 2015-2022 (64-bit)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft Visual C++ 2015-2022 x86": {
                    "winget_id": "Microsoft.VCRedist.2015+.x86",
                    "description": "Bibliothèque Visual C++ 2015-2022 (32-bit)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft Visual C++ 2013 x64": {
                    "winget_id": "Microsoft.VCRedist.2013.x64",
                    "description": "Bibliothèque Visual C++ 2013 (64-bit)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft Visual C++ 2013 x86": {
                    "winget_id": "Microsoft.VCRedist.2013.x86",
                    "description": "Bibliothèque Visual C++ 2013 (32-bit)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft Visual C++ 2012 x64": {
                    "winget_id": "Microsoft.VCRedist.2012.x64",
                    "description": "Bibliothèque Visual C++ 2012 (64-bit)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft Visual C++ 2012 x86": {
                    "winget_id": "Microsoft.VCRedist.2012.x86",
                    "description": "Bibliothèque Visual C++ 2012 (32-bit)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft Visual C++ 2010 x64": {
                    "winget_id": "Microsoft.VCRedist.2010.x64",
                    "description": "Bibliothèque Visual C++ 2010 (64-bit)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft Visual C++ 2010 x86": {
                    "winget_id": "Microsoft.VCRedist.2010.x86",
                    "description": "Bibliothèque Visual C++ 2010 (32-bit)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Java Runtime 21 (Oracle)": {
                    "winget_id": "Oracle.JDK.21",
                    "description": "Java Development Kit 21 (dernière LTS)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Java Runtime 17 (Oracle)": {
                    "winget_id": "Oracle.JDK.17",
                    "description": "Java Development Kit 17 (LTS)",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft OpenJDK 21": {
                    "winget_id": "Microsoft.OpenJDK.21",
                    "description": "Microsoft Build of OpenJDK 21",
                    "category": "Runtimes & Bibliothèques"
                },
                "Microsoft OpenJDK 17": {
                    "winget_id": "Microsoft.OpenJDK.17",
                    "description": "Microsoft Build of OpenJDK 17",
                    "category": "Runtimes & Bibliothèques"
                },
            },
            
            # ===== PILOTES & DRIVERS =====
            "Pilotes & Drivers": {
                "Snappy Driver Installer": {
                    "winget_id": "samlab-ws.SnappyDriverInstaller",
                    "description": "Gestionnaire de pilotes open source",
                    "category": "Pilotes & Drivers"
                },
                "Driver Easy": {
                    "winget_id": "Easeware.DriverEasy",
                    "description": "Mise à jour automatique des pilotes",
                    "category": "Pilotes & Drivers"
                },
            },
            
            # ===== ÉMULATEURS =====
            "Émulateurs": {
                "BlueStacks": {
                    "winget_id": "BlueStack.BlueStacks",
                    "description": "Émulateur Android pour PC",
                    "category": "Émulateurs"
                },
                "Citra": {
                    "winget_id": "CitraEmu.Citra",
                    "description": "Émulateur Nintendo 3DS",
                    "category": "Émulateurs"
                },
                "DOSBox": {
                    "winget_id": "DOSBox.DOSBox",
                    "description": "Émulateur DOS pour jeux rétro",
                    "category": "Émulateurs"
                },
            },
            
            # ===== RÉSEAUX SOCIAUX =====
            "Réseaux Sociaux": {
                "WhatsApp Desktop": {
                    "winget_id": "9NKSQGP7F2NH",
                    "description": "Application WhatsApp pour Windows",
                    "category": "Réseaux Sociaux"
                },
                "Instagram": {
                    "winget_id": "9NBLGGH5L9XT",
                    "description": "Application Instagram (Microsoft Store)",
                    "category": "Réseaux Sociaux"
                },
                "Facebook": {
                    "winget_id": "9WZDNCRFJ2WL",
                    "description": "Application Facebook (Microsoft Store)",
                    "category": "Réseaux Sociaux"
                },
                "TikTok": {
                    "winget_id": "9NH2GPH4JZS4",
                    "description": "Application TikTok (Microsoft Store)",
                    "category": "Réseaux Sociaux"
                },
                "Snapchat": {
                    "winget_id": "9WZDNCRFJ0J7",
                    "description": "Application Snapchat (Microsoft Store)",
                    "category": "Réseaux Sociaux"
                },
                "X (Twitter)": {
                    "winget_id": "9WZDNCRFJ140",
                    "description": "Application X/Twitter (Microsoft Store)",
                    "category": "Réseaux Sociaux"
                },
                "Pinterest": {
                    "winget_id": "9PFHDSF91B9R",
                    "description": "Application Pinterest (Microsoft Store)",
                    "category": "Réseaux Sociaux"
                },
                "Twitch": {
                    "winget_id": "Twitch.Twitch",
                    "description": "Plateforme de streaming en direct",
                    "category": "Réseaux Sociaux"
                },
            },
            
            # ===== STREAMING VIDÉO =====
            "Streaming Vidéo": {
                "Netflix": {
                    "winget_id": "9WZDNCRFJ3TJ",
                    "description": "Service de streaming Netflix",
                    "category": "Streaming Vidéo"
                },
                "Disney+": {
                    "winget_id": "9NXQXXLFST89",
                    "description": "Service de streaming Disney+",
                    "category": "Streaming Vidéo"
                },
                "Prime Video": {
                    "winget_id": "9P6RC76MSMMJ",
                    "description": "Amazon Prime Video",
                    "category": "Streaming Vidéo"
                },
                "Apple TV": {
                    "winget_id": "Apple.AppleTV",
                    "description": "Apple TV - Streaming et contenus Apple",
                    "category": "Streaming Vidéo"
                },
                "Crunchyroll": {
                    "winget_id": "9NBLGGH5Q1F0",
                    "description": "Streaming d'animés (Microsoft Store)",
                    "category": "Streaming Vidéo"
                },
                "Pluto TV": {
                    "winget_id": "9NBLGGH6HPG6",
                    "description": "TV en streaming gratuite (Microsoft Store)",
                    "category": "Streaming Vidéo"
                },
                "YouTube": {
                    "winget_id": "9WZDNCRDT29J",
                    "description": "Application YouTube officielle (Microsoft Store)",
                    "category": "Streaming Vidéo"
                },
                "myCanal": {
                    "winget_id": "9WZDNCRCRVZ9",
                    "description": "Service de streaming Canal+ (Microsoft Store)",
                    "category": "Streaming Vidéo"
                },
            },
            
            # ===== STREAMING AUDIO =====
            "Streaming Audio": {
                "Deezer": {
                    "winget_id": "Deezer.Deezer",
                    "description": "Service de streaming musical Deezer",
                    "category": "Streaming Audio"
                },
                "Apple Music": {
                    "winget_id": "Apple.AppleMusic",
                    "description": "Service de streaming Apple Music",
                    "category": "Streaming Audio"
                },
                "Amazon Music": {
                    "winget_id": "9P6RC76MSMMJ",
                    "description": "Amazon Music - Streaming musical",
                    "category": "Streaming Audio"
                },
                "iTunes": {
                    "winget_id": "Apple.iTunes",
                    "description": "Lecteur multimédia et store Apple",
                    "category": "Streaming Audio"
                },
            },
            
            # ===== IA & ASSISTANTS =====
            "IA & Assistants": {
                "ChatGPT": {
                    "winget_id": "OpenAI.ChatGPT",
                    "description": "Application ChatGPT officielle",
                    "category": "IA & Assistants"
                },
                "Microsoft Copilot": {
                    "winget_id": "9NHT9RB2F4HD",
                    "description": "Assistant IA Microsoft Copilot",
                    "category": "IA & Assistants"
                },
            },
            
            # ===== UTILITAIRES SYSTÈME =====
            "Utilitaires Système Avancés": {
                "Glary Utilities": {
                    "winget_id": "Glarysoft.GlaryUtilities",
                    "description": "Suite d'optimisation et maintenance PC",
                    "category": "Utilitaires Système Avancés"
                },
                "DS4Windows": {
                    "winget_id": "Ryochan7.DS4Windows",
                    "description": "Utiliser une manette PS4/PS5 sur PC",
                    "category": "Utilitaires Système Avancés"
                },
                "TightVNC": {
                    "winget_id": "GlavSoft.TightVNC",
                    "description": "Accès à distance VNC",
                    "category": "Utilitaires Système Avancés"
                },
                "Speedtest by Ookla": {
                    "winget_id": "Ookla.Speedtest.Desktop",
                    "description": "Test de vitesse internet par Ookla",
                    "category": "Utilitaires Système Avancés"
                },
                "nPerf Speed Test": {
                    "winget_id": "nPerf.nPerf",
                    "description": "Test de vitesse et qualité internet",
                    "category": "Utilitaires Système Avancés"
                },
                "CDInfo": {
                    "winget_id": "the-sz.CDInfo",
                    "description": "Informations détaillées sur les CD/DVD",
                    "category": "Utilitaires Système Avancés"
                },
                "Smart Defrag": {
                    "winget_id": "IObit.SmartDefrag",
                    "description": "Défragmentation et optimisation de disque",
                    "category": "Utilitaires Système Avancés"
                },
            },
            
            # ===== IMPRIMANTES & SCAN =====
            "Imprimantes & Scan": {
                "HP Smart": {
                    "winget_id": "9WZDNCRFHWLH",
                    "description": "Application HP Smart pour imprimantes HP",
                    "category": "Imprimantes & Scan"
                },
                "Epson Print and Scan": {
                    "winget_id": "9WZDNCRFJ4P8",
                    "description": "Application Epson pour impression et scan",
                    "category": "Imprimantes & Scan"
                },
                "Canon Print": {
                    "winget_id": "9WZDNCRDP2J6",
                    "description": "Application Canon pour imprimantes Canon",
                    "category": "Imprimantes & Scan"
                },
            },
            
            # ===== CLOUD APPLE =====
            "Services Apple": {
                "iCloud": {
                    "winget_id": "9PKTQ5699M62",
                    "description": "iCloud pour Windows - Stockage Apple",
                    "category": "Services Apple"
                },
            },
            
            # ===== MATÉRIEL CONSTRUCTEUR =====
            "Logiciels Constructeur": {
                "Lenovo Vantage": {
                    "winget_id": "9WZDNCRFJ4MV",
                    "description": "Centre de contrôle Lenovo Vantage",
                    "category": "Logiciels Constructeur"
                },
            },
            
            # ===== SUITE PROFESSIONNELLE =====
            "Suites Professionnelles": {
                "Adobe Creative Cloud": {
                    "winget_id": "Adobe.CreativeCloud",
                    "description": "Suite créative Adobe (gestionnaire d'apps)",
                    "category": "Suites Professionnelles"
                },
                "Adobe Acrobat Reader": {
                    "winget_id": "Adobe.Acrobat.Reader.64-bit",
                    "description": "Lecteur PDF Adobe Acrobat Reader",
                    "category": "Suites Professionnelles"
                },
                "Autodesk Desktop App": {
                    "winget_id": "Autodesk.AutodeskDesktopApp",
                    "description": "Gestionnaire des applications Autodesk",
                    "category": "Suites Professionnelles"
                },
                "Canva": {
                    "winget_id": "Canva.Canva",
                    "description": "Design graphique et création de contenu en ligne",
                    "category": "Suites Professionnelles"
                },
            },
            
            # ===== OUTILS SYSTÈME BOOTABLES =====
            "Outils Système Bootables": {
                "Ventoy": {
                    "winget_id": "Ventoy.Ventoy",
                    "description": "Créer USB bootable multi-ISO",
                    "category": "Outils Système Bootables"
                },
                "balenaEtcher": {
                    "winget_id": "Balena.Etcher",
                    "description": "Graver des images sur USB/SD de manière fiable",
                    "category": "Outils Système Bootables"
                },
                "Autoruns": {
                    "winget_id": "Microsoft.Sysinternals.Autoruns",
                    "description": "Gérer les programmes au démarrage (Sysinternals)",
                    "category": "Outils Système Bootables"
                },
            },
            
            # ===== VIRTUALISATION =====
            "Virtualisation": {
                "VMware Workstation Player": {
                    "winget_id": "VMware.WorkstationPlayer",
                    "description": "Machine virtuelle gratuite VMware",
                    "category": "Virtualisation"
                },
            },
            
            # ===== TÉLÉCHARGEMENT & MÉDIAS =====
            "Téléchargement & Médias": {
                "4K Video Downloader": {
                    "winget_id": "OpenMedia.4KVideoDownloader",
                    "description": "Télécharger vidéos YouTube en haute qualité",
                    "category": "Téléchargement & Médias"
                },
                "4K YouTube to MP3": {
                    "winget_id": "OpenMedia.4KYoutubetoMP3",
                    "description": "Convertir vidéos YouTube en MP3",
                    "category": "Téléchargement & Médias"
                },
                "yt-dlp": {
                    "winget_id": "yt-dlp.yt-dlp",
                    "description": "Téléchargeur vidéo universel (ligne de commande)",
                    "category": "Téléchargement & Médias"
                },
                "FreeTube": {
                    "winget_id": "PrestonN.FreeTube",
                    "description": "Client YouTube desktop axé confidentialité",
                    "category": "Téléchargement & Médias"
                },
            },
            
            # ===== GAMING CONSOLE =====
            "Gaming Console": {
                "PS Remote Play": {
                    "winget_id": "PlayStation.PSRemotePlay",
                    "description": "Jouer à distance sur votre PS4/PS5",
                    "category": "Gaming Console"
                },
                "Google Play Games": {
                    "winget_id": "Google.PlayGames",
                    "description": "Jouer à des jeux Android sur PC",
                    "category": "Gaming Console"
                },
                "GeForce NOW": {
                    "winget_id": "Nvidia.GeForceNow",
                    "description": "Service de cloud gaming NVIDIA",
                    "category": "Gaming Console"
                },
                "Moonlight": {
                    "winget_id": "MoonlightGameStreamingProject.Moonlight",
                    "description": "Client de streaming de jeux PC open source",
                    "category": "Gaming Console"
                },
            },
            
            # ===== BENCHMARKS & TESTS =====
            "Benchmarks & Tests": {
                "OCCT": {
                    "winget_id": "OCCT.OCCT",
                    "description": "Test de stabilité CPU, GPU et alimentation",
                    "category": "Benchmarks & Tests"
                },
            },
            
            # ===== IA LOCALE =====
            "IA Locale": {
                "Ollama": {
                    "winget_id": "Ollama.Ollama",
                    "description": "Exécuter des modèles IA en local (Llama, Mistral, etc.)",
                    "category": "IA Locale"
                },
                "LM Studio": {
                    "winget_id": "ElementLabs.LMStudio",
                    "description": "Interface graphique pour modèles IA locaux",
                    "category": "IA Locale"
                },
                "Jan AI": {
                    "winget_id": "Jan.Jan",
                    "description": "ChatGPT-like 100% local et open source",
                    "category": "IA Locale"
                },
                "Claude Desktop": {
                    "winget_id": "Anthropic.Claude",
                    "description": "Application Claude AI desktop (Anthropic)",
                    "category": "IA Locale"
                },
                "Msty": {
                    "winget_id": "CloudStack.Msty",
                    "description": "Interface multi-modèles IA (GPT, Claude, Ollama)",
                    "category": "IA Locale"
                },
                "Cherry Studio": {
                    "winget_id": "kangfenmao.CherryStudio",
                    "description": "Client desktop multi-IA (GPT, Claude, Gemini, Ollama)",
                    "category": "IA Locale"
                },
                "Reor": {
                    "winget_id": "ReorProject.Reor",
                    "description": "Éditeur notes avec IA locale intégrée",
                    "category": "IA Locale"
                },
            },
            
            # ===== DRIVER GÉNÉRIQUE =====
            "Driver Générique": {
                "DirectX End-User Runtime": {
                    "winget_id": "Microsoft.DirectX",
                    "description": "Runtime DirectX pour les jeux et applications graphiques",
                    "category": "Driver Générique"
                },
                "Microsoft Visual C++ 2015-2022 x64": {
                    "winget_id": "Microsoft.VCRedist.2015+.x64",
                    "description": "Visual C++ Redistributable 2015-2022 (64-bit)",
                    "category": "Driver Générique"
                },
                "Microsoft Visual C++ 2015-2022 x86": {
                    "winget_id": "Microsoft.VCRedist.2015+.x86",
                    "description": "Visual C++ Redistributable 2015-2022 (32-bit)",
                    "category": "Driver Générique"
                },
                "Microsoft Visual C++ 2013 x64": {
                    "winget_id": "Microsoft.VCRedist.2013.x64",
                    "description": "Visual C++ Redistributable 2013 (64-bit)",
                    "category": "Driver Générique"
                },
                "Microsoft Visual C++ 2013 x86": {
                    "winget_id": "Microsoft.VCRedist.2013.x86",
                    "description": "Visual C++ Redistributable 2013 (32-bit)",
                    "category": "Driver Générique"
                },
                "Microsoft Visual C++ 2012 x64": {
                    "winget_id": "Microsoft.VCRedist.2012.x64",
                    "description": "Visual C++ Redistributable 2012 (64-bit)",
                    "category": "Driver Générique"
                },
                "Microsoft Visual C++ 2012 x86": {
                    "winget_id": "Microsoft.VCRedist.2012.x86",
                    "description": "Visual C++ Redistributable 2012 (32-bit)",
                    "category": "Driver Générique"
                },
                "Microsoft Visual C++ 2010 x64": {
                    "winget_id": "Microsoft.VCRedist.2010.x64",
                    "description": "Visual C++ Redistributable 2010 (64-bit)",
                    "category": "Driver Générique"
                },
                "Microsoft Visual C++ 2010 x86": {
                    "winget_id": "Microsoft.VCRedist.2010.x86",
                    "description": "Visual C++ Redistributable 2010 (32-bit)",
                    "category": "Driver Générique"
                },
                "Microsoft .NET Framework 4.8.1": {
                    "winget_id": "Microsoft.DotNet.Framework.DeveloperPack_4",
                    "description": ".NET Framework 4.8.1 pour applications Windows",
                    "category": "Driver Générique"
                },
                "Microsoft .NET 8 Desktop Runtime": {
                    "winget_id": "Microsoft.DotNet.DesktopRuntime.8",
                    "description": ".NET 8 Desktop Runtime pour applications modernes",
                    "category": "Driver Générique"
                },
                "Microsoft .NET 7 Desktop Runtime": {
                    "winget_id": "Microsoft.DotNet.DesktopRuntime.7",
                    "description": ".NET 7 Desktop Runtime",
                    "category": "Driver Générique"
                },
                "Microsoft .NET 6 Desktop Runtime": {
                    "winget_id": "Microsoft.DotNet.DesktopRuntime.6",
                    "description": ".NET 6 Desktop Runtime (LTS)",
                    "category": "Driver Générique"
                },
                "OpenJDK 21": {
                    "winget_id": "Microsoft.OpenJDK.21",
                    "description": "Java Development Kit 21 (OpenJDK)",
                    "category": "Driver Générique"
                },
                "OpenJDK 17": {
                    "winget_id": "Microsoft.OpenJDK.17",
                    "description": "Java Development Kit 17 (OpenJDK LTS)",
                    "category": "Driver Générique"
                },
                "Windows SDK 10.0.18362": {
                    "winget_id": "Microsoft.WindowsSDK.10.0.18362",
                    "description": "Kit de développement logiciel Windows 10 SDK",
                    "category": "Driver Générique"
                },
                "Windows SDK 10.0.17134": {
                    "winget_id": "Microsoft.WindowsSDK.10.0.17134",
                    "description": "Kit de développement logiciel Windows 10 SDK (version 17134)",
                    "category": "Driver Générique"
                },
            },
            
            # ===== SERVEURS & DÉVELOPPEMENT WEB =====
            "Serveurs & Dev Web": {
                "XAMPP 8.2": {
                    "winget_id": "ApacheFriends.Xampp.8.2",
                    "description": "Suite serveur web Apache, MySQL, PHP et Perl",
                    "category": "Serveurs & Dev Web"
                },
                "XAMPP 8.1": {
                    "winget_id": "ApacheFriends.Xampp.8.1",
                    "description": "Suite serveur web Apache, MySQL, PHP et Perl (version 8.1)",
                    "category": "Serveurs & Dev Web"
                },
                "Thonny": {
                    "winget_id": "AivarAnnamaa.Thonny",
                    "description": "IDE Python pour débutants",
                    "category": "Serveurs & Dev Web"
                },
                "Arduino IDE": {
                    "winget_id": "ArduinoSA.IDE.stable",
                    "description": "Environnement de développement Arduino",
                    "category": "Serveurs & Dev Web"
                },
                "Wireshark": {
                    "winget_id": "WiresharkFoundation.Wireshark",
                    "description": "Analyseur de protocoles réseau",
                    "category": "Serveurs & Dev Web"
                },
                "Godot Engine": {
                    "winget_id": "GodotEngine.GodotEngine",
                    "description": "Moteur de jeu open source 2D et 3D",
                    "category": "Serveurs & Dev Web"
                },
            },
            
            # ===== MULTIMÉDIA AVANCÉ =====
            "Multimédia Avancé": {
                "Jellyfin Server": {
                    "winget_id": "Jellyfin.Server",
                    "description": "Serveur média open source (alternative à Plex)",
                    "category": "Multimédia Avancé"
                },
                "Jellyfin Media Player": {
                    "winget_id": "Jellyfin.JellyfinMediaPlayer",
                    "description": "Lecteur multimédia Jellyfin",
                    "category": "Multimédia Avancé"
                },
                "MPV.net": {
                    "winget_id": "mpv.net",
                    "description": "Lecteur multimédia minimaliste et performant",
                    "category": "Multimédia Avancé"
                },
                "Kodi": {
                    "winget_id": "XBMCFoundation.Kodi",
                    "description": "Centre multimédia open source",
                    "category": "Multimédia Avancé"
                },
                "AIMP": {
                    "winget_id": "AIMP.AIMP",
                    "description": "Lecteur audio avancé",
                    "category": "Multimédia Avancé"
                },
            },
            
            # ===== CAO & DESIGN 3D =====
            "CAO & Design 3D": {
                "LibreCAD": {
                    "winget_id": "LibreCAD.LibreCAD",
                    "description": "Logiciel de CAO 2D open source",
                    "category": "CAO & Design 3D"
                },
                "FreeCAD": {
                    "winget_id": "FreeCAD.FreeCAD",
                    "description": "Logiciel de CAO 3D paramétrique open source",
                    "category": "CAO & Design 3D"
                },
                "SketchUp 2025": {
                    "winget_id": "Trimble.SketchUp.2025",
                    "description": "Logiciel de modélisation 3D",
                    "category": "CAO & Design 3D"
                },
                "SketchUp 2023": {
                    "winget_id": "Trimble.SketchUp.2023",
                    "description": "Logiciel de modélisation 3D (version 2023)",
                    "category": "CAO & Design 3D"
                },
            },
            
            # ===== COMMUNICATION SOCIALE =====
            "Communication Sociale": {
                "Beeper": {
                    "winget_id": "Beeper.Beeper",
                    "description": "Messagerie universelle tout-en-un",
                    "category": "Communication Sociale"
                },
                "Caprine": {
                    "winget_id": "Caprine.Caprine",
                    "description": "Client Facebook Messenger non officiel",
                    "category": "Communication Sociale"
                },
                "Notion": {
                    "winget_id": "Notion.Notion",
                    "description": "Espace de travail tout-en-un pour notes et collaboration",
                    "category": "Communication Sociale"
                },
            },
            
            # ===== BUREAUTIQUE ALTERNATIVE =====
            "Bureautique Alternative": {
                "OpenOffice": {
                    "winget_id": "Apache.OpenOffice",
                    "description": "Suite bureautique open source",
                    "category": "Bureautique Alternative"
                },
            },
            
            # ===== UTILITAIRES SYSTÈME EXPERTS =====
            "Utilitaires Système Experts": {
                "VirtualBox": {
                    "winget_id": "Oracle.VirtualBox",
                    "description": "Logiciel de virtualisation open source",
                    "category": "Utilitaires Système Experts"
                },
                "PowerISO": {
                    "winget_id": "PowerSoftware.PowerISO",
                    "description": "Outil de gestion d'images disque ISO",
                    "category": "Utilitaires Système Experts"
                },
            },
        }
        
        return programs
    
    def get_all_programs(self) -> Dict:
        """Retourne tous les programmes disponibles"""
        return self.programs_db
    
    def get_program_count(self) -> int:
        """Compte le nombre total de programmes"""
        count = 0
        for category in self.programs_db.values():
            count += len(category)
        return count
    
    def install_program(
        self, 
        program_name: str,
        program_info: Dict,
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None
    ) -> bool:
        """
        Installe un programme via Winget
        
        Args:
            program_name: Nom du programme
            program_info: Informations du programme (doit contenir winget_id)
            progress_callback: Fonction appelée pour mettre à jour la progression
            log_callback: Fonction appelée pour logger les messages
            
        Returns:
            True si l'installation a réussi, False sinon
        """
        if not self.winget_available:
            if log_callback:
                log_callback(f"[ERROR] Winget n'est pas disponible sur ce système")
            return False
        
        winget_id = program_info.get('winget_id')
        if not winget_id:
            if log_callback:
                log_callback(f"[ERROR] Aucun ID Winget pour {program_name}")
            return False
        
        try:
            if log_callback:
                log_callback(f"[INFO] Installation de {program_name} via Winget...")
            
            # Commande d'installation Winget
            cmd = [
                'winget', 'install',
                '--id', winget_id,
                '--silent',  # Installation silencieuse
                '--accept-source-agreements',
                '--accept-package-agreements',
                '--disable-interactivity'
            ]
            
            if log_callback:
                log_callback(f"[INFO] Commande: {' '.join(cmd)}")
            
            # Exécution de l'installation
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Lecture de la sortie en temps réel
            for line in process.stdout:
                line = line.strip()
                if line:
                    if log_callback:
                        log_callback(f"[WINGET] {line}")
                    
                    # Mise à jour de la progression basée sur le texte
                    if "Téléchargement" in line or "Downloading" in line:
                        if progress_callback:
                            progress_callback(30)
                    elif "Installation" in line or "Installing" in line:
                        if progress_callback:
                            progress_callback(60)
                    elif "terminé" in line or "completed" in line:
                        if progress_callback:
                            progress_callback(90)
            
            # Attendre la fin du processus
            return_code = process.wait()
            
            if return_code == 0:
                if progress_callback:
                    progress_callback(100)
                if log_callback:
                    log_callback(f"[SUCCESS] {program_name} installé avec succès !")
                return True
            else:
                stderr_output = process.stderr.read()
                if log_callback:
                    log_callback(f"[ERROR] Échec de l'installation de {program_name}")
                    if stderr_output:
                        log_callback(f"[ERROR] {stderr_output}")
                return False
                
        except Exception as e:
            if log_callback:
                log_callback(f"[ERROR] Erreur lors de l'installation: {str(e)}")
            logger.exception(f"Erreur installation {program_name}")
            return False
    
    def install_programs(
        self,
        program_names: List[str],
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None,
        finished_callback: Optional[Callable] = None
    ):
        """
        Installe plusieurs programmes
        
        Args:
            program_names: Liste des noms de programmes à installer
            progress_callback: Fonction appelée pour mettre à jour la progression
            log_callback: Fonction appelée pour logger les messages
            finished_callback: Fonction appelée quand tout est terminé
        """
        if log_callback:
            log_callback(f"[INFO] Début de l'installation de {len(program_names)} programme(s)...")
        
        success_count = 0
        fail_count = 0
        
        for i, program_name in enumerate(program_names, 1):
            # Trouver le programme dans la base de données
            program_info = None
            for category_programs in self.programs_db.values():
                if program_name in category_programs:
                    program_info = category_programs[program_name]
                    break
            
            if not program_info:
                if log_callback:
                    log_callback(f"[ERROR] Programme '{program_name}' non trouvé")
                fail_count += 1
                continue
            
            # Callback de progression pour ce programme
            def prog_cb(percent):
                # Progression totale: (programmes complétés + progression actuelle) / total
                total_progress = ((i - 1) * 100 + percent) / len(program_names)
                if progress_callback:
                    progress_callback(int(total_progress))
            
            # Installation
            success = self.install_program(program_name, program_info, prog_cb, log_callback)
            
            if success:
                success_count += 1
            else:
                fail_count += 1
        
        # Message final
        if log_callback:
            log_callback(f"[SUCCESS] Installation terminée: {success_count} réussi(es), {fail_count} échoué(es)")
        
        if finished_callback:
            finished_callback()
    
    def run_windows_repair(
        self,
        command_name: str,
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None
    ) -> bool:
        """
        Exécute une commande de réparation Windows (DISM, SFC, etc.)
        
        Args:
            command_name: Nom de la commande de réparation
            progress_callback: Fonction appelée pour mettre à jour la progression
            log_callback: Fonction appelée pour logger les messages
            
        Returns:
            True si la commande a réussi, False sinon
        """
        # Rechercher la commande dans la catégorie Réparation Windows
        repair_category = self.programs_db.get("🔧 Réparation Windows", {})
        
        if command_name not in repair_category:
            if log_callback:
                log_callback(f"[ERROR] Commande '{command_name}' non trouvée")
            logger.error(f"Commande de réparation non trouvée: {command_name}")
            return False
        
        command_info = repair_category[command_name]
        command = command_info.get("command", "")
        admin_required = command_info.get("admin_required", True)
        
        # Vérifier les privilèges admin si nécessaire
        if admin_required and not self.is_admin:
            if log_callback:
                log_callback(f"[WARNING] Cette commande nécessite des privilèges administrateur")
                log_callback(f"[INFO] Veuillez relancer l'application en tant qu'administrateur")
            logger.warning(f"Privilèges admin requis pour: {command_name}")
            return False
        
        try:
            if log_callback:
                log_callback(f"[INFO] Exécution de: {command_name}")
                log_callback(f"[INFO] Commande: {command}")
            
            if progress_callback:
                progress_callback(10)
            
            # Exécution de la commande
            logger.info(f"🔧 Exécution: {command}")
            
            # Utiliser PowerShell pour exécuter la commande
            process = subprocess.Popen(
                ['powershell', '-Command', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            if progress_callback:
                progress_callback(30)
            
            # Lire la sortie en temps réel
            output_lines = []
            for line in process.stdout:
                line = line.strip()
                if line:
                    output_lines.append(line)
                    if log_callback:
                        log_callback(f"[OUTPUT] {line}")
                    logger.info(f"  {line}")
            
            if progress_callback:
                progress_callback(80)
            
            # Attendre la fin du processus
            return_code = process.wait()
            
            if progress_callback:
                progress_callback(100)
            
            if return_code == 0:
                if log_callback:
                    log_callback(f"[SUCCESS] ✅ Commande exécutée avec succès")
                logger.info(f"✅ Succès: {command_name}")
                return True
            else:
                if log_callback:
                    log_callback(f"[ERROR] ❌ Erreur lors de l'exécution (code: {return_code})")
                logger.error(f"❌ Échec: {command_name} (code {return_code})")
                return False
                
        except Exception as e:
            if log_callback:
                log_callback(f"[ERROR] Erreur lors de l'exécution: {str(e)}")
            logger.exception(f"Erreur exécution commande {command_name}")
            return False
    
    def get_repair_commands(self) -> Dict[str, Dict]:
        """Retourne la liste des commandes de réparation Windows disponibles"""
        return self.programs_db.get("🔧 Réparation Windows", {})
    
    def is_repair_command(self, item_name: str) -> bool:
        """Vérifie si un élément est une commande de réparation"""
        repair_commands = self.get_repair_commands()
        return item_name in repair_commands
    
    def is_system_command(self, item_name: str) -> bool:
        """
        Vérifie si un élément est une commande système (réparation OU paramètres)
        
        Args:
            item_name: Nom de l'élément à vérifier
            
        Returns:
            True si c'est une commande système, False si c'est un programme Winget
        """
        # Chercher dans toutes les catégories
        for category, programs in self.programs_db.items():
            if item_name in programs:
                # Si l'élément a un champ 'command', c'est une commande système
                return 'command' in programs[item_name]
        return False
    
    def run_system_command(
        self,
        item_name: str,
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None
    ) -> bool:
        """
        Exécute une commande système (DISM, paramètres Windows, etc.)
        
        Args:
            item_name: Nom de la commande à exécuter
            progress_callback: Fonction appelée pour mettre à jour la progression
            log_callback: Fonction appelée pour logger les messages
            
        Returns:
            True si la commande a réussi, False sinon
        """
        # Chercher la commande dans toutes les catégories
        command_info = None
        category_name = None
        
        for category, programs in self.programs_db.items():
            if item_name in programs:
                command_info = programs[item_name]
                category_name = category
                break
        
        if not command_info or 'command' not in command_info:
            if log_callback:
                log_callback(f"[ERROR] Commande '{item_name}' non trouvée")
            logger.error(f"Commande système non trouvée: {item_name}")
            return False
        
        command = command_info.get("command", "")
        admin_required = command_info.get("admin_required", False)
        
        # Vérifier les privilèges admin si nécessaire
        if admin_required and not self.is_admin:
            if log_callback:
                log_callback(f"[WARNING] Cette commande nécessite des privilèges administrateur")
                log_callback(f"[INFO] Veuillez relancer l'application en tant qu'administrateur")
            logger.warning(f"Privilèges admin requis pour: {item_name}")
            # Pour msconfig, on essaie quand même (Windows demandera l'élévation)
            if "msconfig" not in command.lower():
                return False
        
        try:
            if log_callback:
                log_callback(f"[INFO] Exécution de: {item_name}")
                log_callback(f"[INFO] Commande: {command}")
            
            if progress_callback:
                progress_callback(20)
            
            logger.info(f"⚙️ Exécution: {command}")
            
            # Déterminer le type de commande
            if command.startswith("start "):
                # Commandes ms-settings:, windowsdefender:, shell:
                # Utiliser PowerShell avec Start-Process
                ps_command = f"Start-Process '{command.replace('start ', '')}'"
                process = subprocess.Popen(
                    ['powershell', '-Command', ps_command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if progress_callback:
                    progress_callback(80)
                
                # Attendre un peu pour voir si ça démarre
                try:
                    return_code = process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    # C'est normal, la fenêtre s'est ouverte
                    return_code = 0
                
            elif any(cmd in command.lower() for cmd in ["dism", "sfc"]):
                # Commandes de réparation (sortie texte détaillée)
                process = subprocess.Popen(
                    ['powershell', '-Command', command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                if progress_callback:
                    progress_callback(40)
                
                # Lire la sortie en temps réel
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        if log_callback:
                            log_callback(f"[OUTPUT] {line}")
                        logger.info(f"  {line}")
                
                if progress_callback:
                    progress_callback(80)
                
                return_code = process.wait()
                
            else:
                # Autres commandes (control, devmgmt.msc, sysdm.cpl, etc.)
                # Exécuter directement
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if progress_callback:
                    progress_callback(80)
                
                # Attendre un peu
                try:
                    return_code = process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    return_code = 0
            
            if progress_callback:
                progress_callback(100)
            
            if return_code == 0:
                if log_callback:
                    log_callback(f"[SUCCESS] ✅ {item_name} exécuté avec succès")
                logger.info(f"✅ Commande réussie: {item_name}")
                return True
            else:
                if log_callback:
                    log_callback(f"[WARNING] Code de retour: {return_code}")
                logger.warning(f"⚠️ Code retour {return_code} pour: {item_name}")
                # Considérer comme succès quand même (la fenêtre s'est probablement ouverte)
                return True
                
        except Exception as e:
            if log_callback:
                log_callback(f"[ERROR] Erreur lors de l'exécution: {str(e)}")
            logger.error(f"❌ Erreur commande système '{item_name}': {e}")
            return False
    
    def export_to_json(self, output_path: str):
        """Exporte la base de données au format JSON compatible avec l'ancien système"""
        flattened = {}
        
        for category, programs in self.programs_db.items():
            for prog_name, prog_info in programs.items():
                flattened[prog_name] = prog_info
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.programs_db, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Base de données exportée: {output_path}")


if __name__ == "__main__":
    # Test du gestionnaire
    logging.basicConfig(level=logging.INFO)
    
    wm = WingetManager()
    print(f"\n✅ Winget disponible: {wm.winget_available}")
    print(f"📊 Nombre de programmes: {wm.get_program_count()}")
    
    # Exporter la base de données
    wm.export_to_json("data/programs_winget.json")
    print("\n✅ Base de données exportée vers data/programs_winget.json")
