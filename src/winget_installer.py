"""
Installation automatique de winget dans la version portable
Télécharge et installe winget sans dépendances du système
"""
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import logging
import zipfile

try:
    import requests
except ImportError:
    requests = None

class WingetInstaller:
    """Installe winget automatiquement pour la version portable"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.winget_url = "https://github.com/microsoft/winget-cli/releases/latest/download/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle"
        self.vclibs_url = "https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx"
        self.xaml_url = "https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.8.6/Microsoft.UI.Xaml.2.8.x64.appx"
        
    def is_winget_installed(self):
        """Vérifie si winget est déjà installé"""
        try:
            result = subprocess.run(
                ["winget", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.logger.info(f"✅ Winget déjà installé: {version}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.logger.info("⚠️ Winget non installé")
        return False
    
    def download_file(self, url, destination):
        """Télécharge un fichier"""
        if not requests:
            self.logger.error("Module requests non disponible")
            return False
        
        try:
            self.logger.info(f"📥 Téléchargement: {url}")
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.logger.info(f"✅ Téléchargé: {destination}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur téléchargement: {e}")
            return False
    
    def install_winget(self, callback=None):
        """Installe winget et ses dépendances"""
        if self.is_winget_installed():
            if callback:
                callback("✅ Winget déjà installé")
            return True
        
        try:
            if callback:
                callback("📦 Installation de winget en cours...")
            
            # Créer dossier temporaire
            temp_dir = Path(tempfile.mkdtemp())
            self.logger.info(f"📁 Dossier temporaire: {temp_dir}")
            
            # Télécharger les dépendances
            vclibs_path = temp_dir / "VCLibs.appx"
            xaml_path = temp_dir / "UIXaml.appx"
            winget_path = temp_dir / "winget.msixbundle"
            
            if callback:
                callback("📥 Téléchargement des dépendances...")
            
            # 1. VCLibs
            if not self.download_file(self.vclibs_url, vclibs_path):
                if callback:
                    callback("❌ Échec téléchargement VCLibs")
                return False
            
            # 2. UI.Xaml
            if not self.download_file(self.xaml_url, xaml_path):
                if callback:
                    callback("❌ Échec téléchargement UI.Xaml")
                return False
            
            # 3. Winget
            if not self.download_file(self.winget_url, winget_path):
                if callback:
                    callback("❌ Échec téléchargement Winget")
                return False
            
            # Installation via PowerShell
            if callback:
                callback("⚙️ Installation de winget...")
            
            ps_script = f"""
            Add-AppxPackage -Path "{vclibs_path}"
            Add-AppxPackage -Path "{xaml_path}"
            Add-AppxPackage -Path "{winget_path}"
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Nettoyage
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            if result.returncode == 0:
                self.logger.info("✅ Winget installé avec succès")
                if callback:
                    callback("✅ Winget installé avec succès!")
                return True
            else:
                self.logger.error(f"❌ Erreur installation: {result.stderr}")
                if callback:
                    callback(f"❌ Erreur: {result.stderr[:100]}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'installation: {e}")
            if callback:
                callback(f"❌ Erreur: {str(e)[:100]}")
            return False
    
    def install_winget_if_needed(self, callback=None):
        """Vérifie et installe winget si nécessaire"""
        if self.is_winget_installed():
            return True
        
        self.logger.info("🔧 Installation automatique de winget...")
        return self.install_winget(callback)
