"""
GUI Manager avec MAXIMUM de visibilité pour NiTrite v.2
Interface optimisée pour afficher clairement toutes les applications
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from pathlib import Path
from datetime import datetime
import logging

class NiTriteGUIMaxVisibility:
    def __init__(self, root, installer_manager=None, config_manager=None):
        self.root = root
        self.installer_manager = installer_manager
        self.config_manager = config_manager
        
        # Variables pour les programmes
        self.program_vars = {}
        self.programs = {}
        self.category_frames = {}
        self.is_installing = False
        
        # Charger les programmes
        self.load_programs()
        
        # Interface
        self.setup_window()
        self.setup_styles()
        self.create_main_interface()
        
        # Logging
        self.logger = logging.getLogger(__name__)
    
    def setup_window(self):
        """Configure la fenêtre principale pour MAXIMUM de visibilité"""
        self.root.title("🚀 NiTrite v.2 - Installateur Automatique de Programmes")
        
        # MAXIMISER complètement la fenêtre
        self.root.state('zoomed')  # Windows maximize
        
        # Configuration responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Couleur de fond claire
        self.root.configure(bg='#ffffff')
        
        # Icône (si disponible)
        try:
            icon_path = Path(__file__).parent.parent / 'assets' / 'icon.ico'
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception:
            pass
    
    def setup_styles(self):
        """Configure les styles pour maximum de visibilité"""
        style = ttk.Style()
        
        # Style principal avec contraste élevé
        style.theme_use('clam')
        
        # Styles personnalisés pour visibilité maximale
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 18, 'bold'),
                       foreground='#2c3e50',
                       background='#ffffff')
        
        style.configure('Category.TLabel', 
                       font=('Segoe UI', 14, 'bold'),
                       foreground='#34495e',
                       background='#ecf0f1')
        
        style.configure('Program.TCheckbutton', 
                       font=('Segoe UI', 11),
                       foreground='#2c3e50',
                       background='#ffffff',
                       focuscolor='#3498db')
        
        style.configure('Action.TButton', 
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#ffffff',
                       background='#e74c3c')
        
        style.configure('Select.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#ffffff',
                       background='#3498db')
        
        style.configure('Clear.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='#ffffff',
                       background='#95a5a6')
    
    def create_main_interface(self):
        """Crée l'interface principale avec MAXIMUM de visibilité"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # En-tête avec titre très visible
        self.create_header(main_frame)
        
        # Barre d'outils avec boutons de sélection rapide
        self.create_toolbar(main_frame)
        
        # Zone principale des programmes
        self.create_programs_area(main_frame)
        
        # Barre de statut et boutons d'action
        self.create_action_bar(main_frame)
    
    def create_header(self, parent):
        """Crée l'en-tête avec titre très visible"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        # Titre principal
        title_label = ttk.Label(
            header_frame,
            text="🎯 NITRITE v.2 - INSTALLATION AUTOMATIQUE",
            style='Title.TLabel'
        )
        title_label.pack()
        
        # Sous-titre
        subtitle_label = ttk.Label(
            header_frame,
            text="Sélectionnez vos programmes • Installation silencieuse • Aucune publicité",
            font=('Segoe UI', 12),
            foreground='#7f8c8d'
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_toolbar(self, parent):
        """Crée la barre d'outils avec sélection rapide"""
        toolbar_frame = ttk.LabelFrame(parent, text="⚡ SÉLECTION RAPIDE", padding=10)
        toolbar_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Boutons de sélection globale
        button_frame = ttk.Frame(toolbar_frame)
        button_frame.pack()
        
        ttk.Button(
            button_frame,
            text="✅ TOUT SÉLECTIONNER",
            command=self.select_all_programs,
            style='Select.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="❌ TOUT DÉSÉLECTIONNER",
            command=self.deselect_all_programs,
            style='Clear.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="⭐ ESSENTIELS",
            command=self.select_essentials,
            style='Select.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🎮 JEUX",
            command=lambda: self.select_category("Jeux"),
            style='Select.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="💻 DÉVELOPPEMENT",
            command=lambda: self.select_category("Développement"),
            style='Select.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🛡️ SÉCURITÉ",
            command=lambda: self.select_category("Sécurité"),
            style='Select.TButton'
        ).pack(side=tk.LEFT, padx=5)
    
    def create_programs_area(self, parent):
        """Crée la zone des programmes avec MAXIMUM de visibilité"""
        # Frame conteneur
        programs_frame = ttk.LabelFrame(parent, text="📋 PROGRAMMES DISPONIBLES", padding=5)
        programs_frame.grid(row=2, column=0, sticky="nsew")
        programs_frame.grid_rowconfigure(0, weight=1)
        programs_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas avec scrollbar pour afficher TOUS les programmes
        self.canvas = tk.Canvas(
            programs_frame, 
            bg='#ffffff',
            highlightthickness=0,
            relief='flat'
        )
        
        scrollbar = ttk.Scrollbar(programs_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configuration du scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Placement
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind scroll avec molette
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Créer les checkboxes pour tous les programmes
        self.create_all_program_checkboxes()
    
    def create_all_program_checkboxes(self):
        """Crée TOUTES les checkboxes avec maximum de visibilité"""
        row = 0
        
        for category, programs in self.programs.items():
            # Titre de catégorie TRÈS visible
            category_label = ttk.Label(
                self.scrollable_frame,
                text=f"📂 {category.upper()}",
                style='Category.TLabel'
            )
            category_label.grid(row=row, column=0, columnspan=4, sticky="w", pady=(15, 5))
            row += 1
            
            # Ligne de séparation
            separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
            separator.grid(row=row, column=0, columnspan=4, sticky="ew", pady=(0, 10))
            row += 1
            
            # Programmes en colonnes pour maximiser l'affichage
            col = 0
            for program_name, program_info in programs.items():
                # Variable pour checkbox
                var = tk.BooleanVar()
                self.program_vars[program_name] = var
                
                # Checkbox avec description visible
                checkbox = ttk.Checkbutton(
                    self.scrollable_frame,
                    text=f"{program_name}",
                    variable=var,
                    style='Program.TCheckbutton'
                )
                checkbox.grid(row=row, column=col, sticky="w", padx=10, pady=2)
                
                # Passer à la colonne suivante (3 colonnes max)
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
            
            # Si on n'a pas fini une ligne complète, passer à la suivante
            if col > 0:
                row += 1
    
    def create_action_bar(self, parent):
        """Crée la barre d'actions en bas"""
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        # Informations de sélection
        self.selection_label = ttk.Label(
            action_frame,
            text="0 programme(s) sélectionné(s)",
            font=('Segoe UI', 11, 'bold'),
            foreground='#2c3e50'
        )
        self.selection_label.pack(side=tk.LEFT, pady=5)
        
        # Bouton d'installation principal
        self.install_button = ttk.Button(
            action_frame,
            text="🚀 INSTALLER LES PROGRAMMES SÉLECTIONNÉS",
            command=self.start_installation,
            style='Action.TButton'
        )
        self.install_button.pack(side=tk.RIGHT, padx=(10, 0), pady=5)
        
        # Barre de progression
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(action_frame, textvariable=self.progress_var)
        self.progress_label.pack(side=tk.RIGHT, padx=10)
        
        # Mettre à jour le compteur
        self.update_selection_count()
    
    def load_programs(self):
        """Charge la liste des programmes depuis le config manager"""
        if self.config_manager:
            self.programs = self.config_manager.get_programs()
        else:
            # Configuration par défaut si pas de config manager
            self.programs = {
                "Navigateurs": {
                    "Google Chrome": {"url": "https://dl.google.com/chrome/install/chrome_installer.exe"},
                    "Mozilla Firefox": {"url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=fr"},
                    "Microsoft Edge": {"url": "https://go.microsoft.com/fwlink/?linkid=2108834"}
                },
                "Utilitaires": {
                    "7-Zip": {"url": "https://www.7-zip.org/a/7z2301-x64.exe"},
                    "WinRAR": {"url": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-611fr.exe"},
                    "Notepad++": {"url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.7/npp.8.5.7.Installer.x64.exe"}
                }
            }
    
    def _on_mousewheel(self, event):
        """Gestion du scroll avec la molette"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def select_all_programs(self):
        """Sélectionne tous les programmes"""
        for var in self.program_vars.values():
            var.set(True)
        self.update_selection_count()
    
    def deselect_all_programs(self):
        """Désélectionne tous les programmes"""
        for var in self.program_vars.values():
            var.set(False)
        self.update_selection_count()
    
    def select_essentials(self):
        """Sélectionne les programmes essentiels"""
        essentials = [
            "Google Chrome", "Mozilla Firefox", "7-Zip", "VLC Media Player",
            "Adobe Acrobat Reader", "Notepad++", "WinRAR"
        ]
        
        self.deselect_all_programs()
        for program_name, var in self.program_vars.items():
            if program_name in essentials:
                var.set(True)
        self.update_selection_count()
    
    def select_category(self, category):
        """Sélectionne tous les programmes d'une catégorie"""
        if category in self.programs:
            for program_name in self.programs[category]:
                if program_name in self.program_vars:
                    self.program_vars[program_name].set(True)
        self.update_selection_count()
    
    def update_selection_count(self):
        """Met à jour le compteur de sélection"""
        selected_count = sum(1 for var in self.program_vars.values() if var.get())
        total_count = len(self.program_vars)
        
        self.selection_label.config(
            text=f"{selected_count} programme(s) sélectionné(s) sur {total_count}"
        )
        
        # Changer la couleur du bouton selon la sélection
        if selected_count > 0:
            self.install_button.config(state='normal')
        else:
            self.install_button.config(state='disabled')
    
    def start_installation(self):
        """Démarre l'installation des programmes sélectionnés"""
        selected_programs = [
            name for name, var in self.program_vars.items() if var.get()
        ]
        
        if not selected_programs:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner au moins un programme.")
            return
        
        # Confirmation
        if messagebox.askyesno(
            "Confirmation d'installation",
            f"Installer {len(selected_programs)} programme(s) sélectionné(s) ?\n\n"
            "L'installation sera automatique et silencieuse."
        ):
            # Lancer l'installation en arrière-plan
            self.is_installing = True
            self.install_button.config(state='disabled', text="⏳ INSTALLATION EN COURS...")
            
            # Thread pour l'installation
            install_thread = threading.Thread(
                target=self._install_programs,
                args=(selected_programs,)
            )
            install_thread.start()
    
    def _install_programs(self, selected_programs):
        """Installation des programmes (thread séparé)"""
        try:
            if self.installer_manager:
                self.installer_manager.install_programs(selected_programs)
            
            # Mise à jour interface à la fin
            self.root.after(0, self._installation_complete)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'installation : {e}")
            self.root.after(0, lambda: self._installation_error(str(e)))
    
    def _installation_complete(self):
        """Appelée quand l'installation est terminée"""
        self.is_installing = False
        self.install_button.config(
            state='normal',
            text="🚀 INSTALLER LES PROGRAMMES SÉLECTIONNÉS"
        )
        self.progress_var.set("✅ Installation terminée !")
        
        messagebox.showinfo(
            "Installation terminée",
            "Tous les programmes sélectionnés ont été installés avec succès !"
        )
    
    def _installation_error(self, error_msg):
        """Appelée en cas d'erreur d'installation"""
        self.is_installing = False
        self.install_button.config(
            state='normal',
            text="🚀 INSTALLER LES PROGRAMMES SÉLECTIONNÉS"
        )
        self.progress_var.set("❌ Erreur d'installation")
        
        messagebox.showerror(
            "Erreur d'installation",
            f"Une erreur est survenue :\n{error_msg}"
        )

# Fonction pour remplacer l'ancien GUI Manager
def create_gui_manager(root, installer_manager=None, config_manager=None):
    """Crée et retourne le nouveau GUI Manager avec maximum de visibilité"""
    return NiTriteGUIMaxVisibility(root, installer_manager, config_manager)