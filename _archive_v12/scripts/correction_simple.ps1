# Script de correction simple pour NiTrite 1.0

Write-Host "Correction de l'erreur NiTrite 1.0..." -ForegroundColor Yellow

$projectPath = "C:\Users\Momo\Documents\Projet NiTrite 1.0"
$scriptPath = Join-Path $projectPath "AppInstallerGUI.ps1"

if (Test-Path $scriptPath) {
    # Faire une sauvegarde
    $backupPath = $scriptPath + ".backup"
    Copy-Item $scriptPath $backupPath -Force
    Write-Host "Sauvegarde creee: $backupPath" -ForegroundColor Green
    
    # Lire et corriger le contenu
    $content = Get-Content $scriptPath -Raw -Encoding UTF8
    
    $oldLine = '$type = $cmbTypeFilter.SelectedItem.Content.ToString()'
    $newLine = 'if ($cmbTypeFilter.SelectedItem -ne $null -and $cmbTypeFilter.SelectedItem.Content -ne $null) { $type = $cmbTypeFilter.SelectedItem.Content.ToString() } else { $type = "Tous" }'
    
    if ($content -match [regex]::Escape($oldLine)) {
        $newContent = $content -replace [regex]::Escape($oldLine), $newLine
        $newContent | Out-File $scriptPath -Encoding UTF8 -Force
        Write-Host "Script corrige avec succes!" -ForegroundColor Green
    } else {
        Write-Host "Ligne problematique non trouvee" -ForegroundColor Yellow
    }
} else {
    Write-Host "Script non trouve: $scriptPath" -ForegroundColor Red
}

Write-Host "Correction terminee!" -ForegroundColor Green
Read-Host "Appuyez sur Entree pour continuer"