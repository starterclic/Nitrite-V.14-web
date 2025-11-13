#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation du projet NiTrite v.2
Vérifie que toutes les dépendances et imports fonctionnent
"""

import sys
import io
import importlib
from pathlib import Path
import json

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("    VALIDATION DU PROJET NITRITE V.2")
print("=" * 70)
print()

errors = []
warnings = []

# Test 1: Vérifier les imports Python standard
print("[1/6] Vérification des imports Python standard...")
standard_imports = ['json', 'logging', 'pathlib', 'threading', 'subprocess', 'os', 'tempfile', 'zipfile', 'shutil']
for module in standard_imports:
    try:
        importlib.import_module(module)
        print(f"   ✅ {module}")
    except ImportError as e:
        errors.append(f"Module standard manquant: {module}")
        print(f"   ❌ {module}: {e}")
print()

# Test 2: Vérifier les dépendances externes
print("[2/6] Vérification des dépendances externes...")
external_deps = {
    'requests': 'requests',
    'PIL': 'Pillow',
    'win32com.client': 'pywin32',
    'winshell': 'winshell'
}
for module, package in external_deps.items():
    try:
        importlib.import_module(module)
        print(f"   ✅ {module} ({package})")
    except ImportError:
        warnings.append(f"Dépendance optionnelle manquante: {package}")
        print(f"   ⚠️  {module} ({package}) - Optionnel")
print()

# Test 3: Vérifier la structure des fichiers
print("[3/6] Vérification de la structure des fichiers...")
required_files = [
    'nitrite_complet.py',
    'src/gui_manager.py',
    'src/installer_manager.py',
    'src/elevation_helper.py',
    'src/winget_installer.py',
    'data/programs.json',
    'requirements.txt',
    'build_exe.py',
    'NiTrite_OrdiPlus_v2.spec'
]
for file_path in required_files:
    if Path(file_path).exists():
        print(f"   ✅ {file_path}")
    else:
        errors.append(f"Fichier manquant: {file_path}")
        print(f"   ❌ {file_path}")
print()

# Test 4: Valider programs.json
print("[4/6] Validation de programs.json...")
try:
    with open('data/programs.json', 'r', encoding='utf-8') as f:
        programs_data = json.load(f)
    
    total_programs = sum(len(progs) if isinstance(progs, dict) else 0 
                        for progs in programs_data.values())
    print(f"   ✅ JSON valide: {len(programs_data)} catégories, {total_programs} programmes")
    
    # Vérifier les champs obligatoires
    required_fields = ['description', 'category']
    invalid_programs = []
    
    for category, programs in programs_data.items():
        if isinstance(programs, dict):
            for prog_name, prog_info in programs.items():
                for field in required_fields:
                    if field not in prog_info:
                        invalid_programs.append(f"{prog_name} (manque '{field}')")
    
    if invalid_programs:
        warnings.append(f"Programmes avec champs manquants: {len(invalid_programs)}")
        print(f"   ⚠️  {len(invalid_programs)} programmes avec champs incomplets")
    else:
        print(f"   ✅ Tous les programmes ont les champs obligatoires")
        
except json.JSONDecodeError as e:
    errors.append(f"Erreur JSON: {e}")
    print(f"   ❌ JSON invalide: {e}")
except FileNotFoundError:
    errors.append("programs.json non trouvé")
    print(f"   ❌ programs.json non trouvé")
print()

# Test 5: Tester les imports du projet
print("[5/6] Test des imports du projet...")
sys.path.insert(0, str(Path.cwd() / 'src'))
try:
    from elevation_helper import is_admin, run_as_admin_silent, create_elevated_process
    print("   ✅ elevation_helper")
except ImportError as e:
    errors.append(f"Import elevation_helper échoué: {e}")
    print(f"   ❌ elevation_helper: {e}")

try:
    from winget_installer import WingetInstaller
    print("   ✅ winget_installer")
except ImportError as e:
    warnings.append(f"Import winget_installer échoué: {e}")
    print(f"   ⚠️  winget_installer: {e}")

try:
    from installer_manager import InstallerManager
    print("   ✅ installer_manager")
except ImportError as e:
    errors.append(f"Import installer_manager échoué: {e}")
    print(f"   ❌ installer_manager: {e}")

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    print("   ✅ tkinter (interface graphique)")
except ImportError as e:
    errors.append(f"Tkinter manquant: {e}")
    print(f"   ❌ tkinter: {e}")
print()

# Test 6: Vérifier le fichier spec PyInstaller
print("[6/6] Validation du fichier .spec...")
try:
    spec_file = Path('NiTrite_OrdiPlus_v2.spec')
    if spec_file.exists():
        spec_content = spec_file.read_text(encoding='utf-8')
        if 'nitrite_complet.py' in spec_content:
            print("   ✅ Fichier .spec valide")
        else:
            warnings.append("Fichier .spec ne référence pas nitrite_complet.py")
            print("   ⚠️  Fichier .spec incomplet")
    else:
        warnings.append("Fichier .spec manquant")
        print("   ⚠️  NiTrite_OrdiPlus_v2.spec manquant")
except Exception as e:
    warnings.append(f"Erreur lecture .spec: {e}")
    print(f"   ⚠️  Erreur: {e}")
print()

# Résumé
print("=" * 70)
print("    📊 RÉSUMÉ DE LA VALIDATION")
print("=" * 70)
print()

if errors:
    print(f"❌ ERREURS CRITIQUES ({len(errors)}):")
    for error in errors:
        print(f"   • {error}")
    print()

if warnings:
    print(f"⚠️  AVERTISSEMENTS ({len(warnings)}):")
    for warning in warnings:
        print(f"   • {warning}")
    print()

if not errors and not warnings:
    print("✅ PROJET VALIDÉ - Aucune erreur détectée!")
    print()
    print("🚀 Prêt pour la compilation:")
    print("   python build_exe.py")
    print()
    sys.exit(0)
elif not errors:
    print("✅ PROJET VALIDÉ - Quelques avertissements mineurs")
    print()
    print("🚀 Prêt pour la compilation (avec warnings):")
    print("   python build_exe.py")
    print()
    sys.exit(0)
else:
    print("❌ ÉCHEC DE LA VALIDATION")
    print()
    print("Corrigez les erreurs critiques avant de compiler.")
    print()
    sys.exit(1)

print("=" * 70)