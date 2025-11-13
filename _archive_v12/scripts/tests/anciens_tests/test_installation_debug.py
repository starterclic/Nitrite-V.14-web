"""
Test d'installation simple pour déboguer
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
from pathlib import Path

# Configuration des chemins
if getattr(sys, 'frozen', False):
    app_dir = Path(sys.executable).parent
else:
    app_dir = Path(__file__).parent.parent.parent  # scripts/tests/anciens_tests/ -> racine

sys.path.insert(0, str(app_dir / 'src'))

from config_manager import ConfigManager
from installer_manager import InstallerManager

def test_installation():
    """Test d'installation d'un programme"""
    
    # Créer fenêtre de test
    root = tk.Tk()
    root.title("Test Installation NiTrite")
    root.geometry("800x600")
    
    # Zone de log
    log_text = scrolledtext.ScrolledText(root, height=30)
    log_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def log(message):
        log_text.insert('end', message + '\n')
        log_text.see('end')
        root.update()
    
    # Initialiser les managers
    log("📦 Initialisation des managers...")
    config_manager = ConfigManager()
    installer_manager = InstallerManager(config_manager)
    
    log(f"✅ {len(installer_manager.programs)} programmes chargés")
    
    # Trouver AnyDesk Portable (programme simple)
    anydesk = None
    for category, progs in installer_manager.programs.items():
        if "AnyDesk Portable" in progs:
            anydesk = progs["AnyDesk Portable"]
            log(f"✅ Trouvé: AnyDesk Portable dans {category}")
            break
    
    if not anydesk:
        log("❌ AnyDesk Portable non trouvé!")
        return
    
    log(f"📋 Info programme:")
    log(f"   URL: {anydesk.get('download_url', 'N/A')}")
    log(f"   Args: {anydesk.get('install_args', 'N/A')}")
    log(f"   Portable: {anydesk.get('portable', False)}")
    log(f"   Admin: {anydesk.get('admin_required', 'N/A')}")
    
    # Bouton d'installation
    def installer():
        log("\n" + "="*60)
        log("🚀 DÉMARRAGE DE L'INSTALLATION")
        log("="*60)
        
        try:
            # Créer la liste des programmes sélectionnés
            selected = {
                "Outils OrdiPlus": {
                    "AnyDesk Portable": anydesk
                }
            }
            
            log("📝 Programmes sélectionnés:")
            for cat, progs in selected.items():
                for name in progs.keys():
                    log(f"   • {name} ({cat})")
            
            # Lancer l'installation
            log("\n🔧 Appel de installer_manager.install_programs()...")
            
            # Callback pour les logs
            def progress_callback(message):
                log(f"   {message}")
            
            installer_manager.install_programs(selected, progress_callback)
            
            log("\n✅ Installation terminée!")
            
        except Exception as e:
            log(f"\n❌ ERREUR: {e}")
            import traceback
            log("\n📋 Traceback complet:")
            log(traceback.format_exc())
    
    btn = tk.Button(root, text="🚀 INSTALLER ANYDESK", command=installer, 
                    bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                    padx=20, pady=10)
    btn.pack(pady=10)
    
    log("\n✅ Interface prête. Cliquez sur le bouton pour tester l'installation.")
    
    root.mainloop()

if __name__ == "__main__":
    test_installation()
