#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des liens pour NiTriTe V13.0
Vérifie tous les liens d'applications et d'outils
Génère un rapport des liens morts
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple
import time

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
except ImportError:
    print("❌ Module 'requests' non trouvé")
    print("📥 Installation automatique...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry

from src.tools_data_complete import get_all_tools


def create_session():
    """Créer une session HTTP avec retry automatique"""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    return session


def check_url(url: str, session) -> Tuple[bool, str]:
    """
    Vérifier si une URL est accessible

    Returns:
        (is_valid, status_message)
    """
    try:
        # Certains sites comme GitHub nécessitent GET au lieu de HEAD
        if 'github.com' in url or 'massgrave' in url:
            response = session.get(url, timeout=10, allow_redirects=True)
        else:
            response = session.head(url, timeout=10, allow_redirects=True)

        if response.status_code < 400:
            return True, f"✓ OK ({response.status_code})"
        else:
            return False, f"✗ Erreur {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "✗ Timeout (>10s)"
    except requests.exceptions.ConnectionError:
        return False, "✗ Connexion impossible"
    except requests.exceptions.TooManyRedirects:
        return False, "✗ Trop de redirections"
    except requests.exceptions.RequestException as e:
        return False, f"✗ Erreur: {str(e)[:50]}"
    except Exception as e:
        return False, f"✗ Erreur inattendue: {str(e)[:50]}"


def verify_tools_links():
    """Vérifier tous les liens des outils système"""
    print("\n" + "="*80)
    print("🔍 VÉRIFICATION DES LIENS - OUTILS SYSTÈME")
    print("="*80 + "\n")

    all_tools = get_all_tools()
    session = create_session()

    total_links = 0
    valid_links = 0
    invalid_links = []

    for section_name, tools_list in all_tools.items():
        print(f"\n📂 {section_name}")
        print("-" * 80)

        for tool_name, tool_action in tools_list:
            # Vérifier si c'est une URL (commence par http)
            if not isinstance(tool_action, str) or not tool_action.startswith('http'):
                continue

            total_links += 1
            is_valid, status = check_url(tool_action, session)

            if is_valid:
                valid_links += 1
                print(f"  {status} {tool_name}")
            else:
                invalid_links.append((section_name, tool_name, tool_action, status))
                print(f"  {status} {tool_name}")
                print(f"      URL: {tool_action}")

            # Petit délai pour ne pas surcharger les serveurs
            time.sleep(0.1)

    return total_links, valid_links, invalid_links


def verify_apps_links():
    """Vérifier tous les liens des applications"""
    print("\n" + "="*80)
    print("🔍 VÉRIFICATION DES LIENS - APPLICATIONS")
    print("="*80 + "\n")

    # Charger programs.json
    programs_file = Path(__file__).parent / 'data' / 'programs.json'

    if not programs_file.exists():
        print(f"⚠️  Fichier programs.json non trouvé : {programs_file}")
        return 0, 0, []

    try:
        with open(programs_file, 'r', encoding='utf-8') as f:
            programs_data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors du chargement de programs.json: {e}")
        return 0, 0, []

    session = create_session()
    total_links = 0
    valid_links = 0
    invalid_links = []

    for category, apps in programs_data.items():
        print(f"\n📂 {category}")
        print("-" * 80)

        for app_name, app_data in apps.items():
            # Chercher les URLs dans les données de l'application
            urls = []
            if 'download_url' in app_data and app_data['download_url']:
                urls.append(('download_url', app_data['download_url']))
            if 'web_url' in app_data and app_data['web_url']:
                urls.append(('web_url', app_data['web_url']))

            for url_type, url in urls:
                if not url.startswith('http'):
                    continue

                total_links += 1
                is_valid, status = check_url(url, session)

                if is_valid:
                    valid_links += 1
                    print(f"  {status} {app_name} ({url_type})")
                else:
                    invalid_links.append((category, app_name, url, status))
                    print(f"  {status} {app_name} ({url_type})")
                    print(f"      URL: {url}")

                time.sleep(0.1)

    return total_links, valid_links, invalid_links


def verify_master_install_links():
    """Vérifier les liens de la page Master Installation"""
    print("\n" + "="*80)
    print("🔍 VÉRIFICATION DES LIENS - MASTER INSTALLATION")
    print("="*80 + "\n")

    # URLs de la page Master Installation (copiées depuis gui_modern_v13.py)
    master_apps = {
        "Adobe Acrobat Reader": "https://get.adobe.com/reader/",
        "VLC Media Player": "https://www.videolan.org/vlc/",
        "Pack Office 2007": "https://gravesoft.dev/office_c2r_links#2007",
        "Pack Office 2024": "https://gravesoft.dev/office_c2r_links#2024",
        "Spybot Search & Destroy": "https://www.safer-networking.org/download/",
        "AdwCleaner": "https://www.malwarebytes.com/adwcleaner",
        "AnyDesk": "https://anydesk.com/en/downloads/thank-you?dv=win_exe",
        "RustDesk": "https://github.com/rustdesk/rustdesk/releases/latest",
        "Wise Disk Cleaner": "https://www.wisecleaner.com/wise-disk-cleaner.html",
        "Malwarebytes": "https://www.malwarebytes.com/",
        "Firefox": "https://www.mozilla.org/firefox/download/",
        "MassGrave (Actions Rapides)": "https://massgrave.dev/",
        "Activation Script": "https://get.activated.win",
    }

    session = create_session()
    total_links = len(master_apps)
    valid_links = 0
    invalid_links = []

    for app_name, url in master_apps.items():
        is_valid, status = check_url(url, session)

        if is_valid:
            valid_links += 1
            print(f"  {status} {app_name}")
        else:
            invalid_links.append(("Master Installation", app_name, url, status))
            print(f"  {status} {app_name}")
            print(f"      URL: {url}")

        time.sleep(0.1)

    return total_links, valid_links, invalid_links


def generate_report(all_invalid_links, output_file='links_report.txt'):
    """Générer un rapport détaillé des liens morts"""
    if not all_invalid_links:
        return

    print(f"\n📝 Génération du rapport dans {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT DE VÉRIFICATION DES LIENS - NiTriTe V13.0\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Total de liens morts trouvés : {len(all_invalid_links)}\n\n")

        for section, name, url, status in all_invalid_links:
            f.write(f"Section : {section}\n")
            f.write(f"Nom     : {name}\n")
            f.write(f"URL     : {url}\n")
            f.write(f"Statut  : {status}\n")
            f.write("-" * 80 + "\n")

    print(f"✓ Rapport généré : {output_file}")


def main():
    """Fonction principale"""
    print("\n" + "="*80)
    print("🔗 VÉRIFICATEUR DE LIENS - NiTriTe V13.0")
    print("="*80)

    # Vérifier les outils système
    tools_total, tools_valid, tools_invalid = verify_tools_links()

    # Vérifier les applications
    apps_total, apps_valid, apps_invalid = verify_apps_links()

    # Vérifier Master Installation
    master_total, master_valid, master_invalid = verify_master_install_links()

    # Combiner tous les liens invalides
    all_invalid = tools_invalid + apps_invalid + master_invalid

    # Résumé global
    print("\n" + "="*80)
    print("📊 RÉSUMÉ GLOBAL")
    print("="*80)

    total_total = tools_total + apps_total + master_total
    total_valid = tools_valid + apps_valid + master_valid
    total_invalid = len(all_invalid)

    print(f"\n🔗 Total de liens vérifiés : {total_total}")
    print(f"✅ Liens valides          : {total_valid} ({total_valid/total_total*100:.1f}%)")
    print(f"❌ Liens morts             : {total_invalid} ({total_invalid/total_total*100:.1f}%)")

    print(f"\nDétails par section :")
    print(f"  • Outils Système        : {tools_valid}/{tools_total} valides")
    print(f"  • Applications          : {apps_valid}/{apps_total} valides")
    print(f"  • Master Installation   : {master_valid}/{master_total} valides")

    # Générer le rapport si des liens morts trouvés
    if all_invalid:
        print("\n⚠️  Des liens morts ont été détectés !")
        generate_report(all_invalid)
    else:
        print("\n🎉 Tous les liens sont valides !")

    print("\n" + "="*80)
    print("✓ Vérification terminée")
    print("="*80 + "\n")

    input("Appuyez sur ENTRÉE pour fermer...")


if __name__ == "__main__":
    main()
