"""
Script de correction complète pour NiTrite v.2
Corrige tous les problèmes d'installation identifiés
"""

import json
import logging
import sys
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_empty_urls():
    """Corrige les URLs vides en ajoutant des URLs de téléchargement valides"""
    programs_file = Path(__file__).parent / 'data' / 'programs.json'
    
    if not programs_file.exists():
        logger.error(f"Fichier non trouvé: {programs_file}")
        return False
    
    logger.info("🔧 Correction des URLs vides...")
    
    # Charger le fichier
    with open(programs_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # URLs de remplacement pour les programmes populaires
    url_fixes = {
        "7-Zip": "https://www.7-zip.org/a/7z2301-x64.exe",
        "Visual Studio Code": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user",
        "Google Chrome": "https://dl.google.com/chrome/install/GoogleChromeStandaloneEnterprise64.msi",
        "Mozilla Firefox": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=fr",
        "VLC Media Player": "https://download.videolan.org/pub/videolan/vlc/last/win64/vlc-3.0.18-win64.exe",
        "Notepad++": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.8/npp.8.5.8.Installer.x64.exe",
        "Git": "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe",
        "Python": "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe",
        "Node.js": "https://nodejs.org/dist/v20.8.1/node-v20.8.1-x64.msi",
        "Adobe Acrobat Reader DC": "https://ardownload2.adobe.com/pub/adobe/reader/win/AcrobatDC/2300820360/AcroRdrDC2300820360_fr_FR.exe",
        "LibreOffice": "https://download.libreoffice.org/libreoffice/stable/7.6.2/win/x86_64/LibreOffice_7.6.2_Win_x64.msi",
        "GIMP": "https://download.gimp.org/pub/gimp/v2.10/windows/gimp-2.10.34-setup-3.exe",
        "Audacity": "https://github.com/audacity/audacity/releases/download/Audacity-3.4.2/audacity-win-3.4.2-64bit.exe",
        "OBS Studio": "https://github.com/obsproject/obs-studio/releases/download/29.1.3/OBS-Studio-29.1.3-Full-Installer-x64.exe"
    }
    
    urls_fixed = 0
    
    for category, programs in data.items():
        if not isinstance(programs, dict):
            continue
        
        for program_name, program_info in programs.items():
            if not program_info.get('download_url', '').strip():
                if program_name in url_fixes:
                    program_info['download_url'] = url_fixes[program_name]
                    urls_fixed += 1
                    logger.info(f"✅ URL ajoutée pour {program_name}")
    
    # Sauvegarder le fichier modifié
    if urls_fixed > 0:
        # Créer une sauvegarde
        backup_file = programs_file.with_suffix('.json.backup_urls_fix')
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Sauvegarder le fichier principal
        with open(programs_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ {urls_fixed} URLs corrigées et sauvegardées")
    else:
        logger.info("ℹ️ Aucune URL à corriger")
    
    return True

def create_requirements_file():
    """Crée un fichier requirements.txt optimisé"""
    requirements_content = """# NiTrite v.2 - Dépendances requises
requests>=2.31.0
urllib3>=2.0.0
certifi>=2023.0.0
packaging>=23.0

# Dépendances optionnelles (pour améliorer les fonctionnalités)
tqdm>=4.66.0
colorama>=0.4.6
psutil>=5.9.0

# Dépendances Windows (si disponibles)
pywin32>=306; sys_platform == "win32"
"""
    
    requirements_file = Path(__file__).parent / 'requirements.txt'
    try:
        with open(requirements_file, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        logger.info(f"✅ Fichier requirements.txt créé: {requirements_file}")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur création requirements.txt: {e}")
        return False

def create_install_dependencies_script():
    """Crée un script d'installation des dépendances"""
    script_content = """@echo off
echo Installation des dependances NiTrite v.2...
echo.

REM Installer les dependances via pip
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --user

echo.
echo Installation terminee!
pause
"""
    
    script_file = Path(__file__).parent / 'install_dependencies.bat'
    try:
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        logger.info(f"✅ Script d'installation créé: {script_file}")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur création script: {e}")
        return False

def test_winget_availability():
    """Teste la disponibilité de winget"""
    import subprocess
    try:
        result = subprocess.run(['winget', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info(f"✅ Winget disponible: {result.stdout.strip()}")
            return True
        else:
            logger.warning("⚠️ Winget non disponible")
            return False
    except Exception as e:
        logger.warning(f"⚠️ Erreur test winget: {e}")
        return False

def create_winget_installer_batch():
    """Crée un script batch pour installer winget si nécessaire"""
    script_content = """@echo off
echo Verification et installation de winget...
echo.

REM Tester si winget est deja installe
winget --version >nul 2>&1
if %errorlevel% == 0 (
    echo Winget est deja installe!
    goto :end
)

echo Winget non trouve, installation en cours...
echo.

REM Installer via Microsoft Store ou PowerShell
powershell -Command "& {Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe}"

echo.
echo Installation de winget terminee!

:end
pause
"""
    
    script_file = Path(__file__).parent / 'install_winget.bat'
    try:
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        logger.info(f"✅ Script winget créé: {script_file}")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur création script winget: {e}")
        return False

def main():
    """Fonction principale de correction"""
    logger.info("🔧 CORRECTION COMPLÈTE DE NITRITE V.2")
    logger.info("=" * 50)
    
    success_count = 0
    total_tasks = 5
    
    # 1. Corriger les URLs vides
    logger.info("1️⃣ Correction des URLs vides...")
    if fix_empty_urls():
        success_count += 1
    
    # 2. Créer requirements.txt
    logger.info("2️⃣ Création du fichier requirements.txt...")
    if create_requirements_file():
        success_count += 1
    
    # 3. Créer script d'installation des dépendances
    logger.info("3️⃣ Création du script d'installation des dépendances...")
    if create_install_dependencies_script():
        success_count += 1
    
    # 4. Tester winget
    logger.info("4️⃣ Test de winget...")
    if test_winget_availability():
        success_count += 1
    
    # 5. Créer script d'installation winget
    logger.info("5️⃣ Création du script d'installation winget...")
    if create_winget_installer_batch():
        success_count += 1
    
    # Rapport final
    logger.info("=" * 50)
    logger.info(f"📊 RAPPORT: {success_count}/{total_tasks} tâches réussies")
    
    if success_count == total_tasks:
        logger.info("✅ CORRECTION COMPLÈTE RÉUSSIE!")
        logger.info("🚀 Votre projet NiTrite v.2 est maintenant optimisé.")
        logger.info("")
        logger.info("📋 ÉTAPES SUIVANTES:")
        logger.info("1. Exécutez 'install_dependencies.bat' pour installer les dépendances")
        logger.info("2. Exécutez 'install_winget.bat' si winget n'est pas disponible")
        logger.info("3. Testez l'installation de quelques programmes")
    else:
        logger.warning("⚠️ Certaines corrections ont échoué")
        logger.info("Vérifiez les logs ci-dessus pour plus de détails")
    
    return success_count == total_tasks

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)