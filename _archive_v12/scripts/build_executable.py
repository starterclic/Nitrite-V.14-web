"""
Script pour créer un exécutable standalone de NiTrite v.2
Utilise PyInstaller pour créer un .exe indépendant
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Installe PyInstaller si nécessaire"""
    try:
        import PyInstaller
        print("PyInstaller est déjà installé")
        return True
    except ImportError:
        print("Installation de PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("PyInstaller installé avec succès")
            return True
        except subprocess.CalledProcessError:
            print("Erreur lors de l'installation de PyInstaller")
            return False

def create_executable():
    """Crée l'exécutable avec PyInstaller"""
    
    # Vérifier que PyInstaller est disponible
    if not install_pyinstaller():
        return False
    
    # Paramètres de PyInstaller
    project_root = Path(__file__).parent.parent
    script_path = project_root / 'NiTrite_Standalone.py'  # Nouveau script unique
    
    # Vérifier si l'icône existe
    icon_path = project_root / 'assets' / 'icon.ico'
    
    pyinstaller_args = [
        sys.executable,                 # Utiliser le Python actuel
        '-m', 'PyInstaller',            # Lancer PyInstaller comme module
        '--onefile',                    # Un seul fichier exécutable
        '--windowed',                   # Sans console (interface graphique)
        '--name', 'NiTrite_OrdiPlus_v2',  # Nom de l'exécutable
    ]
    
    # Ajouter l'icône seulement si elle existe
    if icon_path.exists():
        pyinstaller_args.extend(['--icon', str(icon_path)])
    
    # Ajouter les données et imports (uniquement data et assets, plus src/)
    pyinstaller_args.extend([
        '--add-data', f'{project_root / "data"};data',      # Inclure le dossier data
        '--add-data', f'{project_root / "assets"};assets',  # Inclure le dossier assets (logo)
        '--hidden-import', 'tkinter',   # Imports cachés
        '--hidden-import', 'tkinter.ttk',
        '--hidden-import', 'tkinter.scrolledtext',
        '--hidden-import', 'tkinter.simpledialog',
        '--hidden-import', 'PIL',
        '--hidden-import', 'PIL.Image',
        '--hidden-import', 'PIL.ImageTk',
        '--clean',                      # Nettoyer avant compilation
        '--noconfirm',                  # Pas de confirmation
        str(script_path)
    ])
    
    print("Création de l'exécutable en cours...")
    print(f"Commande: {' '.join(pyinstaller_args)}")
    
    try:
        subprocess.check_call(pyinstaller_args)
        print("\n✅ Exécutable créé avec succès!")
        print("📁 Fichier généré: dist/NiTrite_OrdiPlus_v2.exe")
        
        # Instructions pour l'utilisateur
        print("\n📋 Instructions:")
        print("1. L'exécutable se trouve dans le dossier 'dist'")
        print("2. Vous pouvez le déplacer où vous voulez")
        print("3. L'exécutable est complètement autonome")
        print("4. Il créera automatiquement ses dossiers de travail")
        print("\n🎨 Fonctionnalités incluses:")
        print("   • Interface avec thème Ordi Plus (orange #FF6B00 et bleu #003366)")
        print("   • Logo Ordi Plus en arrière-plan")
        print("   • 279 programmes dans 25 catégories")
        print("   • 28 outils de réparation système")
        print("   • 12 commandes de mise à jour Winget")
        print("   • Fonction d'ajout de programmes personnalisés")
        print("   • Fonction de réorganisation des programmes")
        print("   • Interface optimisée 4 colonnes")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de la création de l'exécutable: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ PyInstaller non trouvé dans le PATH")
        return False

def create_spec_file():
    """Crée un fichier .spec personnalisé pour plus de contrôle"""
    
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['NiTrite_Standalone.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.simpledialog',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
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
    name='NiTrite_OrdiPlus_v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='assets/icon.ico'
)
"""
    
    spec_path = Path(__file__).parent / 'nitrite.spec'
    try:
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        print(f"Fichier .spec créé: {spec_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la création du fichier .spec: {e}")
        return False

def create_version_info():
    """Crée un fichier d'informations de version pour l'exécutable"""
    
    version_info = """
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'Ordi Plus France'),
            StringStruct(u'FileDescription', u'NiTrite v.2 Ordi Plus - Installateur de programmes automatique avec interface Ordi Plus'),
            StringStruct(u'FileVersion', u'2.0.0.0'),
            StringStruct(u'InternalName', u'NiTrite_OrdiPlus_v2'),
            StringStruct(u'LegalCopyright', u'Copyright © 2024 Ordi Plus France'),
            StringStruct(u'OriginalFilename', u'NiTrite_OrdiPlus_v2.exe'),
            StringStruct(u'ProductName', u'NiTrite v.2 Ordi Plus Edition'),
            StringStruct(u'ProductVersion', u'2.0.0.0')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    version_path = Path(__file__).parent / 'version_info.txt'
    try:
        with open(version_path, 'w', encoding='utf-8') as f:
            f.write(version_info)
        print(f"Fichier de version créé: {version_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la création du fichier de version: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 NiTrite v.2 Ordi Plus - Générateur d'exécutable")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon dossier
    project_root = Path(__file__).parent.parent
    if not (project_root / 'NiTrite_Standalone.py').exists():
        print("❌ Erreur: NiTrite_Standalone.py non trouvé")
        print("Assurez-vous d'exécuter ce script depuis le dossier du projet")
        return
    
    # Vérifier que les assets existent
    if not (project_root / 'assets' / 'logo_ordiplus_bg.png').exists():
        print("⚠️ Avertissement: Logo Ordi Plus non trouvé")
        print("   Le logo sera absent de l'exécutable")
    
    print("✅ Script unique NiTrite_Standalone.py trouvé")
    print("📝 Ce script contient TOUT le code en un seul fichier")
    
    # Créer les fichiers nécessaires
    print("\n📝 Création des fichiers de configuration...")
    create_version_info()
    
    # Créer l'exécutable
    if create_executable():
        print("\n🎉 Build terminé avec succès!")
        
        # Informations sur le fichier créé
        exe_path = Path('dist') / 'NiTrite_OrdiPlus_v2.exe'
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 Taille de l'exécutable: {size_mb:.1f} MB")
            print(f"📁 Emplacement: {exe_path.absolute()}")
        
    else:
        print("\n❌ Échec de la création de l'exécutable")
        print("Vérifiez les messages d'erreur ci-dessus")

if __name__ == "__main__":
    main()