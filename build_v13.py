#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de build pour NiTriTe V13.0
Crée un exécutable portable avec PyInstaller

⚠️ IMPORTANT : Ce script doit être exécuté sur Windows !

   NiTriTe est une application Windows utilisant :
   - tkinter (GUI Windows)
   - win32 API (privilèges admin)
   - Chemins Windows

   Voir GUIDE_BUILD_WINDOWS.md pour instructions complètes
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import zipfile
from datetime import datetime

# Couleurs pour le terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Afficher un en-tête"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_step(step_num, text):
    """Afficher une étape"""
    print(f"{Colors.OKBLUE}{Colors.BOLD}[Étape {step_num}]{Colors.ENDC} {text}")

def print_success(text):
    """Afficher un succès"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    """Afficher un avertissement"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    """Afficher une erreur"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def check_dependencies():
    """Vérifier et installer toutes les dépendances automatiquement"""
    print_step(1, "Vérification et installation des dépendances...")

    # Vérifier Python
    if sys.version_info < (3, 8):
        print_error("Python 3.8+ requis")
        print("\n💡 Téléchargez Python depuis: https://www.python.org/downloads/")
        input("\nAppuyez sur ENTRÉE pour fermer...")
        return False
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} OK")

    # Liste complète des dépendances requises
    required_packages = {
        'pyinstaller': 'PyInstaller',
        'PIL': 'Pillow',
        'requests': 'requests',
        'urllib3': 'urllib3',
        'certifi': 'certifi',
    }

    # Dépendances optionnelles mais recommandées
    optional_packages = {
        'psutil': 'psutil',
        'tqdm': 'tqdm',
        'colorama': 'colorama',
    }

    # Windows uniquement
    if sys.platform == 'win32':
        required_packages['win32api'] = 'pywin32'

    missing = []

    # Vérifier les dépendances requises
    print("\n📦 Vérification des dépendances requises...")
    for module_name, package_name in required_packages.items():
        try:
            if module_name == 'pyinstaller':
                import PyInstaller
                print_success(f"{package_name} {PyInstaller.__version__}")
            elif module_name == 'PIL':
                import PIL
                print_success(f"{package_name} {PIL.__version__}")
            elif module_name == 'requests':
                import requests
                print_success(f"{package_name} {requests.__version__}")
            elif module_name == 'urllib3':
                import urllib3
                print_success(f"{package_name} {urllib3.__version__}")
            elif module_name == 'certifi':
                import certifi
                print_success(f"{package_name}")
            elif module_name == 'win32api':
                import win32api
                print_success(f"{package_name}")
        except ImportError:
            print_warning(f"{package_name} manquant")
            missing.append(package_name)

    # Si des dépendances manquent, installer automatiquement
    if missing:
        print(f"\n⚠️  {len(missing)} dépendance(s) manquante(s)")
        print("📥 Installation automatique depuis requirements.txt...\n")

        try:
            # Installer toutes les dépendances depuis requirements.txt
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                check=True,
                capture_output=False
            )

            if result.returncode != 0:
                print_error("L'installation a échoué")
                print("\n💡 Essayez manuellement:")
                print("   pip install -r requirements.txt")
                input("\nAppuyez sur ENTRÉE pour fermer...")
                return False

            print_success("✓ Toutes les dépendances ont été installées")

            # Revérifier
            print("\n🔄 Revérification...")
            still_missing = []
            for module_name, package_name in required_packages.items():
                try:
                    if module_name == 'pyinstaller':
                        import PyInstaller
                    elif module_name == 'PIL':
                        import PIL
                    elif module_name == 'requests':
                        import requests
                    elif module_name == 'win32api':
                        import win32api
                    print_success(f"{package_name} OK")
                except ImportError:
                    still_missing.append(package_name)

            if still_missing:
                print_error(f"Certaines dépendances n'ont pas pu être installées: {', '.join(still_missing)}")
                print("\n💡 Installez manuellement:")
                for pkg in still_missing:
                    print(f"   pip install {pkg}")
                input("\nAppuyez sur ENTRÉE pour fermer...")
                return False

        except subprocess.CalledProcessError as e:
            print_error(f"Échec de l'installation des dépendances (code {e.returncode})")
            print("\n💡 Essayez manuellement:")
            print("   pip install -r requirements.txt")
            print("\nOu installez une par une:")
            print("   pip install pyinstaller pillow requests pywin32")
            input("\nAppuyez sur ENTRÉE pour fermer...")
            return False
        except Exception as e:
            print_error(f"Erreur inattendue: {e}")
            import traceback
            traceback.print_exc()
            input("\nAppuyez sur ENTRÉE pour fermer...")
            return False

    # Vérifier tkinter (inclus avec Python sur Windows)
    try:
        import tkinter
        print_success("tkinter OK (inclus avec Python)")
    except ImportError:
        print_warning("tkinter non trouvé - Réinstaller Python avec tcl/tk")

    print_success("\n✓ Toutes les dépendances sont installées (mode portable)")
    return True

def clean_build():
    """Nettoyer les anciens builds"""
    print_step(2, "Nettoyage des anciens builds...")

    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print_success(f"Supprimé : {dir_name}/")

    # Nettoyer les __pycache__ dans src/
    for root, dirs, files in os.walk('src'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))

    print_success("Nettoyage terminé")

def create_spec_file():
    """Créer le fichier .spec pour PyInstaller"""
    print_step(3, "Création du fichier .spec...")

    spec_content = """# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis(
    ['nitrite_v13_modern.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),  # Inclure TOUT le dossier src/
        ('data', 'data'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        # Tkinter et GUI
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        # PIL/Pillow
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL._tkinter_finder',
        # Networking
        'requests',
        'urllib3',
        'certifi',
        'http.client',
        'urllib.request',
        # Modules de l'application (src/)
        'src.modern_colors',  # COULEURS (évite import circulaire!)
        'src.translations',  # SYSTÈME DE TRADUCTION FR/EN (NOUVEAU!)
        'src.gui_modern_v13',
        'src.advanced_pages',  # PAGES AVANCÉES (CRITIQUE!)
        'src.tools_data_complete',
        'src.profiles_manager',
        'src.portable_paths',  # MODULE PORTABLE (IMPORTANT!)
        'src.portable_database',
        'src.layout_manager',  # MODULE DE RÉORGANISATION (NOUVEAU!)
        'src.installer_manager',
        'src.winget_manager',
        'src.winget_installer',
        'src.config_manager',
        'src.dependency_manager',
        'src.elevation_helper',
        'src.cleanup_manager',
        'src.url_updater',
        # Diagnostics système (CRITIQUE pour pages avancées!)
        'psutil',
        'psutil._common',
        'psutil._psutil_windows',
        'psutil._pswindows',
        'wmi',
        'win32com',
        'win32com.client',
        'pythoncom',
        'pywintypes',
        # Windows API (pour privilèges admin et système)
        'win32api',
        'win32con',
        'win32process',
        'win32security',
        'win32event',
        'win32file',
        # Bibliothèques standard nécessaires
        'json',
        'threading',
        'webbrowser',
        'datetime',
        'logging',
        'pathlib',
        'sqlite3',
        'subprocess',
        'shutil',
        'platform',
        'tempfile',
        'zipfile',
        'time',
        'os',
        'sys',
        're',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NiTriTe_V13_Modern',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI mode
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
"""

    with open('NiTriTe_V13.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print_success("Fichier .spec créé")

def build_executable():
    """Compiler l'exécutable avec PyInstaller"""
    print_step(4, "Compilation de l'exécutable...")
    print("⏳ Cette étape peut prendre 2-5 minutes...\n")

    try:
        # Exécuter PyInstaller via python -m (plus fiable que 'pyinstaller' direct)
        # Cela fonctionne même si pyinstaller.exe n'est pas dans le PATH
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', '--clean', '--noconfirm', 'NiTriTe_V13.spec'],
            capture_output=False,  # Afficher la sortie en temps réel
            text=True
        )

        if result.returncode != 0:
            print_error(f"PyInstaller a échoué avec le code : {result.returncode}")
            print("\n💡 Conseils de dépannage :")
            print("  1. Vérifiez que tous les modules sont installés : pip install -r requirements.txt")
            print("  2. Vérifiez les erreurs ci-dessus pour voir quel module manque")
            print("  3. Assurez-vous d'être sur Windows avec Python 3.8+")
            print("  4. Essayez de supprimer build/ et dist/ puis relancez")
            print("\n💡 Relisez TOUTES les erreurs ci-dessus pour comprendre le problème")
            input("\nAppuyez sur ENTRÉE pour fermer...")
            return False

        # Vérifier que l'exe a bien été créé
        exe_path = Path('dist') / 'NiTriTe_V13_Modern.exe'
        if not exe_path.exists():
            print_error("L'exécutable n'a pas été créé dans dist/")
            print("\n💡 Vérifiez les messages d'erreur de PyInstaller ci-dessus")
            print("💡 L'exe devrait être dans: dist/NiTriTe_V13_Modern.exe")
            input("\nAppuyez sur ENTRÉE pour fermer...")
            return False

        print_success("Compilation terminée")
        return True

    except FileNotFoundError:
        print_error("Python non trouvé ! Vérifiez votre installation Python")
        input("\nAppuyez sur ENTRÉE pour fermer...")
        return False
    except Exception as e:
        print_error(f"Erreur inattendue lors de la compilation : {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Une erreur inattendue s'est produite")
        print("\n💡 Si le message dit 'No module named PyInstaller', réinstallez:")
        print("   pip install --force-reinstall pyinstaller")
        input("\nAppuyez sur ENTRÉE pour fermer...")
        return False

def create_portable_package():
    """Créer le package portable"""
    print_step(5, "Création du package portable...")

    try:
        # Créer le dossier de distribution à la racine du projet
        dist_dir = Path('dist')
        package_name = "NiTriTe V13.1 Portable"
        package_dir = Path(package_name)  # À la racine, pas dans dist/

        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir(parents=True, exist_ok=True)

        # Copier l'exécutable
        exe_name = 'NiTriTe_V13_Modern.exe'
        if (dist_dir / exe_name).exists():
            shutil.copy2(dist_dir / exe_name, package_dir / exe_name)
            print_success(f"Copié : {exe_name}")
        else:
            print_error(f"Exécutable non trouvé : {exe_name}")
            print("\n💡 L'exe devrait être dans dist/NiTriTe_V13_Modern.exe")
            print("💡 Vérifiez que l'étape de compilation s'est bien terminée")
            input("\nAppuyez sur ENTRÉE pour fermer...")
            return False

        # Copier les fichiers essentiels
        files_to_copy = [
            'README_V13.md',
            'LANCER.bat',
        ]

        for file_name in files_to_copy:
            if os.path.exists(file_name):
                shutil.copy2(file_name, package_dir / file_name)
                print_success(f"Copié : {file_name}")

        # Créer un fichier README pour le package
        readme_content = """# NiTriTe V13.1 - Édition Portable

## 🚀 Démarrage Rapide

1. Double-cliquez sur `NiTriTe_V13_Modern.exe`
2. L'application se lance automatiquement
3. Aucune installation requise !

## 📦 Contenu

- `NiTriTe_V13_Modern.exe` - Application principale (8 pages avancées)
- `README_V13.md` - Documentation complète
- `LANCER.bat` - Raccourci de lancement (optionnel)

## ✨ Nouvelles Fonctionnalités V13.1

### 📦 Applications (715 apps)
- 24 catégories optimisées
- Grille 4 colonnes pour meilleure lisibilité
- Scroll fluide avec roulette souris

### 🛠️ Outils Système (553+ outils)
- Organisation par sections repliables
- Réorganisation drag & drop des catégories
- Scroll automatique au survol

### 🔄 Vérifications & Mises à Jour
- Détection apps installées (winget)
- Vérification mises à jour disponibles
- Update automatique en un clic

### 💾 Backup & Restauration
- Sauvegarde liste apps installées
- Création point de restauration Windows
- Backup drivers système (DISM)

### ⚡ Optimisations Windows
- Désactivation télémétrie Microsoft
- Gestion services et démarrage
- Nettoyage registre

### 🔍 Diagnostic & Benchmark
- Tests performances CPU, GPU, RAM, disque
- Score de santé PC global
- Comparaison avant/après maintenance

### ⚙️ Paramètres
- 4 thèmes (sombre/clair orange, bleu, violet)
- Mode clair/sombre toggle
- Statistiques visuelles (graphiques)

## 💡 Utilisation

### Page Applications
- Recherchez et sélectionnez les applications à installer
- Cliquez sur 🌐 pour accéder au site web
- Cliquez sur "INSTALLER SÉLECTION" pour installer en masse

### Page Outils
- Accédez à 553+ outils système
- Repliez/dépliez les sections par catégorie
- Réorganisez l'ordre des catégories (▲/▼)
- Cliquez sur un outil pour l'exécuter

## ⚠️ Avertissement

Cette application nécessite :
- Windows 10/11 (64-bit)
- Privilèges administrateur pour certaines installations
- Connexion Internet pour télécharger les applications
- WinGet (intégré à Windows 11, ou App Installer sur Windows 10)

## 📞 Support

Pour plus d'informations, consultez README_V13.md

Version : 13.1
Date : {date}
Type : Portable Edition
Build : Production
""".format(date=datetime.now().strftime('%Y-%m-%d'))

        with open(package_dir / 'README.txt', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print_success("Créé : README.txt")

        # Créer l'archive ZIP à la racine
        print("\n📦 Création de l'archive ZIP...")
        zip_path = Path(f"{package_name}.zip")  # À la racine

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(package_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(Path('.'))
                    zipf.write(file_path, arcname)
                    print(f"  + {arcname}")

        print_success(f"Archive créée : {zip_path.name}")

        # Afficher les tailles
        exe_size = (package_dir / exe_name).stat().st_size / (1024 * 1024)
        zip_size = zip_path.stat().st_size / (1024 * 1024)

        print(f"\n📊 Tailles :")
        print(f"  - Exécutable : {exe_size:.1f} MB")
        print(f"  - Archive ZIP : {zip_size:.1f} MB")
        print(f"  - Dossier portable : {package_name}/")

        print(f"\n✨ Package prêt dans : {Colors.BOLD}{package_name}/{Colors.ENDC}")

        return True

    except Exception as e:
        print_error(f"Erreur lors de la création du package : {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Vérifiez que vous avez les droits d'écriture dans dist/")
        input("\nAppuyez sur ENTRÉE pour fermer...")
        return False

def main():
    """Fonction principale"""
    print_header("NiTriTe V13.0 - Build Script Automatique")
    print(f"{Colors.OKCYAN}Build portable avec installation automatique des dépendances{Colors.ENDC}\n")
    print("📦 Ce script va automatiquement :")
    print("   1. Vérifier Python 3.8+")
    print("   2. Installer TOUTES les dépendances (PyInstaller, Pillow, etc.)")
    print("   3. Nettoyer les anciens builds")
    print("   4. Créer le fichier .spec avec 548 outils")
    print("   5. Compiler l'exe portable (35-50 MB)")
    print("   6. Créer le package ZIP final")
    print()
    print(f"{Colors.WARNING}⚠️  Durée totale : 5-10 minutes (première fois){Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓  Aucune action manuelle requise !{Colors.ENDC}\n")

    # Vérifier la plateforme
    if sys.platform != "win32":
        print_warning(f"⚠️  Plateforme détectée : {sys.platform}")
        print_warning("Ce script est conçu pour Windows !")
        print()
        print("NiTriTe V13 est une application Windows utilisant :")
        print("  - tkinter (GUI Windows)")
        print("  - win32 API (privilèges admin)")
        print("  - Chemins Windows spécifiques")
        print()
        print(f"{Colors.OKBLUE}📚 Consultez GUIDE_BUILD_WINDOWS.md pour instructions{Colors.ENDC}")
        print()
        response = input("Continuer quand même ? (y/N) : ").strip().lower()
        if response != 'y':
            print("Build annulé.")
            return 0

    # Vérifier qu'on est dans le bon dossier
    if not os.path.exists('nitrite_v13_modern.py'):
        print_error("Fichier nitrite_v13_modern.py non trouvé")
        print("Assurez-vous d'exécuter ce script depuis le dossier racine du projet")
        return 1

    # Exécuter les étapes
    steps = [
        (check_dependencies, "Vérification des dépendances"),
        (clean_build, "Nettoyage"),
        (create_spec_file, "Création du fichier .spec"),
        (build_executable, "Compilation"),
        (create_portable_package, "Packaging"),
    ]

    for step_func, step_name in steps:
        result = step_func()
        if result is False:
            print_error(f"Échec à l'étape : {step_name}")
            print("\n💡 Consultez les messages ci-dessus pour voir l'erreur")
            print("📚 Documentation : BUILD_SIMPLE.md ou BUILD_QUICK_START.md\n")
            input("Appuyez sur ENTRÉE pour fermer...")
            return 1
        print()

    # Succès !
    print_header("BUILD TERMINÉ AVEC SUCCÈS")
    print(f"{Colors.OKGREEN}{Colors.BOLD}🎉 NiTriTe V13.1 est prêt !{Colors.ENDC}\n")
    print(f"📦 Package disponible dans : {Colors.BOLD}NiTriTe V13.1 Portable/{Colors.ENDC}\n")
    print(f"📦 Archive ZIP disponible : {Colors.BOLD}NiTriTe V13.1 Portable.zip{Colors.ENDC}\n")
    print(f"{Colors.OKCYAN}Vous pouvez maintenant distribuer le dossier ou l'archive ZIP !{Colors.ENDC}\n")

    # Pause pour que l'utilisateur puisse lire les messages
    input("\nAppuyez sur ENTRÉE pour fermer...")
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Build interrompu par l'utilisateur{Colors.ENDC}")
        input("\nAppuyez sur ENTRÉE pour fermer...")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Une erreur inattendue s'est produite")
        print("📚 Consultez BUILD_SIMPLE.md pour le dépannage\n")
        input("Appuyez sur ENTRÉE pour fermer...")
        sys.exit(1)
