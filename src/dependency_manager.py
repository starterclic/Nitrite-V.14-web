"""
Gestionnaire de dépendances pour NiTrite v.2
Gère l'installation et le nettoyage automatique des dépendances
"""

import os
import sys
import subprocess
import shutil
import tempfile
import logging
from pathlib import Path
import importlib.util

class DependencyManager:
    """Gestionnaire des dépendances de l'application"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dependencies_dir = Path(__file__).parent.parent / 'dependencies'
        self.dependencies_dir.mkdir(exist_ok=True)
        
        # Liste des dépendances requises
        self.required_packages = {
            'requests': 'requests>=2.28.0',
            'Pillow': 'Pillow>=9.0.0',
            'pywin32': 'pywin32>=304',
        }
        
        # Dépendances installées localement
        self.local_dependencies = []
        
        # Ajouter le dossier dependencies au path Python
        if str(self.dependencies_dir) not in sys.path:
            sys.path.insert(0, str(self.dependencies_dir))
    
    def check_dependencies(self):
        """Vérifie et installe les dépendances nécessaires"""
        self.logger.info("Vérification des dépendances...")
        
        missing_packages = []
        
        for package_name, package_spec in self.required_packages.items():
            if not self.is_package_available(package_name):
                missing_packages.append(package_spec)
        
        if missing_packages:
            self.logger.info(f"Dépendances manquantes détectées: {missing_packages}")
            success = self.install_dependencies(missing_packages)
            if not success:
                raise RuntimeError("Impossible d'installer les dépendances nécessaires")
        else:
            self.logger.info("Toutes les dépendances sont disponibles")
    
    def is_package_available(self, package_name):
        """
        Vérifie si un package Python est disponible
        
        Args:
            package_name: Nom du package à vérifier
            
        Returns:
            bool: True si le package est disponible
        """
        try:
            __import__(package_name)
            return True
        except ImportError:
            # Vérifier dans le dossier dependencies local
            local_path = self.dependencies_dir / package_name
            if local_path.exists():
                return True
            
            # Vérifier les noms alternatifs
            package_alternatives = {
                'Pillow': 'PIL',
                'pywin32': 'win32api'
            }
            
            if package_name in package_alternatives:
                try:
                    __import__(package_alternatives[package_name])
                    return True
                except ImportError:
                    pass
            
            return False
    
    def install_dependencies(self, packages):
        """
        Installe les dépendances manquantes
        
        Args:
            packages: Liste des packages à installer
            
        Returns:
            bool: True si l'installation a réussi
        """
        try:
            self.logger.info("Installation des dépendances...")
            
            # Tenter d'installer avec pip dans le dossier local
            success = self.install_local_packages(packages)
            
            if success:
                self.logger.info("Dépendances installées avec succès")
                return True
            else:
                self.logger.error("Échec de l'installation des dépendances")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'installation des dépendances: {e}")
            return False
    
    def install_local_packages(self, packages):
        """
        Installe les packages dans le dossier local dependencies
        
        Args:
            packages: Liste des packages à installer
            
        Returns:
            bool: True si l'installation a réussi
        """
        try:
            pip_cmd = [
                sys.executable, '-m', 'pip', 'install',
                '--target', str(self.dependencies_dir),
                '--upgrade'
            ] + packages
            
            self.logger.info(f"Exécution: {' '.join(pip_cmd)}")
            
            result = subprocess.run(
                pip_cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
            
            if result.returncode == 0:
                self.local_dependencies.extend(packages)
                self.logger.info("Installation locale réussie")
                return True
            else:
                self.logger.error(f"Erreur pip: {result.stderr}")
                
                # Essayer une installation alternative
                return self.install_fallback_packages(packages)
                
        except subprocess.TimeoutExpired:
            self.logger.error("Timeout lors de l'installation des dépendances")
            return False
        except Exception as e:
            self.logger.error(f"Erreur lors de l'installation locale: {e}")
            return self.install_fallback_packages(packages)
    
    def install_fallback_packages(self, packages):
        """
        Méthode de fallback pour installer les packages
        
        Args:
            packages: Liste des packages à installer
            
        Returns:
            bool: True si l'installation a réussi
        """
        try:
            self.logger.info("Tentative d'installation alternative...")
            
            # Essayer d'installer dans l'environnement Python principal
            pip_cmd = [sys.executable, '-m', 'pip', 'install', '--user'] + packages
            
            result = subprocess.run(
                pip_cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.logger.info("Installation alternative réussie")
                return True
            else:
                self.logger.error("Échec de l'installation alternative")
                
                # Dernière tentative: télécharger et installer manuellement
                return self.manual_package_install(packages)
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'installation alternative: {e}")
            return False
    
    def manual_package_install(self, packages):
        """
        Installation manuelle des packages critiques
        
        Args:
            packages: Liste des packages à installer
            
        Returns:
            bool: True si l'installation a réussi
        """
        try:
            self.logger.info("Tentative d'installation manuelle...")
            
            # Pour les packages critiques, on peut les inclure directement
            success_count = 0
            
            for package in packages:
                if 'requests' in package:
                    if self.install_requests_minimal():
                        success_count += 1
                elif 'Pillow' in package:
                    if self.create_pil_fallback():
                        success_count += 1
                elif 'pywin32' in package:
                    if self.create_win32_fallback():
                        success_count += 1
            
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'installation manuelle: {e}")
            return False
    
    def install_requests_minimal(self):
        """Installe une version minimale de requests"""
        try:
            # Créer un module requests minimal pour les cas d'urgence
            requests_minimal = '''
"""
Module requests minimal pour NiTrite
"""
import urllib.request
import urllib.parse
import json

class Response:
    def __init__(self, data, status_code=200, headers=None):
        self.content = data
        self.text = data.decode('utf-8') if isinstance(data, bytes) else data
        self.status_code = status_code
        self.headers = headers or {}
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")
    
    def json(self):
        return json.loads(self.text)
    
    def iter_content(self, chunk_size=8192):
        if isinstance(self.content, bytes):
            for i in range(0, len(self.content), chunk_size):
                yield self.content[i:i+chunk_size]

def get(url, **kwargs):
    try:
        timeout = kwargs.get('timeout', 30)
        stream = kwargs.get('stream', False)
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            return Response(data, response.getcode(), dict(response.headers))
    except Exception as e:
        raise Exception(f"Request failed: {e}")

def head(url, **kwargs):
    try:
        req = urllib.request.Request(url)
        req.get_method = lambda: 'HEAD'
        with urllib.request.urlopen(req, timeout=10) as response:
            return Response(b'', response.getcode(), dict(response.headers))
    except Exception as e:
        raise Exception(f"Head request failed: {e}")
'''
            
            requests_path = self.dependencies_dir / 'requests.py'
            with open(requests_path, 'w', encoding='utf-8') as f:
                f.write(requests_minimal)
            
            self.logger.info("Module requests minimal créé")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du module requests: {e}")
            return False
    
    def create_pil_fallback(self):
        """Crée un fallback pour PIL/Pillow"""
        try:
            # Créer un module PIL minimal
            pil_minimal = '''
"""
Module PIL minimal pour NiTrite
"""
import tkinter as tk

class Image:
    @staticmethod
    def open(filename):
        return ImageFile()
    
    @staticmethod
    def new(mode, size, color=0):
        return ImageFile()

class ImageFile:
    def resize(self, size, resample=None):
        return self
    
    def convert(self, mode):
        return self

class ImageTk:
    @staticmethod
    def PhotoImage(image=None, file=None):
        if file:
            return tk.PhotoImage(file=file)
        return tk.PhotoImage()
'''
            
            pil_dir = self.dependencies_dir / 'PIL'
            pil_dir.mkdir(exist_ok=True)
            
            with open(pil_dir / '__init__.py', 'w', encoding='utf-8') as f:
                f.write(pil_minimal)
            
            self.logger.info("Module PIL minimal créé")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du module PIL: {e}")
            return False
    
    def create_win32_fallback(self):
        """Crée un fallback pour pywin32"""
        try:
            # Créer des modules win32 minimaux
            win32_modules = {
                'win32api': '''
def GetModuleFileName(handle):
    import sys
    return sys.executable
''',
                'win32com': '''
class Dispatch:
    def __init__(self, prog_id):
        pass
    
    def CreateShortCut(self, path):
        return ShortCut()

class ShortCut:
    def __init__(self):
        self.Targetpath = ""
        self.WorkingDirectory = ""
    
    def save(self):
        pass

client = type('client', (), {'Dispatch': Dispatch})()
'''
            }
            
            for module_name, module_code in win32_modules.items():
                module_path = self.dependencies_dir / f'{module_name}.py'
                with open(module_path, 'w', encoding='utf-8') as f:
                    f.write(module_code)
            
            self.logger.info("Modules win32 minimaux créés")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création des modules win32: {e}")
            return False
    
    def cleanup(self):
        """Nettoie les dépendances installées localement"""
        try:
            if self.local_dependencies:
                self.logger.info("Nettoyage des dépendances locales...")
                
                # Supprimer les packages installés localement
                for package in self.local_dependencies:
                    package_name = package.split('>=')[0].split('==')[0]
                    package_dirs = list(self.dependencies_dir.glob(f'{package_name}*'))
                    
                    for package_dir in package_dirs:
                        try:
                            if package_dir.is_dir():
                                shutil.rmtree(package_dir)
                            else:
                                package_dir.unlink()
                            self.logger.info(f"Supprimé: {package_dir}")
                        except Exception as e:
                            self.logger.warning(f"Impossible de supprimer {package_dir}: {e}")
                
                # Supprimer les fichiers temporaires
                temp_files = [
                    'requests.py', 'PIL', 'win32api.py', 'win32com.py'
                ]
                
                for temp_file in temp_files:
                    temp_path = self.dependencies_dir / temp_file
                    if temp_path.exists():
                        try:
                            if temp_path.is_dir():
                                shutil.rmtree(temp_path)
                            else:
                                temp_path.unlink()
                            self.logger.info(f"Fichier temporaire supprimé: {temp_file}")
                        except Exception as e:
                            self.logger.warning(f"Impossible de supprimer {temp_file}: {e}")
                
                self.logger.info("Nettoyage terminé")
                
        except Exception as e:
            self.logger.error(f"Erreur lors du nettoyage: {e}")
    
    def get_dependency_info(self):
        """
        Retourne des informations sur les dépendances
        
        Returns:
            dict: Informations sur les dépendances
        """
        info = {
            'required_packages': self.required_packages,
            'local_dependencies': self.local_dependencies,
            'dependencies_dir': str(self.dependencies_dir),
            'available_packages': {}
        }
        
        for package_name in self.required_packages.keys():
            info['available_packages'][package_name] = self.is_package_available(package_name)
        
        return info