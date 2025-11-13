
                Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
                Write-Host "  DISM - Scanner l'image" -ForegroundColor Yellow
                Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
                Write-Host ""
                
                # Exécuter la commande
                DISM /Online /Cleanup-Image /ScanHealth
                
                Write-Host ""
                Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
                Write-Host "  Terminé ! Appuyez sur une touche pour fermer..." -ForegroundColor Green
                Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                