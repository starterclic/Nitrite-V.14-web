
# Script de correction pour NiTrite 1.0
# Corrige l'erreur "Impossible d'appeler une méthode dans une expression Null"

Write-Host "🔧 Correction de l'erreur NiTrite 1.0..." -ForegroundColor Yellow

$projectPath = "C:\Users\Momo\Documents\Projet NiTrite 1.0"

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
