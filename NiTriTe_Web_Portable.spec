# -*- mode: python ; coding: utf-8 -*-
"""
Configuration PyInstaller pour NiTriTe V.13 Web Portable
Crée un exécutable standalone avec serveur Flask intégré
"""

import os
import sys

block_cipher = None

# Collecter tous les fichiers du dossier web
web_datas = []
for root, dirs, files in os.walk('web'):
    for file in files:
        src = os.path.join(root, file)
        dst = os.path.dirname(src)
        web_datas.append((src, dst))

# Collecter les fichiers data
data_datas = []
for root, dirs, files in os.walk('data'):
    for file in files:
        src = os.path.join(root, file)
        dst = os.path.dirname(src)
        data_datas.append((src, dst))

# Collecter les assets
asset_datas = []
if os.path.exists('assets'):
    for root, dirs, files in os.walk('assets'):
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.dirname(src)
            asset_datas.append((src, dst))

# Collecter tous les fichiers Python du dossier src
src_datas = []
if os.path.exists('src'):
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                src = os.path.join(root, file)
                dst = os.path.dirname(src)
                src_datas.append((src, dst))

# web_backend.py à la racine
web_backend_data = []
if os.path.exists('web_backend.py'):
    web_backend_data = [('web_backend.py', '.')]

# Modules cachés nécessaires
hiddenimports = [
    # Flask et dépendances
    'flask',
    'flask.json',
    'flask.json.provider',
    'flask_cors',
    'werkzeug',
    'werkzeug.security',
    'werkzeug.datastructures',
    'jinja2',
    'jinja2.ext',
    'click',
    'itsdangerous',
    'markupsafe',

    # Modules standards
    'json',
    'subprocess',
    'platform',
    'shutil',
    'tempfile',
    'pathlib',
    'logging',
    'threading',
    'webbrowser',
    'time',

    # Modules optionnels
    'psutil',
    'winreg',

    # Modules du projet src/
    'installer_manager',
    'winget_manager',
    'elevation_helper',
    'config_manager',
    'portable_database',
    'tools_data_complete',
    'gui_modern_v13',
    'advanced_pages',
    'profiles_manager',
    'cleanup_manager',
    'dependency_manager',
    'modern_colors',
    'splash_screen',
    'layout_manager',
    'portable_paths',
    'translations',
    'url_updater',
    'winget_installer',
]

# Modules à exclure pour réduire la taille
excludes = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    'tkinter',
    '_tkinter',
    'cv2',
    'PyQt5',
    'PyQt6',
    'PySide2',
    'PySide6',
    'wx',
]

# Combiner toutes les données
all_datas = web_datas + data_datas + asset_datas + src_datas + web_backend_data

a = Analysis(
    ['nitrite_web_portable.py'],
    pathex=[],
    binaries=[],
    datas=all_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
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
    console=True,  # Console visible pour voir les logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
