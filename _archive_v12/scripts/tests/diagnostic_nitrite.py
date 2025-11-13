"""
Script de diagnostic pour NiTrite v.2
Identifie les problèmes potentiels et propose des solutions
"""

import sys
import os
import subprocess
import json
from pathlib import Path
import logging

def check_powershell_scripts():
    """Vérifie s'il y a des scripts PowerShell qui interfèrent"""
    print("🔍 Vérification des scripts PowerShell en cours...")
    
    try:
        # Vérifier les processus PowerShell en cours
        result = subprocess.run([
            'powershell', '-Command', 
            'Get-Process -Name powershell, pwsh -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, StartTime'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("  ✅ PowerShell accessible")
            if result.stdout.strip():
                print("  📊 Processus PowerShell détectés:")
                print(result.stdout)
        else:
            print("  ⚠️  Problème d'accès à PowerShell")
            
    except subprocess.TimeoutExpired:
        print("  ⏰ Timeout lors de la vérification PowerShell")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

def check_conflicting_software():
    """Vérifie s'il y a des logiciels qui pourraient interférer"""
    print("\n🔍 Vérification des logiciels potentiellement conflictuels...")
    
    # Logiciels connus pour causer des problèmes
    potential_conflicts = [
        'ninite', 'chocolatey', 'winget', 'scoop'
    ]
    
    for software in potential_conflicts:
        try:
            result = subprocess.run([
                'where', software
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  ⚠️  {software.upper()} détecté: {result.stdout.strip()}")
            else:
                print(f"  ✅ {software.upper()} non installé")
                
        except Exception:
            print(f"  ✅ {software.upper()} non accessible")

def check_registry_permissions():
    """Vérifie les permissions d'accès au registre"""
    print("\n🔍 Vérification des permissions registre...")
    
    try:
        import winreg
        
        # Test d'accès en lecture au registre
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE")
        winreg.CloseKey(key)
        print("  ✅ Accès lecture au registre OK")
        
        # Test d'accès aux clés des programmes installés
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
            winreg.CloseKey(key)
            print("  ✅ Accès aux informations des programmes installés OK")
        except Exception as e:
            print(f"  ⚠️  Problème d'accès aux informations des programmes: {e}")
            
    except Exception as e:
        print(f"  ❌ Erreur d'accès au registre: {e}")

def check_antivirus_interference():
    """Vérifie les interférences potentielles de l'antivirus"""
    print("\n🔍 Vérification des interférences antivirus...")
    
    try:
        # Vérifier Windows Defender
        result = subprocess.run([
            'powershell', '-Command', 
            'Get-MpPreference | Select-Object DisableRealtimeMonitoring'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if "True" in result.stdout:
                print("  ✅ Windows Defender temps réel désactivé")
            else:
                print("  ⚠️  Windows Defender temps réel actif (peut causer des blocages)")
        
    except Exception as e:
        print(f"  ❌ Impossible de vérifier Windows Defender: {e}")

def check_disk_space():
    """Vérifie l'espace disque disponible"""
    print("\n🔍 Vérification de l'espace disque...")
    
    try:
        import shutil
        
        # Vérifier l'espace sur le disque C:
        total, used, free = shutil.disk_usage("C:\\")
        free_gb = free / (1024**3)
        total_gb = total / (1024**3)
        
        print(f"  📊 Espace libre sur C:: {free_gb:.1f} GB / {total_gb:.1f} GB")
        
        if free_gb < 1:
            print("  ❌ Espace disque insuffisant (< 1 GB)")
        elif free_gb < 5:
            print("  ⚠️  Espace disque faible (< 5 GB)")
        else:
            print("  ✅ Espace disque suffisant")
            
    except Exception as e:
        print(f"  ❌ Erreur lors de la vérification de l'espace: {e}")

def check_network_connectivity():
    """Vérifie la connectivité réseau"""
    print("\n🔍 Vérification de la connectivité réseau...")
    
    test_urls = [
        "https://www.google.com",
        "https://download.mozilla.org",
        "https://dl.google.com"
    ]
    
    for url in test_urls:
        try:
            import requests
            response = requests.head(url, timeout=5)
            if response.status_code < 400:
                print(f"  ✅ {url} accessible")
            else:
                print(f"  ⚠️  {url} retourne {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {url} inaccessible: {e}")

def check_nitrite_configuration():
    """Vérifie la configuration de NiTrite"""
    print("\n🔍 Vérification de la configuration NiTrite...")
    
    config_file = Path("data/config.json")
    programs_file = Path("data/programs.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("  ✅ Fichier config.json valide")
            print(f"    Version: {config.get('app_version', 'non définie')}")
            print(f"    Langue: {config.get('language', 'non définie')}")
        except Exception as e:
            print(f"  ❌ Erreur dans config.json: {e}")
    else:
        print("  ❌ Fichier config.json manquant")
    
    if programs_file.exists():
        try:
            with open(programs_file, 'r', encoding='utf-8') as f:
                programs = json.load(f)
            print(f"  ✅ Fichier programs.json valide ({len(programs)} programmes)")
        except Exception as e:
            print(f"  ❌ Erreur dans programs.json: {e}")
    else:
        print("  ❌ Fichier programs.json manquant")

def check_python_environment():
    """Vérifie l'environnement Python"""
    print("\n🔍 Vérification de l'environnement Python...")
    
    print(f"  📊 Version Python: {sys.version}")
    print(f"  📊 Exécutable Python: {sys.executable}")
    
    # Vérifier les modules requis
    required_modules = ['tkinter', 'requests', 'PIL', 'win32api']
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ Module {module} disponible")
        except ImportError:
            print(f"  ❌ Module {module} manquant")

def generate_solutions():
    """Génère des solutions pour les problèmes détectés"""
    print("\n" + "="*60)
    print("💡 SOLUTIONS RECOMMANDÉES")
    print("="*60)
    
    print("\n🔧 Pour résoudre l'erreur 'LogPath':")
    print("1. Fermez tous les scripts PowerShell en cours")
    print("2. Redémarrez votre terminal PowerShell")
    print("3. Lancez NiTrite avec des droits administrateur")
    print("4. Vérifiez qu'aucun autre installateur n'est en cours")
    
    print("\n🔧 Pour optimiser les installations:")
    print("1. Désactivez temporairement l'antivirus")
    print("2. Fermez les programmes en cours d'utilisation")
    print("3. Libérez de l'espace disque si nécessaire")
    print("4. Vérifiez votre connexion Internet")
    
    print("\n🔧 Pour éviter les conflits:")
    print("1. N'utilisez qu'un seul installateur à la fois")
    print("2. Évitez de lancer plusieurs instances de NiTrite")
    print("3. Attendez la fin d'une installation avant d'en lancer une autre")

def main():
    """Fonction principale de diagnostic"""
    print("🩺 NiTrite v.2 - Diagnostic du système")
    print("="*60)
    
    # Changer vers le dossier du projet
    try:
        os.chdir(Path(__file__).parent.parent.parent  # scripts/tests/ -> racine)
    except:
        pass
    
    # Exécuter tous les checks
    check_python_environment()
    check_nitrite_configuration()
    check_powershell_scripts()
    check_conflicting_software()
    check_registry_permissions()
    check_antivirus_interference()
    check_disk_space()
    check_network_connectivity()
    
    # Générer les solutions
    generate_solutions()
    
    print("\n✅ Diagnostic terminé!")
    print("Si les problèmes persistent, consultez les solutions ci-dessus.")

if __name__ == "__main__":
    main()
    input("\nAppuyez sur Entrée pour continuer...")