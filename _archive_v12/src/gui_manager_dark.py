"""
NiTrite v.2 - Interface Graphique avec MODE SOMBRE
Interface moderne et élégante affichant TOUS les programmes
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from pathlib import Path
from datetime import datetime
import logging

class NiTriteDarkMode:
    """Interface graphique avec mode sombre élégant"""
    
    # Couleurs du thème sombre
    DARK_BG = '#1e1e1e'          # Fond principal
    DARK_BG2 = '#252526'         # Fond secondaire
    DARK_BG3 = '#2d2d30'         # Fond tertiaire
    DARK_FG = '#d4d4d4'          # Texte principal
    DARK_FG2 = '#969696'         # Texte secondaire
    ACCENT_BLUE = '#007acc'      # Accent bleu
    ACCENT_GREEN = '#4ec9b0'     # Accent vert
    ACCENT_ORANGE = '#ce9178'    # Accent orange
    ACCENT_RED = '#f48771'       # Accent rouge
    ACCENT_PURPLE = '#c586c0'    # Accent violet
    BORDER = '#3e3e42'           # Bordures
    
    def __init__(self, root, installer_manager=None, config_manager=None):
        self.root = root
        self.installer_manager = installer_manager
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Variables
        self.program_vars = {}
        self.programs = {}
        self.category_widgets = {}
        self.collapsed_categories = set()
        self.is_installing = False
        self.dark_mode = True  # Mode sombre activé par défaut
        
        # Charger les programmes
        self.load_all_programs()
        
        # Interface
        self.setup_window()
        self.apply_dark_theme()
        self.create_main_interface()
    
    def setup_window(self):
        """Configure la fenêtre principale"""
        total_programs = sum(len(progs) if isinstance(progs, dict) else 0 
                           for progs in self.programs.values())
        
        self.root.title(f"🚀 NiTrite v.2 - MODE SOMBRE - {total_programs}+ Applications")
        
        # Maximiser
        self.root.state('zoomed')
        
        # Configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Fond sombre
        self.root.configure(bg=self.DARK_BG)
    
    def apply_dark_theme(self):
        """Applique le thème sombre à ttk"""
        style = ttk.Style()
        
        # Configurer le thème
        style.theme_use('clam')
        
        # Styles pour le mode sombre
        style.configure('.',
                       background=self.DARK_BG,
                       foreground=self.DARK_FG,
                       fieldbackground=self.DARK_BG2,
                       bordercolor=self.BORDER,
                       darkcolor=self.DARK_BG,
                       lightcolor=self.DARK_BG3)
        
        # Labels
        style.configure('TLabel',
                       background=self.DARK_BG,
                       foreground=self.DARK_FG)
        
        # Frames
        style.configure('TFrame',
                       background=self.DARK_BG)
        
        # LabelFrames
        style.configure('TLabelframe',
                       background=self.DARK_BG,
                       foreground=self.ACCENT_BLUE,
                       bordercolor=self.BORDER)
        style.configure('TLabelframe.Label',
                       background=self.DARK_BG,
                       foreground=self.ACCENT_BLUE,
                       font=('Segoe UI', 10, 'bold'))
        
        # Boutons
        style.configure('TButton',
                       background=self.DARK_BG2,
                       foreground=self.DARK_FG,
                       bordercolor=self.BORDER,
                       focuscolor=self.ACCENT_BLUE,
                       font=('Segoe UI', 9))
        style.map('TButton',
                 background=[('active', self.DARK_BG3), ('pressed', self.ACCENT_BLUE)],
                 foreground=[('active', self.DARK_FG)])
        
        # Checkbuttons
        style.configure('TCheckbutton',
                       background=self.DARK_BG,
                       foreground=self.DARK_FG,
                       font=('Segoe UI', 9))
        style.map('TCheckbutton',
                 background=[('active', self.DARK_BG)],
                 foreground=[('active', self.ACCENT_GREEN)])
        
        # Progressbar
        style.configure('TProgressbar',
                       background=self.ACCENT_BLUE,
                       troughcolor=self.DARK_BG2,
                       bordercolor=self.BORDER,
                       lightcolor=self.ACCENT_BLUE,
                       darkcolor=self.ACCENT_BLUE)
        
        # Scrollbar
        style.configure('TScrollbar',
                       background=self.DARK_BG2,
                       troughcolor=self.DARK_BG,
                       bordercolor=self.BORDER,
                       arrowcolor=self.DARK_FG)
        
        # Separator
        style.configure('TSeparator',
                       background=self.BORDER)
        
        # Styles personnalisés
        style.configure('Title.TLabel',
                       font=('Segoe UI', 20, 'bold'),
                       foreground=self.ACCENT_BLUE,
                       background=self.DARK_BG)
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 11),
                       foreground=self.DARK_FG2,
                       background=self.DARK_BG)
        
        style.configure('Category.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.ACCENT_ORANGE,
                       background=self.DARK_BG2)
        
        style.configure('Install.TButton',
                       font=('Segoe UI', 12, 'bold'),
                       background=self.ACCENT_GREEN,
                       foreground='white')
        style.map('Install.TButton',
                 background=[('active', self.ACCENT_BLUE)])
    
    def load_all_programs(self):
        """Charge TOUS les programmes depuis programs.json"""
        try:
            # Essayer d'abord programs_massive.json, puis programs.json
            for filename in ['programs_massive.json', 'programs.json', 'programs_extended.json']:
                programs_file = Path(__file__).parent.parent / 'data' / filename
                
                if programs_file.exists():
                    with open(programs_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convertir le format extended vers le format par catégorie si nécessaire
                    if filename == 'programs_extended.json':
                        self.programs = self._convert_extended_format(data)
                    else:
                        self.programs = data
                    
                    total = sum(len(progs) if isinstance(progs, dict) else 0 
                              for progs in self.programs.values())
                    
                    self.logger.info(f"✅ {total} programmes chargés depuis {filename}")
                    return
                    
            self.logger.warning("⚠️ Aucun fichier de programmes trouvé")
            self.programs = {}
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du chargement: {e}")
            self.programs = {}
    
    def _convert_extended_format(self, extended_data):
        """Convertit le format extended vers le format par catégorie"""
        categorized = {}
        
        for prog_id, prog_info in extended_data.items():
            category = prog_info.get('category', 'Divers')
            
            if category not in categorized:
                categorized[category] = {}
            
            name = prog_info.get('name', prog_id)
            categorized[category][name] = prog_info
        
        return categorized
    
    def create_main_interface(self):
        """Crée l'interface principale"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # En-tête
        self.create_header(main_frame)
        
        # Barre d'outils
        self.create_toolbar(main_frame)
        
        # Zone des programmes
        self.create_programs_area(main_frame)
        
        # Barre d'actions
        self.create_action_bar(main_frame)
    
    def create_header(self, parent):
        """Crée l'en-tête avec logo et titre"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Calcul du total
        total_programs = sum(len(progs) if isinstance(progs, dict) else 0 
                           for progs in self.programs.values())
        
        # Titre avec gradient simulé
        title_label = ttk.Label(
            header_frame,
            text=f"🌙 NITRITE v.2 - MODE SOMBRE - {total_programs}+ APPLICATIONS",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0)
        
        # Sous-titre
        subtitle_label = ttk.Label(
            header_frame,
            text="Installation automatique • Sources officielles • Mode sombre élégant",
            style='Subtitle.TLabel'
        )
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
        # Bouton pour basculer le mode
        toggle_frame = ttk.Frame(header_frame)
        toggle_frame.grid(row=0, column=1, rowspan=2, padx=10)
        
        self.mode_button = ttk.Button(
            toggle_frame,
            text="☀️ Mode Clair",
            command=self.toggle_theme,
            width=15
        )
        self.mode_button.pack()
    
    def create_toolbar(self, parent):
        """Crée la barre d'outils avec sélection rapide"""
        toolbar_frame = ttk.LabelFrame(parent, text="⚡ SÉLECTION RAPIDE", padding=10)
        toolbar_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        button_frame = ttk.Frame(toolbar_frame)
        button_frame.pack()
        
        # Boutons de sélection globale
        ttk.Button(
            button_frame,
            text="✅ TOUT SÉLECTIONNER",
            command=self.select_all_programs,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="❌ TOUT DÉSÉLECTIONNER",
            command=self.deselect_all_programs,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(button_frame, orient='vertical').pack(side=tk.LEFT, fill='y', padx=10, pady=5)
        
        # Boutons par catégorie (icônes colorées)
        categories_colors = {
            "Navigateurs": ("🌐", self.ACCENT_BLUE),
            "Développement": ("💻", self.ACCENT_GREEN),
            "Jeux": ("🎮", self.ACCENT_PURPLE),
            "Sécurité": ("🛡️", self.ACCENT_ORANGE),
            "Utilitaires": ("🔧", self.DARK_FG),
            "Communication": ("💬", self.ACCENT_BLUE),
            "Multimédia": ("🎨", self.ACCENT_PURPLE),
            "Bureautique": ("📝", self.DARK_FG),
        }
        
        for category in list(self.programs.keys())[:8]:  # Limiter à 8 boutons
            if category in self.programs:
                count = len(self.programs[category])
                icon, color = categories_colors.get(category, ("📦", self.DARK_FG))
                
                btn = ttk.Button(
                    button_frame,
                    text=f"{icon} {category} ({count})",
                    command=lambda c=category: self.select_category(c),
                    width=22
                )
                btn.pack(side=tk.LEFT, padx=3)
    
    def create_programs_area(self, parent):
        """Crée la zone scrollable des programmes"""
        programs_frame = ttk.LabelFrame(parent, text="📋 PROGRAMMES DISPONIBLES", padding=5)
        programs_frame.grid(row=2, column=0, sticky="nsew")
        programs_frame.grid_rowconfigure(0, weight=1)
        programs_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas avec scrollbar
        self.main_canvas = tk.Canvas(
            programs_frame,
            bg=self.DARK_BG,
            highlightthickness=0,
            highlightbackground=self.BORDER
        )
        
        scrollbar = ttk.Scrollbar(programs_frame, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=1800)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.main_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind scroll
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Créer les checkboxes
        self.create_all_program_checkboxes()
    
    def create_all_program_checkboxes(self):
        """Crée toutes les checkboxes par catégorie"""
        row = 0
        
        category_icons = {
            'Navigateurs': '🌐',
            'Développement': '💻',
            'Bureautique': '📝',
            'Multimédia': '🎨',
            'Utilitaires': '🔧',
            'Communication': '💬',
            'Jeux': '🎮',
            'Sécurité': '🛡️',
            'Internet': '🌍'
        }
        
        for category, programs in sorted(self.programs.items()):
            if not isinstance(programs, dict) or len(programs) == 0:
                continue
            
            icon = category_icons.get(category, '📦')
            
            # En-tête de catégorie
            category_header = tk.Frame(self.scrollable_frame, bg=self.DARK_BG2, bd=1, relief='solid')
            category_header.grid(row=row, column=0, sticky="ew", pady=(15, 5), padx=5)
            category_header.grid_columnconfigure(1, weight=1)
            
            # Bouton plier/déplier
            collapse_btn = tk.Button(
                category_header,
                text="▼",
                width=3,
                bg=self.DARK_BG3,
                fg=self.DARK_FG,
                activebackground=self.ACCENT_BLUE,
                activeforeground='white',
                relief='flat',
                command=lambda cat=category: self.toggle_category(cat)
            )
            collapse_btn.grid(row=0, column=0, padx=5, pady=5)
            
            # Label de catégorie
            category_label = tk.Label(
                category_header,
                text=f"{icon} {category.upper()} - {len(programs)} programmes",
                bg=self.DARK_BG2,
                fg=self.ACCENT_ORANGE,
                font=('Segoe UI', 12, 'bold')
            )
            category_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
            
            # Bouton sélectionner tout
            select_btn = tk.Button(
                category_header,
                text="✓ Tout",
                width=10,
                bg=self.DARK_BG3,
                fg=self.ACCENT_GREEN,
                activebackground=self.ACCENT_GREEN,
                activeforeground='white',
                relief='flat',
                command=lambda c=category: self.select_category(c)
            )
            select_btn.grid(row=0, column=2, padx=5, pady=5)
            
            row += 1
            
            # Ligne de séparation
            sep = tk.Frame(self.scrollable_frame, height=1, bg=self.BORDER)
            sep.grid(row=row, column=0, sticky="ew", pady=(0, 5))
            row += 1
            
            # Container pour les programmes
            programs_container = tk.Frame(self.scrollable_frame, bg=self.DARK_BG)
            programs_container.grid(row=row, column=0, sticky="ew", padx=20, pady=5)
            
            for i in range(5):  # 5 colonnes
                programs_container.grid_columnconfigure(i, weight=1, minsize=300)
            
            # Stocker les widgets
            self.category_widgets[category] = {
                'collapse_btn': collapse_btn,
                'programs_container': programs_container
            }
            
            # Programmes en 5 colonnes
            prog_row = 0
            col = 0
            
            for program_name, program_info in sorted(programs.items()):
                var = tk.BooleanVar()
                self.program_vars[program_name] = var
                
                # Frame pour ce programme
                prog_frame = tk.Frame(programs_container, bg=self.DARK_BG)
                prog_frame.grid(row=prog_row, column=col, sticky="w", padx=5, pady=4)
                
                # Checkbox
                checkbox = tk.Checkbutton(
                    prog_frame,
                    text=program_name,
                    variable=var,
                    bg=self.DARK_BG,
                    fg=self.DARK_FG,
                    activebackground=self.DARK_BG,
                    activeforeground=self.ACCENT_GREEN,
                    selectcolor=self.DARK_BG2,
                    font=('Segoe UI', 9),
                    relief='flat'
                )
                checkbox.pack(anchor='w')
                
                var.trace_add('write', lambda *args: self.safe_update_selection_count())
                
                # Description
                desc = program_info.get('description', '')
                if desc:
                    desc_short = desc[:45] + "..." if len(desc) > 45 else desc
                    desc_label = tk.Label(
                        prog_frame,
                        text=desc_short,
                        bg=self.DARK_BG,
                        fg=self.DARK_FG2,
                        font=('Segoe UI', 8)
                    )
                    desc_label.pack(anchor='w', padx=(20, 0))
                
                col += 1
                if col >= 5:
                    col = 0
                    prog_row += 1
            
            row += 1
    
    def create_action_bar(self, parent):
        """Crée la barre d'actions en bas"""
        action_frame = tk.Frame(parent, bg=self.DARK_BG2, bd=2, relief='ridge')
        action_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        action_frame.grid_columnconfigure(1, weight=1)
        
        # Label de sélection
        self.selection_label = tk.Label(
            action_frame,
            text="0 programme(s) sélectionné(s)",
            bg=self.DARK_BG2,
            fg=self.ACCENT_GREEN,
            font=('Segoe UI', 12, 'bold')
        )
        self.selection_label.grid(row=0, column=0, sticky="w", padx=15, pady=10)
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            action_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            style='TProgressbar'
        )
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=20, pady=10)
        
        # Bouton d'installation
        self.install_button = tk.Button(
            action_frame,
            text="🚀 INSTALLER LES PROGRAMMES SÉLECTIONNÉS",
            command=self.start_installation,
            bg=self.ACCENT_GREEN,
            fg='white',
            activebackground=self.ACCENT_BLUE,
            activeforeground='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.install_button.grid(row=0, column=2, sticky="e", padx=15, pady=10)
    
    def _on_mousewheel(self, event):
        """Gestion du scroll"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def safe_update_selection_count(self):
        """Mise à jour sécurisée du compteur"""
        if hasattr(self, 'selection_label'):
            self.update_selection_count()
    
    def update_selection_count(self):
        """Met à jour le compteur de sélection"""
        selected_count = sum(1 for var in self.program_vars.values() if var.get())
        total_count = len(self.program_vars)
        
        self.selection_label.config(
            text=f"✨ {selected_count} programme(s) sélectionné(s) sur {total_count}"
        )
        
        if selected_count > 0:
            self.install_button.config(state='normal')
        else:
            self.install_button.config(state='disabled')
    
    def select_all_programs(self):
        """Sélectionne tous les programmes"""
        for var in self.program_vars.values():
            var.set(True)
    
    def deselect_all_programs(self):
        """Désélectionne tous les programmes"""
        for var in self.program_vars.values():
            var.set(False)
    
    def select_category(self, category):
        """Sélectionne tous les programmes d'une catégorie"""
        if category in self.programs:
            for program_name in self.programs[category]:
                if program_name in self.program_vars:
                    self.program_vars[program_name].set(True)
    
    def toggle_category(self, category):
        """Plie/déplie une catégorie"""
        if category in self.category_widgets:
            widgets = self.category_widgets[category]
            
            if category in self.collapsed_categories:
                widgets['programs_container'].grid()
                widgets['collapse_btn'].config(text="▼")
                self.collapsed_categories.remove(category)
            else:
                widgets['programs_container'].grid_remove()
                widgets['collapse_btn'].config(text="▶")
                self.collapsed_categories.add(category)
            
            self.scrollable_frame.update_idletasks()
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def toggle_theme(self):
        """Bascule entre mode sombre et clair"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            self.mode_button.config(text="☀️ Mode Clair")
            # Appliquer le thème sombre
            self.apply_dark_theme()
        else:
            self.mode_button.config(text="🌙 Mode Sombre")
            # Appliquer le thème clair (TODO)
            messagebox.showinfo("Info", "Le mode clair sera disponible dans une prochaine version!")
    
    def start_installation(self):
        """Démarre l'installation"""
        selected_programs = [
            name for name, var in self.program_vars.items() if var.get()
        ]
        
        if not selected_programs:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner au moins un programme.")
            return
        
        if messagebox.askyesno(
            "Confirmation d'installation",
            f"🚀 Installer {len(selected_programs)} programme(s) ?\n\n"
            "L'installation sera automatique et silencieuse.\n\n"
            f"Premiers programmes:\n" + "\n".join(f"• {p}" for p in selected_programs[:15]) +
            (f"\n... et {len(selected_programs) - 15} autres" if len(selected_programs) > 15 else "")
        ):
            self.logger.info(f"Installation lancée pour {len(selected_programs)} programmes")
            
            # Désactiver le bouton d'installation
            self.is_installing = True
            self.install_button.config(state='disabled', text="⏳ Installation en cours...")
            
            # Lancer l'installation dans un thread séparé
            if self.installer_manager:
                install_thread = threading.Thread(
                    target=self.installer_manager.install_programs,
                    args=(
                        selected_programs,
                        self.update_progress,
                        self.log_installation_message,
                        self.on_installation_finished
                    ),
                    daemon=True
                )
                install_thread.start()
            else:
                messagebox.showerror(
                    "Erreur",
                    "Le gestionnaire d'installation n'est pas disponible!"
                )
                self.is_installing = False
                self.install_button.config(state='normal', text="🚀 INSTALLER LES PROGRAMMES SÉLECTIONNÉS")
    
    def update_progress(self, value, message=""):
        """Met à jour la barre de progression"""
        self.progress_var.set(value)
        if message:
            self.selection_label.config(text=f"⏳ {message}")
        self.root.update_idletasks()
    
    def log_installation_message(self, message, level="info"):
        """Affiche un message de log"""
        colors = {
            "info": self.DARK_FG,
            "success": self.ACCENT_GREEN,
            "warning": self.ACCENT_ORANGE,
            "error": self.ACCENT_RED
        }
        color = colors.get(level, self.DARK_FG)
        
        print(f"[{level.upper()}] {message}")
        self.logger.info(message)
    
    def on_installation_finished(self, success):
        """Appelé quand l'installation est terminée"""
        self.is_installing = False
        self.install_button.config(state='normal', text="🚀 INSTALLER LES PROGRAMMES SÉLECTIONNÉS")
        
        if success:
            messagebox.showinfo(
                "Installation terminée",
                "✅ L'installation de tous les programmes sélectionnés est terminée !\n\n"
                "Vérifiez vos applications installées."
            )
            # Désélectionner tous les programmes
            self.deselect_all_programs()
        else:
            messagebox.showwarning(
                "Installation interrompue",
                "⚠️ L'installation a été interrompue.\n\n"
                "Certains programmes peuvent avoir été installés."
            )
        
        self.update_progress(0, "")
        self.update_selection_count()


def create_gui_manager(root, installer_manager=None, config_manager=None):
    """Crée et retourne le GUI Manager en mode sombre"""
    return NiTriteDarkMode(root, installer_manager, config_manager)
