# -*- coding: utf-8 -*-
"""
Build automatique de NiTrite en exécutable autonome
Aucune dépendance requise sur le PC cible
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path
import io

# Configurer l'encodage UTF-8 pour stdout/stderr
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("    🚀 BUILD EXÉCUTABLE AUTONOME - NiTriTe V12.0 Portable")
print("=" * 70)
print()

# Étape 1: Vérifier PyInstaller
print("[1/5] Vérification de PyInstaller...")
try:
    import PyInstaller
    print(f"✅ PyInstaller {PyInstaller.__version__} détecté")
except ImportError:
    print("📦 Installation de PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("✅ PyInstaller installé")
print()

# Étape 2: Nettoyer les anciens builds
print("[2/5] Nettoyage des anciens builds...")
for folder in ["build", "dist", "NiTriTe V12 Portable"]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"   🗑️  {folder}/ supprimé")
print("✅ Nettoyage terminé")
print()

# Étape 3: Build avec PyInstaller
print("[3/5] 🔨 Compilation (2-5 minutes)...")
print("   ⏳ Création d'un .exe avec Python + tkinter + dépendances...")
print()

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "scripts/NiTrite_v12_Final.spec"
]

result = subprocess.run(cmd, capture_output=False)

if result.returncode != 0:
    print("\n❌ Erreur lors de la compilation")
    sys.exit(1)

print()
print("✅ Compilation réussie !")
print()

# Étape 4: Créer le package de distribution
print("[4/5] 📦 Création du package...")

# Créer le dossier
os.makedirs("NiTriTe V12 Portable", exist_ok=True)

# Copier l'exécutable
exe_source = Path("dist/NiTrite_v12_Final.exe")
exe_dest = Path("NiTriTe V12 Portable/NiTriTe V12.0.exe")

if exe_source.exists():
    shutil.copy2(exe_source, exe_dest)
    size_mb = exe_source.stat().st_size / (1024 * 1024)
    print(f"   ✅ Exécutable copié ({size_mb:.1f} MB)")
else:
    print("   ❌ Exécutable introuvable!")
    sys.exit(1)

# Créer le lanceur
launcher_content = """@echo off
start "" "NiTriTe V12.0.exe"
"""
with open("NiTriTe V12 Portable/Lancer NiTriTe.bat", "w") as f:
    f.write(launcher_content)
print("   ✅ Lanceur créé")

# Créer le README
readme_content = """╔════════════════════════════════════════════════════════════════╗
║  🚀 NiTriTe V12.0 - VERSION PORTABLE AUTONOME                 ║
╚════════════════════════════════════════════════════════════════╝

✅ AUCUNE INSTALLATION REQUISE !

Cette version inclut TOUT :
  ✅ Python embarqué
  ✅ Tkinter (interface graphique V12.0)
  ✅ Toutes les dépendances
  ✅ Base de données de 715 programmes + 553 outils système

════════════════════════════════════════════════════════════════
🚀 UTILISATION
════════════════════════════════════════════════════════════════

Option 1 : Double-clic sur "Lancer NiTriTe.bat"
Option 2 : Double-clic sur "NiTriTe V12.0.exe"

C'est tout ! L'application s'ouvre immédiatement.

════════════════════════════════════════════════════════════════
⚙️ CONFIGURATION REQUISE
════════════════════════════════════════════════════════════════

✅ Windows 10 ou Windows 11
✅ 4 GB RAM minimum
✅ Connexion Internet (pour télécharger les programmes)
❌ AUCUNE installation Python requise
❌ AUCUNE dépendance à installer

════════════════════════════════════════════════════════════════
📋 FONCTIONNALITÉS V12.0
════════════════════════════════════════════════════════════════

🌐 715 programmes disponibles (25 catégories)
🛠️ 553 outils système (18 sections personnalisables)
📦 Installation automatique via WinGet
👤 Interface V12.0 avec titre multicolore vert pomme
⚡ Multi-threading pour vitesse optimale
🔒 Gestion automatique des privilèges admin
🎨 Design sombre premium avec boutons optimisés

════════════════════════════════════════════════════════════════
© 2025 NiTriTe V12.0 - Installation simplifiée Windows
════════════════════════════════════════════════════════════════
"""
with open("NiTriTe V12 Portable/README.txt", "w", encoding="utf-8") as f:
    f.write(readme_content)
print("   ✅ README créé")
print()

# Étape 5: Créer le ZIP
print("[5/5] 📦 Compression en ZIP...")
try:
    shutil.make_archive("NiTriTe V12 Portable", "zip", "NiTriTe V12 Portable")
    zip_size = Path("NiTriTe V12 Portable.zip").stat().st_size / (1024 * 1024)
    print(f"✅ ZIP créé ({zip_size:.1f} MB)")
except Exception as e:
    print(f"⚠️  Erreur lors de la création du ZIP: {e}")
print()

# Nettoyer
print("🧹 Nettoyage final...")
if os.path.exists("build"):
    shutil.rmtree("build")
print("✅ Nettoyage terminé")
print()

# Résultats
print("=" * 70)
print("    ✅ BUILD TERMINÉ AVEC SUCCÈS !")
print("=" * 70)
print()
print("📊 RÉSULTATS :")
print()
print("   📂 NiTriTe V12 Portable/")
print(f"      ├── NiTriTe V12.0.exe      (~{size_mb:.0f} MB)")
print("      ├── Lancer NiTriTe.bat")
print("      └── README.txt")
print()
print(f"   📦 NiTriTe V12 Portable.zip  (~{zip_size:.0f} MB)")
print()
print("=" * 70)
print()
print("🎯 POUR TESTER :")
print("   cd \"NiTriTe V12 Portable\"")
print("   \"Lancer NiTriTe.bat\"")
print()
print("📤 POUR DISTRIBUER :")
print("   Partagez : NiTriTe V12 Portable.zip")
print()
print("✨ L'utilisateur n'a RIEN à installer !")
print("   Juste décompresser et double-clic ! 🚀")
print()
print("=" * 70)
