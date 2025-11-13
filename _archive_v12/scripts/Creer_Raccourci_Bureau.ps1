# Creation d'un raccourci sur le bureau pour NiTrite v.2
# Script PowerShell pour creer un raccourci pratique

Write-Host "Creation du raccourci NiTrite v.2 sur le bureau..." -ForegroundColor Cyan

try {
    # Chemins
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $targetPath = Join-Path $scriptPath "Lancer_NiTrite.bat"
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "NiTrite v.2.lnk"
    
    # Verifier que le fichier cible existe
    if (-not (Test-Path $targetPath)) {
        Write-Host "Erreur: Lancer_NiTrite.bat non trouve!" -ForegroundColor Red
        exit 1
    }
    
    # Creer le raccourci
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $targetPath
    $Shortcut.WorkingDirectory = $scriptPath
    $Shortcut.Description = "NiTrite v.2 - Installateur de programmes silencieux"
    $Shortcut.IconLocation = "imageres.dll,21"
    $Shortcut.Save()
    
    Write-Host "Raccourci cree avec succes!" -ForegroundColor Green
    Write-Host "Emplacement: $shortcutPath" -ForegroundColor Yellow
    Write-Host "Vous pouvez maintenant double-cliquer sur 'NiTrite v.2' sur votre bureau!" -ForegroundColor Cyan
    
} catch {
    Write-Host "Erreur lors de la creation du raccourci: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Raccourci cree! Appuyez sur Entree pour continuer..." -ForegroundColor Green
Read-Host