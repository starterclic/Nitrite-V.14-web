"""
Gestionnaire de base de données locale pour les exécutables portables
Crée et maintient une base de données SQLite avec tous les programmes téléchargés
"""

import sqlite3
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
import logging


class PortableDatabase:
    """Gestionnaire de base de données pour les applications portables"""
    
    def __init__(self, db_path=None, apps_folder=None):
        """
        Initialise la base de données portable
        
        Args:
            db_path: Chemin vers le fichier de base de données SQLite
            apps_folder: Dossier contenant les applications portables
        """
        self.logger = logging.getLogger(__name__)
        
        # Déterminer le chemin de la base de données
        if db_path is None:
            self.db_path = Path.cwd() / "portable_apps.db"
        else:
            self.db_path = Path(db_path)
        
        # Déterminer le dossier des applications
        if apps_folder is None:
            self.apps_folder = Path.cwd() / "downloads"
        else:
            self.apps_folder = Path(apps_folder)
        
        # Créer le dossier s'il n'existe pas
        self.apps_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialiser la base de données
        self._init_database()
    
    def _init_database(self):
        """Crée la structure de la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table principale des applications
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    display_name TEXT,
                    category TEXT,
                    description TEXT,
                    version TEXT,
                    executable_path TEXT NOT NULL,
                    file_size INTEGER,
                    file_hash TEXT,
                    download_url TEXT,
                    download_date TEXT,
                    last_updated TEXT,
                    is_portable BOOLEAN DEFAULT 1,
                    install_args TEXT,
                    notes TEXT,
                    icon_path TEXT,
                    official_website TEXT,
                    admin_required BOOLEAN DEFAULT 0
                )
            ''')
            
            # Table des métadonnées
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metadata (
                    app_id INTEGER,
                    key TEXT,
                    value TEXT,
                    FOREIGN KEY (app_id) REFERENCES applications(id),
                    PRIMARY KEY (app_id, key)
                )
            ''')
            
            # Table des catégories
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    icon TEXT
                )
            ''')
            
            # Table d'historique des exécutions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS execution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_id INTEGER,
                    execution_date TEXT,
                    duration INTEGER,
                    success BOOLEAN,
                    notes TEXT,
                    FOREIGN KEY (app_id) REFERENCES applications(id)
                )
            ''')
            
            # Index pour améliorer les performances
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_app_name ON applications(name)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_category ON applications(category)
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"✅ Base de données initialisée: {self.db_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
            raise
    
    def _calculate_file_hash(self, file_path):
        """Calcule le hash SHA256 d'un fichier"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.logger.error(f"Erreur lors du calcul du hash: {e}")
            return None
    
    def add_application(self, name, executable_path, **kwargs):
        """
        Ajoute une application à la base de données
        
        Args:
            name: Nom unique de l'application
            executable_path: Chemin vers l'exécutable
            **kwargs: Autres attributs (display_name, category, description, etc.)
        
        Returns:
            ID de l'application ajoutée ou None en cas d'erreur
        """
        try:
            exe_path = Path(executable_path)
            
            # Vérifier que le fichier existe
            if not exe_path.exists():
                self.logger.error(f"❌ Fichier non trouvé: {executable_path}")
                return None
            
            # Calculer les métadonnées du fichier
            file_size = exe_path.stat().st_size
            file_hash = self._calculate_file_hash(exe_path)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Préparer les données
            current_time = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT OR REPLACE INTO applications 
                (name, display_name, category, description, version, 
                 executable_path, file_size, file_hash, download_url, 
                 download_date, last_updated, is_portable, install_args, 
                 notes, icon_path, official_website, admin_required)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name,
                kwargs.get('display_name', name),
                kwargs.get('category', 'Non classé'),
                kwargs.get('description', ''),
                kwargs.get('version', 'Unknown'),
                str(exe_path.absolute()),
                file_size,
                file_hash,
                kwargs.get('download_url', ''),
                kwargs.get('download_date', current_time),
                current_time,
                kwargs.get('is_portable', True),
                kwargs.get('install_args', ''),
                kwargs.get('notes', ''),
                kwargs.get('icon_path', ''),
                kwargs.get('official_website', ''),
                kwargs.get('admin_required', False)
            ))
            
            app_id = cursor.lastrowid
            
            # Ajouter les métadonnées supplémentaires
            for key, value in kwargs.items():
                if key not in ['display_name', 'category', 'description', 'version', 
                               'download_url', 'is_portable', 'install_args', 'notes',
                               'icon_path', 'official_website', 'admin_required']:
                    cursor.execute('''
                        INSERT OR REPLACE INTO metadata (app_id, key, value)
                        VALUES (?, ?, ?)
                    ''', (app_id, key, str(value)))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"✅ Application ajoutée: {name} (ID: {app_id})")
            return app_id
            
        except sqlite3.IntegrityError as e:
            self.logger.error(f"❌ Application déjà existante: {name}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'ajout de l'application: {e}")
            return None
    
    def get_application(self, name=None, app_id=None):
        """Récupère les informations d'une application"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if app_id:
                cursor.execute('SELECT * FROM applications WHERE id = ?', (app_id,))
            elif name:
                cursor.execute('SELECT * FROM applications WHERE name = ?', (name,))
            else:
                return None
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération: {e}")
            return None
    
    def list_applications(self, category=None, portable_only=True):
        """
        Liste toutes les applications
        
        Args:
            category: Filtrer par catégorie (optionnel)
            portable_only: Ne lister que les applications portables
        
        Returns:
            Liste de dictionnaires contenant les informations des applications
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM applications WHERE 1=1'
            params = []
            
            if category:
                query += ' AND category = ?'
                params.append(category)
            
            if portable_only:
                query += ' AND is_portable = 1'
            
            query += ' ORDER BY category, name'
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du listing: {e}")
            return []
    
    def search_applications(self, search_term):
        """Recherche des applications par nom ou description"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            search_pattern = f'%{search_term}%'
            cursor.execute('''
                SELECT * FROM applications 
                WHERE name LIKE ? OR display_name LIKE ? OR description LIKE ?
                ORDER BY name
            ''', (search_pattern, search_pattern, search_pattern))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la recherche: {e}")
            return []
    
    def update_application(self, name, **kwargs):
        """Met à jour les informations d'une application"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Construire la requête dynamiquement
            fields = []
            values = []
            for key, value in kwargs.items():
                fields.append(f"{key} = ?")
                values.append(value)
            
            # Ajouter la date de mise à jour
            fields.append("last_updated = ?")
            values.append(datetime.now().isoformat())
            
            values.append(name)
            
            query = f"UPDATE applications SET {', '.join(fields)} WHERE name = ?"
            cursor.execute(query, values)
            
            conn.commit()
            affected_rows = cursor.rowcount
            conn.close()
            
            if affected_rows > 0:
                self.logger.info(f"✅ Application mise à jour: {name}")
                return True
            else:
                self.logger.warning(f"⚠️ Application non trouvée: {name}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la mise à jour: {e}")
            return False
    
    def delete_application(self, name=None, app_id=None):
        """Supprime une application de la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if app_id:
                cursor.execute('DELETE FROM applications WHERE id = ?', (app_id,))
            elif name:
                cursor.execute('DELETE FROM applications WHERE name = ?', (name,))
            else:
                return False
            
            conn.commit()
            affected_rows = cursor.rowcount
            conn.close()
            
            if affected_rows > 0:
                self.logger.info(f"✅ Application supprimée: {name or app_id}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la suppression: {e}")
            return False
    
    def get_categories(self):
        """Récupère la liste de toutes les catégories"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT category FROM applications 
                WHERE category IS NOT NULL 
                ORDER BY category
            ''')
            
            categories = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return categories
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération des catégories: {e}")
            return []
    
    def get_statistics(self):
        """Retourne des statistiques sur la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Nombre total d'applications
            cursor.execute('SELECT COUNT(*) FROM applications')
            stats['total_apps'] = cursor.fetchone()[0]
            
            # Nombre d'applications par catégorie
            cursor.execute('''
                SELECT category, COUNT(*) as count 
                FROM applications 
                GROUP BY category 
                ORDER BY count DESC
            ''')
            stats['apps_by_category'] = dict(cursor.fetchall())
            
            # Espace total utilisé
            cursor.execute('SELECT SUM(file_size) FROM applications')
            total_size = cursor.fetchone()[0] or 0
            stats['total_size_bytes'] = total_size
            stats['total_size_mb'] = round(total_size / (1024 * 1024), 2)
            stats['total_size_gb'] = round(total_size / (1024 * 1024 * 1024), 2)
            
            # Applications portables vs non-portables
            cursor.execute('SELECT is_portable, COUNT(*) FROM applications GROUP BY is_portable')
            portable_stats = dict(cursor.fetchall())
            stats['portable_apps'] = portable_stats.get(1, 0)
            stats['installed_apps'] = portable_stats.get(0, 0)
            
            conn.close()
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du calcul des statistiques: {e}")
            return {}
    
    def import_from_json(self, json_path, downloads_folder):
        """
        Importe les applications depuis un fichier programs.json
        
        Args:
            json_path: Chemin vers le fichier programs.json
            downloads_folder: Dossier contenant les fichiers téléchargés
        
        Returns:
            Nombre d'applications importées
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                programs_data = json.load(f)
            
            downloads_path = Path(downloads_folder)
            imported_count = 0
            
            for category, programs in programs_data.items():
                if not isinstance(programs, dict):
                    continue
                
                for program_name, program_info in programs.items():
                    # Chercher l'exécutable dans le dossier downloads
                    is_portable = program_info.get('portable', False)
                    
                    if is_portable:
                        # Rechercher le fichier .exe correspondant
                        exe_files = list(downloads_path.glob(f"*{program_name.replace(' ', '*')}*.exe"))
                        
                        if not exe_files:
                            # Essayer sans espace
                            exe_files = list(downloads_path.glob(f"*{program_name.replace(' ', '')}*.exe"))
                        
                        if exe_files:
                            exe_path = exe_files[0]
                            
                            # Ajouter à la base de données
                            app_id = self.add_application(
                                name=program_name,
                                executable_path=str(exe_path),
                                display_name=program_name,
                                category=category,
                                description=program_info.get('description', ''),
                                download_url=program_info.get('download_url', ''),
                                is_portable=True,
                                install_args=program_info.get('install_args', ''),
                                admin_required=program_info.get('admin_required', False),
                                notes=program_info.get('note', ''),
                                essential=program_info.get('essential', False),
                                winget_id=program_info.get('winget_id', '')
                            )
                            
                            if app_id:
                                imported_count += 1
            
            self.logger.info(f"✅ Importation terminée: {imported_count} applications ajoutées")
            return imported_count
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'importation: {e}")
            return 0
    
    def export_to_json(self, output_path):
        """Exporte la base de données vers un fichier JSON"""
        try:
            apps = self.list_applications(portable_only=False)
            
            # Organiser par catégorie
            export_data = {}
            for app in apps:
                category = app.get('category', 'Non classé')
                if category not in export_data:
                    export_data[category] = {}
                
                export_data[category][app['name']] = {
                    'description': app.get('description', ''),
                    'executable_path': app.get('executable_path', ''),
                    'version': app.get('version', ''),
                    'download_url': app.get('download_url', ''),
                    'is_portable': bool(app.get('is_portable', True)),
                    'file_size': app.get('file_size', 0),
                    'admin_required': bool(app.get('admin_required', False)),
                    'notes': app.get('notes', '')
                }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"✅ Export réussi: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'export: {e}")
            return False
    
    def verify_integrity(self):
        """Vérifie l'intégrité de la base de données"""
        try:
            apps = self.list_applications(portable_only=False)
            issues = []
            
            for app in apps:
                exe_path = Path(app['executable_path'])
                
                # Vérifier l'existence du fichier
                if not exe_path.exists():
                    issues.append({
                        'app': app['name'],
                        'issue': 'Fichier non trouvé',
                        'path': str(exe_path)
                    })
                    continue
                
                # Vérifier le hash
                current_hash = self._calculate_file_hash(exe_path)
                if current_hash != app.get('file_hash'):
                    issues.append({
                        'app': app['name'],
                        'issue': 'Hash modifié (fichier potentiellement modifié)',
                        'path': str(exe_path)
                    })
            
            if issues:
                self.logger.warning(f"⚠️ {len(issues)} problèmes détectés")
                for issue in issues:
                    self.logger.warning(f"  - {issue['app']}: {issue['issue']}")
            else:
                self.logger.info("✅ Intégrité vérifiée: Aucun problème détecté")
            
            return issues
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la vérification: {e}")
            return []


def main():
    """Fonction de test et démonstration"""
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Créer la base de données
    db = PortableDatabase(
        db_path="portable_apps.db",
        apps_folder="downloads"
    )
    
    # Afficher les statistiques
    print("\n" + "="*60)
    print("STATISTIQUES DE LA BASE DE DONNÉES")
    print("="*60)
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Lister les catégories
    print("\n" + "="*60)
    print("CATÉGORIES")
    print("="*60)
    categories = db.get_categories()
    for cat in categories:
        print(f"  - {cat}")
    
    # Lister quelques applications
    print("\n" + "="*60)
    print("APPLICATIONS (premières 10)")
    print("="*60)
    apps = db.list_applications()
    for app in apps[:10]:
        print(f"\n{app['name']}")
        print(f"  Catégorie: {app['category']}")
        print(f"  Chemin: {app['executable_path']}")
        print(f"  Taille: {app['file_size'] / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
