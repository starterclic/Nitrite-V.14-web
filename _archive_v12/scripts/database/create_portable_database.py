"""
Script pour créer et peupler la base de données des applications portables
Scanne le dossier downloads et crée une base de données SQLite
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier parent au path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(parent_dir / 'src'))

from src.portable_database import PortableDatabase
import logging


def main():
    """Fonction principale"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("="*70)
    print(" CRÉATION DE LA BASE DE DONNÉES DES APPLICATIONS PORTABLES")
    print("="*70)
    
    # Chemins
    project_root = parent_dir
    downloads_folder = project_root / "downloads"
    db_path = project_root / "portable_apps.db"
    programs_json = project_root / "data" / "programs.json"
    
    print(f"\n📁 Dossier du projet: {project_root}")
    print(f"📥 Dossier downloads: {downloads_folder}")
    print(f"💾 Base de données: {db_path}")
    print(f"📄 Fichier programs.json: {programs_json}")
    
    # Vérifier que le dossier downloads existe
    if not downloads_folder.exists():
        print(f"\n⚠️ Le dossier downloads n'existe pas. Création...")
        downloads_folder.mkdir(parents=True, exist_ok=True)
    
    # Créer la base de données
    print("\n" + "="*70)
    print("INITIALISATION DE LA BASE DE DONNÉES")
    print("="*70)
    
    db = PortableDatabase(
        db_path=str(db_path),
        apps_folder=str(downloads_folder)
    )
    
    # Importer depuis programs.json si disponible
    if programs_json.exists():
        print("\n" + "="*70)
        print("IMPORTATION DES APPLICATIONS DEPUIS programs.json")
        print("="*70)
        
        imported = db.import_from_json(
            json_path=str(programs_json),
            downloads_folder=str(downloads_folder)
        )
        
        print(f"\n✅ {imported} applications importées")
    else:
        print(f"\n⚠️ Fichier programs.json non trouvé: {programs_json}")
        print("Création d'une base de données vide.")
    
    # Afficher les statistiques
    print("\n" + "="*70)
    print("STATISTIQUES DE LA BASE DE DONNÉES")
    print("="*70)
    
    stats = db.get_statistics()
    print(f"\n📊 Applications totales: {stats.get('total_apps', 0)}")
    print(f"📦 Applications portables: {stats.get('portable_apps', 0)}")
    print(f"💿 Applications installées: {stats.get('installed_apps', 0)}")
    print(f"💾 Espace total: {stats.get('total_size_gb', 0):.2f} GB ({stats.get('total_size_mb', 0):.2f} MB)")
    
    print("\n📁 Applications par catégorie:")
    for category, count in stats.get('apps_by_category', {}).items():
        print(f"  • {category}: {count}")
    
    # Lister les catégories
    print("\n" + "="*70)
    print("CATÉGORIES DISPONIBLES")
    print("="*70)
    
    categories = db.get_categories()
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    
    # Vérifier l'intégrité
    print("\n" + "="*70)
    print("VÉRIFICATION DE L'INTÉGRITÉ")
    print("="*70)
    
    issues = db.verify_integrity()
    
    if not issues:
        print("\n✅ Aucun problème détecté - Base de données intègre")
    else:
        print(f"\n⚠️ {len(issues)} problèmes détectés:")
        for issue in issues:
            print(f"\n  Application: {issue['app']}")
            print(f"  Problème: {issue['issue']}")
            print(f"  Chemin: {issue['path']}")
    
    # Exporter vers JSON pour sauvegarde
    export_path = project_root / "portable_apps_export.json"
    print("\n" + "="*70)
    print("EXPORT DE LA BASE DE DONNÉES")
    print("="*70)
    print(f"\nExport vers: {export_path}")
    
    if db.export_to_json(str(export_path)):
        print("✅ Export réussi")
    else:
        print("❌ Échec de l'export")
    
    # Lister quelques exemples d'applications
    print("\n" + "="*70)
    print("EXEMPLES D'APPLICATIONS (10 premières)")
    print("="*70)
    
    apps = db.list_applications()
    for app in apps[:10]:
        print(f"\n📦 {app['name']}")
        print(f"   Catégorie: {app['category']}")
        print(f"   Description: {app['description'][:60]}...")
        print(f"   Chemin: {Path(app['executable_path']).name}")
        if app['file_size']:
            print(f"   Taille: {app['file_size'] / 1024 / 1024:.2f} MB")
    
    print("\n" + "="*70)
    print("✅ CRÉATION DE LA BASE DE DONNÉES TERMINÉE")
    print("="*70)
    print(f"\n💾 Base de données créée: {db_path}")
    print(f"📊 {stats.get('total_apps', 0)} applications enregistrées")
    print(f"📁 {len(categories)} catégories")
    print("\nVous pouvez maintenant utiliser la base de données dans votre application.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
