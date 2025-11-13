# 📦 Base de Données Portable - NiTrite v.2

## 📋 Vue d'ensemble

Ce système permet de gérer une base de données locale SQLite contenant tous les exécutables des applications portables téléchargées.

## 🎯 Fonctionnalités

### ✅ Gestion complète des applications
- ✨ Ajout/Suppression/Modification d'applications
- 🔍 Recherche par nom, catégorie, description
- 📊 Statistiques détaillées (nombre d'apps, espace utilisé, etc.)
- 🔐 Vérification d'intégrité (hash SHA256)
- 📁 Organisation par catégories
- 📝 Métadonnées complètes pour chaque application

### 💾 Stockage des informations
- Nom de l'application
- Catégorie
- Description
- Version
- Chemin de l'exécutable
- Taille du fichier
- Hash SHA256 (pour vérifier l'intégrité)
- URL de téléchargement
- Date de téléchargement
- Arguments d'installation
- Notes et métadonnées personnalisées

## 🚀 Utilisation

### 1️⃣ Créer la base de données

```bash
# Depuis le dossier du projet
python scripts\create_portable_database.py
```

Ce script va :
- ✅ Créer le fichier `portable_apps.db`
- 📥 Importer les applications depuis `data/programs.json`
- 📊 Afficher les statistiques
- 💾 Créer un export JSON

### 2️⃣ Scanner et ajouter automatiquement les applications

```bash
python scripts\scan_portable_apps.py
```

Ce script va :
- 🔍 Scanner le dossier `downloads/`
- 🤖 Détecter automatiquement les catégories
- 📦 Ajouter les .exe trouvés dans la base
- ⏭️ Ignorer les applications déjà présentes

### 3️⃣ Utiliser dans votre code Python

```python
from src.portable_database import PortableDatabase

# Initialiser la base de données
db = PortableDatabase(
    db_path="portable_apps.db",
    apps_folder="downloads"
)

# Ajouter une application
app_id = db.add_application(
    name="AnyDesk Portable",
    executable_path="downloads/AnyDesk.exe",
    category="Outils OrdiPlus",
    description="Bureau à distance rapide",
    version="7.1.14",
    is_portable=True
)

# Rechercher des applications
results = db.search_applications("anydesk")

# Lister par catégorie
apps = db.list_applications(category="Outils OrdiPlus")

# Obtenir les statistiques
stats = db.get_statistics()
print(f"Total: {stats['total_apps']} apps")
print(f"Espace: {stats['total_size_gb']:.2f} GB")

# Vérifier l'intégrité
issues = db.verify_integrity()

# Exporter vers JSON
db.export_to_json("backup.json")
```

## 📊 Structure de la base de données

### Table `applications`
| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER | ID unique (auto-incrémenté) |
| name | TEXT | Nom unique de l'application |
| display_name | TEXT | Nom d'affichage |
| category | TEXT | Catégorie |
| description | TEXT | Description |
| version | TEXT | Version |
| executable_path | TEXT | Chemin vers l'exécutable |
| file_size | INTEGER | Taille en octets |
| file_hash | TEXT | Hash SHA256 |
| download_url | TEXT | URL de téléchargement |
| download_date | TEXT | Date de téléchargement |
| last_updated | TEXT | Dernière mise à jour |
| is_portable | BOOLEAN | Est portable? |
| install_args | TEXT | Arguments d'installation |
| notes | TEXT | Notes |
| icon_path | TEXT | Chemin vers l'icône |
| official_website | TEXT | Site officiel |
| admin_required | BOOLEAN | Nécessite admin? |

### Table `metadata`
Métadonnées personnalisées pour chaque application.

### Table `categories`
Liste des catégories disponibles.

### Table `execution_history`
Historique des exécutions (pour future implémentation).

## 🔧 Intégration avec NiTrite

### Modifier `installer_manager.py`

```python
from .portable_database import PortableDatabase

class InstallerManager:
    def __init__(self, config_path=None, log_callback=None):
        # ... code existant ...
        
        # Initialiser la base de données portable
        self.portable_db = PortableDatabase(
            db_path=Path.cwd() / "portable_apps.db",
            apps_folder=self.download_dir
        )
    
    def download_program(self, program_name, download_url):
        # ... téléchargement ...
        
        # Ajouter à la base de données si portable
        if program_info.get('portable', False):
            self.portable_db.add_application(
                name=program_name,
                executable_path=str(exe_path),
                category=program_info.get('category', 'Non classé'),
                description=program_info.get('description', ''),
                download_url=download_url,
                is_portable=True
            )
```

### Créer une interface de gestion

```python
class PortableAppsManager:
    """Interface GUI pour gérer les applications portables"""
    
    def __init__(self, root, db):
        self.root = root
        self.db = db
        
        # Créer l'interface
        self.create_widgets()
    
    def create_widgets(self):
        # Liste des applications
        # Boutons: Lancer, Supprimer, Mettre à jour
        # Barre de recherche
        # Filtres par catégorie
        pass
    
    def launch_app(self, app_name):
        """Lance une application portable"""
        app = self.db.get_application(name=app_name)
        if app:
            subprocess.Popen(app['executable_path'])
```

## 📁 Structure des fichiers

```
Projet NiTrite v.2/
├── portable_apps.db              # Base de données SQLite
├── portable_apps_export.json     # Export JSON (backup)
├── downloads/                     # Exécutables portables
│   ├── AnyDesk.exe
│   ├── RustDesk.exe
│   └── ...
├── src/
│   └── portable_database.py      # Module principal
└── scripts/
    ├── create_portable_database.py  # Créer la BDD
    └── scan_portable_apps.py        # Scanner et ajouter
```

## 🔍 Requêtes SQL utiles

### Lister toutes les applications portables
```sql
SELECT name, category, executable_path 
FROM applications 
WHERE is_portable = 1 
ORDER BY category, name;
```

### Applications par catégorie avec taille totale
```sql
SELECT category, 
       COUNT(*) as count,
       SUM(file_size)/1024/1024 as total_mb
FROM applications 
GROUP BY category 
ORDER BY total_mb DESC;
```

### Applications manquantes (fichier non trouvé)
```sql
SELECT name, executable_path 
FROM applications 
WHERE NOT EXISTS (
    SELECT 1 FROM applications a2 
    WHERE a2.id = applications.id
);
```
(Note: Utiliser `verify_integrity()` pour une vérification complète)

## 🛠️ Maintenance

### Vérifier l'intégrité
```python
db = PortableDatabase()
issues = db.verify_integrity()
```

### Nettoyer les entrées orphelines
```python
apps = db.list_applications()
for app in apps:
    if not Path(app['executable_path']).exists():
        db.delete_application(name=app['name'])
```

### Mettre à jour les métadonnées
```python
db.update_application(
    name="AnyDesk Portable",
    version="7.2.0",
    notes="Mise à jour vers version 7.2"
)
```

## 📈 Statistiques disponibles

```python
stats = db.get_statistics()

# Affiche:
{
    'total_apps': 150,
    'portable_apps': 130,
    'installed_apps': 20,
    'total_size_bytes': 5368709120,
    'total_size_mb': 5120.0,
    'total_size_gb': 5.0,
    'apps_by_category': {
        'Outils OrdiPlus': 25,
        'Navigateurs': 15,
        'Multimédia': 30,
        # ...
    }
}
```

## ⚠️ Notes importantes

1. **Hash SHA256** : Calculé automatiquement pour vérifier l'intégrité des fichiers
2. **Portabilité** : Le champ `is_portable` permet de différencier les apps portables des installées
3. **Backup** : Utilisez `export_to_json()` régulièrement pour sauvegarder
4. **Performance** : Des index sont créés automatiquement pour optimiser les recherches

## 🔄 Import/Export

### Importer depuis programs.json
```python
db.import_from_json(
    json_path="data/programs.json",
    downloads_folder="downloads"
)
```

### Exporter vers JSON
```python
db.export_to_json("backup.json")
```

## 🐛 Dépannage

### La base de données ne se crée pas
- Vérifiez les permissions d'écriture
- Vérifiez que SQLite est disponible (`import sqlite3`)

### Les applications ne sont pas trouvées
- Vérifiez le chemin du dossier downloads
- Utilisez `verify_integrity()` pour identifier les problèmes

### Erreur de hash
- Le fichier a peut-être été modifié
- Recalculez le hash avec `update_application()`

## 📞 Support

Pour toute question ou problème, consultez :
- La documentation du code (`portable_database.py`)
- Les exemples dans `scripts/`
- Les logs générés par le système

---

**Créé pour NiTrite v.2** - Gestionnaire d'installations automatisées
