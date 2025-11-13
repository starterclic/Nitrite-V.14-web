# Script de vérification NiTrite v.2.5 OrdiPlus
# Vérifie que tous les fichiers et dépendances sont en place

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   🔍 VÉRIFICATION NITRITE v.2.5 ORDIPLUS EDITION" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# Fonction pour vérifier un fichier
function Test-FileExists {
    param($path, $description)
    if (Test-Path $path) {
        Write-Host "✅ $description" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ MANQUANT: $description" -ForegroundColor Red
        return $false
    }
}

# Fonction pour vérifier un module Python
function Test-PythonModule {
    param($module, $description)
    $result = python -c "import $module" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Module Python: $description" -ForegroundColor Green
        return $true
    } else {
        Write-Host "⚠️  MANQUANT: Module Python $description" -ForegroundColor Yellow
        return $false
    }
}

Write-Host "📁 VÉRIFICATION DES FICHIERS PRINCIPAUX" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray

if (-not (Test-FileExists "nitrite_complet.py" "Script principal")) { $errors++ }
if (-not (Test-FileExists "Lancer_NiTrite.bat" "Lanceur principal")) { $errors++ }
if (-not (Test-FileExists "Lancer_NiTrite_OrdiPlus.bat" "Lanceur OrdiPlus")) { $errors++ }
if (-not (Test-FileExists "install_requirements.bat" "Script installation dépendances")) { $errors++ }

Write-Host ""
Write-Host "📂 VÉRIFICATION DES DOSSIERS" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray

if (-not (Test-FileExists "data" "Dossier data")) { $errors++ }
if (-not (Test-FileExists "src" "Dossier src")) { $errors++ }
if (-not (Test-FileExists "logs" "Dossier logs")) { 
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "   📁 Dossier logs créé" -ForegroundColor Cyan
}
if (-not (Test-FileExists "downloads" "Dossier downloads")) { 
    New-Item -ItemType Directory -Path "downloads" | Out-Null
    Write-Host "   📁 Dossier downloads créé" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "📄 VÉRIFICATION DES FICHIERS DATA" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray

if (-not (Test-FileExists "data\programs.json" "Base de données programmes")) { $errors++ }
if (-not (Test-FileExists "data\office_links.json" "Configuration Office")) { $warnings++ }

Write-Host ""
Write-Host "🔧 VÉRIFICATION DES SOURCES" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray

if (-not (Test-FileExists "src\gui_manager_complet.py" "Interface graphique")) { $errors++ }
if (-not (Test-FileExists "src\installer_manager.py" "Gestionnaire installation")) { $warnings++ }
if (-not (Test-FileExists "src\config_manager.py" "Gestionnaire configuration")) { $warnings++ }

Write-Host ""
Write-Host "📚 VÉRIFICATION DE LA DOCUMENTATION" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray

Test-FileExists "README_V2.5_ORDIPLUS.md" "README principal" | Out-Null
Test-FileExists "CHANGELOG_ORDIPLUS.md" "Journal des modifications" | Out-Null
Test-FileExists "GUIDE_INSTALLATION_ORDIPLUS.md" "Guide d'installation" | Out-Null
Test-FileExists "DEMARRAGE_RAPIDE.md" "Guide démarrage rapide" | Out-Null
Test-FileExists "RECAP_MODIFICATIONS.md" "Récapitulatif modifications" | Out-Null
Test-FileExists "APERCU_VISUEL.md" "Aperçu visuel" | Out-Null

Write-Host ""
Write-Host "🐍 VÉRIFICATION DE PYTHON" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray

$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python installé: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python NON INSTALLÉ" -ForegroundColor Red
    Write-Host "   📥 Télécharger depuis: https://www.python.org/downloads/" -ForegroundColor Yellow
    $errors++
}

Write-Host ""
Write-Host "📦 VÉRIFICATION DES MODULES PYTHON" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray

if (-not (Test-PythonModule "tkinter" "tkinter (GUI)")) { $warnings++ }
if (-not (Test-PythonModule "requests" "requests (HTTP)")) { $warnings++ }
if (-not (Test-PythonModule "win32com.client" "pywin32 (Windows)")) { 
    Write-Host "   💡 Installer avec: pip install pywin32" -ForegroundColor Cyan
    $warnings++ 
}
if (-not (Test-PythonModule "winshell" "winshell (Bureau)")) { 
    Write-Host "   💡 Installer avec: pip install winshell" -ForegroundColor Cyan
    $warnings++ 
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                      📊 RÉSUMÉ" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "🎉 PARFAIT ! Tout est en ordre !" -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ NiTrite v.2.5 OrdiPlus est prêt à l'emploi" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Pour démarrer :" -ForegroundColor Cyan
    Write-Host "   1. Double-clic sur: Lancer_NiTrite_OrdiPlus.bat" -ForegroundColor White
    Write-Host ""
} elseif ($errors -eq 0 -and $warnings -gt 0) {
    Write-Host "⚠️  $warnings avertissement(s) détecté(s)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 Actions recommandées :" -ForegroundColor Cyan
    Write-Host "   1. Exécuter: install_requirements.bat" -ForegroundColor White
    Write-Host "   2. Ou manuellement: pip install pywin32 winshell requests" -ForegroundColor White
    Write-Host ""
    Write-Host "ℹ️  NiTrite devrait fonctionner, mais certaines fonctionnalités" -ForegroundColor Gray
    Write-Host "   (création dossier Bureau) pourraient ne pas marcher." -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "❌ $errors erreur(s) et $warnings avertissement(s) détecté(s)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Actions requises :" -ForegroundColor Yellow
    Write-Host "   1. Vérifier que tous les fichiers sont présents" -ForegroundColor White
    Write-Host "   2. Installer Python si manquant" -ForegroundColor White
    Write-Host "   3. Exécuter: install_requirements.bat" -ForegroundColor White
    Write-Host ""
}

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Pause pour lire les résultats
Read-Host "Appuyez sur Entrée pour quitter"
