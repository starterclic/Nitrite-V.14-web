"""
Tests unitaires pour les fonctionnalités de base de NiTrite
"""

import unittest
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_manager import ConfigManager
from src.portable_database import PortableDatabase
import tempfile
import json


class TestConfigManager(unittest.TestCase):
    """Tests pour le gestionnaire de configuration"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.config_manager = ConfigManager()

    def test_default_config(self):
        """Test de la configuration par défaut"""
        self.assertIsNotNone(self.config_manager.config)
        self.assertEqual(self.config_manager.config['app_version'], '2.0.0')
        self.assertEqual(self.config_manager.config['language'], 'fr')

    def test_get_config_value(self):
        """Test de récupération d'une valeur"""
        version = self.config_manager.get('app_version')
        self.assertEqual(version, '2.0.0')

    def test_get_config_value_with_default(self):
        """Test de récupération avec valeur par défaut"""
        value = self.config_manager.get('non_existent_key', 'default_value')
        self.assertEqual(value, 'default_value')

    def test_set_config_value(self):
        """Test de modification d'une valeur"""
        self.config_manager.set('test_key', 'test_value')
        self.assertEqual(self.config_manager.get('test_key'), 'test_value')


class TestPortableDatabase(unittest.TestCase):
    """Tests pour la base de données portable"""

    def setUp(self):
        """Initialisation avant chaque test"""
        # Créer une base de données temporaire
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / 'test_portable.db'
        self.db = PortableDatabase(
            db_path=str(self.db_path),
            apps_folder=self.temp_dir
        )

    def tearDown(self):
        """Nettoyage après chaque test"""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_database_initialization(self):
        """Test de l'initialisation de la base de données"""
        self.assertTrue(self.db_path.exists())

    def test_get_categories(self):
        """Test de récupération des catégories"""
        categories = self.db.get_categories()
        self.assertIsInstance(categories, list)

    def test_get_statistics(self):
        """Test des statistiques"""
        stats = self.db.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_apps', stats)
        self.assertEqual(stats['total_apps'], 0)  # Base vide au départ

    def test_list_applications_empty(self):
        """Test du listing d'applications (base vide)"""
        apps = self.db.list_applications()
        self.assertIsInstance(apps, list)
        self.assertEqual(len(apps), 0)

    def test_search_applications(self):
        """Test de recherche d'applications"""
        results = self.db.search_applications('test')
        self.assertIsInstance(results, list)


class TestDataFiles(unittest.TestCase):
    """Tests pour vérifier l'intégrité des fichiers de données"""

    def setUp(self):
        """Initialisation"""
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / 'data'

    def test_config_json_exists(self):
        """Test de l'existence de config.json"""
        config_file = self.data_dir / 'config.json'
        self.assertTrue(config_file.exists(), "config.json doit exister")

    def test_config_json_valid(self):
        """Test de la validité de config.json"""
        config_file = self.data_dir / 'config.json'
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Vérifier les clés obligatoires
        required_keys = ['app_version', 'language', 'max_concurrent_downloads']
        for key in required_keys:
            self.assertIn(key, config, f"La clé '{key}' doit être présente")

    def test_programs_json_exists(self):
        """Test de l'existence de programs.json"""
        programs_file = self.data_dir / 'programs.json'
        self.assertTrue(programs_file.exists(), "programs.json doit exister")

    def test_programs_json_valid(self):
        """Test de la validité de programs.json"""
        programs_file = self.data_dir / 'programs.json'
        with open(programs_file, 'r', encoding='utf-8') as f:
            programs = json.load(f)

        self.assertIsInstance(programs, dict)
        self.assertGreater(len(programs), 0, "Il doit y avoir au moins une catégorie")


class TestModuleImports(unittest.TestCase):
    """Tests pour vérifier que tous les modules peuvent être importés"""

    def test_import_config_manager(self):
        """Test d'import du config manager"""
        try:
            from src.config_manager import ConfigManager
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Impossible d'importer ConfigManager: {e}")

    def test_import_installer_manager(self):
        """Test d'import de l'installer manager"""
        try:
            from src.installer_manager import InstallerManager
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Impossible d'importer InstallerManager: {e}")

    def test_import_portable_database(self):
        """Test d'import de la base de données portable"""
        try:
            from src.portable_database import PortableDatabase
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Impossible d'importer PortableDatabase: {e}")

    def test_import_elevation_helper(self):
        """Test d'import du helper d'élévation"""
        try:
            from src.elevation_helper import is_admin
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Impossible d'importer elevation_helper: {e}")


def run_tests():
    """Exécute tous les tests"""
    # Créer la suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Ajouter tous les tests
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestPortableDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestDataFiles))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleImports))

    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    print("="*70)
    print("🧪 Tests Unitaires NiTrite v2.0")
    print("="*70)
    print()

    success = run_tests()

    print()
    print("="*70)
    if success:
        print("✅ Tous les tests sont passés avec succès")
    else:
        print("❌ Certains tests ont échoué")
    print("="*70)

    sys.exit(0 if success else 1)
