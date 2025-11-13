"""
Script pour afficher la structure finale organisée du projet
"""
import os
from pathlib import Path

def print_tree(directory, prefix="", max_depth=3, current_depth=0):
    """Affiche l'arborescence d'un dossier"""
    if current_depth >= max_depth:
        return
    
    path = Path(directory)
    if not path.exists():
        return
    
    items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        
        # Ignorer certains dossiers/fichiers
        if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules']:
            continue
            
        print(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir() and current_depth < max_depth - 1:
            extension = "    " if is_last else "│   "
            print_tree(item, prefix + extension, max_depth, current_depth + 1)

def main():
    """Affiche la structure complète du projet organisé"""
    print("🎉 STRUCTURE FINALE - PROJET NITRITE V2.0 ORGANISÉ")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    print(f"📁 {project_root.name}/")
    
    print_tree(project_root, max_depth=4)
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE L'ORGANISATION")
    print("=" * 60)
    
    # Compter les fichiers par dossier
    stats = {}
    for root, dirs, files in os.walk(project_root):
        # Ignorer les dossiers cachés
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        rel_path = Path(root).relative_to(project_root)
        folder_name = str(rel_path) if str(rel_path) != '.' else 'racine'
        
        if folder_name not in stats:
            stats[folder_name] = {'files': 0, 'folders': 0}
        
        stats[folder_name]['files'] += len(files)
        stats[folder_name]['folders'] += len(dirs)
    
    print("\n📁 STATISTIQUES PAR DOSSIER:")
    for folder, data in sorted(stats.items()):
        if data['files'] > 0 or data['folders'] > 0:
            print(f"  {folder:30} | {data['files']:3} fichiers | {data['folders']:2} dossiers")
    
    print("\n✅ ORGANISATION TERMINÉE AVEC SUCCÈS !")
    print("🎯 Projet prêt pour le développement et la distribution")

if __name__ == "__main__":
    main()