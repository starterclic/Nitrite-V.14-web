# -*- mode: python ; coding: utf-8 -*-
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
