#!/usr/bin/env python3
"""
Script de build pour NiTriTe V.13 - Version Bureau
Compile la version bureau Tkinter en exécutable portable .exe
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_header(text):
    """Affiche un en-tête"""
    print("\n" + "=" * 70)
    print(f"   {text}")
    print("=" * 70 + "\n")

def check_pyinstaller():
    """Vérifie si PyInstaller est installé"""
    try:
        import PyInstaller
        print("[OK] PyInstaller est installé")
        return True
    except ImportError:
        print("[ERREUR] PyInstaller n'est pas installé")
        print("\nInstallez-le avec: pip install pyinstaller")
        return False

def clean_build():
    """Nettoie les dossiers de build précédents"""
    print("[INFO] Nettoyage des builds précédents...")

    dirs_to_clean = ['build', 'dist/__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  - Supprimé: {dir_name}")

    print("[OK] Nettoyage terminé\n")

def build_executable():
    """Compile l'exécutable avec PyInstaller"""
    print_header("COMPILATION EN COURS")

    spec_file = "NiTriTe_V13.spec"

    if not os.path.exists(spec_file):
        print(f"[ERREUR] Fichier {spec_file} introuvable")
        return False

    print(f"[INFO] Utilisation du fichier: {spec_file}")
    print("[INFO] Cela peut prendre 2-5 minutes...\n")

    try:
        # Lancer PyInstaller
        result = subprocess.run(
            ['pyinstaller', '--clean', '--noconfirm', spec_file],
            check=True,
            capture_output=False
        )

        return True

    except subprocess.CalledProcessError as e:
        print(f"\n[ERREUR] La compilation a échoué (code: {e.returncode})")
        return False
    except Exception as e:
        print(f"\n[ERREUR] Erreur inattendue: {e}")
        return False

def verify_build():
    """Vérifie que l'exécutable a été créé"""
    exe_path = "dist/NiTriTe_V13_Modern.exe"

    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n[OK] Exécutable créé: {exe_path}")
        print(f"[INFO] Taille: {size_mb:.1f} MB")
        return True
    else:
        print(f"\n[ERREUR] Exécutable introuvable: {exe_path}")
        return False

def main():
    """Point d'entrée principal"""
    print_header("BUILD NiTriTe V.13 - Version Bureau")

    # Vérifier que nous sommes dans le bon dossier
    if not os.path.exists("nitrite_v13_modern.py"):
        print("[ERREUR] Fichier nitrite_v13_modern.py introuvable")
        print("Assurez-vous d'exécuter ce script depuis le dossier racine du projet")
        sys.exit(1)

    print("[OK] Dossier du projet détecté")

    # Vérifier PyInstaller
    if not check_pyinstaller():
        sys.exit(1)

    # Nettoyer
    clean_build()

    # Compiler
    if not build_executable():
        sys.exit(1)

    # Vérifier
    if not verify_build():
        sys.exit(1)

    # Succès
    print_header("BUILD TERMINE AVEC SUCCES !")

    print("L'exécutable est prêt à être utilisé:")
    print("  - Emplacement: dist/NiTriTe_V13_Modern.exe")
    print("  - Double-cliquez pour lancer")
    print("  - Totalement portable (aucune installation requise)")
    print("\n" + "=" * 70 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Build interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERREUR] Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
