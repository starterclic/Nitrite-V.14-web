#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter massivement des applications à programs.json
Objectif: Dépasser 500 applications avec minimum 30 par catégorie
"""

import json
import sys
from pathlib import Path

# Chemin vers le fichier programs.json
PROJECT_ROOT = Path(__file__).parent.parent
PROGRAMS_FILE = PROJECT_ROOT / 'data' / 'programs.json'
BACKUP_FILE = PROJECT_ROOT / 'data' / 'programs_backup.json'

def load_programs():
    """Charge le fichier programs.json"""
    with open(PROGRAMS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_programs(programs):
    """Sauvegarde le fichier programs.json avec backup"""
    # Backup de l'ancien fichier
    if PROGRAMS_FILE.exists():
        with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
            with open(PROGRAMS_FILE, 'r', encoding='utf-8') as src:
                f.write(src.read())
        print(f"✅ Backup créé: {BACKUP_FILE}")

    # Sauvegarde du nouveau fichier
    with open(PROGRAMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(programs, f, indent=4, ensure_ascii=False)
    print(f"✅ Fichier sauvegardé: {PROGRAMS_FILE}")

def count_apps_by_category(programs):
    """Compte le nombre d'applications par catégorie"""
    counts = {}
    for category, apps in programs.items():
        counts[category] = len(apps)
    return counts

# Définitions massives d'applications par catégorie
# Format: {"nom": {"description": ..., "download_url": ..., ...}}

NAVIGATEURS_APPS = {
    "Google Chrome": {
        "description": "Navigateur web de Google, rapide et sécurisé",
        "download_url": "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
        "install_args": "/silent /install",
        "category": "Navigateurs",
        "winget_id": "Google.Chrome",
        "admin_required": True
    },
    "Mozilla Firefox": {
        "description": "Navigateur open source et respectueux de la vie privée",
        "download_url": "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=fr",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "Mozilla.Firefox",
        "admin_required": True
    },
    "Microsoft Edge": {
        "description": "Navigateur moderne de Microsoft basé sur Chromium",
        "download_url": "https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx",
        "install_args": "/silent /install",
        "category": "Navigateurs",
        "winget_id": "Microsoft.Edge",
        "admin_required": True
    },
    "Opera": {
        "description": "Navigateur avec VPN intégré et bloqueur de publicités",
        "download_url": "https://net.geo.opera.com/opera/stable/windows",
        "install_args": "/silent /launchopera=0 /setdefaultbrowser=0",
        "category": "Navigateurs",
        "winget_id": "Opera.Opera",
        "admin_required": True
    },
    "Opera GX": {
        "description": "Navigateur optimisé pour les gamers",
        "download_url": "https://net.geo.opera.com/opera_gx/stable/windows",
        "install_args": "/silent /launchopera=0 /setdefaultbrowser=0",
        "category": "Navigateurs",
        "winget_id": "Opera.OperaGX",
        "admin_required": True
    },
    "Brave": {
        "description": "Navigateur privé et sécurisé avec bloqueur de publicités",
        "download_url": "https://laptop-updates.brave.com/latest/winx64",
        "install_args": "/silent /install",
        "category": "Navigateurs",
        "winget_id": "Brave.Brave",
        "admin_required": True
    },
    "Vivaldi": {
        "description": "Navigateur hautement personnalisable pour utilisateurs avancés",
        "download_url": "https://downloads.vivaldi.com/stable/Vivaldi.exe",
        "install_args": "--vivaldi-silent --do-not-launch-chrome",
        "category": "Navigateurs",
        "winget_id": "VivaldiTechnologies.Vivaldi",
        "admin_required": True
    },
    "Tor Browser": {
        "description": "Navigateur pour navigation anonyme via le réseau Tor",
        "download_url": "https://www.torproject.org/dist/torbrowser/latest/torbrowser-install-win64-fr.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "TorProject.TorBrowser",
        "admin_required": False
    },
    "Waterfox": {
        "description": "Navigateur basé sur Firefox optimisé pour la confidentialité",
        "download_url": "https://cdn1.waterfox.net/waterfox/releases/latest/windows/installer/Waterfox%20Setup.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "Waterfox.Waterfox",
        "admin_required": True
    },
    "LibreWolf": {
        "description": "Fork de Firefox axé sur la vie privée et la sécurité",
        "download_url": "https://gitlab.com/api/v4/projects/24386000/packages/generic/librewolf/latest/librewolf-setup.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "LibreWolf.LibreWolf",
        "admin_required": True
    },
    "Chromium": {
        "description": "Version open source de Google Chrome",
        "download_url": "https://download-chromium.appspot.com/dl/Win_x64?type=snapshots",
        "install_args": "",
        "category": "Navigateurs",
        "winget_id": "Hibbiki.Chromium",
        "portable": True,
        "cleanup_folder": "Navigateurs Portables"
    },
    "Pale Moon": {
        "description": "Navigateur open source optimisé pour Windows",
        "download_url": "https://rm-eu.palemoon.org/release/palemoon-latest.win64.installer.exe",
        "install_args": "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-",
        "category": "Navigateurs",
        "winget_id": "MoonchildProductions.PaleMoon",
        "admin_required": True
    },
    "Basilisk": {
        "description": "Navigateur XUL basé sur Firefox ESR legacy",
        "download_url": "https://eu.basilisk-browser.org/release/basilisk-latest.win64.installer.exe",
        "install_args": "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Maxthon": {
        "description": "Navigateur cloud avec synchronisation multi-appareils",
        "download_url": "https://dl.maxthon.com/mx6/maxthon_portable.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "Maxthon.Maxthon",
        "admin_required": True
    },
    "SlimBrowser": {
        "description": "Navigateur léger et rapide basé sur Chromium",
        "download_url": "https://www.slimbrowser.net/filedownload/sbrowser-installer.exe",
        "install_args": "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART",
        "category": "Navigateurs",
        "admin_required": True
    },
    "UC Browser": {
        "description": "Navigateur avec compression de données intégrée",
        "download_url": "https://www.ucweb.com/download/uc-browser-pc",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "UCWeb.UCBrowser",
        "admin_required": True
    },
    "Cent Browser": {
        "description": "Navigateur Chromium amélioré avec fonctionnalités avancées",
        "download_url": "http://static.centbrowser.com/installer_64/centbrowser_5_installer.exe",
        "install_args": "/install /silent",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Yandex Browser": {
        "description": "Navigateur russe avec Turbo mode et sécurité Kaspersky",
        "download_url": "https://browser.yandex.com/download/?os=win&x64=1",
        "install_args": "/silent /install",
        "category": "Navigateurs",
        "winget_id": "Yandex.Browser",
        "admin_required": True
    },
    "Avast Secure Browser": {
        "description": "Navigateur sécurisé avec protection de la vie privée",
        "download_url": "https://www.avast.com/download-secure-browser",
        "install_args": "/silent",
        "category": "Navigateurs",
        "winget_id": "AVAST.SecureBrowser",
        "admin_required": True
    },
    "AVG Secure Browser": {
        "description": "Navigateur sécurisé de AVG",
        "download_url": "https://www.avg.com/download-secure-browser",
        "install_args": "/silent",
        "category": "Navigateurs",
        "winget_id": "AVG.SecureBrowser",
        "admin_required": True
    },
    "Epic Privacy Browser": {
        "description": "Navigateur axé sur la confidentialité avec proxy VPN intégré",
        "download_url": "https://epicbrowser.com/installers/EpicBrowserSetup.exe",
        "install_args": "/silent /install",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Comodo Dragon": {
        "description": "Navigateur sécurisé basé sur Chromium par Comodo",
        "download_url": "https://download.comodo.com/dragon/DragonSetup.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Comodo IceDragon": {
        "description": "Navigateur sécurisé basé sur Firefox par Comodo",
        "download_url": "https://download.comodo.com/icedragon/IceDragonSetup.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Seamonkey": {
        "description": "Suite Internet complète (navigateur, mail, IRC)",
        "download_url": "https://archive.mozilla.org/pub/seamonkey/releases/latest/win64/en-US/seamonkey-setup.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "Mozilla.SeaMonkey",
        "admin_required": True
    },
    "K-Meleon": {
        "description": "Navigateur Gecko ultra-léger pour Windows",
        "download_url": "http://kmeleonbrowser.org/download.php?latest",
        "install_args": "/S",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Falkon": {
        "description": "Navigateur KDE léger utilisant QtWebEngine",
        "download_url": "https://download.kde.org/stable/falkon/latest/Falkon-Installer.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "KDE.Falkon",
        "admin_required": True
    },
    "Midori": {
        "description": "Navigateur léger et rapide open source",
        "download_url": "https://astian.org/midori-browser/download/",
        "install_args": "/S",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Sleipnir": {
        "description": "Navigateur japonais avec gestion avancée des onglets",
        "download_url": "http://www.fenrir-inc.com/jp/sleipnir/download/windows/",
        "install_args": "/S",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Min Browser": {
        "description": "Navigateur minimaliste et rapide",
        "download_url": "https://github.com/minbrowser/min/releases/latest/download/Min-Installer.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Beaker Browser": {
        "description": "Navigateur P2P expérimental pour le Web décentralisé",
        "download_url": "https://github.com/beakerbrowser/beaker/releases/latest/download/beaker-browser-setup.exe",
        "install_args": "/S",
        "category": "Navigateurs",
        "admin_required": True
    },
    "Polypane": {
        "description": "Navigateur pour développeurs web avec multi-viewports",
        "download_url": "https://polypane.app/download/",
        "install_args": "/S",
        "category": "Navigateurs",
        "winget_id": "Polypane.Polypane",
        "admin_required": True
    }
}

# Continuation dans le prochain message...
print("Script de génération d'applications chargé...")
