# -*- mode: python ; coding: utf-8 -*-
"""
Configuration PyInstaller pour NiTriTe V.13 Web Portable
Crée un exécutable standalone qui lance le serveur web et ouvre le navigateur
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collecter tous les fichiers web
web_files = []
for root, dirs, files in os.walk('web'):
    for file in files:
        file_path = os.path.join(root, file)
        dest_dir = os.path.dirname(file_path)
        web_files.append((file_path, dest_dir))

# Collecter les données
data_files = []
for root, dirs, files in os.walk('data'):
    for file in files:
        file_path = os.path.join(root, file)
        dest_dir = os.path.dirname(file_path)
        data_files.append((file_path, dest_dir))

# Collecter les assets
asset_files = []
for root, dirs, files in os.walk('assets'):
    for file in files:
        file_path = os.path.join(root, file)
        dest_dir = os.path.dirname(file_path)
        asset_files.append((file_path, dest_dir))

# Modules cachés à inclure
hidden_imports = [
    'flask',
    'flask_cors',
    'werkzeug',
    'jinja2',
    'click',
    'itsdangerous',
    'markupsafe',
    'psutil',
    'json',
    'subprocess',
    'platform',
    'shutil',
    'tempfile',
    'pathlib',
    'logging',
    # Modules du projet
    'installer_manager',
    'winget_manager',
    'elevation_helper',
    'config_manager',
    'portable_database',
    'tools_data_complete',
]

# Données supplémentaires de Flask
flask_datas = collect_data_files('flask')

a = Analysis(
    ['nitrite_web_portable.py'],
    pathex=[],
    binaries=[],
    datas=web_files + data_files + asset_files + flask_datas + [
        ('web_backend.py', '.'),
        ('src', 'src'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
        '_tkinter',
        'cv2',
    ],
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
    name='NiTriTe_Web_V13',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Afficher la console pour voir les logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
