# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Chemins relatifs pour la portabilité
# Le .spec est dans scripts/, donc remonter au parent (racine du projet)
BASE_DIR = Path(SPECPATH).parent

a = Analysis(
    [str(BASE_DIR / 'nitrite_complet.py')],
    pathex=[],
    binaries=[],
    datas=[
        (str(BASE_DIR / 'data'), 'data'),
        (str(BASE_DIR / 'src'), 'src'),
        (str(BASE_DIR / 'assets'), 'assets')
    ],
    hiddenimports=[
        'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.messagebox',
        'PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL._tkinter_finder',
        'win32com.client', 'winshell', 'pywintypes', 'win32api',
        'requests', 'urllib3', 'charset_normalizer', 'certifi', 'idna',
        'packaging', 'packaging.version', 'packaging.specifiers',
        'logging', 'logging.handlers', 'json', 'pathlib', 'threading'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NiTrite_v12_Final',
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
)
