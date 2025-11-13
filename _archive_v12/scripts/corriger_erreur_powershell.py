"""
Script de correction pour l'erreur PowerShell NiTrite 1.0
Corrige l'erreur "Impossible d'appeler une méthode dans une expression Null"
"""

import os
import sys
import subprocess
from pathlib import Path

def find_nitrite_1_project():
    """Trouve le projet NiTrite 1.0"""
    potential_paths = [
        r"C:\Users\Momo\Documents\Projet NiTrite 1.0",
        r"C:\Users\Momo\Documents\NiTrite 1.0",
        r"C:\Users\Momo\Desktop\Projet NiTrite 1.0"
    ]
    
    for path in potential_paths:
        if Path(path).exists():
            return Path(path)
    
    return None

def check_powershell_script(script_path):
    """Vérifie le script PowerShell problématique"""
    if not script_path.exists():
        return False, "Script non trouvé"
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher la ligne problématique
        problematic_line = "$type = $cmbTypeFilter.SelectedItem.Content.ToString()"
        
        if problematic_line in content:
            return True, "Ligne problématique trouvée"
        else:
            return False, "Ligne problématique non trouvée"
            
    except Exception as e:
        return False, f"Erreur de lecture: {e}"

def create_powershell_fix():
    """Crée un script PowerShell pour corriger l'erreur"""
    
    fix_script = '''
# Script de correction pour NiTrite 1.0
# Corrige l'erreur "Impossible d'appeler une méthode dans une expression Null"

Write-Host "🔧 Correction de l'erreur NiTrite 1.0..." -ForegroundColor Yellow

$projectPath = "C:\\Users\\Momo\\Documents\\Projet NiTrite 1.0"

if (-not (Test-Path $projectPath)) {
    Write-Host "❌ Projet NiTrite 1.0 non trouvé à $projectPath" -ForegroundColor Red
    exit 1
}

$scriptPath = Join-Path $projectPath "AppInstallerGUI.ps1"

if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ Script AppInstallerGUI.ps1 non trouvé" -ForegroundColor Red
    exit 1
}

# Faire une sauvegarde
$backupPath = $scriptPath + ".backup"
Copy-Item $scriptPath $backupPath -Force
Write-Host "✅ Sauvegarde créée: $backupPath" -ForegroundColor Green

# Lire le contenu du script
$content = Get-Content $scriptPath -Raw -Encoding UTF8

# Rechercher et remplacer la ligne problématique
$problematicLine = '$type = $cmbTypeFilter.SelectedItem.Content.ToString()'
$fixedLine = @'
# Correction pour éviter l'erreur null
if ($cmbTypeFilter.SelectedItem -ne $null -and $cmbTypeFilter.SelectedItem.Content -ne $null) {
    $type = $cmbTypeFilter.SelectedItem.Content.ToString()
} else {
    $type = "Tous"
    Write-Host "⚠️  Filtre de type non défini, utilisation de 'Tous'" -ForegroundColor Yellow
}
'@

if ($content -match [regex]::Escape($problematicLine)) {
    $newContent = $content -replace [regex]::Escape($problematicLine), $fixedLine
    
    # Sauvegarder le fichier corrigé
    $newContent | Out-File $scriptPath -Encoding UTF8 -Force
    
    Write-Host "✅ Script corrigé avec succès!" -ForegroundColor Green
    Write-Host "📝 La ligne problématique a été remplacée par une vérification sécurisée" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  Ligne problématique non trouvée dans le script" -ForegroundColor Yellow
    Write-Host "Le script pourrait déjà être corrigé ou avoir été modifié" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Actions recommandées:" -ForegroundColor Cyan
Write-Host "1. Testez le script corrigé"
Write-Host "2. Si le problème persiste, consultez les logs"
Write-Host "3. En cas de problème, restaurez depuis $backupPath"
Write-Host ""
Write-Host "✅ Correction terminée!" -ForegroundColor Green
'''
    
    fix_script_path = Path(__file__).parent / 'corriger_nitrite_1.ps1'
    
    try:
        with open(fix_script_path, 'w', encoding='utf-8') as f:
            f.write(fix_script)
        
        return fix_script_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du script de correction: {e}")
        return None

def create_isolation_script():
    """Crée un script pour isoler les deux projets NiTrite"""
    
    isolation_script = '''
"""
Script d'isolation pour éviter les conflits entre NiTrite 1.0 et NiTrite v.2
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_running_nitrite_processes():
    """Vérifie les processus NiTrite en cours"""
    print("🔍 Vérification des processus NiTrite...")
    
    try:
        # Vérifier PowerShell avec NiTrite
        result = subprocess.run([
            'powershell', '-Command', 
            'Get-Process | Where-Object {$_.ProcessName -like "*powershell*" -and $_.MainWindowTitle -like "*NiTrite*"}'
        ], capture_output=True, text=True, timeout=5)
        
        if result.stdout.strip():
            print("⚠️  NiTrite 1.0 (PowerShell) détecté en cours d'exécution")
            return True
        else:
            print("✅ Aucun processus NiTrite 1.0 détecté")
            return False
            
    except Exception as e:
        print(f"ℹ️  Vérification des processus: {e}")
        return False

def stop_nitrite_1_processes():
    """Arrête les processus NiTrite 1.0"""
    print("🛑 Arrêt des processus NiTrite 1.0...")
    
    try:
        subprocess.run([
            'powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowTitle -like "*NiTrite*"} | Stop-Process -Force'
        ], capture_output=True, text=True, timeout=10)
        
        print("✅ Processus NiTrite 1.0 arrêtés")
        time.sleep(2)
        
    except Exception as e:
        print(f"⚠️  Arrêt partiel des processus: {e}")

def set_nitrite_v2_environment():
    """Configure l'environnement pour NiTrite v.2"""
    print("⚙️  Configuration de l'environnement NiTrite v.2...")
    
    # Variables d'environnement pour éviter les conflits
    os.environ['NITRITE_VERSION'] = '2.0'
    os.environ['NITRITE_MODE'] = 'PYTHON'
    os.environ['POWERSHELL_NITRITE_DISABLED'] = '1'
    
    print("✅ Environnement configuré pour NiTrite v.2")

def launch_nitrite_v2():
    """Lance NiTrite v.2 en mode isolé"""
    print("🚀 Lancement de NiTrite v.2...")
    
    try:
        current_dir = Path(__file__).parent
        nitrite_script = current_dir / 'nitrite_installer.py'
        
        if nitrite_script.exists():
            subprocess.run([sys.executable, str(nitrite_script)])
        else:
            print("❌ Script NiTrite v.2 non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

def main():
    """Fonction principale d'isolation"""
    print("🔧 NiTrite - Script d'isolation des versions")
    print("=" * 50)
    
    # Vérifier et arrêter NiTrite 1.0 si nécessaire
    if check_running_nitrite_processes():
        response = input("Voulez-vous arrêter NiTrite 1.0 pour lancer NiTrite v.2 ? (o/n): ")
        if response.lower() == 'o':
            stop_nitrite_1_processes()
    
    # Configurer l'environnement
    set_nitrite_v2_environment()
    
    # Lancer NiTrite v.2
    launch_nitrite_v2()

if __name__ == "__main__":
    main()
'''
    
    isolation_script_path = Path(__file__).parent / 'isoler_versions.py'
    
    try:
        with open(isolation_script_path, 'w', encoding='utf-8') as f:
            f.write(isolation_script)
        
        return isolation_script_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du script d'isolation: {e}")
        return None

def main():
    """Fonction principale"""
    print("🔧 Correction de l'erreur NiTrite 1.0")
    print("=" * 50)
    
    # Trouver le projet NiTrite 1.0
    nitrite_1_path = find_nitrite_1_project()
    
    if nitrite_1_path:
        print(f"✅ Projet NiTrite 1.0 trouvé: {nitrite_1_path}")
        
        script_path = nitrite_1_path / "AppInstallerGUI.ps1"
        has_error, message = check_powershell_script(script_path)
        
        print(f"📋 Vérification du script: {message}")
        
        if has_error:
            print("\n🔧 Création du script de correction...")
            fix_script = create_powershell_fix()
            
            if fix_script:
                print(f"✅ Script de correction créé: {fix_script}")
                print("\nPour corriger l'erreur, exécutez:")
                print(f"powershell -ExecutionPolicy Bypass -File \"{fix_script}\"")
            
    else:
        print("⚠️  Projet NiTrite 1.0 non trouvé")
        print("L'erreur pourrait provenir d'un autre emplacement")
    
    # Créer le script d'isolation
    print("\n🔧 Création du script d'isolation...")
    isolation_script = create_isolation_script()
    
    if isolation_script:
        print(f"✅ Script d'isolation créé: {isolation_script}")
    
    print("\n" + "=" * 50)
    print("💡 SOLUTIONS DISPONIBLES:")
    print("=" * 50)
    print("1. 🔧 corriger_nitrite_1.ps1 - Corrige l'erreur PowerShell")
    print("2. 🔄 isoler_versions.py - Isole les deux versions")
    print("3. 🚀 Utilisez NiTrite v.2 (notre projet Python) qui n'a pas ce problème")
    
    print("\n🎯 RECOMMANDATION:")
    print("Utilisez NiTrite v.2 qui est plus stable et ne présente pas ces erreurs!")
    
    response = input("\nVoulez-vous lancer NiTrite v.2 maintenant ? (o/n): ")
    if response.lower() == 'o':
        try:
            current_dir = Path(__file__).parent
            subprocess.run([sys.executable, str(current_dir / 'nitrite_installer.py')])
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
    input("\nAppuyez sur Entrée pour continuer...")