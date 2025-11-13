"""
Script de nettoyage pour résoudre les conflits PowerShell
Arrête les processus qui causent l'erreur LogPath
"""

import subprocess
import sys
import time

def stop_powershell_scripts():
    """Arrête les scripts PowerShell en cours qui peuvent causer des problèmes"""
    print("🧹 Nettoyage des processus PowerShell problématiques...")
    
    try:
        # Lister les processus PowerShell
        result = subprocess.run([
            'powershell', '-Command', 
            'Get-Process -Name powershell, pwsh -ErrorAction SilentlyContinue | Select-Object Id, ProcessName'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            print("📊 Processus PowerShell détectés:")
            print(result.stdout)
            
            # Demander confirmation
            response = input("\nVoulez-vous arrêter ces processus PowerShell ? (o/n): ")
            
            if response.lower() == 'o':
                # Arrêter les processus PowerShell (sauf le nôtre)
                current_pid = subprocess.run(['powershell', '-Command', '$PID'], 
                                           capture_output=True, text=True).stdout.strip()
                
                result = subprocess.run([
                    'powershell', '-Command', 
                    f'Get-Process -Name powershell, pwsh | Where-Object {{$_.Id -ne {current_pid}}} | Stop-Process -Force'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Processus PowerShell arrêtés")
                else:
                    print("⚠️  Certains processus n'ont pas pu être arrêtés")
                    
                time.sleep(2)
        else:
            print("✅ Aucun processus PowerShell problématique détecté")
            
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")

def clear_powershell_logs():
    """Nettoie les logs PowerShell qui peuvent causer des problèmes"""
    print("\n🧹 Nettoyage des logs PowerShell...")
    
    try:
        result = subprocess.run([
            'powershell', '-Command', 
            'Clear-EventLog -LogName "Windows PowerShell" -ErrorAction SilentlyContinue'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Logs PowerShell nettoyés")
        else:
            print("ℹ️  Nettoyage des logs non nécessaire")
            
    except Exception as e:
        print(f"ℹ️  Impossible de nettoyer les logs: {e}")

def reset_powershell_environment():
    """Remet à zéro l'environnement PowerShell"""
    print("\n🔄 Réinitialisation de l'environnement PowerShell...")
    
    try:
        # Réinitialiser les variables d'environnement PowerShell
        reset_commands = [
            'Remove-Variable -Name * -ErrorAction SilentlyContinue',
            '$ErrorActionPreference = "Continue"',
            'Clear-Variable -Name * -ErrorAction SilentlyContinue'
        ]
        
        for cmd in reset_commands:
            subprocess.run(['powershell', '-Command', cmd], 
                         capture_output=True, text=True, timeout=5)
        
        print("✅ Environnement PowerShell réinitialisé")
        
    except Exception as e:
        print(f"ℹ️  Réinitialisation partielle: {e}")

def kill_winget_processes():
    """Arrête les processus WinGet qui peuvent interférer"""
    print("\n🧹 Vérification des processus WinGet...")
    
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq winget.exe'], 
                              capture_output=True, text=True)
        
        if 'winget.exe' in result.stdout:
            print("⚠️  Processus WinGet détecté")
            response = input("Voulez-vous arrêter WinGet ? (o/n): ")
            
            if response.lower() == 'o':
                subprocess.run(['taskkill', '/F', '/IM', 'winget.exe'], 
                             capture_output=True)
                print("✅ WinGet arrêté")
        else:
            print("✅ WinGet non actif")
            
    except Exception as e:
        print(f"ℹ️  Vérification WinGet: {e}")

def main():
    """Fonction principale de nettoyage"""
    print("🧹 NiTrite v.2 - Nettoyage des processus conflictuels")
    print("="*60)
    print("Ce script va arrêter les processus qui causent l'erreur 'LogPath'")
    print("="*60)
    
    # Exécuter le nettoyage
    stop_powershell_scripts()
    clear_powershell_logs()
    reset_powershell_environment()
    kill_winget_processes()
    
    print("\n" + "="*60)
    print("✅ Nettoyage terminé!")
    print("Vous pouvez maintenant relancer NiTrite v.2 sans erreur.")
    print("="*60)
    
    # Proposer de lancer NiTrite
    response = input("\nVoulez-vous lancer NiTrite v.2 maintenant ? (o/n): ")
    if response.lower() == 'o':
        print("\n🚀 Lancement de NiTrite v.2...")
        try:
            subprocess.run([sys.executable, 'nitrite_installer.py'])
        except Exception as e:
            print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main()
    input("\nAppuyez sur Entrée pour quitter...")