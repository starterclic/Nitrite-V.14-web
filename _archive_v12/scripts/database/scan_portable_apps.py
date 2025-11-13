"""
Script pour scanner le dossier downloads et ajouter automatiquement 
les exécutables trouvés dans la base de données
"""

import sys
import os
from pathlib import Path
import re

# Ajouter le dossier parent au path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(parent_dir / 'src'))

from src.portable_database import PortableDatabase
import logging


def detect_category_from_name(filename):
    """Détecte la catégorie probable d'après le nom du fichier"""
    filename_lower = filename.lower()
    
    categories_keywords = {
        'Outils OrdiPlus': ['anydesk', 'rustdesk', 'malware', 'adwcleaner', 'wise', 'cleaner', 'spybot'],
        'Navigateurs': ['chrome', 'firefox', 'edge', 'brave', 'opera', 'vivaldi', 'tor'],
        'Antivirus': ['avast', 'avg', 'kaspersky', 'bitdefender', 'norton', 'eset', 'mcafee'],
        'Bureautique': ['office', 'libreoffice', 'pdf', 'reader', 'acrobat', 'notepad'],
        'Multimédia': ['vlc', 'media', 'audacity', 'obs', 'gimp', 'paint', 'video'],
        'Développement': ['vscode', 'git', 'node', 'python', 'visual', 'studio', 'sublime'],
        'Utilitaires': ['7zip', 'winrar', 'everything', 'powertoys', 'cpu-z', 'gpu-z'],
        'Communication': ['teamviewer', 'skype', 'zoom', 'teams', 'discord', 'telegram'],
        'Compression': ['zip', 'rar', 'peazip', 'bandizip'],
        'Sécurité': ['ccleaner', 'hitman', 'firewall', 'comodo']
    }
    
    for category, keywords in categories_keywords.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category
    
    return 'Non classé'


def extract_version_from_filename(filename):
    """Tente d'extraire la version du nom de fichier"""
    # Patterns courants: v1.2.3, version-1.2, 1.2.3, etc.
    patterns = [
        r'v?(\d+\.\d+\.\d+)',
        r'v?(\d+\.\d+)',
        r'-(\d+\.\d+\.\d+)',
        r'_(\d+\.\d+\.\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return 'Unknown'


def scan_and_add_apps(db, downloads_folder, auto_add=True, skip_existing=True):
    """
    Scanne le dossier downloads et ajoute les applications
    
    Args:
        db: Instance de PortableDatabase
        downloads_folder: Dossier à scanner
        auto_add: Ajouter automatiquement sans confirmation
        skip_existing: Ignorer les applications déjà dans la BDD
    
    Returns:
        Nombre d'applications ajoutées
    """
    downloads_path = Path(downloads_folder)
    
    if not downloads_path.exists():
        print(f"❌ Dossier non trouvé: {downloads_folder}")
        return 0
    
    # Trouver tous les fichiers .exe
    exe_files = list(downloads_path.glob("*.exe"))
    
    print(f"\n📂 Scan du dossier: {downloads_folder}")
    print(f"📄 {len(exe_files)} fichiers .exe trouvés\n")
    
    if not exe_files:
        print("⚠️ Aucun fichier .exe trouvé")
        return 0
    
    added_count = 0
    skipped_count = 0
    
    for exe_file in exe_files:
        # Nettoyer le nom du fichier
        clean_name = exe_file.stem
        clean_name = re.sub(r'[-_]setup', '', clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r'[-_]installer', '', clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r'[-_]portable', '', clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r'[-_]v?\d+(\.\d+)*', '', clean_name)
        clean_name = clean_name.strip('-_ ')
        
        # Vérifier si l'application existe déjà
        if skip_existing:
            existing = db.get_application(name=clean_name)
            if existing:
                print(f"⏭️ Ignoré (déjà existant): {clean_name}")
                skipped_count += 1
                continue
        
        # Détecter la catégorie
        category = detect_category_from_name(exe_file.name)
        
        # Extraire la version
        version = extract_version_from_filename(exe_file.name)
        
        print(f"\n📦 {exe_file.name}")
        print(f"   Nom: {clean_name}")
        print(f"   Catégorie: {category}")
        print(f"   Version: {version}")
        print(f"   Taille: {exe_file.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Ajouter ou demander confirmation
        if auto_add or input("   Ajouter à la base de données? (O/n): ").lower() != 'n':
            app_id = db.add_application(
                name=clean_name,
                executable_path=str(exe_file.absolute()),
                display_name=clean_name,
                category=category,
                description=f"Application portable {clean_name}",
                version=version,
                is_portable=True,
                notes=f"Ajouté automatiquement depuis {exe_file.name}"
            )
            
            if app_id:
                print(f"   ✅ Ajouté (ID: {app_id})")
                added_count += 1
            else:
                print(f"   ❌ Erreur lors de l'ajout")
        else:
            print("   ⏭️ Ignoré")
            skipped_count += 1
    
    return added_count, skipped_count


def main():
    """Fonction principale"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("="*70)
    print(" SCAN ET AJOUT AUTOMATIQUE DES APPLICATIONS PORTABLES")
    print("="*70)
    
    # Chemins
    project_root = parent_dir
    downloads_folder = project_root / "downloads"
    db_path = project_root / "portable_apps.db"
    
    print(f"\n📁 Dossier du projet: {project_root}")
    print(f"📥 Dossier downloads: {downloads_folder}")
    print(f"💾 Base de données: {db_path}")
    
    # Créer/ouvrir la base de données
    db = PortableDatabase(
        db_path=str(db_path),
        apps_folder=str(downloads_folder)
    )
    
    # Scanner et ajouter
    print("\n" + "="*70)
    print("SCAN EN COURS...")
    print("="*70)
    
    added, skipped = scan_and_add_apps(
        db=db,
        downloads_folder=str(downloads_folder),
        auto_add=True,
        skip_existing=True
    )
    
    # Résumé
    print("\n" + "="*70)
    print("RÉSUMÉ")
    print("="*70)
    print(f"\n✅ Applications ajoutées: {added}")
    print(f"⏭️ Applications ignorées: {skipped}")
    
    # Statistiques finales
    stats = db.get_statistics()
    print(f"\n📊 Total dans la base: {stats.get('total_apps', 0)} applications")
    print(f"💾 Espace total: {stats.get('total_size_gb', 0):.2f} GB")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
