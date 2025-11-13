"""
Gestionnaire d'interface graphique pour NiTriTe V5.0
VERSION COMPLÈTE - Affiche TOUS les programmes disponibles (80+)
MODE SOMBRE Ordi Plus
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
from pathlib import Path
from datetime import datetime
import logging
import webbrowser
import subprocess
import win32com.client
import winshell
from PIL import Image, ImageTk

class NiTriteGUIComplet:
    """Interface graphique complète affichant TOUS les programmes"""
    
    # 🎨 PALETTE DE COULEURS MODERNE - Thème Sombre Premium
    # Fonds avec profondeur
    DARK_BG = '#0f0f0f'          # Fond principal - Noir profond
    DARK_BG2 = '#1a1a1a'         # Fond secondaire - Gris très foncé
    DARK_BG3 = '#252525'         # Fond tertiaire - Gris foncé élégant
    DARK_BG4 = '#2f2f2f'         # Fond quaternaire - Gris moyen

    # Textes avec hiérarchie
    DARK_FG = '#ffffff'          # Texte principal - Blanc pur
    DARK_FG2 = '#e0e0e0'         # Texte secondaire - Blanc cassé
    DARK_FG3 = '#b0b0b0'         # Texte tertiaire - Gris clair

    # Accents vibrants avec gradients
    ACCENT_ORANGE = '#FF6B00'    # Orange Ordi Plus - Principal
    ACCENT_ORANGE_LIGHT = '#FF8533'  # Orange clair - Hover
    ACCENT_ORANGE_DARK = '#CC5500'   # Orange foncé - Active

    ACCENT_BLUE = '#0066cc'      # Bleu moderne
    ACCENT_BLUE_LIGHT = '#3385db' # Bleu clair - Hover
    ACCENT_BLUE_DARK = '#004d99'  # Bleu foncé - Active

    ACCENT_GREEN = '#00e676'     # Vert néon - Succès
    ACCENT_GREEN_LIGHT = '#33eb8f' # Vert clair
    ACCENT_GREEN_DARK = '#00b359'  # Vert foncé

    ACCENT_APPLE_GREEN = '#7CFC00'  # Vert pomme - Titre

    ACCENT_RED = '#ff1744'       # Rouge vif - Erreur
    ACCENT_YELLOW = '#ffd600'    # Jaune or - Warning
    ACCENT_PURPLE = '#7c4dff'    # Violet - Premium
    ACCENT_CYAN = '#00e5ff'      # Cyan - Info

    # Barre de progression animée
    PROGRESS_BG = '#1a1a1a'      # Fond barre
    PROGRESS_FILL = '#00e676'    # Remplissage vert néon
    PROGRESS_GLOW = '#33eb8f'    # Lueur verte

    # Bordures et ombres
    BORDER = '#404040'           # Bordure principale
    BORDER_LIGHT = '#505050'     # Bordure claire
    SHADOW = '#000000'           # Ombre portée
    HIGHLIGHT = '#ffffff'        # Surbrillance
    
    def __init__(self, root, installer_manager=None, config_manager=None):
        self.root = root
        self.installer_manager = installer_manager
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Variables pour les programmes
        self.program_vars = {}
        self.programs = {}
        self.category_frames = {}
        self.category_widgets = {}
        self.collapsed_categories = set()
        self.is_installing = False
        self.installation_start_time = None  # Pour calculer le temps restant

        # Tracking des installations pour rapport détaillé
        self.successful_installs = []
        self.failed_installs = []

        # Variables pour le drag & drop des sections/catégories
        self.section_titles = []  # Liste des frames de titres de sections
        self.section_frames = {}  # Dict des frames de sections {title: frame}
        self.dragging_category = None
        self.drag_start_y = 0

        # Variables pour le drag & drop des boutons
        self.all_buttons = []  # Liste de tous les boutons
        self.dragging_button = None
        self.drag_button_section = None

        # Compteur de boutons du panneau d'outils
        self.tools_buttons_count = 0
        
        # Charger le logo Ordi Plus pour l'arrière-plan
        self.load_background_logo()
        
        # Charger TOUS les programmes
        self.load_all_programs()
        
        # Interface
        self.setup_window()
        self.setup_styles()
        self.create_main_interface()
        
        # Protocole de fermeture propre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_background_logo(self):
        """Charge le logo Ordi Plus pour l'arrière-plan avec transparence"""
        try:
            import sys
            # Chemins compatibles PyInstaller
            if getattr(sys, 'frozen', False):
                # Mode exécutable
                base_path = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(sys.executable).parent
            else:
                # Mode développement
                base_path = Path(__file__).parent.parent

            logo_path = base_path / 'assets' / 'logo_ordiplus_bg.png'
            if logo_path.exists():
                # Charger le logo
                img = Image.open(logo_path)

                # Redimensionner à 400x400 pixels
                img = img.resize((400, 400), Image.Resampling.LANCZOS)

                # Appliquer 15% d'opacité (85% de transparence)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Réduire l'opacité à 15%
                alpha = img.split()[3]
                alpha = alpha.point(lambda p: int(p * 0.15))
                img.putalpha(alpha)

                self.bg_logo = ImageTk.PhotoImage(img)
            else:
                self.bg_logo = None
                self.logger.warning(f"Logo Ordi Plus non trouvé : {logo_path}")
        except Exception as e:
            self.bg_logo = None
            self.logger.error(f"Erreur chargement logo : {e}")
    
    def setup_window(self):
        """Configure la fenêtre principale en plein écran"""
        self.root.title("🚀 NiTriTe v12 Final - Installateur Automatique de Programmes (80+ applications)")
        
        # MAXIMISER complètement la fenêtre
        self.root.state('zoomed')
        
        # Configuration responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Couleur de fond SOMBRE
        self.root.configure(bg=self.DARK_BG)
        
        # Icône (si disponible)
        try:
            import sys
            # Chemins compatibles PyInstaller
            if getattr(sys, 'frozen', False):
                base_path = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(sys.executable).parent
            else:
                base_path = Path(__file__).parent.parent
            
            icon_path = base_path / 'assets' / 'icon.ico'
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception as e:
            self.logger.warning(f"Impossible de charger l'icône: {e}")
    
    def setup_styles(self):
        """🎨 Configure les styles ULTRA-MODERNES pour mode sombre premium"""
        style = ttk.Style()
        style.theme_use('clam')

        # ═══════════════════════════════════════════════════════════
        # 🌟 CONFIGURATION GLOBALE MODE SOMBRE PREMIUM
        # ═══════════════════════════════════════════════════════════
        style.configure('.',
                       background=self.DARK_BG,
                       foreground=self.DARK_FG,
                       fieldbackground=self.DARK_BG2,
                       bordercolor=self.BORDER_LIGHT,
                       darkcolor=self.DARK_BG2,
                       lightcolor=self.DARK_BG3,
                       relief='flat')

        # ═══════════════════════════════════════════════════════════
        # 📝 LABELS MODERNISÉS
        # ═══════════════════════════════════════════════════════════
        style.configure('TLabel',
                       background=self.DARK_BG,
                       foreground=self.DARK_FG,
                       font=('Segoe UI', 9))

        # ═══════════════════════════════════════════════════════════
        # 📦 FRAMES ET CONTENEURS
        # ═══════════════════════════════════════════════════════════
        style.configure('TFrame',
                       background=self.DARK_BG,
                       borderwidth=0)

        # ═══════════════════════════════════════════════════════════
        # 🏷️ LABELFRAMES AVEC BORDURES ÉLÉGANTES
        # ═══════════════════════════════════════════════════════════
        style.configure('TLabelframe',
                       background=self.DARK_BG,
                       foreground=self.ACCENT_BLUE_LIGHT,
                       bordercolor=self.BORDER_LIGHT,
                       borderwidth=2,
                       relief='solid')
        style.configure('TLabelframe.Label',
                       background=self.DARK_BG,
                       foreground=self.ACCENT_BLUE_LIGHT,
                       font=('Segoe UI', 11, 'bold'))

        # ═══════════════════════════════════════════════════════════
        # 🔘 BOUTONS STANDARDS MODERNISÉS
        # ═══════════════════════════════════════════════════════════
        style.configure('TButton',
                       background=self.DARK_BG3,
                       foreground=self.DARK_FG,
                       bordercolor=self.BORDER_LIGHT,
                       borderwidth=1,
                       relief='raised',
                       font=('Segoe UI', 9, 'bold'),
                       padding=(10, 5))
        style.map('TButton',
                 background=[
                     ('active', self.DARK_BG4),
                     ('pressed', self.ACCENT_ORANGE),
                     ('disabled', self.DARK_BG2)
                 ],
                 foreground=[
                     ('active', self.DARK_FG),
                     ('pressed', '#ffffff'),
                     ('disabled', self.DARK_FG3)
                 ],
                 bordercolor=[
                     ('active', self.ACCENT_ORANGE_LIGHT),
                     ('pressed', self.ACCENT_ORANGE_DARK)
                 ])

        # ═══════════════════════════════════════════════════════════
        # ✅ CHECKBUTTONS PERSONNALISÉS
        # ═══════════════════════════════════════════════════════════
        style.configure('TCheckbutton',
                       background=self.DARK_BG,
                       foreground=self.DARK_FG2,
                       font=('Segoe UI', 9),
                       borderwidth=0,
                       indicatorcolor=self.ACCENT_GREEN,
                       indicatorrelief='flat')
        style.map('TCheckbutton',
                 background=[('active', self.DARK_BG)],
                 foreground=[
                     ('active', self.DARK_FG),
                     ('selected', self.ACCENT_GREEN_LIGHT)
                 ])

        # ═══════════════════════════════════════════════════════════
        # 🎯 TITRE PRINCIPAL - ULTRA MODERNE
        # ═══════════════════════════════════════════════════════════
        style.configure('Title.TLabel',
                       font=('Segoe UI', 20, 'bold'),
                       foreground=self.ACCENT_ORANGE,
                       background=self.DARK_BG,
                       padding=(0, 10))

        # ═══════════════════════════════════════════════════════════
        # 📂 CATÉGORIES - DESIGN MODERNE
        # ═══════════════════════════════════════════════════════════
        style.configure('Category.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.ACCENT_ORANGE_LIGHT,
                       background=self.DARK_BG3,
                       padding=(15, 8),
                       relief='flat')

        # ═══════════════════════════════════════════════════════════
        # 🚀 BOUTONS D'ACTION - EFFET 3D PREMIUM
        # ═══════════════════════════════════════════════════════════
        style.configure('Action.TButton',
                       font=('Segoe UI', 12, 'bold'),
                       padding=(20, 12),
                       background=self.ACCENT_ORANGE,
                       foreground='#ffffff',
                       borderwidth=2,
                       relief='raised',
                       bordercolor=self.ACCENT_ORANGE_DARK)
        style.map('Action.TButton',
                 background=[
                     ('active', self.ACCENT_ORANGE_LIGHT),
                     ('pressed', self.ACCENT_ORANGE_DARK),
                     ('disabled', self.DARK_BG3)
                 ],
                 foreground=[
                     ('active', '#ffffff'),
                     ('pressed', '#ffffff'),
                     ('disabled', self.DARK_FG3)
                 ],
                 relief=[
                     ('pressed', 'sunken')
                 ],
                 bordercolor=[
                     ('active', self.ACCENT_ORANGE_LIGHT),
                     ('pressed', self.ACCENT_ORANGE)
                 ])

        # ═══════════════════════════════════════════════════════════
        # 📊 BARRE DE PROGRESSION - DESIGN FUTURISTE
        # ═══════════════════════════════════════════════════════════
        style.configure('Green.Horizontal.TProgressbar',
                       background=self.PROGRESS_FILL,
                       troughcolor=self.PROGRESS_BG,
                       bordercolor=self.BORDER_LIGHT,
                       darkcolor=self.PROGRESS_FILL,
                       lightcolor=self.PROGRESS_GLOW,
                       thickness=35,
                       borderwidth=2,
                       relief='flat')

        # ═══════════════════════════════════════════════════════════
        # 🎯 BOUTON DE SÉLECTION CATÉGORIE
        # ═══════════════════════════════════════════════════════════
        style.configure('Select.TButton',
                       font=('Segoe UI', 9, 'bold'),
                       padding=(8, 4),
                       background=self.ACCENT_GREEN,
                       foreground='#ffffff',
                       borderwidth=1,
                       relief='raised')
        style.map('Select.TButton',
                 background=[
                     ('active', self.ACCENT_GREEN_LIGHT),
                     ('pressed', self.ACCENT_GREEN_DARK)
                 ])

        # ═══════════════════════════════════════════════════════════
        # 🛠️ BOUTONS PANNEAU D'OUTILS - Taille optimisée
        # ═══════════════════════════════════════════════════════════
        style.configure('ToolPanel.TButton',
                       font=('Segoe UI', 9),
                       padding=(6, 3),
                       background=self.DARK_BG3,
                       foreground=self.DARK_FG,
                       borderwidth=1,
                       relief='raised')
        style.map('ToolPanel.TButton',
                 background=[
                     ('active', self.DARK_BG4),
                     ('pressed', self.ACCENT_BLUE)
                 ],
                 foreground=[
                     ('active', self.DARK_FG),
                     ('pressed', '#ffffff')
                 ])
    
    def load_all_programs(self):
        """Charge TOUS les programmes depuis programs.json"""
        try:
            import sys
            # Chemins compatibles PyInstaller
            if getattr(sys, 'frozen', False):
                base_path = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(sys.executable).parent
            else:
                base_path = Path(__file__).parent.parent
            
            programs_file = base_path / 'data' / 'programs.json'
            
            if programs_file.exists():
                with open(programs_file, 'r', encoding='utf-8') as f:
                    self.programs = json.load(f)
                
                # Compter le total
                total = sum(len(progs) if isinstance(progs, dict) else 0 
                          for progs in self.programs.values())
                
                self.logger.info(f"✅ {total} programmes chargés depuis {len(self.programs)} catégories")
                
            else:
                self.logger.warning("⚠️ Fichier programs.json non trouvé")
                self.programs = {}
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du chargement des programmes: {e}")
            self.programs = {}
    
    def create_main_interface(self):
        """Crée l'interface principale avec PanedWindow redimensionnable et logo en arrière-plan"""
        # Frame principal MODE SOMBRE
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Logo en arrière-plan (si disponible) - placé en premier pour être derrière
        if self.bg_logo:
            bg_label = tk.Label(main_frame, image=self.bg_logo, bg=self.DARK_BG)
            bg_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # En-tête
        self.create_header(main_frame)
        
        # Barre d'actions (AVANT pour initialiser selection_label)
        self.create_action_bar(main_frame)
        
        # PanedWindow pour séparer programmes et outils avec diviseur draggable
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=2, column=0, sticky="nsew")
        
        # Frame gauche pour les programmes
        programs_container = ttk.Frame(self.paned_window)
        self.paned_window.add(programs_container, weight=4)

        # Frame droit pour les outils (ratio 4:3 pour élargir le panneau d'outils)
        tools_container = ttk.Frame(self.paned_window)
        self.paned_window.add(tools_container, weight=3)
        
        # Zone principale des programmes (dans le container gauche)
        self.create_programs_area_in_container(programs_container)
        
        # Panel d'outils à droite (dans le container droit)
        self.create_tools_panel_in_container(tools_container)
    
    def create_header(self, parent):
        """🎨 Crée l'en-tête ULTRA-MODERNE avec design premium"""
        # Frame principal avec fond dégradé simulé
        header_outer = tk.Frame(
            parent,
            bg=self.DARK_BG2,
            relief='raised',
            bd=3,
            highlightthickness=2,
            highlightbackground=self.ACCENT_ORANGE
        )
        header_outer.grid(row=0, column=0, sticky="ew", pady=(5, 10), padx=10)

        # Calcul du nombre total de programmes
        total_programs = sum(len(progs) if isinstance(progs, dict) else 0
                           for progs in self.programs.values())

        # 🎯 Titre principal - V12.0 avec lettres colorées
        title_frame = tk.Frame(header_outer, bg=self.DARK_BG2, pady=12)
        title_frame.pack()

        # Créer le titre avec N, T, T, e, V en vert pomme
        title_parts = [
            ('N', self.ACCENT_APPLE_GREEN),
            ('i', self.ACCENT_ORANGE),
            ('T', self.ACCENT_APPLE_GREEN),
            ('ri', self.ACCENT_ORANGE),
            ('T', self.ACCENT_APPLE_GREEN),
            ('e', self.ACCENT_APPLE_GREEN),
            (' ', self.ACCENT_ORANGE),
            ('V', self.ACCENT_APPLE_GREEN),
            ('12.0', self.ACCENT_ORANGE)
        ]

        for text, color in title_parts:
            label = tk.Label(
                title_frame,
                text=text,
                font=('Segoe UI', 28, 'bold'),
                fg=color,
                bg=self.DARK_BG2
            )
            label.pack(side='left')

        # Badge compteur avec applications + boutons
        # Note: Le compteur de boutons sera initialisé après la création du panneau
        self.count_badge = tk.Label(
            header_outer,
            text=f"⭐ {total_programs} Applications",
            font=('Segoe UI', 14, 'bold'),
            fg='#ffffff',
            bg=self.ACCENT_BLUE,
            padx=20,
            pady=8,
            relief='raised',
            bd=2
        )
        self.count_badge.pack(pady=(5, 10))

        # 💫 Sous-titre élégant
        subtitle_label = tk.Label(
            header_outer,
            text="✨ Installation Silencieuse • Sources Officielles • Design Premium ✨",
            font=('Segoe UI', 11, 'italic'),
            fg=self.ACCENT_CYAN,
            bg=self.DARK_BG2,
            pady=10
        )
        subtitle_label.pack()
    
    def create_programs_area_in_container(self, parent):
        """Crée la zone des programmes avec TOUS les programmes affichés"""
        programs_frame = ttk.LabelFrame(parent, text="📋 PROGRAMMES", padding=3)
        programs_frame.pack(fill="both", expand=True)
        programs_frame.grid_rowconfigure(0, weight=1)
        programs_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas principal avec scrollbar MODE SOMBRE
        self.main_canvas = tk.Canvas(
            programs_frame,
            bg=self.DARK_BG,
            highlightthickness=0
        )

        # Ajouter le logo OrdiPlus en filigrane (centré, 400x400, 15% opacité)
        if self.bg_logo:
            # Le logo sera centré après le premier redimensionnement de la fenêtre
            self.watermark_id = self.main_canvas.create_image(
                0, 0,  # Position temporaire, sera centrée plus tard
                image=self.bg_logo,
                anchor="center"
            )
            # Centrer le logo lors du redimensionnement du canvas
            self.main_canvas.bind('<Configure>', self._center_watermark)

        main_scrollbar = ttk.Scrollbar(programs_frame, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        # Configuration du scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=1800)
        self.main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Placement
        self.main_canvas.grid(row=0, column=0, sticky="nsew")
        main_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind scroll avec molette
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Créer les checkboxes pour TOUS les programmes
        self.create_all_program_checkboxes()
        
        # Mettre à jour le compteur initial
        if hasattr(self, 'selection_label'):
            self.update_selection_count()
    
    def safe_update_selection_count(self):
        """Version sûre de update_selection_count"""
        if hasattr(self, 'selection_label'):
            self.update_selection_count()
    
    def create_all_program_checkboxes(self):
        """Crée les checkboxes pour TOUS les programmes par catégorie"""
        row = 0
        
        # Icônes pour les catégories
        category_icons = {
            'Navigateurs': '🌐',
            'Développement': '💻',
            'Bureautique': '📝',
            'Multimédia': '🎨',
            'Utilitaires': '🔧',
            'Communication': '💬',
            'Jeux': '🎮',
            'Sécurité': '🛡️',
            'Internet': '🌍',
            'Outils OrdiPlus': '🛠️',
            'Pack Office': '📦'
        }
        
        # Ordre d'affichage des catégories (OrdiPlus en premier)
        category_order = [
            'Outils OrdiPlus',
            'Pack Office',
            'Navigateurs',
            'Bureautique',
            'Multimédia',
            'Développement',
            'Utilitaires',
            'Sécurité',
            'Communication',
            'Jeux',
            'Internet'
        ]
        
        # Afficher dans l'ordre défini
        sorted_categories = []
        for cat in category_order:
            if cat in self.programs and isinstance(self.programs[cat], dict) and len(self.programs[cat]) > 0:
                sorted_categories.append((cat, self.programs[cat]))
        
        # Ajouter les catégories manquantes
        for category, programs in sorted(self.programs.items()):
            if category not in category_order and isinstance(programs, dict) and len(programs) > 0:
                sorted_categories.append((category, programs))
        
        for category, programs in sorted_categories:
            icon = category_icons.get(category, '📦')
            
            # 🎨 Header de catégorie ULTRA-MODERNE avec fond dégradé
            category_header = tk.Frame(
                self.scrollable_frame,
                bg=self.DARK_BG3,
                relief='raised',
                bd=2,
                highlightthickness=1,
                highlightbackground=self.ACCENT_ORANGE
            )
            category_header.grid(row=row, column=0, sticky="ew", pady=(10, 5), padx=5)
            category_header.grid_columnconfigure(1, weight=1)

            # 🔽 Bouton plier/déplier compact
            collapse_btn = tk.Button(
                category_header,
                text="▼",
                bg=self.ACCENT_ORANGE,
                fg='#ffffff',
                font=('Segoe UI', 8),
                relief='raised',
                bd=2,
                cursor='hand2',
                padx=6,
                pady=2,
                command=lambda cat=category: self.toggle_category(cat)
            )
            collapse_btn.grid(row=0, column=0, padx=8, pady=5)

            # 📂 Label de catégorie avec fond et style moderne
            category_label = tk.Label(
                category_header,
                text=f"  {icon}  {category.upper()}  •  {len(programs)} programmes",
                font=('Segoe UI', 13, 'bold'),
                fg=self.ACCENT_ORANGE_LIGHT,
                bg=self.DARK_BG3,
                anchor='w',
                padx=10
            )
            category_label.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

            # ✅ Bouton sélectionner tout - Compact
            select_cat_btn = tk.Button(
                category_header,
                text="✓ Tout sélectionner",
                font=('Segoe UI', 8),
                bg=self.ACCENT_GREEN,
                fg='#ffffff',
                relief='raised',
                bd=2,
                cursor='hand2',
                padx=8,
                pady=3,
                command=lambda c=category: self.select_category(c)
            )
            select_cat_btn.grid(row=0, column=2, padx=8, pady=5)
            
            row += 1

            # 🌈 Ligne de séparation moderne avec dégradé (simulé par Frame)
            separator_frame = tk.Frame(self.scrollable_frame, height=2, bg=self.ACCENT_ORANGE, relief='flat')
            separator_frame.grid(row=row, column=0, sticky="ew", pady=(2, 8), padx=20)
            row += 1
            
            # Frame pour les programmes de cette catégorie MODE SOMBRE
            programs_container = ttk.Frame(self.scrollable_frame)
            programs_container.grid(row=row, column=0, sticky="ew", padx=15)
            
            # 5 COLONNES pour gagner de la place
            for i in range(5):
                programs_container.grid_columnconfigure(i, weight=1)
            
            # Stocker les widgets pour le plier/déplier
            self.category_widgets[category] = {
                'collapse_btn': collapse_btn,
                'programs_container': programs_container
            }
            
            # Programmes en 5 colonnes pour maximiser l'affichage
            prog_row = 0
            col = 0
            
            checkbox_count = 0
            button_count = 0
            
            for program_name, program_info in sorted(programs.items()):
                # Frame pour ce programme (COMPACT)
                prog_frame = ttk.Frame(programs_container)
                prog_frame.grid(row=prog_row, column=col, sticky="w", padx=3, pady=2)
                
                # Vérifier si c'est un désinstallateur (catégorie spéciale)
                is_uninstaller = category == "Désinstallateurs Antivirus"

                # Tous les programmes ont maintenant une checkbox
                checkbox_count += 1
                var = tk.BooleanVar()
                self.program_vars[program_name] = var

                # Frame horizontal pour bouton web + checkbox
                checkbox_frame = ttk.Frame(prog_frame)
                checkbox_frame.pack(anchor='w', fill='x')

                # • Point pour lien web (plus grand pour visibilité)
                download_url = program_info.get('download_url', '')
                if download_url:
                    web_point = tk.Label(
                        checkbox_frame,
                        text="•",
                        font=('Arial', 16),
                        fg=self.ACCENT_BLUE,
                        bg=self.DARK_BG,
                        cursor='hand2'
                    )
                    web_point.pack(side='left', padx=(0, 6))
                    web_point.bind("<Button-1>", lambda e, url=download_url: self.open_download_link(url))

                # Checkbox avec nom du programme (à droite du bouton web)
                checkbox = ttk.Checkbutton(
                    checkbox_frame,
                    text=program_name,
                    variable=var,
                    style='Program.TCheckbutton'
                )
                checkbox.pack(side='left', anchor='w')

                # Configurer la police plus petite
                checkbox.configure(style='Program.TCheckbutton')

                # Lier manuellement le changement
                var.trace_add('write', lambda *args: self.safe_update_selection_count())

                # Pour les désinstallateurs, ajouter un bouton de téléchargement supplémentaire
                if is_uninstaller:
                    if download_url:
                        download_btn = ttk.Button(
                            prog_frame,
                            text="📥 Télécharger",
                            command=lambda url=download_url: self.open_download_link(url),
                            width=15
                        )
                        download_btn.pack(anchor='w', padx=(20, 0), pady=(2, 0))
                
                # Description (SI DISPONIBLE et COURTE)
                desc = program_info.get('description', '')
                if desc and len(desc) < 60:
                    desc_label = ttk.Label(
                        prog_frame,
                        text=desc[:40] + "..." if len(desc) > 40 else desc,
                        font=('Segoe UI', 7),
                        foreground='#7f8c8d'
                    )
                    desc_label.pack(anchor='w', padx=(20, 0))
                
                # Passer à la colonne suivante
                col += 1
                if col >= 5:  # 5 colonnes
                    col = 0
                    prog_row += 1
            
            # Logger le nombre de checkboxes créées pour cette catégorie
            if checkbox_count > 0 or button_count > 0:
                self.logger.info(f"📊 {category}: {checkbox_count} checkboxes, {button_count} boutons")
            
            row += 1
    
    def toggle_category(self, category):
        """Plie ou déplie une catégorie"""
        if category in self.category_widgets:
            widgets = self.category_widgets[category]
            
            if category in self.collapsed_categories:
                # Déplier
                widgets['programs_container'].grid()
                widgets['collapse_btn'].config(text="▼")
                self.collapsed_categories.remove(category)
            else:
                # Plier
                widgets['programs_container'].grid_remove()
                widgets['collapse_btn'].config(text="▶")
                self.collapsed_categories.add(category)
            
            # Mettre à jour la région de défilement
            self.scrollable_frame.update_idletasks()
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def create_action_bar(self, parent):
        """🎨 Crée la barre d'actions ULTRA-MODERNE"""
        # Frame principal avec fond moderne
        action_outer = tk.Frame(
            parent,
            bg=self.DARK_BG2,
            relief='raised',
            bd=2,
            highlightthickness=1,
            highlightbackground=self.BORDER_LIGHT
        )
        action_outer.grid(row=1, column=0, sticky="ew", pady=(8, 8), padx=10)

        action_frame = tk.Frame(action_outer, bg=self.DARK_BG2)
        action_frame.pack(fill="both", expand=True, padx=15, pady=12)

        # 📊 Label de sélection - MODERNE avec badge
        selection_container = tk.Frame(action_frame, bg=self.DARK_BG3, relief='raised', bd=2)
        selection_container.pack(side="left", padx=(0, 20))

        self.selection_label = tk.Label(
            selection_container,
            text="📋 0 programme(s) sélectionné(s)",
            font=('Segoe UI', 12, 'bold'),
            fg=self.ACCENT_CYAN,
            bg=self.DARK_BG3,
            padx=20,
            pady=8
        )
        self.selection_label.pack()

        # 📊 Frame pour la barre de progression
        progress_container = tk.Frame(action_frame, bg=self.DARK_BG2)
        progress_container.pack(side="left", fill="x", expand=True, padx=10)

        # Label pour le pourcentage - MODERNE
        self.progress_label = tk.Label(
            progress_container,
            text="",
            font=('Segoe UI', 10, 'bold'),
            fg=self.PROGRESS_FILL,
            bg=self.DARK_BG2,
            anchor='w'
        )
        self.progress_label.pack(fill="x", pady=(0, 5))

        # 🎯 Barre de progression ULTRA-MODERNE
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_container,
            variable=self.progress_var,
            maximum=100,
            length=300,
            style='Green.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill="x")

        # Container pour les boutons d'action
        buttons_frame = tk.Frame(action_frame, bg=self.DARK_BG2)
        buttons_frame.pack(side="right", padx=(10, 0))

        # 🔄 Bouton d'organisation
        self.organize_button = ttk.Button(
            buttons_frame,
            text="🔄 ORGANISER",
            command=self.open_organize_dialog,
            style='Action.TButton'
        )
        self.organize_button.pack(side="left", padx=5)

        # ➕ Bouton d'ajout
        self.add_program_button = ttk.Button(
            buttons_frame,
            text="➕ AJOUTER",
            command=self.add_custom_program,
            style='Action.TButton'
        )
        self.add_program_button.pack(side="left", padx=5)

        # 🚀 Bouton d'installation - ULTRA VISIBLE
        self.install_button = ttk.Button(
            buttons_frame,
            text="🚀 INSTALLER",
            command=self.start_installation,
            style='Action.TButton',
            state='disabled'
        )
        self.install_button.pack(side="left", padx=5)
    
    def _on_mousewheel(self, event):
        """Gestion du scroll avec la molette"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _center_watermark(self, event=None):
        """Centre le logo en filigrane dans le canvas"""
        if hasattr(self, 'bg_logo') and self.bg_logo and hasattr(self, 'watermark_id'):
            # Obtenir la taille du canvas
            canvas_width = self.main_canvas.winfo_width()
            canvas_height = self.main_canvas.winfo_height()

            # Centrer le logo
            center_x = canvas_width // 2
            center_y = canvas_height // 2

            # Mettre à jour la position du logo
            self.main_canvas.coords(self.watermark_id, center_x, center_y)

            # S'assurer que le logo reste en arrière-plan
            self.main_canvas.tag_lower(self.watermark_id)

    def select_all_programs(self):
        """Sélectionne TOUS les programmes"""
        for var in self.program_vars.values():
            var.set(True)
        self.update_selection_count()
    
    def deselect_all_programs(self):
        """Désélectionne tous les programmes"""
        for var in self.program_vars.values():
            var.set(False)
        self.update_selection_count()
    
    def select_category(self, category):
        """Sélectionne tous les programmes d'une catégorie"""
        if category in self.programs:
            for program_name in self.programs[category]:
                if program_name in self.program_vars:
                    self.program_vars[program_name].set(True)
        self.update_selection_count()
    
    def update_selection_count(self):
        """🎨 Met à jour le compteur de sélection avec style moderne"""
        selected_count = sum(1 for var in self.program_vars.values() if var.get())
        total_count = len(self.program_vars)

        # Couleur dynamique selon le nombre de sélections
        if selected_count == 0:
            color = self.DARK_FG3
            icon = "📋"
        elif selected_count < 10:
            color = self.ACCENT_CYAN
            icon = "📌"
        elif selected_count < 30:
            color = self.ACCENT_YELLOW
            icon = "⭐"
        else:
            color = self.ACCENT_GREEN
            icon = "🎯"

        self.selection_label.config(
            text=f"{icon} {selected_count} / {total_count} programmes sélectionnés",
            fg=color
        )

        # Activer/désactiver le bouton avec animation visuelle
        if selected_count > 0:
            self.install_button.config(state='normal')
        else:
            self.install_button.config(state='disabled')
    
    def start_installation(self):
        """Démarre l'installation ou l'exécution de commandes"""
        self.logger.info("🔔 Bouton INSTALLER cliqué !")
        
        selected_programs = [
            name for name, var in self.program_vars.items() if var.get()
        ]
        
        self.logger.info(f"📊 Programmes sélectionnés: {len(selected_programs)}")
        self.logger.info(f"📋 Liste: {selected_programs}")
        
        if not selected_programs:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner au moins un programme ou commande.")
            return
        
        # Séparer les commandes des programmes
        commands_to_run = []
        programs_to_install = []
        
        self.logger.info(f"🔍 Recherche dans programs_db...")
        
        for prog_name in selected_programs:
            # Chercher le programme dans la base de données
            prog_info = None
            for category_progs in self.programs.values():
                if prog_name in category_progs:
                    prog_info = category_progs[prog_name]
                    break
            
            self.logger.info(f"🔍 {prog_name} -> prog_info={prog_info is not None}, is_command={prog_info.get('is_command', False) if prog_info else 'N/A'}")
            
            if prog_info and prog_info.get('is_command'):
                commands_to_run.append((prog_name, prog_info))
                self.logger.info(f"➡️ {prog_name} ajouté aux commandes")
            else:
                programs_to_install.append(prog_name)
                self.logger.info(f"➡️ {prog_name} ajouté aux programmes à installer")
        
        # Exécuter les commandes immédiatement
        if commands_to_run:
            self.logger.info(f"⚡ Exécution de {len(commands_to_run)} commande(s)")
            self.execute_commands(commands_to_run)
        
        # Installer les programmes si nécessaire
        if programs_to_install:
            self.logger.info(f"📦 {len(programs_to_install)} programme(s) à installer")
            # Confirmation
            if messagebox.askyesno(
                "Confirmation d'installation",
                f"Installer {len(programs_to_install)} programme(s) ?\n\n"
                "L'installation sera automatique et silencieuse."
            ):
                self.logger.info(f"✅ Installation confirmée pour {len(programs_to_install)} programmes")
                
                # Désactiver le bouton d'installation
                self.is_installing = True
                self.install_button.config(state='disabled', text="⏳ Installation...")

                # Initialiser le temps de démarrage pour le calcul du temps restant
                import time
                self.installation_start_time = time.time()

                # Lancer l'installation dans un thread séparé
                if self.installer_manager:
                    self.logger.info(f"🚀 Démarrage du thread d'installation...")
                    install_thread = threading.Thread(
                        target=self.installer_manager.install_programs,
                        args=(
                            programs_to_install,
                            self.update_progress,
                            self.on_installation_finished,
                            self.successful_installs,  # Liste des succès
                            self.failed_installs        # Liste des échecs
                        ),
                        daemon=True
                    )
                    install_thread.start()
                else:
                    self.logger.error("❌ InstallerManager n'est pas disponible!")
                    messagebox.showerror(
                        "Erreur",
                        "Le gestionnaire d'installation n'est pas disponible!"
                    )
                    self.is_installing = False
                    self.install_button.config(state='normal', text="🚀 INSTALLER")
            else:
                self.logger.info("❌ Installation annulée par l'utilisateur")
        elif not commands_to_run:
            self.logger.warning("⚠️ Aucune action à effectuer")
            messagebox.showwarning("Aucune sélection", "Aucune action à effectuer.")
    
    def execute_commands(self, commands_list):
        """Exécute les commandes Windows sélectionnées"""
        import subprocess
        
        executed_count = 0
        failed_count = 0
        
        for prog_name, prog_info in commands_list:
            command = prog_info.get('command', '')
            admin_required = prog_info.get('admin_required', False)
            
            try:
                if admin_required:
                    # Exécuter en mode administrateur avec PowerShell
                    ps_command = f'Start-Process cmd.exe -ArgumentList "/c {command}" -Verb RunAs'
                    subprocess.Popen(
                        ["powershell.exe", "-Command", ps_command],
                        shell=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                else:
                    # Exécuter normalement
                    subprocess.Popen(
                        command,
                        shell=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                
                self.logger.info(f"✅ Commande exécutée: {prog_name}")
                executed_count += 1
                
            except Exception as e:
                self.logger.error(f"❌ Erreur lors de l'exécution de {prog_name}: {e}")
                failed_count += 1
        
        # Désélectionner les commandes exécutées
        for prog_name, _ in commands_list:
            if prog_name in self.program_vars:
                self.program_vars[prog_name].set(False)
        
        self.update_selection_count()
        
        # Message de résultat
        if executed_count > 0:
            message = f"✅ {executed_count} commande(s) exécutée(s)"
            if failed_count > 0:
                message += f"\n⚠️ {failed_count} échec(s)"
            
            messagebox.showinfo("Commandes exécutées", message)

    
    def update_progress(self, value, message=""):
        """Met à jour la barre de progression avec pourcentage et temps restant"""
        import time

        self.progress_var.set(value)
        if message:
            self.selection_label.config(text=f"⏳ {message}")

        # Calculer et afficher le pourcentage et temps restant
        if value > 0 and self.installation_start_time:
            elapsed_time = time.time() - self.installation_start_time

            # Estimer le temps restant basé sur le pourcentage actuel
            if value > 0:
                total_estimated_time = (elapsed_time / value) * 100
                remaining_time = total_estimated_time - elapsed_time

                # Convertir en minutes et secondes
                remaining_minutes = int(remaining_time // 60)
                remaining_seconds = int(remaining_time % 60)

                # Formater le texte
                progress_text = f"{int(value)}% • Temps restant: {remaining_minutes}min {remaining_seconds}s"
            else:
                progress_text = f"{int(value)}%"
        else:
            # Pas d'installation en cours, vider le label
            progress_text = ""

        self.progress_label.config(text=progress_text)
        self.root.update_idletasks()
    
    def log_installation_message(self, message, level="info"):
        """Affiche un message de log"""
        print(f"[{level.upper()}] {message}")
        self.logger.info(message)

    def generate_installation_report(self, success_list, failed_list):
        """Génère un rapport HTML détaillé des installations"""
        from datetime import datetime
        import os

        # Créer dossier rapports
        reports_dir = Path.home() / "Desktop" / "NiTriTe_Rapports"
        reports_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = reports_dir / f"Rapport_Installation_{timestamp}.html"

        # Générer HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rapport d'Installation NiTriTe V5.0</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            color: #ffffff;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #FF6B00;
            border-bottom: 3px solid #FF6B00;
            padding-bottom: 10px;
        }}
        h2 {{
            margin-top: 30px;
        }}
        .summary {{
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            display: flex;
            gap: 40px;
            justify-content: center;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 48px;
            font-weight: bold;
        }}
        .success {{ color: #2ecc71; }}
        .failed {{ color: #ff3333; }}
        .total {{ color: #FFB800; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #2a2a2a;
            border-radius: 8px;
            overflow: hidden;
        }}
        th {{
            background: #FF6B00;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #333;
        }}
        tr:hover {{
            background: #333;
        }}
        .success-icon {{ color: #2ecc71; font-size: 20px; }}
        .failed-icon {{ color: #ff3333; font-size: 20px; }}
        .reason {{
            font-size: 12px;
            color: #aaa;
            font-style: italic;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #333;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>🚀 Rapport d'Installation NiTriTe V5.0</h1>
    <p><strong>Date:</strong> {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}</p>

    <div class="summary">
        <div class="stat">
            <div class="stat-number total">{len(success_list) + len(failed_list)}</div>
            <div>Total</div>
        </div>
        <div class="stat">
            <div class="stat-number success">{len(success_list)}</div>
            <div>Réussies</div>
        </div>
        <div class="stat">
            <div class="stat-number failed">{len(failed_list)}</div>
            <div>Échouées</div>
        </div>
    </div>

    <h2 style="color: #2ecc71;">✅ Applications installées avec succès ({len(success_list)})</h2>
    <table>
        <tr>
            <th>N°</th>
            <th>Application</th>
            <th>Catégorie</th>
            <th>Méthode</th>
        </tr>
"""

        for idx, app in enumerate(success_list, 1):
            html_content += f"""        <tr>
            <td>{idx}</td>
            <td><span class="success-icon">✓</span> {app.get('name', 'N/A')}</td>
            <td>{app.get('category', 'N/A')}</td>
            <td>{app.get('method', 'Direct')}</td>
        </tr>
"""

        html_content += f"""    </table>

    <h2 style="color: #ff3333;">❌ Applications échouées ({len(failed_list)})</h2>
    <table>
        <tr>
            <th>N°</th>
            <th>Application</th>
            <th>Catégorie</th>
            <th>Raison de l'échec</th>
        </tr>
"""

        for idx, app in enumerate(failed_list, 1):
            reason = app.get('reason', 'Erreur inconnue')
            html_content += f"""        <tr>
            <td>{idx}</td>
            <td><span class="failed-icon">✗</span> {app.get('name', 'N/A')}</td>
            <td>{app.get('category', 'N/A')}</td>
            <td><span class="reason">{reason}</span></td>
        </tr>
"""

        html_content += """    </table>

    <footer>
        <p>NiTriTe V5.0 - Installateur Automatique de Programmes</p>
        <p>Rapport généré automatiquement</p>
    </footer>
</body>
</html>
"""

        # Écrire le fichier
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.logger.info(f"Rapport généré: {report_file}")

            # Ouvrir le rapport dans le navigateur
            webbrowser.open(str(report_file))

            return report_file
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du rapport: {e}")
            return None

    def on_installation_finished(self, success):
        """Appelé quand l'installation est terminée"""
        self.is_installing = False
        self.installation_start_time = None  # Réinitialiser le temps de démarrage
        self.install_button.config(state='normal', text="🚀 INSTALLER")

        # Générer le rapport détaillé si des installations ont été effectuées
        report_file = None
        if self.successful_installs or self.failed_installs:
            report_file = self.generate_installation_report(
                self.successful_installs,
                self.failed_installs
            )

        if success:
            # Message personnalisé avec statistiques
            if report_file:
                messagebox.showinfo(
                    "Installation terminée",
                    f"✅ Installation terminée !\n\n"
                    f"Réussies: {len(self.successful_installs)}\n"
                    f"Échouées: {len(self.failed_installs)}\n\n"
                    f"📄 Rapport détaillé ouvert dans votre navigateur.\n"
                    f"Fichier: {report_file.name}"
                )
            else:
                messagebox.showinfo(
                    "Installation terminée",
                    "✅ L'installation de tous les programmes sélectionnés est terminée !\n\n"
                    "Vérifiez vos applications installées."
                )
            # Créer le dossier "Outils de nettoyage" si nécessaire
            self.create_cleanup_folder()
            # Désélectionner tous les programmes
            self.deselect_all_programs()
        else:
            if report_file:
                messagebox.showwarning(
                    "Installation interrompue",
                    f"⚠️ L'installation a été interrompue.\n\n"
                    f"Réussies: {len(self.successful_installs)}\n"
                    f"Échouées: {len(self.failed_installs)}\n\n"
                    f"📄 Rapport détaillé disponible: {report_file.name}"
                )
            else:
                messagebox.showwarning(
                    "Installation interrompue",
                    "⚠️ L'installation a été interrompue.\n\n"
                    "Certains programmes peuvent avoir été installés."
                )

        # Réinitialiser les listes pour la prochaine installation
        self.successful_installs = []
        self.failed_installs = []

        self.update_progress(0, "")
        self.update_selection_count()
    
    def create_cleanup_folder(self):
        """Crée le dossier 'Outils de nettoyage' sur le bureau avec les raccourcis"""
        try:
            import os
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            cleanup_folder = Path(desktop) / "Outils de nettoyage"
            cleanup_folder.mkdir(exist_ok=True)
            
            # Programmes à inclure dans le dossier
            cleanup_programs = {
                "Malwarebytes": r"C:\Program Files\Malwarebytes\Anti-Malware\mbam.exe",
                "AdwCleaner": r"C:\Program Files\Malwarebytes\AdwCleaner\adwcleaner.exe",
                "Wise Disk Cleaner": r"C:\Program Files (x86)\Wise\Wise Disk Cleaner\WiseDiskCleaner.exe",
                "Spybot": r"C:\Program Files (x86)\Spybot - Search & Destroy 2\SDWelcome.exe"
            }
            
            # Télécharger les portables
            portable_downloads = Path(__file__).parent.parent / "downloads"
            anydesk_exe = portable_downloads / "AnyDesk.exe"
            rustdesk_exe = portable_downloads / "rustdesk.exe"
            
            # Copier les exécutables portables
            if anydesk_exe.exists():
                import shutil
                shutil.copy(anydesk_exe, cleanup_folder / "AnyDesk.exe")
            
            if rustdesk_exe.exists():
                import shutil
                shutil.copy(rustdesk_exe, cleanup_folder / "RustDesk.exe")
            
            # Créer les raccourcis
            shell = Dispatch('WScript.Shell')
            
            for prog_name, exe_path in cleanup_programs.items():
                if Path(exe_path).exists():
                    shortcut_path = cleanup_folder / f"{prog_name}.lnk"
                    shortcut = shell.CreateShortCut(str(shortcut_path))
                    shortcut.Targetpath = exe_path
                    shortcut.WorkingDirectory = str(Path(exe_path).parent)
                    shortcut.IconLocation = exe_path
                    shortcut.save()
            
            self.logger.info(f"✅ Dossier 'Outils de nettoyage' créé sur le bureau")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Impossible de créer le dossier Outils de nettoyage: {e}")
    
    def open_massgrave(self):
        """Ouvre le site MAS dans le navigateur"""
        import webbrowser
        webbrowser.open("https://massgrave.dev/")
        self.logger.info("🔐 Ouverture du site MAS (Microsoft Activation Scripts)")
    
    def activate_windows(self):
        """Lance la commande d'activation Windows en admin"""
        if messagebox.askyesno(
            "Activation Windows",
            "⚡ Cette commande va lancer le script d'activation Windows.\n\n"
            "Voulez-vous continuer ?\n\n"
            "Note: Un terminal PowerShell s'ouvrira avec les privilèges administrateur."
        ):
            try:
                import subprocess
                
                # Commande PowerShell à exécuter en admin
                command = 'irm https://get.activated.win | iex'
                
                # Lancer PowerShell en admin avec fenêtre visible - MÉTHODE CORRIGÉE
                ps_command = f'Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoExit","-Command","irm https://get.activated.win | iex"'
                
                subprocess.Popen(
                    ['powershell.exe', '-Command', ps_command],
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                
                self.logger.info("⚡ Commande d'activation Windows lancée")
                messagebox.showinfo(
                    "Activation lancée",
                    "✅ Le script d'activation a été lancé !\n\n"
                    "Suivez les instructions dans la fenêtre PowerShell."
                )
                
            except Exception as e:
                self.logger.error(f"❌ Erreur lors de l'activation: {e}")
                messagebox.showerror(
                    "Erreur",
                    f"❌ Impossible de lancer l'activation:\n{e}"
                )
    
    def create_tools_panel_in_container(self, parent):
        """Crée le panel d'outils à droite avec UNE SEULE SCROLLBAR et layout dynamique 6-8 colonnes"""
        tools_frame = ttk.LabelFrame(parent, text="🛠️ OUTILS WINDOWS - PLUS DE 500 BOUTONS UTILES", padding=5)
        tools_frame.pack(fill="both", expand=True)

        # Frame principal avec scrollbar UNIQUE
        main_container = ttk.Frame(tools_frame)
        main_container.pack(fill="both", expand=True)

        # Scrollbar unique pour TOUT le panneau
        scrollbar = ttk.Scrollbar(main_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Canvas principal avec scrollbar unique
        self.tools_canvas = tk.Canvas(
            main_container,
            bg=self.DARK_BG,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.tools_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tools_canvas.yview)

        # Frame contenant TOUTES les sections (scrollable)
        self.sections_container = ttk.Frame(self.tools_canvas)
        self.tools_canvas.create_window((0, 0), window=self.sections_container, anchor="nw")

        # Bind pour mettre à jour la région scrollable
        self.sections_container.bind(
            "<Configure>",
            lambda e: self.tools_canvas.configure(scrollregion=self.tools_canvas.bbox("all"))
        )

        # Bind scroll avec molette
        self.tools_canvas.bind_all("<MouseWheel>", self._on_mousewheel_tools)

        # Créer toutes les sections dans le container unique
        self.create_all_tools_sections()

    def _on_mousewheel_tools(self, event):
        """Gestion du scroll avec la molette pour le panneau outils"""
        try:
            self.tools_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass

    def get_columns_count(self):
        """Détermine le nombre de colonnes selon la largeur d'écran"""
        screen_width = self.root.winfo_screenwidth()
        return 8 if screen_width > 1500 else 6

    def create_section(self, title, icon, buttons_data, is_web=False, allow_reorder=True):
        """
        Fonction helper pour créer une section avec des boutons et options de réorganisation

        Args:
            title: Titre de la section
            icon: Emoji/icône de la section
            buttons_data: Liste de tuples (label, url_ou_commande)
            is_web: Si True, tous les boutons ouvrent des URLs web
            allow_reorder: Si True, ajoute les boutons UP/DOWN et drag & drop
        """
        # Frame principale de section
        section_main_frame = tk.Frame(self.sections_container, bg=self.DARK_BG2)
        section_main_frame.pack(fill="x", pady=(10, 0))

        # Frame titre avec boutons de contrôle
        title_frame = tk.Frame(section_main_frame, bg=self.DARK_BG2)
        title_frame.pack(fill="x", padx=5, pady=2)

        # Titre de la section - Compact
        title_label = tk.Label(
            title_frame,
            text=f"{icon} {title}",
            font=("Segoe UI", 9, "bold"),
            bg=self.DARK_BG2,
            fg=self.ACCENT_ORANGE
        )
        title_label.pack(side="left", padx=10)

        # Ajouter les boutons de réorganisation si demandé - Compacts
        if allow_reorder:
            # Bouton UP
            btn_up = tk.Button(
                title_frame,
                text="▲",
                command=lambda: self.move_section_up(title),
                bg=self.DARK_BG3,
                fg=self.DARK_FG,
                relief="flat",
                font=("Segoe UI", 7),
                padx=4,
                pady=1
            )
            btn_up.pack(side="right", padx=2)

            # Bouton DOWN
            btn_down = tk.Button(
                title_frame,
                text="▼",
                command=lambda: self.move_section_down(title),
                bg=self.DARK_BG3,
                fg=self.DARK_FG,
                relief="flat",
                font=("Segoe UI", 7),
                padx=4,
                pady=1
            )
            btn_down.pack(side="right", padx=2)

            # Ajouter menu contextuel
            self.add_category_context_menu(title_frame, title)

        # Stocker les informations de la section
        self.section_titles.append(title_frame)
        self.section_frames[title] = section_main_frame

        # Frame de section (pour les boutons)
        section_frame = ttk.LabelFrame(
            section_main_frame,
            text="",
            padding=5
        )
        section_frame.pack(fill="x", padx=2, pady=3)

        # Container pour les boutons
        buttons_frame = ttk.Frame(section_frame)
        buttons_frame.pack(fill="x", padx=2, pady=2)

        # Déterminer nombre de colonnes dynamiquement
        columns = self.get_columns_count()

        # Configuration des colonnes
        for i in range(columns):
            buttons_frame.grid_columnconfigure(i, weight=1)

        # Créer les boutons en grille
        for idx, (label, cmd_or_url) in enumerate(buttons_data):
            row = idx // columns
            col = idx % columns

            # Déterminer la commande à exécuter
            if is_web or (isinstance(cmd_or_url, str) and cmd_or_url.startswith('http')):
                command = lambda u=cmd_or_url: webbrowser.open(u)
            elif isinstance(cmd_or_url, str) and cmd_or_url.startswith('ms-'):
                command = lambda u=cmd_or_url: webbrowser.open(u)
            elif callable(cmd_or_url):
                command = cmd_or_url
            else:
                command = lambda c=cmd_or_url: self.execute_quick_command(c, True)

            btn = ttk.Button(
                buttons_frame,
                text=label,
                command=command,
                style='ToolPanel.TButton'
            )
            btn.grid(row=row, column=col, pady=1, padx=1, sticky="ew")

            # Ajouter à la liste des boutons pour le drag & drop
            self.all_buttons.append(btn)

            # Compter les boutons du panneau d'outils
            self.tools_buttons_count += 1

        return section_main_frame

    def create_all_tools_sections(self):
        """Crée toutes les sections d'outils avec BEAUCOUP plus de boutons"""

        # Ordre personnalisé des sections (selon demande utilisateur)
        self.create_activation_section()           # 1. Activation et Téléchargements
        self.create_winget_section()               # 2. Winget - Package Manager
        self.create_drivers_section()              # 3. drivers et pilotes
        self.create_parametres_section()           # 4. parametre Windows
        self.create_support_section()              # 5. Support constructeur
        self.create_reparation_section()           # 6. reparation système
        self.create_maintenance_section()          # 7. maintenance et nettoyage
        self.create_diagnostics_section()          # 8. Diagnostics et info

        # Autres sections (ordre standard)
        self.create_reseau_section()
        self.create_benchmark_section()
        self.create_fournisseurs_section()
        self.create_documentation_section()

        # Activer le drag & drop pour les catégories et boutons
        self.enable_category_drag_drop()
        self.enable_buttons_drag_drop()

        # Charger l'ordre des sections si disponible
        self.load_sections_order()

        # Mettre à jour le badge avec le nombre total de boutons
        self.update_count_badge()

    def enable_category_drag_drop(self):
        """Active le drag & drop pour réorganiser les catégories"""
        # Créer un mapping inverse title_frame -> title_string pour faciliter le drag
        self.title_frame_to_string = {}
        for title_str, main_frame in self.section_frames.items():
            for child in main_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    self.title_frame_to_string[child] = title_str
                    break

        for section_title in self.section_titles:
            section_title.bind("<Button-1>", self.start_category_drag)
            section_title.bind("<B1-Motion>", self.do_category_drag)
            section_title.bind("<ButtonRelease-1>", self.end_category_drag)
            section_title.config(cursor="hand2")

    def start_category_drag(self, event):
        """Début du drag d'une catégorie"""
        self.dragging_category = event.widget
        self.drag_start_y = event.y_root
        # Feedback visuel immédiat
        event.widget.config(bg=self.ACCENT_ORANGE, relief="raised")

    def do_category_drag(self, event):
        """Pendant le drag - montrer la position actuelle"""
        if self.dragging_category:
            delta_y = event.y_root - self.drag_start_y
            # Calculer combien de positions on se déplace
            steps = int(delta_y / 50)
            if steps != 0:
                # Montrer visuellement le déplacement
                self.dragging_category.config(bg=self.ACCENT_ORANGE if abs(steps) > 0 else self.DARK_BG2)

    def end_category_drag(self, event):
        """Fin du drag - réorganiser"""
        if self.dragging_category:
            delta_y = event.y_root - self.drag_start_y
            self.reorder_sections_by_drag(self.dragging_category, delta_y)
            self.dragging_category.config(bg=self.DARK_BG2, relief="flat")
            self.dragging_category = None

    def reorder_sections_by_drag(self, moved_title_frame, delta):
        """Réorganise les sections après drag"""
        # Trouver le titre dans la liste
        if moved_title_frame not in self.section_titles:
            return

        # Si déplacement significatif (réduit à 20 pour plus de sensibilité)
        if abs(delta) > 20:
            current_index = self.section_titles.index(moved_title_frame)

            # Calculer le nouvel index basé sur le delta (permet plusieurs positions)
            steps = int(delta / 50)  # Chaque 50 pixels = 1 position
            new_index = current_index + steps

            # Limiter aux bornes
            new_index = max(0, min(new_index, len(self.section_titles) - 1))

            if new_index != current_index:
                # Utiliser le mapping pour trouver le titre string
                moved_title_str = self.title_frame_to_string.get(moved_title_frame)

                if not moved_title_str:
                    # Fallback: utiliser l'index
                    sections_list = list(self.section_frames.keys())
                    if current_index < len(sections_list):
                        moved_title_str = sections_list[current_index]

                if moved_title_str:
                    # Réorganiser section_titles
                    moved_item = self.section_titles.pop(current_index)
                    self.section_titles.insert(new_index, moved_item)

                    # Réorganiser section_frames dans le nouvel ordre
                    sections_list = list(self.section_frames.items())

                    # Trouver l'item à déplacer
                    item_to_move = None
                    old_index = None
                    for i, (key, val) in enumerate(sections_list):
                        if key == moved_title_str:
                            item_to_move = (key, val)
                            old_index = i
                            break

                    if item_to_move and old_index is not None:
                        sections_list.pop(old_index)
                        sections_list.insert(new_index, item_to_move)
                        self.section_frames = dict(sections_list)

                        # Reconstruire le mapping après réorganisation
                        self.title_frame_to_string = {}
                        for title_str, main_frame in self.section_frames.items():
                            for child in main_frame.winfo_children():
                                if isinstance(child, tk.Frame):
                                    self.title_frame_to_string[child] = title_str
                                    break

                    # Réorganiser visuellement
                    self.refresh_sections_order()
                    self.save_sections_order()

    def move_section_up(self, section_title):
        """Déplace une section vers le haut"""
        if section_title not in self.section_frames:
            return

        # Trouver l'index dans la liste des sections
        section_frame = self.section_frames[section_title]
        all_sections = list(self.section_frames.values())
        current_index = all_sections.index(section_frame)

        if current_index > 0:
            # Échanger avec la section précédente
            sections_list = list(self.section_frames.items())
            sections_list[current_index], sections_list[current_index - 1] = \
                sections_list[current_index - 1], sections_list[current_index]

            # Reconstruire le dictionnaire
            self.section_frames = dict(sections_list)
            self.refresh_sections_order()
            self.save_sections_order()

    def move_section_down(self, section_title):
        """Déplace une section vers le bas"""
        if section_title not in self.section_frames:
            return

        # Trouver l'index dans la liste des sections
        section_frame = self.section_frames[section_title]
        all_sections = list(self.section_frames.values())
        current_index = all_sections.index(section_frame)

        if current_index < len(all_sections) - 1:
            # Échanger avec la section suivante
            sections_list = list(self.section_frames.items())
            sections_list[current_index], sections_list[current_index + 1] = \
                sections_list[current_index + 1], sections_list[current_index]

            # Reconstruire le dictionnaire
            self.section_frames = dict(sections_list)
            self.refresh_sections_order()
            self.save_sections_order()

    def refresh_sections_order(self):
        """Rafraîchit l'ordre visuel des sections"""
        for section_frame in self.section_frames.values():
            section_frame.pack_forget()

        for section_frame in self.section_frames.values():
            section_frame.pack(fill="x", pady=(10, 0))

        # Mettre à jour la région scrollable
        if hasattr(self, 'sections_container'):
            self.sections_container.update_idletasks()
            self.tools_canvas.configure(scrollregion=self.tools_canvas.bbox("all"))

    def add_category_context_menu(self, title_frame, section_title):
        """Ajoute menu clic droit sur les titres"""
        menu = tk.Menu(title_frame, tearoff=0, bg=self.DARK_BG2, fg=self.DARK_FG)
        menu.add_command(label="▲ Monter", command=lambda: self.move_section_up(section_title))
        menu.add_command(label="▼ Descendre", command=lambda: self.move_section_down(section_title))
        menu.add_separator()
        menu.add_command(label="🔄 Réinitialiser l'ordre", command=self.reset_sections_order)

        title_frame.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

    def save_sections_order(self):
        """Sauvegarde l'ordre des sections dans un fichier JSON"""
        try:
            config_dir = Path.home() / ".nitrite"
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / "sections_order.json"

            sections_order = list(self.section_frames.keys())

            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(sections_order, f, indent=2)

            self.logger.info(f"Ordre des sections sauvegardé: {config_file}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de l'ordre des sections: {e}")

    def update_count_badge(self):
        """Met à jour le badge avec le nombre d'applications et de boutons"""
        if hasattr(self, 'count_badge'):
            total_programs = sum(len(progs) if isinstance(progs, dict) else 0
                               for progs in self.programs.values())
            self.count_badge.config(
                text=f"⭐ {total_programs} Applications  •  🛠️ {self.tools_buttons_count} Boutons Utiles"
            )

    def load_sections_order(self):
        """Charge l'ordre des sections depuis le fichier JSON"""
        try:
            config_file = Path.home() / ".nitrite" / "sections_order.json"

            if not config_file.exists():
                return

            with open(config_file, 'r', encoding='utf-8') as f:
                sections_order = json.load(f)

            # Réorganiser selon l'ordre chargé
            new_dict = {}
            for section_name in sections_order:
                if section_name in self.section_frames:
                    new_dict[section_name] = self.section_frames[section_name]

            # Ajouter les sections manquantes
            for section_name, section_frame in self.section_frames.items():
                if section_name not in new_dict:
                    new_dict[section_name] = section_frame

            self.section_frames = new_dict
            self.refresh_sections_order()

            self.logger.info("Ordre des sections chargé depuis le fichier")
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de l'ordre des sections: {e}")

    def reset_sections_order(self):
        """Réinitialise l'ordre des sections"""
        try:
            config_file = Path.home() / ".nitrite" / "sections_order.json"
            if config_file.exists():
                config_file.unlink()

            messagebox.showinfo(
                "Ordre réinitialisé",
                "L'ordre des sections a été réinitialisé.\n"
                "Redémarrez l'application pour voir les changements."
            )
        except Exception as e:
            self.logger.error(f"Erreur lors de la réinitialisation: {e}")
            messagebox.showerror("Erreur", f"Impossible de réinitialiser l'ordre: {e}")

    def enable_buttons_drag_drop(self):
        """Active le drag & drop pour les boutons"""
        for button in self.all_buttons:
            button.bind("<Button-1>", self.start_button_drag, add="+")
            button.bind("<B1-Motion>", self.do_button_drag, add="+")
            button.bind("<ButtonRelease-1>", self.end_button_drag, add="+")

    def start_button_drag(self, event):
        """Début du drag d'un bouton"""
        self.dragging_button = event.widget
        self.drag_button_section = self.find_button_section(event.widget)

    def do_button_drag(self, event):
        """Pendant le drag du bouton"""
        if self.dragging_button:
            # Indication visuelle (optionnel)
            pass

    def end_button_drag(self, event):
        """Fin du drag - réorganiser le bouton"""
        if self.dragging_button:
            closest_button = self.find_closest_button(event)
            if closest_button and closest_button != self.dragging_button:
                self.swap_buttons(self.dragging_button, closest_button)
            self.dragging_button = None

    def find_button_section(self, button):
        """Trouve la section d'un bouton"""
        parent = button.master
        while parent and not isinstance(parent, ttk.LabelFrame):
            parent = parent.master
        return parent

    def find_closest_button(self, event):
        """Trouve le bouton le plus proche de la position de la souris"""
        # Implémentation basique - peut être améliorée
        return None

    def swap_buttons(self, button1, button2):
        """Échange deux boutons de position"""
        # Récupérer les infos de grille
        info1 = button1.grid_info()
        info2 = button2.grid_info()

        # Échanger les positions
        button1.grid(row=info2['row'], column=info2['column'])
        button2.grid(row=info1['row'], column=info1['column'])

    def create_reparation_section(self):
        """Section Réparation Système avec 30+ commandes Windows"""
        buttons_data = [
            # DISM & SFC
            ("🔍 DISM Check", "DISM /Online /Cleanup-Image /CheckHealth"),
            ("🔎 DISM Scan", "DISM /Online /Cleanup-Image /ScanHealth"),
            ("🔧 DISM Restore", "DISM /Online /Cleanup-Image /RestoreHealth"),
            ("🧹 DISM Clean", "DISM /Online /Cleanup-Image /StartComponentCleanup"),
            ("🧹+ DISM Reset", "DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase"),
            ("🛡️ SFC Scan", "sfc /scannow"),
            ("🔨 DISM+SFC Full", "DISM /Online /Cleanup-Image /RestoreHealth & sfc /scannow"),

            # Disque & Boot
            ("💿 ChkDsk C:", "chkdsk C: /F /R"),
            ("💾 ChkDsk Scan", "chkdsk C: /scan"),
            ("🔄 Fix Boot", "bootrec /fixmbr & bootrec /fixboot & bootrec /rebuildbcd"),
            ("💿 Fix MBR", "bootrec /fixmbr"),
            ("💾 Rebuild BCD", "bootrec /rebuildbcd"),

            # Réseau
            ("🔥 Flush DNS", "ipconfig /flushdns"),
            ("🌐 Reset Winsock", "netsh winsock reset"),
            ("📡 Reset TCP/IP", "netsh int ip reset"),
            ("🔌 Renew IP", "ipconfig /release & ipconfig /renew"),

            # Système
            ("🧼 Reset Store", "wsreset.exe"),
            ("⚙️ MSConfig", "msconfig"),
            ("ℹ️ WinVer", "winver"),
            ("🖥️ System Props", "sysdm.cpl"),
            ("🎛️ Device Mgr", "devmgmt.msc"),
            ("💾 Disk Mgmt", "diskmgmt.msc"),
            ("🔌 Services", "services.msc"),
            ("📋 Registry", "regedit"),
            ("🖨️ Printers", "control printers"),

            # Explorateur
            ("📁 AppData", "explorer %appdata%"),
            ("🗑️ Temp", "explorer %temp%"),
            ("🌐 Programs", "explorer shell:Programs"),
            ("🚀 Startup", "explorer shell:Startup"),
            ("💻 System32", "explorer C:\\Windows\\System32"),
            ("🗂️ ProgramData", "explorer C:\\ProgramData")
        ]
        self.create_section("RÉPARATION SYSTÈME", "🔧", buttons_data, is_web=False)
    
    def create_activation_section(self):
        """Section Activation & Téléchargements avec 30+ sites"""
        buttons_data = [
            # Outils activation (commandes spéciales)
            ("🔐 MAS Activator", self.open_massgrave),
            ("⚡ Activate Windows", self.activate_windows),
            ("💾 Portables DB", self.show_portable_database_stats),

            # Outils Microsoft
            ("⚡ PowerToys", "https://github.com/microsoft/PowerToys/releases/latest"),

            # Office & Microsoft
            ("📦 Office FR", "https://gravesoft.dev/office_c2r_links#french-fr-fr"),
            ("📋 Office EN", "https://gravesoft.dev/office_c2r_links"),
            ("🪟 Windows ISOs", "https://massgrave.dev/genuine-installation-media.html"),

            # Torrents & Downloads
            ("🌊 YggTorrent", "https://www.yggtorrent.top/"),
            ("🏴‍☠️ The Pirate Bay", "https://thepiratebay.org/"),
            ("🎯 1337x", "https://1337x.to/"),
            ("⚡ RARBG Mirror", "https://rarbg.to/"),
            ("🌐 Torrentz2", "https://torrentz2.eu/"),

            # Software repositories
            ("📚 Archive.org", "https://archive.org/"),
            ("🎮 FitGirl Repacks", "https://fitgirl-repacks.site/"),
            ("🔧 MajorGeeks", "https://www.majorgeeks.com/"),
            ("📦 Portable AppZ", "https://portableappz.blogspot.com/"),
            ("💿 PortableApps", "https://portableapps.com/"),
            ("🎯 Ninite", "https://ninite.com/"),
            ("📦 Chocolatey", "https://chocolatey.org/"),
            ("🔧 Patch My PC", "https://patchmypc.com/"),
            ("📥 FileHippo", "https://filehippo.com/"),
            ("💾 Softonic", "https://www.softonic.com/"),
            ("📦 Download.com", "https://download.cnet.com/"),
            ("🎯 Uptodown", "https://uptodown.com/"),
            ("📱 APKMirror", "https://www.apkmirror.com/"),
            ("📲 APKPure", "https://apkpure.com/"),
            ("🕰️ OldVersion", "http://www.oldversion.com/"),
            ("📜 OldApps", "https://www.oldapps.com/"),

            # Mac & Linux
            ("🍎 EveryMac", "https://everymac.com/"),
            ("🐧 Ubuntu", "https://ubuntu.com/download"),
            ("🎩 Fedora", "https://getfedora.org/"),
            ("🌀 Debian", "https://www.debian.org/"),
        ]
        self.create_section("ACTIVATION & TÉLÉCHARGEMENTS", "🔑", buttons_data, is_web=False)

    def create_maintenance_section(self):
        """Section Maintenance & Nettoyage - Outils Windows uniquement"""
        buttons_data = [
            # Nettoyage
            ("🗑️ Vider Corbeille", "PowerShell -Command \"Clear-RecycleBin -Force\""),
            ("🧹 Disk Cleanup", "cleanmgr"),
            ("📦 Cleanup Full", "cleanmgr /sageset:1 & cleanmgr /sagerun:1"),
            ("🗂️ Clean WinSxS", "DISM /Online /Cleanup-Image /StartComponentCleanup"),
            ("🗑️ Vider Temp", "del /q /f %temp%\\* & rd /s /q %temp%"),
            ("🧹 Clean Prefetch", "del /q /f C:\\Windows\\Prefetch\\*"),
            ("📥 Open Downloads", "explorer %USERPROFILE%\\Downloads"),
            ("🧼 Store Reset", "wsreset.exe"),

            # Défragmentation & Optimisation
            ("🔄 Defrag C:", "defrag C: /O"),
            ("📊 Defrag UI", "dfrgui"),
            ("⚡ Optimize All", "defrag /C /O"),

            # Gestionnaires Windows
            ("⚡ Task Manager", "taskmgr"),
            ("📈 Resource Monitor", "resmon"),
            ("🗂️ Storage Sense", "start ms-settings:storagesense"),
            ("🔌 Uninstall Apps", "appwiz.cpl"),
            ("💾 Disk Mgmt", "diskmgmt.msc"),
        ]
        self.create_section("MAINTENANCE & NETTOYAGE", "🧹", buttons_data, is_web=False)

    def create_diagnostics_section(self):
        """Section Diagnostics & Infos - 60+ outils"""
        buttons_data = [
            # Commandes Windows
            ("💻 System Info", "msinfo32"),
            ("🎮 DirectX Diag", "dxdiag"),
            ("📊 Event Viewer", "eventvwr.msc"),
            ("📈 Perf Monitor", "perfmon"),
            ("💾 Disk Mgmt", "diskmgmt.msc"),
            ("🔧 Reliability", "perfmon /rel"),
            ("🖥️ System Props", "sysdm.cpl"),
            ("ℹ️ WinVer", "winver"),
            ("🔌 Device Mgr", "devmgmt.msc"),
            ("🔋 Battery Report", "powercfg /batteryreport"),
            ("⚡ Energy Report", "powercfg /energy"),
            ("📡 Network Config", "ncpa.cpl"),
            ("🧪 Memory Test", "MdSched.exe"),
            ("🔍 Health Check", "DISM /Online /Cleanup-Image /CheckHealth"),

            # Logiciels Info Système
            ("🔍 Speccy", "https://www.ccleaner.com/speccy"),
            ("⚡ CPU-Z", "https://www.cpuid.com/softwares/cpu-z.html"),
            ("🎮 GPU-Z", "https://www.techpowerup.com/gpuz/"),
            ("💾 HWiNFO", "https://www.hwinfo.com/download/"),
            ("📈 AIDA64", "https://www.aida64.com/downloads"),
            ("🔧 HWMonitor", "https://www.cpuid.com/softwares/hwmonitor.html"),
            ("💻 PC-Wizard", "https://www.cpuid.com/softwares/pc-wizard.html"),
            ("🔍 SIW", "https://www.gtopala.com/"),
            ("💻 Belarc Advisor", "https://www.belarc.com/products/belarc-advisor"),
            ("🌡️ Core Temp", "https://www.alcpu.com/CoreTemp/"),
            ("📊 Open HW Monitor", "https://openhardwaremonitor.org/downloads/"),
            ("⚙️ MSI Afterburner", "https://www.msi.com/Landing/afterburner/graphics-cards"),
            ("🌡️ SpeedFan", "http://www.almico.com/speedfan.php"),
            ("📊 HWMonitor Pro", "https://www.cpuid.com/softwares/hwmonitor-pro.html"),

            # Sysinternals
            ("🛠️ Sysinternals", "https://learn.microsoft.com/sysinternals/"),
            ("🔍 Process Explorer", "https://learn.microsoft.com/sysinternals/downloads/process-explorer"),
            ("📊 Process Monitor", "https://learn.microsoft.com/sysinternals/downloads/procmon"),
            ("🚀 Autoruns", "https://learn.microsoft.com/sysinternals/downloads/autoruns"),
            ("💾 RamMap", "https://learn.microsoft.com/sysinternals/downloads/rammap"),

            # Disques
            ("💿 CrystalDiskInfo", "https://crystalmark.info/en/software/crystaldiskinfo/"),
            ("📊 CrystalDiskMark", "https://crystalmark.info/en/software/crystaldiskmark/"),
            ("💾 HD Tune", "https://www.hdtune.com/download.html"),
            ("📈 AS SSD Bench", "https://www.alex-is.de/"),
            ("⚡ ATTO Disk Bench", "https://www.atto.com/disk-benchmark/"),
            ("💾 Victoria HDD", "https://hdd.by/victoria/"),
            ("📦 Samsung Magician", "https://www.samsung.com/semiconductor/minisite/ssd/product/consumer/magician/"),
            ("💿 Crucial SE", "https://www.crucial.com/support/storage-executive"),
            ("⚡ WD Dashboard", "https://support.wdc.com/downloads.aspx"),

            # Tests & Stress
            ("🔍 OCCT", "https://www.ocbase.com/"),
            ("🛠️ Prime95", "https://www.mersenne.org/download/"),
            ("🔥 FurMark", "https://geeks3d.com/furmark/"),
            ("⚡ UserBenchmark", "https://www.userbenchmark.com/"),
            ("🔧 MemTest86", "https://www.memtest86.com/download.htm"),
            ("📊 MemTest64", "https://www.techpowerup.com/memtest64/"),
            ("🔍 Intel Burn Test", "https://www.techspot.com/downloads/4965-intel-burn-test.html"),
            ("📈 LinX", "https://www.techpowerup.com/download/linx/"),

            # Benchmarks
            ("📈 3DMark", "https://benchmarks.ul.com/3dmark"),
            ("💻 PCMark", "https://benchmarks.ul.com/pcmark10"),
            ("🔍 Geekbench", "https://www.geekbench.com/download/"),
            ("⚡ Cinebench", "https://www.maxon.net/en/cinebench"),
            ("📊 Blender Bench", "https://opendata.blender.org/"),
            ("⚡ V-Ray Bench", "https://www.chaos.com/vray/benchmark"),
        ]
        self.create_section("DIAGNOSTICS & INFOS", "🔍", buttons_data, is_web=False)

    def create_reseau_section(self):
        """Section Réseau & Internet - Outils Windows + Speedtest"""
        buttons_data = [
            # Commandes Windows
            ("🌐 Ping Google", "ping 8.8.8.8 -n 10"),
            ("🔍 NSLookup", "nslookup google.com"),
            ("📡 IPConfig", "ipconfig /all"),
            ("🗺️ Traceroute", "tracert google.com"),
            ("📊 Netstat", "netstat -ano"),
            ("🔥 Flush DNS", "ipconfig /flushdns"),
            ("🌐 Reset Winsock", "netsh winsock reset"),
            ("📡 Reset TCP/IP", "netsh int ip reset"),
            ("🔌 Renew IP", "ipconfig /release & ipconfig /renew"),
            ("🛡️ Firewall", "firewall.cpl"),
            ("🌐 Network Config", "ncpa.cpl"),
            ("📈 Resource Mon", "resmon"),
            ("🔍 Ping Test", "ping 8.8.8.8 -t"),
            ("📡 WiFi Info", "netsh wlan show interfaces"),
            ("🔐 Proxy Settings", "start ms-settings:network-proxy"),

            # Speed Tests
            ("⚡ Speedtest.net", "https://www.speedtest.net/"),
            ("🚀 Fast.com", "https://fast.com/"),
            ("⚡ TestMy.net", "https://testmy.net/"),
            ("📊 SpeedOf.Me", "https://speedof.me/"),
            ("⚡ Comparitech", "https://www.comparitech.com/internet-providers/speed-test/"),
            ("⚡ M-Lab Test", "https://speed.measurementlab.net/"),
            ("🌐 Google Fiber", "https://fiber.google.com/speedtest/"),
        ]
        self.create_section("RÉSEAU & INTERNET", "🌐", buttons_data, is_web=False)

    def create_winget_section(self):
        """Section Winget - Package Manager"""
        buttons_data = [
            ("🔄 Upgrade All", "winget upgrade --all"),
            ("📋 List Upgrades", "winget upgrade"),
            ("🔍 Search", "winget search"),
            ("📦 List Installed", "winget list"),
            ("⚙️ Winget Info", "winget --info"),
            ("🧹 Reset Cache", "winget source reset --force"),
            ("📥 UPD Chrome", "winget upgrade Google.Chrome"),
            ("🦊 UPD Firefox", "winget upgrade Mozilla.Firefox"),
            ("📝 UPD VSCode", "winget upgrade Microsoft.VisualStudioCode"),
            ("💬 UPD Discord", "winget upgrade Discord.Discord"),
            ("🎮 UPD Steam", "winget upgrade Valve.Steam"),
            ("🎵 UPD Spotify", "winget upgrade Spotify.Spotify"),
        ]
        self.create_section("WINGET - PACKAGE MANAGER", "🔄", buttons_data, is_web=False)

    def create_parametres_section(self):
        """Section Paramètres Windows"""
        buttons_data = [
            ("⚙️ Settings", "start ms-settings:"),
            ("🖥️ Display", "start ms-settings:display"),
            ("🔊 Sound", "start ms-settings:sound"),
            ("🔋 Battery", "start ms-settings:batterysaver"),
            ("🌐 Network", "start ms-settings:network"),
            ("🔒 Privacy", "start ms-settings:privacy"),
            ("🔄 Update", "start ms-settings:windowsupdate"),
            ("💾 Storage", "start ms-settings:storagesense"),
            ("🎨 Personalize", "start ms-settings:personalization"),
            ("🔐 Accounts", "start ms-settings:yourinfo"),
            ("⏰ Time & Lang", "start ms-settings:dateandtime"),
            ("♿ Accessibility", "start ms-settings:easeofaccess"),
            ("🎮 Gaming", "start ms-settings:gaming"),
            ("📱 Phone", "start ms-settings:mobile-devices"),
            ("🔔 Notifications", "start ms-settings:notifications"),
            ("⚡ Power", "start ms-settings:powersleep"),
            ("🖱️ Mouse", "start ms-settings:mousetouchpad"),
            ("⌨️ Keyboard", "start ms-settings:typing"),
            ("🖼️ Apps", "start ms-settings:appsfeatures"),
        ]
        self.create_section("PARAMÈTRES WINDOWS", "⚙️", buttons_data, is_web=False)

    def create_support_section(self):
        """Section Support Constructeurs"""
        buttons_data = [
            ("💻 Dell Support", "https://www.dell.com/support/"),
            ("🖥️ HP Support", "https://support.hp.com/"),
            ("💼 Lenovo Support", "https://support.lenovo.com/"),
            ("🎯 ASUS Support", "https://www.asus.com/support/"),
            ("🔧 Acer Support", "https://www.acer.com/support/"),
            ("⚡ MSI Support", "https://www.msi.com/support"),
            ("🌐 Gigabyte Support", "https://www.gigabyte.com/Support"),
            ("🎮 Razer Support", "https://support.razer.com/"),
            ("📱 Samsung Support", "https://www.samsung.com/support/"),
            ("🍎 Apple Support", "https://support.apple.com/"),
            ("💻 Microsoft Support", "https://support.microsoft.com/"),
            ("🎯 Intel Support", "https://www.intel.com/content/www/us/en/support.html"),
            ("🔴 AMD Support", "https://www.amd.com/support"),
            ("🎮 NVIDIA Support", "https://www.nvidia.com/support/"),
            ("💾 Western Digital", "https://support.wdc.com/"),
            ("📦 Seagate Support", "https://www.seagate.com/support/"),
            ("⚡ Corsair Support", "https://help.corsair.com/"),
            ("🔧 Logitech Support", "https://support.logi.com/"),
        ]
        self.create_section("SUPPORT CONSTRUCTEURS", "🛠️", buttons_data, is_web=True)

    def create_fournisseurs_section(self):
        """Section Fournisseurs & Achats - 50+ sites"""
        buttons_data = [
            # France B2B
            ("🔧 1fo Trade", "https://www.1fotrade.com/"),
            ("💻 Acadia Info", "https://www.acadia-info.com/"),
            ("📦 Flexit", "https://shop.flexitdistribution.com/"),
            ("💰 1fo Discount", "https://www.1fodiscount.com/"),
            ("📦 Noriak Distri", "https://www.noriak-distri.com/"),

            # France Grand Public
            ("🛒 Amazon FR", "https://www.amazon.fr/"),
            ("🏪 Cdiscount", "https://www.cdiscount.com/"),
            ("🌐 eBay FR", "https://www.ebay.fr/"),
            ("📢 Leboncoin", "https://www.leboncoin.fr/"),
            ("📚 Fnac", "https://www.fnac.com/"),
            ("🔌 Darty", "https://www.darty.com/"),
            ("🏪 Boulanger", "https://www.boulanger.com/"),
            ("🛒 E.Leclerc", "https://www.e.leclerc/"),
            ("🏬 Rue Commerce", "https://www.rueducommerce.fr/"),
            ("🎌 Rakuten", "https://fr.shopping.rakuten.com/"),

            # Spécialistes PC
            ("🔝 TopAchat", "https://www.topachat.com/"),
            ("💻 Grosbill", "https://www.grosbill.com/"),
            ("💼 Inmac Wstore", "https://www.inmac-wstore.com/"),
            ("🖥️ Visiodirect", "https://www.visiodirect.net/"),
            ("🔧 LDLC", "https://www.ldlc.com/"),
            ("💻 Materiel.net", "https://www.materiel.net/"),
            ("🎮 PC21", "https://www.pc21.fr/"),
            ("💼 Cybertek", "https://www.cybertek.fr/"),
            ("🎯 Config-Gamer", "https://www.config-gamer.fr/"),

            # Comparateurs & Deals
            ("💡 Idealo", "https://www.idealo.fr/"),
            ("🔥 Dealabs", "https://www.dealabs.com/"),
            ("🔍 Le Dénicheur", "https://ledenicheur.fr/"),

            # Apple & Mac
            ("🍎 OKA Mac", "https://www.okamac.com/fr/"),
            ("🍎 MacWay", "https://www.macway.com/"),

            # International
            ("🇨🇭 Digitec CH", "https://www.digitec.ch/fr"),
            ("🌍 Amazon DE", "https://www.amazon.de/"),
            ("🌐 Amazon UK", "https://www.amazon.co.uk/"),
            ("🇺🇸 Amazon US", "https://www.amazon.com/"),
            ("🇺🇸 Newegg", "https://www.newegg.com/"),
            ("📷 B&H Photo", "https://www.bhphotovideo.com/"),

            # Reconditionné
            ("♻️ BackMarket", "https://www.backmarket.fr/"),
            ("🔄 Refurbed", "https://www.refurbed.fr/"),
            ("📦 2ememain.be", "https://www.2ememain.be/"),

            # Asie
            ("🛒 AliExpress", "https://www.aliexpress.com/"),
            ("💰 Wish", "https://www.wish.com/"),
            ("📦 Banggood", "https://www.banggood.com/"),

            # Composants
            ("💾 Crucial FR", "https://www.crucial.fr/"),
            ("💼 Dell FR", "https://www.dell.com/fr-fr"),
            ("🖨️ HP FR", "https://www.hp.com/fr-fr/shop/"),
            ("💻 Lenovo FR", "https://www.lenovo.com/fr/fr/"),
            ("📱 Samsung FR", "https://www.samsung.com/fr/"),

            # Auto (bonus)
            ("🚗 La Centrale", "https://www.lacentrale.fr/"),
        ]
        self.create_section("FOURNISSEURS & ACHATS", "🛒", buttons_data, is_web=True)

    def create_securite_section(self):
        """Section Sécurité & Confidentialité - 50+ outils"""
        buttons_data = [
            # VPN
            ("🔒 ProtonVPN", "https://protonvpn.com/"),
            ("🛡️ NordVPN", "https://nordvpn.com/"),
            ("⚡ ExpressVPN", "https://www.expressvpn.com/"),
            ("🔐 Surfshark", "https://surfshark.com/"),
            ("🔒 PIA VPN", "https://www.privateinternetaccess.com/"),
            ("🌐 Mullvad VPN", "https://mullvad.net/"),
            ("🔐 CyberGhost", "https://www.cyberghostvpn.com/"),
            ("⚡ Windscribe", "https://windscribe.com/"),

            # Antivirus
            ("🔐 Malwarebytes", "https://www.malwarebytes.com/"),
            ("🛡️ Kaspersky", "https://www.kaspersky.fr/"),
            ("🔒 Bitdefender", "https://www.bitdefender.com/"),
            ("⚡ Avast Free", "https://www.avast.com/free-antivirus-download"),
            ("🔐 AVG Free", "https://www.avg.com/free-antivirus-download"),
            ("🛡️ Windows Defender", "windowsdefender:"),
            ("🔒 ESET NOD32", "https://www.eset.com/"),
            ("⚡ Sophos Home", "https://home.sophos.com/"),

            # Password Managers
            ("🔐 Bitwarden", "https://bitwarden.com/download/"),
            ("🛡️ KeePass", "https://keepass.info/download.html"),
            ("🔒 1Password", "https://1password.com/"),
            ("⚡ LastPass", "https://www.lastpass.com/"),
            ("🔐 Dashlane", "https://www.dashlane.com/"),
            ("🛡️ RoboForm", "https://www.roboform.com/"),
            ("🔒 Keeper", "https://www.keepersecurity.com/"),
            ("⚡ NordPass", "https://nordpass.com/"),

            # 2FA
            ("🔐 Authy", "https://authy.com/"),
            ("🛡️ Google Auth", "https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2"),
            ("🔒 MS Authenticator", "https://www.microsoft.com/security/mobile-authenticator-app"),

            # Privacy Tools
            ("🔐 Signal Desktop", "https://signal.org/download/"),
            ("🛡️ Threema", "https://threema.ch/"),
            ("🔒 Telegram", "https://telegram.org/"),
            ("⚡ ProtonMail", "https://proton.me/mail"),

            # Security Analysis
            ("🌐 Have I Been Pwned", "https://haveibeenpwned.com/"),
            ("🔐 VirusTotal", "https://www.virustotal.com/"),
            ("🛡️ Hybrid Analysis", "https://www.hybrid-analysis.com/"),
            ("🔒 Any.Run", "https://any.run/"),
            ("⚡ URLScan.io", "https://urlscan.io/"),
            ("🔐 Shodan", "https://www.shodan.io/"),
            ("🛡️ Joe Sandbox", "https://www.joesandbox.com/"),

            # Privacy OS
            ("🔒 Tails OS", "https://tails.boum.org/"),
            ("🛡️ Whonix", "https://www.whonix.org/"),
            ("⚡ Qubes OS", "https://www.qubes-os.org/"),

            # Ad Blocking
            ("🔐 Pi-hole", "https://pi-hole.net/"),
            ("🛡️ AdGuard DNS", "https://adguard-dns.io/"),
            ("🔒 uBlock Origin", "https://ublockorigin.com/"),
            ("⚡ Privacy Badger", "https://privacybadger.org/"),

            # Encryption
            ("🔐 VeraCrypt", "https://www.veracrypt.fr/"),
            ("🛡️ Cryptomator", "https://cryptomator.org/"),
            ("🔒 AxCrypt", "https://www.axcrypt.net/"),
        ]
        self.create_section("SÉCURITÉ & CONFIDENTIALITÉ", "🔒", buttons_data, is_web=True)

    def create_benchmark_section(self):
        """Section Benchmark & Tests - 40+ outils"""
        buttons_data = [
            ("⚡ UserBenchmark", "https://www.userbenchmark.com/"),
            ("📊 3DMark", "https://benchmarks.ul.com/3dmark"),
            ("💻 PCMark", "https://benchmarks.ul.com/pcmark10"),
            ("🔍 Geekbench", "https://www.geekbench.com/"),
            ("⚡ Cinebench", "https://www.maxon.net/en/cinebench"),
            ("📈 PassMark", "https://www.passmark.com/"),
            ("💾 CrystalDiskMark", "https://crystalmark.info/en/software/crystaldiskmark/"),
            ("📊 AS SSD Bench", "https://www.alex-is.de/"),
            ("⚡ ATTO Disk Bench", "https://www.atto.com/disk-benchmark/"),
            ("🔍 HD Tune", "https://www.hdtune.com/"),
            ("📈 Unigine Heaven", "https://benchmark.unigine.com/heaven"),
            ("💻 Unigine Valley", "https://benchmark.unigine.com/valley"),
            ("📊 Unigine Superpos.", "https://benchmark.unigine.com/superposition"),
            ("⚡ FurMark", "https://geeks3d.com/furmark/"),
            ("🔍 Prime95", "https://www.mersenne.org/download/"),
            ("📈 AIDA64", "https://www.aida64.com/"),
            ("💾 MemTest86", "https://www.memtest86.com/"),
            ("📊 MemTest64", "https://www.techpowerup.com/memtest64/"),
            ("⚡ OCCT", "https://www.ocbase.com/"),
            ("🔍 Intel Burn Test", "https://www.techspot.com/downloads/4965-intel-burn-test.html"),
            ("📈 LinX", "https://www.techpowerup.com/download/linx/"),
            ("💻 Y-Cruncher", "http://www.numberworld.org/y-cruncher/"),
            ("📊 Blender Bench", "https://opendata.blender.org/"),
            ("⚡ V-Ray Bench", "https://www.chaos.com/vray/benchmark"),
            ("🔍 Basemark GPU", "https://www.basemark.com/products/basemark-gpu/"),
            ("📈 GFXBench", "https://gfxbench.com/"),
            ("💾 ADATA SSD Toolbox", "https://www.adata.com/us/ss/software-5/"),
            ("📦 Samsung Magician", "https://www.samsung.com/semiconductor/minisite/ssd/product/consumer/magician/"),
            ("⚡ WD Dashboard", "https://support.wdc.com/downloads.aspx"),
            ("🔍 Crucial SE", "https://www.crucial.com/support/storage-executive"),
            ("📈 NovaBench", "https://novabench.com/"),
            ("💻 CPU Monkey", "https://www.cpu-monkey.com/"),
            ("📊 GPU Check", "https://www.gpucheck.com/"),
            ("⚡ CPU-World", "http://www.cpu-world.com/"),
            ("🔍 TechPowerUp", "https://www.techpowerup.com/"),
        ]
        self.create_section("BENCHMARK & TESTS", "📊", buttons_data, is_web=True)


    def create_utilitaires_systeme_section(self):
        """Section Utilitaires Système Windows - 40+ outils"""
        buttons_data = [
            # PowerToys & Utilitaires Microsoft
            ("⚡ PowerToys", "https://github.com/microsoft/PowerToys/releases"),
            ("🔍 Everything", "https://www.voidtools.com/"),
            ("👁️ QuickLook", "https://github.com/QL-Win/QuickLook/releases"),
            ("📸 ShareX", "https://getsharex.com/"),
            ("🎯 Greenshot", "https://getgreenshot.org/"),
            ("📷 Lightshot", "https://app.prntscr.com/"),

            # Compression
            ("📦 7-Zip", "https://www.7-zip.org/"),
            ("🗜️ WinRAR", "https://www.win-rar.com/"),
            ("📦 PeaZip", "https://peazip.github.io/"),
            ("🗜️ Bandizip", "https://www.bandisoft.com/bandizip/"),

            # Éditeurs Texte
            ("📝 Notepad++", "https://notepad-plus-plus.org/"),
            ("⚡ Sublime Text", "https://www.sublimetext.com/"),
            ("💻 VS Code", "https://code.visualstudio.com/"),
            ("📝 Atom", "https://atom.io/"),
            ("✍️ Typora", "https://typora.io/"),

            # Automation
            ("⚡ AutoHotkey", "https://www.autohotkey.com/"),
            ("🎨 Rainmeter", "https://www.rainmeter.net/"),
            ("🔧 WinAutomation", "https://www.winautomation.com/"),

            # Gestionnaires Fichiers
            ("📁 Total Commander", "https://www.ghisler.com/"),
            ("🗂️ FreeCommander", "https://freecommander.com/"),
            ("📂 XYplorer", "https://www.xyplorer.com/"),
            ("🗃️ Directory Opus", "https://www.gpsoft.com.au/"),

            # Utilities diverses
            ("🖱️ X-Mouse Button", "https://www.highrez.co.uk/downloads/XMouseButtonControl.htm"),
            ("⌨️ SharpKeys", "https://github.com/randyrants/sharpkeys/releases"),
            ("🎯 WinDirStat", "https://windirstat.net/"),
            ("📊 SpaceSniffer", "http://www.uderzo.it/main_products/space_sniffer/"),
            ("🔍 Agent Ransack", "https://www.mythicsoft.com/agentransack/"),
            ("🗂️ DropIt", "http://www.dropitproject.com/"),
            ("⏰ f.lux", "https://justgetflux.com/"),
            ("💡 Clover", "http://en.ejie.me/"),

            # Lanceurs d'applications
            ("🚀 Launchy", "https://www.launchy.net/"),
            ("⚡ Wox", "http://www.wox.one/"),
            ("🎯 Keypirinha", "https://keypirinha.com/"),

            # Clipboard Managers
            ("📋 Ditto", "https://ditto-cp.sourceforge.io/"),
            ("📝 ClipClip", "https://clipclip.com/"),
            ("⚡ CopyQ", "https://hluk.github.io/CopyQ/"),

            # Window Management
            ("🪟 FancyZones", "https://learn.microsoft.com/windows/powertoys/fancyzones"),
            ("📐 AquaSnap", "https://www.nurgo-software.com/products/aquasnap"),
            ("🎯 DisplayFusion", "https://www.displayfusion.com/"),
        ]
        self.create_section("UTILITAIRES SYSTÈME", "🛠️", buttons_data, is_web=True)

    def create_multimedia_section(self):
        """Section Multimédia & Création - 50+ logiciels"""
        buttons_data = [
            # Lecteurs Multimé dia
            ("🎬 VLC Media Player", "https://www.videolan.org/vlc/"),
            ("▶️ MPC-HC", "https://mpc-hc.org/"),
            ("🎥 PotPlayer", "https://potplayer.daum.net/"),
            ("📺 Kodi", "https://kodi.tv/"),
            ("🎞️ MPV", "https://mpv.io/"),

            # Montage Vidéo
            ("🎬 OBS Studio", "https://obsproject.com/"),
            ("📹 XSplit", "https://www.xsplit.com/"),
            ("🎥 vMix", "https://www.vmix.com/"),
            ("✂️ DaVinci Resolve", "https://www.blackmagicdesign.com/products/davinciresolve"),
            ("🎞️ Kdenlive", "https://kdenlive.org/"),
            ("📽️ OpenShot", "https://www.openshot.org/"),
            ("🎬 Shotcut", "https://www.shotcut.org/"),
            ("📹 HitFilm Express", "https://fxhome.com/hitfilm-express"),

            # 3D & Modélisation
            ("🎨 Blender", "https://www.blender.org/"),
            ("🏗️ SketchUp", "https://www.sketchup.com/"),
            ("📐 FreeCAD", "https://www.freecadweb.org/"),
            ("🎯 Meshmixer", "https://www.meshmixer.com/"),

            # Graphisme & Design
            ("🎨 Inkscape", "https://inkscape.org/"),
            ("🖌️ Krita", "https://krita.org/"),
            ("🎨 GIMP", "https://www.gimp.org/"),
            ("🖼️ Paint.NET", "https://www.getpaint.net/"),
            ("📐 Figma", "https://www.figma.com/downloads/"),
            ("🎯 Canva", "https://www.canva.com/"),

            # Audio
            ("🎵 Audacity", "https://www.audacityteam.org/"),
            ("🎼 Reaper", "https://www.reaper.fm/"),
            ("🎹 FL Studio", "https://www.image-line.com/fl-studio/"),
            ("🎧 Ableton Live", "https://www.ableton.com/live/"),
            ("🎚️ Ardour", "https://ardour.org/"),
            ("🎵 Ocenaudio", "https://www.ocenaudio.com/"),

            # DJ & Mix
            ("🎧 VirtualDJ", "https://www.virtualdj.com/"),
            ("🎛️ Traktor", "https://www.native-instruments.com/traktor/"),
            ("🎵 Serato DJ", "https://serato.com/"),
            ("🎚️ Mixxx", "https://www.mixxx.org/"),

            # Conversion & Encodage
            ("🔄 HandBrake", "https://handbrake.fr/"),
            ("⚡ FFmpeg", "https://ffmpeg.org/"),
            ("🎬 Format Factory", "http://www.pcfreetime.com/formatfactory/"),
            ("📹 MediaCoder", "https://www.mediacoderhq.com/"),
            ("🎞️ MKVToolNix", "https://mkvtoolnix.download/"),

            # Streaming
            ("📡 Streamlabs OBS", "https://streamlabs.com/"),
            ("🎥 Restream", "https://restream.io/"),
            ("📹 vMix", "https://www.vmix.com/"),

            # Photo
            ("📷 Darktable", "https://www.darktable.org/"),
            ("🖼️ RawTherapee", "https://www.rawtherapee.com/"),
            ("📸 digiKam", "https://www.digikam.org/"),
            ("🎨 Photopea", "https://www.photopea.com/"),

            # Utilitaires Média
            ("🎵 MusicBee", "https://getmusicbee.com/"),
            ("📻 Spotify", "https://www.spotify.com/download/"),
            ("🎼 foobar2000", "https://www.foobar2000.org/"),
        ]
        self.create_section("MULTIMÉDIA & CRÉATION", "🎬", buttons_data, is_web=True)

    def create_bureautique_section(self):
        """Section Bureautique & Productivité - 40+ outils"""
        buttons_data = [
            # Suite Office
            ("📦 LibreOffice", "https://www.libreoffice.org/"),
            ("📄 OpenOffice", "https://www.openoffice.org/"),
            ("☁️ Google Workspace", "https://workspace.google.com/"),
            ("📊 OnlyOffice", "https://www.onlyoffice.com/"),
            ("📝 WPS Office", "https://www.wps.com/"),

            # Notes & PKM
            ("📓 Notion", "https://www.notion.so/"),
            ("🗒️ Obsidian", "https://obsidian.md/"),
            ("📔 OneNote", "https://www.onenote.com/"),
            ("📝 Evernote", "https://evernote.com/"),
            ("🗂️ Joplin", "https://joplinapp.org/"),
            ("✍️ Typora", "https://typora.io/"),
            ("📓 Logseq", "https://logseq.com/"),

            # Todo & Task Management
            ("✅ Todoist", "https://todoist.com/"),
            ("📋 TickTick", "https://ticktick.com/"),
            ("✔️ Any.do", "https://www.any.do/"),
            ("📝 Microsoft To Do", "https://to-do.microsoft.com/"),
            ("🎯 Trello", "https://trello.com/"),
            ("📊 Asana", "https://asana.com/"),
            ("🗂️ Monday.com", "https://monday.com/"),

            # Time Tracking
            ("⏱️ Toggl Track", "https://toggl.com/track/"),
            ("⏰ RescueTime", "https://www.rescuetime.com/"),
            ("🕐 Clockify", "https://clockify.me/"),
            ("⏲️ Harvest", "https://www.getharvest.com/"),

            # Communication
            ("💬 Slack", "https://slack.com/downloads/"),
            ("👥 Microsoft Teams", "https://www.microsoft.com/teams/"),
            ("📹 Zoom", "https://zoom.us/download"),
            ("🎥 Google Meet", "https://meet.google.com/"),
            ("📞 Webex", "https://www.webex.com/downloads.html"),
            ("💬 Discord", "https://discord.com/download"),
            ("🗨️ Mattermost", "https://mattermost.com/"),
            ("🚀 Rocket.Chat", "https://rocket.chat/"),

            # PDF
            ("📄 PDF24", "https://tools.pdf24.org/"),
            ("📋 PDFtk", "https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/"),
            ("📝 PDF-XChange", "https://www.tracker-software.com/product/pdf-xchange-editor"),
            ("📄 Foxit Reader", "https://www.foxit.com/pdf-reader/"),
            ("📋 Sumatra PDF", "https://www.sumatrapdfreader.org/"),

            # Calendrier
            ("📅 Google Calendar", "https://calendar.google.com/"),
            ("📆 Outlook", "https://outlook.com/"),
            ("🗓️ Thunderbird", "https://www.thunderbird.net/"),

            # Mind Mapping
            ("🧠 XMind", "https://www.xmind.net/"),
            ("🗺️ FreeMind", "http://freemind.sourceforge.net/"),
            ("💭 MindMeister", "https://www.mindmeister.com/"),
        ]
        self.create_section("BUREAUTIQUE & PRODUCTIVITÉ", "📄", buttons_data, is_web=True)

    def create_developpement_web_section(self):
        """Section Développement Web & Programming - 40+ outils"""
        buttons_data = [
            # IDEs & Editeurs
            ("💻 VS Code", "https://code.visualstudio.com/"),
            ("⚡ Sublime Text", "https://www.sublimetext.com/"),
            ("🎯 Atom", "https://atom.io/"),
            ("📝 Notepad++", "https://notepad-plus-plus.org/"),
            ("🔧 WebStorm", "https://www.jetbrains.com/webstorm/"),
            ("💼 PhpStorm", "https://www.jetbrains.com/phpstorm/"),
            ("🎨 PyCharm", "https://www.jetbrains.com/pycharm/"),
            ("☕ IntelliJ IDEA", "https://www.jetbrains.com/idea/"),

            # Git & Version Control
            ("🐙 GitHub Desktop", "https://desktop.github.com/"),
            ("🦊 GitKraken", "https://www.gitkraken.com/"),
            ("🌿 SourceTree", "https://www.sourcetreeapp.com/"),
            ("🔧 TortoiseGit", "https://tortoisegit.org/"),

            # Serveurs Locaux
            ("📦 XAMPP", "https://www.apachefriends.org/"),
            ("⚡ WAMP", "https://www.wampserver.com/"),
            ("🎯 Laragon", "https://laragon.org/"),
            ("💼 MAMP", "https://www.mamp.info/"),

            # Bases de Données
            ("🐬 MySQL Workbench", "https://www.mysql.com/products/workbench/"),
            ("🐘 pgAdmin", "https://www.pgadmin.org/"),
            ("📊 DBeaver", "https://dbeaver.io/"),
            ("💾 HeidiSQL", "https://www.heidisql.com/"),

            # API Testing
            ("📡 Postman", "https://www.postman.com/downloads/"),
            ("⚡ Insomnia", "https://insomnia.rest/"),
            ("🔧 Hoppscotch", "https://hoppscotch.io/"),
            ("📋 Thunder Client", "https://www.thunderclient.com/"),

            # Docker & Containers
            ("🐳 Docker Desktop", "https://www.docker.com/products/docker-desktop"),
            ("☸️ Kubernetes", "https://kubernetes.io/"),
            ("📦 Podman", "https://podman.io/"),

            # Terminal
            ("💻 Windows Terminal", "https://apps.microsoft.com/detail/9N0DX20HK701"),
            ("⚡ Cmder", "https://cmder.app/"),
            ("🔧 ConEmu", "https://conemu.github.io/"),
            ("🎯 Hyper", "https://hyper.is/"),

            # FTP/SFTP
            ("📁 FileZilla", "https://filezilla-project.org/"),
            ("🌐 WinSCP", "https://winscp.net/"),
            ("📦 Cyberduck", "https://cyberduck.io/"),

            # Node.js & Package Managers
            ("🟢 Node.js", "https://nodejs.org/"),
            ("📦 npm", "https://www.npmjs.com/"),
            ("⚡ Yarn", "https://yarnpkg.com/"),
            ("🎯 pnpm", "https://pnpm.io/"),

            # Python
            ("🐍 Python", "https://www.python.org/downloads/"),
            ("📦 Anaconda", "https://www.anaconda.com/products/distribution"),
            ("🎯 PyPI", "https://pypi.org/"),

            # Documentation
            ("📚 DevDocs", "https://devdocs.io/"),
            ("💡 MDN Web Docs", "https://developer.mozilla.org/"),
            ("📖 W3Schools", "https://www.w3schools.com/"),
            ("🔍 Stack Overflow", "https://stackoverflow.com/"),
        ]
        self.create_section("DÉVELOPPEMENT WEB", "💻", buttons_data, is_web=True)
    def create_depannage_section(self):
        """Section Dépannage à Distance"""
        buttons_data = [
            ("💻 TeamViewer", "https://www.teamviewer.com/"),
            ("🖥️ AnyDesk", "https://anydesk.com/"),
            ("🌐 Chrome Remote", "https://remotedesktop.google.com/"),
            ("⚡ RustDesk", "https://rustdesk.com/"),
            ("🔧 TightVNC", "https://www.tightvnc.com/"),
            ("💼 UltraVNC", "https://uvnc.com/"),
            ("🎯 RealVNC", "https://www.realvnc.com/"),
            ("📡 Ammyy Admin", "https://www.ammyy.com/"),
            ("🌐 Splashtop", "https://www.splashtop.com/"),
            ("⚡ Parsec", "https://parsec.app/"),
            ("🔧 Moonlight", "https://moonlight-stream.org/"),
            ("💻 Remmina", "https://remmina.org/"),
            ("🖥️ NoMachine", "https://www.nomachine.com/"),
            ("📦 Supremo", "https://www.supremocontrol.com/"),
        ]
        self.create_section("DÉPANNAGE À DISTANCE", "🖥️", buttons_data, is_web=True)

    def create_drivers_section(self):
        """Section Drivers & Pilotes"""
        buttons_data = [
            ("🔧 Snappy Driver", "https://www.snappy-driver-installer.org/"),
            ("⚡ Driver Booster", "https://www.iobit.com/driver-booster.php"),
            ("💻 Driver Easy", "https://www.drivereasy.com/"),
            ("🎯 DriverPack", "https://drp.su/"),
            ("🔍 Driver Genius", "https://www.driver-soft.com/"),
            ("📦 NVIDIA Drivers", "https://www.nvidia.com/download/index.aspx"),
            ("🔴 AMD Drivers", "https://www.amd.com/support"),
            ("🎯 Intel Drivers", "https://www.intel.com/content/www/us/en/download-center/home.html"),
            ("💻 Dell Drivers", "https://www.dell.com/support/home/"),
            ("🖥️ HP Drivers", "https://support.hp.com/drivers"),
            ("📱 Lenovo Drivers", "https://support.lenovo.com/solutions/ht003029"),
            ("🎮 ASUS Drivers", "https://www.asus.com/support/download-center/"),
            ("⚡ MSI Drivers", "https://www.msi.com/support/download"),
            ("🔧 Realtek Drivers", "https://www.realtek.com/downloads/"),
        ]
        self.create_section("DRIVERS & PILOTES", "🔌", buttons_data, is_web=True)

    def create_documentation_section(self):
        """Section Documentation & Aide"""
        buttons_data = [
            ("📚 Microsoft Docs", "https://learn.microsoft.com/"),
            ("💻 Windows Tips", "https://support.microsoft.com/windows"),
            ("🔧 Sysinternals", "https://learn.microsoft.com/sysinternals/"),
            ("📖 SS64 CMD", "https://ss64.com/nt/"),
            ("⚡ PowerShell Docs", "https://learn.microsoft.com/powershell/"),
            ("🌐 TechNet", "https://technet.microsoft.com/"),
            ("📚 How-To Geek", "https://www.howtogeek.com/"),
            ("💡 Tom's Hardware", "https://www.tomshardware.com/"),
            ("🔍 Stack Overflow", "https://stackoverflow.com/"),
            ("📖 Reddit r/techsupport", "https://www.reddit.com/r/techsupport/"),
            ("💻 Bleeping Computer", "https://www.bleepingcomputer.com/"),
            ("🔧 Ninite", "https://ninite.com/"),
            ("📚 AlternativeTo", "https://alternativeto.net/"),
            ("💡 CNET Download", "https://download.cnet.com/"),
            ("🌐 PortableApps", "https://portableapps.com/"),
        ]
        self.create_section("DOCUMENTATION & AIDE", "📚", buttons_data, is_web=True)
    def create_draggable_header(self, parent, title, section_name):
        """Crée un en-tête draggable pour réorganiser les sections"""
        header = tk.Frame(parent, bg=self.ACCENT_BLUE, cursor="hand2", height=30)  # Bleu foncé Ordi Plus
        
        label = tk.Label(
            header, 
            text=f"⋮⋮ {title}",
            bg=self.ACCENT_BLUE,  # Bleu foncé Ordi Plus
            fg="white",
            font=('Segoe UI', 9, 'bold'),
            pady=5
        )
        label.pack(fill="both", expand=True)
        
        # Bind drag events
        header.bind("<Button-1>", lambda e: self.start_drag(e, section_name))
        header.bind("<B1-Motion>", lambda e: self.on_drag(e, section_name))
        header.bind("<ButtonRelease-1>", lambda e: self.end_drag(e, section_name))
        
        label.bind("<Button-1>", lambda e: self.start_drag(e, section_name))
        label.bind("<B1-Motion>", lambda e: self.on_drag(e, section_name))
        label.bind("<ButtonRelease-1>", lambda e: self.end_drag(e, section_name))
        
        return header
    
    def start_drag(self, event, section_name):
        """Début du drag d'une section"""
        self.drag_data = {
            'section': section_name,
            'start_y': event.y_root,
            'original_index': self.sections_order.index(section_name)
        }
    
    def on_drag(self, event, section_name):
        """Pendant le drag"""
        if hasattr(self, 'drag_data'):
            delta_y = event.y_root - self.drag_data['start_y']
            # Visuel du drag (optionnel)
            pass
    
    def end_drag(self, event, section_name):
        """Fin du drag - réorganise les sections"""
        if not hasattr(self, 'drag_data'):
            return
        
        delta_y = event.y_root - self.drag_data['start_y']
        original_index = self.drag_data['original_index']
        
        # Calculer le nouvel index basé sur le déplacement
        # Chaque section fait environ 200px
        sections_moved = round(delta_y / 200)
        new_index = max(0, min(len(self.sections_order) - 1, original_index + sections_moved))
        
        if new_index != original_index:
            # Réorganiser l'ordre
            self.sections_order.pop(original_index)
            self.sections_order.insert(new_index, section_name)
            
            # Reconstruire le PanedWindow
            self.rebuild_tools_panel()
        
        del self.drag_data
    
    def rebuild_tools_panel(self):
        """Reconstruit le panneau d'outils avec le nouvel ordre"""
        # Retirer toutes les sections
        for child in self.tools_paned.panes():
            self.tools_paned.forget(child)
        
        # Réajouter dans le nouvel ordre
        for section_name in self.sections_order:
            if section_name in self.section_widgets:
                self.tools_paned.add(self.section_widgets[section_name])
    
    def open_manufacturer_support(self, url):
        """Ouvre le lien de support du fabricant dans le navigateur"""
        import webbrowser
        try:
            webbrowser.open(url)
            self.logger.info(f"✅ Ouverture du support fabricant: {url}")
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'ouverture du lien: {e}")
            messagebox.showerror(
                "Erreur",
                f"❌ Impossible d'ouvrir le lien:\n{e}"
            )
    
    def open_download_link(self, url):
        """Ouvre le lien de téléchargement dans le navigateur"""
        import webbrowser
        try:
            if url:
                webbrowser.open(url)
                self.logger.info(f"✅ Ouverture du lien de téléchargement: {url}")
                messagebox.showinfo(
                    "Téléchargement",
                    "Le lien de téléchargement a été ouvert dans votre navigateur.\n\n"
                    "Téléchargez l'outil et exécutez-le pour désinstaller proprement l'antivirus."
                )
            else:
                messagebox.showerror(
                    "Erreur",
                    "Aucun lien de téléchargement disponible pour cet outil."
                )
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'ouverture du lien: {e}")
            messagebox.showerror(
                "Erreur",
                f"❌ Impossible d'ouvrir le lien:\n{e}"
            )
    
    def execute_quick_command(self, command, admin_required=False):
        """Exécute une commande Windows rapidement (boutons d'accès rapide)"""
        import subprocess
        
        try:
            if admin_required:
                # Confirmation pour les commandes admin
                if not messagebox.askyesno(
                    "Droits administrateur requis",
                    f"Cette commande nécessite les droits administrateur:\n\n{command}\n\n"
                    "Voulez-vous continuer ?"
                ):
                    return
                
                # Exécuter en mode administrateur avec PowerShell - FENÊTRE VISIBLE
                ps_command = f'Start-Process cmd.exe -ArgumentList "/k {command}" -Verb RunAs'
                subprocess.Popen(
                    ["powershell.exe", "-Command", ps_command],
                    shell=True
                )
                self.logger.info(f"✅ Commande admin exécutée: {command}")
                
            else:
                # Exécuter normalement - FENÊTRE VISIBLE
                subprocess.Popen(
                    ["cmd.exe", "/k", command],
                    shell=True
                )
                self.logger.info(f"✅ Commande exécutée: {command}")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'exécution de la commande: {e}")
            messagebox.showerror(
                "Erreur",
                f"❌ Impossible d'exécuter la commande:\n{e}"
            )
    
    def open_organize_dialog(self):
        """Ouvre le dialogue d'organisation des programmes avec drag & drop"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 Organiser les programmes")
        dialog.geometry("900x700")
        dialog.configure(bg=self.DARK_BG)
        
        # Centrer la fenêtre
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Titre
        title_label = ttk.Label(
            main_frame,
            text="🔄 Organiser les programmes - Glissez-déposez entre les catégories",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 10))
        
        # Frame pour les deux listes côte à côte
        lists_frame = ttk.Frame(main_frame)
        lists_frame.pack(fill="both", expand=True)
        lists_frame.grid_columnconfigure(0, weight=1)
        lists_frame.grid_columnconfigure(1, weight=1)
        
        # Variables pour le drag & drop
        self.drag_data = {"source_cat": None, "program_name": None}
        
        # Frame gauche - Catégories et programmes
        left_frame = ttk.LabelFrame(lists_frame, text="📁 Catégories et Programmes", padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Sélecteur de catégorie
        cat_select_frame = ttk.Frame(left_frame)
        cat_select_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(cat_select_frame, text="Catégorie:").pack(side="left", padx=(0, 10))
        
        category_var = tk.StringVar()
        categories = sorted(self.programs.keys())
        category_combo = ttk.Combobox(cat_select_frame, textvariable=category_var, values=categories, state='readonly', width=30)
        category_combo.pack(side="left", fill="x", expand=True)
        
        # Liste des programmes de la catégorie sélectionnée
        programs_list = tk.Listbox(left_frame, bg=self.DARK_BG2, fg=self.DARK_FG, height=25, selectmode=tk.SINGLE)
        programs_list.pack(fill="both", expand=True)
        
        # Scrollbar pour la liste
        scrollbar_left = ttk.Scrollbar(left_frame, orient="vertical", command=programs_list.yview)
        scrollbar_left.pack(side="right", fill="y")
        programs_list.config(yscrollcommand=scrollbar_left.set)
        
        # Frame droit - Destination
        right_frame = ttk.LabelFrame(lists_frame, text="🎯 Déplacer vers la catégorie", padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Sélecteur de catégorie destination
        dest_cat_frame = ttk.Frame(right_frame)
        dest_cat_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(dest_cat_frame, text="Catégorie destination:").pack(side="left", padx=(0, 10))
        
        dest_category_var = tk.StringVar()
        dest_category_combo = ttk.Combobox(dest_cat_frame, textvariable=dest_category_var, values=categories, state='readonly', width=30)
        dest_category_combo.pack(side="left", fill="x", expand=True)
        
        # Zone d'information
        info_text = scrolledtext.ScrolledText(right_frame, bg=self.DARK_BG2, fg=self.DARK_FG, height=25, wrap=tk.WORD)
        info_text.pack(fill="both", expand=True)
        info_text.insert("1.0", "👆 Sélectionnez un programme à gauche\n📂 Choisissez une catégorie de destination\n✅ Cliquez sur 'Déplacer' pour transférer")
        info_text.config(state='disabled')
        
        # Fonction pour charger les programmes d'une catégorie
        def load_programs(event=None):
            programs_list.delete(0, tk.END)
            cat = category_var.get()
            if cat and cat in self.programs:
                for prog_name in sorted(self.programs[cat].keys()):
                    programs_list.insert(tk.END, prog_name)
        
        category_combo.bind("<<ComboboxSelected>>", load_programs)
        
        # Charger la première catégorie par défaut
        if categories:
            category_combo.current(0)
            load_programs()
        
        # Fonction de déplacement
        def move_program():
            selection = programs_list.curselection()
            if not selection:
                messagebox.showwarning("Sélection requise", "Veuillez sélectionner un programme à déplacer.")
                return
            
            source_cat = category_var.get()
            dest_cat = dest_category_var.get()
            program_name = programs_list.get(selection[0])
            
            if not dest_cat:
                messagebox.showwarning("Destination requise", "Veuillez sélectionner une catégorie de destination.")
                return
            
            if source_cat == dest_cat:
                messagebox.showinfo("Même catégorie", "Le programme est déjà dans cette catégorie.")
                return
            
            # Confirmation
            if not messagebox.askyesno("Confirmer", f"Déplacer '{program_name}'\nDe: {source_cat}\nVers: {dest_cat}\n\nContinuer?"):
                return
            
            try:
                # Charger programs.json
                import sys
                if getattr(sys, 'frozen', False):
                    base_path = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(sys.executable).parent
                else:
                    base_path = Path(__file__).parent.parent
                
                programs_file = base_path / 'data' / 'programs.json'
                with open(programs_file, 'r', encoding='utf-8') as f:
                    all_programs = json.load(f)
                
                # Déplacer le programme
                program_data = all_programs[source_cat].pop(program_name)
                
                if dest_cat not in all_programs:
                    all_programs[dest_cat] = {}
                
                all_programs[dest_cat][program_name] = program_data
                
                # Sauvegarder
                with open(programs_file, 'w', encoding='utf-8') as f:
                    json.dump(all_programs, f, indent=4, ensure_ascii=False)
                
                # Mettre à jour l'affichage
                self.programs = all_programs
                load_programs()
                
                messagebox.showinfo("Succès", f"✅ '{program_name}' déplacé vers '{dest_cat}'!\n\nRedémarrez l'application pour voir les changements.")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Erreur lors du déplacement:\n{e}")
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="➡️ Déplacer", command=move_program, style='Action.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="🔄 Rafraîchir", command=load_programs).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Fermer", command=dialog.destroy).pack(side="right", padx=5)
    
    def add_custom_program(self):
        """Permet d'ajouter un programme personnalisé via URL de téléchargement"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Ajouter un programme personnalisé")
        dialog.geometry("600x400")
        dialog.configure(bg=self.DARK_BG)
        dialog.resizable(False, False)
        
        # Centrer la fenêtre
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Titre
        title_label = ttk.Label(
            main_frame,
            text="➕ Ajouter un nouveau programme",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Nom du programme
        ttk.Label(main_frame, text="📝 Nom du programme:").pack(anchor="w", pady=(0, 5))
        name_entry = ttk.Entry(main_frame, width=60)
        name_entry.pack(fill="x", pady=(0, 15))
        
        # URL de téléchargement
        ttk.Label(main_frame, text="🔗 URL de téléchargement (.exe, .msi):").pack(anchor="w", pady=(0, 5))
        url_entry = ttk.Entry(main_frame, width=60)
        url_entry.pack(fill="x", pady=(0, 15))
        
        # Catégorie
        ttk.Label(main_frame, text="📁 Catégorie:").pack(anchor="w", pady=(0, 5))
        category_var = tk.StringVar(value="Utilitaires")
        categories = sorted(self.programs.keys())
        category_combo = ttk.Combobox(main_frame, textvariable=category_var, values=categories, width=57, state='readonly')
        category_combo.pack(fill="x", pady=(0, 15))
        
        # Description
        ttk.Label(main_frame, text="📄 Description (optionnelle):").pack(anchor="w", pady=(0, 5))
        desc_entry = ttk.Entry(main_frame, width=60)
        desc_entry.pack(fill="x", pady=(0, 20))
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        def save_program():
            name = name_entry.get().strip()
            url = url_entry.get().strip()
            category = category_var.get()
            description = desc_entry.get().strip() or name
            
            if not name or not url:
                messagebox.showwarning("Champs manquants", "Veuillez remplir le nom et l'URL du programme.")
                return
            
            if not url.startswith(('http://', 'https://')):
                messagebox.showwarning("URL invalide", "L'URL doit commencer par http:// ou https://")
                return
            
            # Ajouter le programme à programs.json
            try:
                import sys
                if getattr(sys, 'frozen', False):
                    base_path = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(sys.executable).parent
                else:
                    base_path = Path(__file__).parent.parent
                
                programs_file = base_path / 'data' / 'programs.json'
                with open(programs_file, 'r', encoding='utf-8') as f:
                    all_programs = json.load(f)
                
                # Créer l'entrée du programme
                program_entry = {
                    "name": name,
                    "description": description,
                    "url": url,
                    "installer_type": "direct",
                    "silent_args": "/S",
                    "essential": False
                }
                
                # Ajouter à la catégorie
                if category not in all_programs:
                    all_programs[category] = {}
                
                all_programs[category][name] = program_entry
                
                # Sauvegarder
                with open(programs_file, 'w', encoding='utf-8') as f:
                    json.dump(all_programs, f, indent=4, ensure_ascii=False)
                
                messagebox.showinfo("Succès", f"✅ Programme '{name}' ajouté avec succès!\n\nRedémarrez l'application pour voir les changements.")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Erreur lors de l'ajout:\n{e}")
        
        ttk.Button(button_frame, text="✅ Ajouter", command=save_program, style='Action.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Annuler", command=dialog.destroy).pack(side="left", padx=5)
    
    def on_closing(self):
        """Fermeture propre de l'application avec arrêt des processus enfants"""
        import sys
        import gc

        try:
            # Arrêter toute installation en cours
            if self.is_installing:
                if not messagebox.askyesno(
                    "Installation en cours",
                    "Une installation est en cours. Voulez-vous vraiment quitter?\n"
                    "Cela arrêtera tous les téléchargements et installations."
                ):
                    return

            # Afficher message d'arrêt des processus
            if hasattr(self, 'selection_label'):
                self.selection_label.config(text="⏹️ Arrêt des processus en cours...")
                self.root.update_idletasks()

            # Arrêter proprement tous les processus enfants avec psutil
            try:
                import psutil
                import os

                self.logger.info("🔴 Arrêt de tous les processus enfants...")

                # Obtenir le processus courant
                current_process = psutil.Process(os.getpid())

                # Obtenir tous les enfants (récursif)
                children = current_process.children(recursive=True)

                if children:
                    self.logger.info(f"📊 Trouvé {len(children)} processus enfant(s) à arrêter")

                    # Terminer poliment d'abord
                    for child in children:
                        try:
                            self.logger.info(f"⏹️ Arrêt du processus {child.pid} ({child.name()})")
                            child.terminate()
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            self.logger.warning(f"⚠️ Impossible d'arrêter {child.pid}: {e}")

                    # Attendre un peu (max 3 secondes)
                    gone, alive = psutil.wait_procs(children, timeout=3)

                    # Log des processus terminés
                    if gone:
                        self.logger.info(f"✅ {len(gone)} processus terminés proprement")

                    # Forcer les survivants
                    if alive:
                        self.logger.warning(f"⚠️ {len(alive)} processus nécessitent un arrêt forcé")
                        for child in alive:
                            try:
                                self.logger.warning(f"💥 Force kill du processus {child.pid}")
                                child.kill()
                            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                                self.logger.error(f"❌ Impossible de tuer {child.pid}: {e}")

                    self.logger.info("✅ Tous les processus enfants arrêtés")
                else:
                    self.logger.info("ℹ️ Aucun processus enfant à arrêter")

            except ImportError:
                self.logger.warning("⚠️ psutil non disponible - arrêt simple")
            except Exception as e:
                self.logger.error(f"❌ Erreur lors de l'arrêt des processus: {e}")

            # Fermer tous les logs
            logging.shutdown()

            # Nettoyer les références
            self.logger.info("🧹 Nettoyage des références...")
            if hasattr(self, 'program_vars'):
                self.program_vars.clear()
            if hasattr(self, 'programs'):
                self.programs.clear()
            if hasattr(self, 'category_frames'):
                self.category_frames.clear()
            if hasattr(self, 'category_widgets'):
                self.category_widgets.clear()
            if hasattr(self, 'section_frames'):
                self.section_frames.clear()
            if hasattr(self, 'section_titles'):
                self.section_titles.clear()
            if hasattr(self, 'all_buttons'):
                self.all_buttons.clear()

            # Forcer le garbage collector
            gc.collect()

            # Détruire la fenêtre
            self.logger.info("🚪 Fermeture de NiTriTe V5.0")
            self.root.quit()
            self.root.destroy()

            # Forcer la sortie
            sys.exit(0)

        except Exception as e:
            print(f"❌ Erreur lors de la fermeture: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(0)

    # ===============================================
    # MÉTHODES BASE DE DONNÉES PORTABLE
    # ===============================================
    
    def show_portable_database_stats(self):
        """Affiche les statistiques de la base de données portable"""
        from tkinter import messagebox, scrolledtext
        import tkinter as tk
        from tkinter import ttk
        
        if not self.installer_manager or not hasattr(self.installer_manager, 'portable_db') or not self.installer_manager.portable_db:
            messagebox.showinfo(
                "Base de données portable",
                "💾 La base de données portable n'est pas disponible.\n\n"
                "Elle sera créée automatiquement lors de l'installation d'applications portables."
            )
            return
        
        try:
            db = self.installer_manager.portable_db
            stats = db.get_statistics()
            categories = db.get_categories()
            
            # Créer une fenêtre de dialogue
            dialog = tk.Toplevel(self.root)
            dialog.title("💾 Base de Données Portable - Statistiques")
            dialog.geometry("700x600")
            dialog.configure(bg=self.DARK_BG)
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Frame principal
            main_frame = ttk.Frame(dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Titre
            title_label = tk.Label(
                main_frame,
                text="📊 STATISTIQUES BASE DE DONNÉES PORTABLE",
                font=('Segoe UI', 16, 'bold'),
                bg=self.DARK_BG,
                fg=self.ACCENT_ORANGE
            )
            title_label.pack(pady=(0, 20))
            
            # Frame pour les statistiques
            stats_frame = ttk.LabelFrame(main_frame, text=" 📈 Statistiques globales ", padding=15)
            stats_frame.pack(fill="x", pady=10)
            
            # Statistiques générales
            stats_text = f"""
📦 Applications totales : {stats.get('total_apps', 0)}
✅ Applications portables : {stats.get('portable_apps', 0)}
💿 Applications installées : {stats.get('installed_apps', 0)}
📁 Catégories : {len(categories)}

💾 ESPACE UTILISÉ :
   • Total : {stats.get('total_size_gb', 0):.2f} GB
   • Détails : {stats.get('total_size_mb', 0):.2f} MB
   • Octets : {stats.get('total_size_bytes', 0):,}
"""
            
            stats_label = tk.Label(
                stats_frame,
                text=stats_text,
                font=('Consolas', 10),
                bg=self.DARK_BG2,
                fg=self.DARK_FG,
                justify="left",
                anchor="w"
            )
            stats_label.pack(fill="x")
            
            # Frame pour les catégories
            cat_frame = ttk.LabelFrame(main_frame, text=" 📁 Applications par catégorie ", padding=15)
            cat_frame.pack(fill="both", expand=True, pady=10)
            
            # Créer un canvas avec scrollbar pour les catégories
            cat_canvas = tk.Canvas(cat_frame, bg=self.DARK_BG2, height=200)
            cat_scrollbar = ttk.Scrollbar(cat_frame, orient="vertical", command=cat_canvas.yview)
            cat_scrollable = ttk.Frame(cat_canvas)
            
            cat_scrollable.bind(
                "<Configure>",
                lambda e: cat_canvas.configure(scrollregion=cat_canvas.bbox("all"))
            )
            
            cat_canvas.create_window((0, 0), window=cat_scrollable, anchor="nw")
            cat_canvas.configure(yscrollcommand=cat_scrollbar.set)
            
            cat_canvas.pack(side="left", fill="both", expand=True)
            cat_scrollbar.pack(side="right", fill="y")
            
            # Afficher les catégories
            apps_by_cat = stats.get('apps_by_category', {})
            if apps_by_cat:
                for idx, (category, count) in enumerate(sorted(apps_by_cat.items(), key=lambda x: x[1], reverse=True)):
                    cat_label = tk.Label(
                        cat_scrollable,
                        text=f"  • {category}: {count} app(s)",
                        font=('Consolas', 9),
                        bg=self.DARK_BG2,
                        fg=self.DARK_FG2,
                        anchor="w"
                    )
                    cat_label.pack(fill="x", pady=2)
            else:
                no_cat_label = tk.Label(
                    cat_scrollable,
                    text="Aucune catégorie pour le moment",
                    font=('Consolas', 9),
                    bg=self.DARK_BG2,
                    fg=self.ACCENT_YELLOW,
                    anchor="w"
                )
                no_cat_label.pack(fill="x", pady=2)
            
            # Boutons d'action
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=(20, 0))
            
            ttk.Button(
                button_frame,
                text="🔍 Voir toutes les apps",
                command=lambda: self.show_all_portable_apps(dialog),
                style='Action.TButton'
            ).pack(side="left", padx=5)
            
            ttk.Button(
                button_frame,
                text="🔐 Vérifier intégrité",
                command=lambda: self.verify_database_integrity(dialog)
            ).pack(side="left", padx=5)
            
            ttk.Button(
                button_frame,
                text="📤 Exporter JSON",
                command=lambda: self.export_database_json(dialog)
            ).pack(side="left", padx=5)
            
            ttk.Button(
                button_frame,
                text="❌ Fermer",
                command=dialog.destroy
            ).pack(side="right", padx=5)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'affichage des statistiques: {e}")
            messagebox.showerror(
                "Erreur",
                f"❌ Impossible d'afficher les statistiques:\n\n{e}"
            )

    def show_all_portable_apps(self, parent_dialog=None):
        """Affiche toutes les applications portables de la base de données"""
        from tkinter import scrolledtext
        import tkinter as tk
        from tkinter import ttk
        
        if not self.installer_manager or not self.installer_manager.portable_db:
            return
        
        try:
            db = self.installer_manager.portable_db
            apps = db.list_applications(portable_only=True)
            
            # Créer une fenêtre
            dialog = tk.Toplevel(parent_dialog or self.root)
            dialog.title(f"📦 Applications Portables ({len(apps)})")
            dialog.geometry("900x600")
            dialog.configure(bg=self.DARK_BG)
            
            # Frame principal
            main_frame = ttk.Frame(dialog)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Titre
            title_label = tk.Label(
                main_frame,
                text=f"📦 {len(apps)} APPLICATIONS PORTABLES",
                font=('Segoe UI', 14, 'bold'),
                bg=self.DARK_BG,
                fg=self.ACCENT_GREEN
            )
            title_label.pack(pady=(0, 10))
            
            # Zone de texte avec scrollbar
            text_frame = ttk.Frame(main_frame)
            text_frame.pack(fill="both", expand=True)
            
            text_widget = scrolledtext.ScrolledText(
                text_frame,
                font=('Consolas', 9),
                bg=self.DARK_BG2,
                fg=self.DARK_FG,
                wrap="word"
            )
            text_widget.pack(fill="both", expand=True)
            
            # Afficher les applications
            for app in apps:
                text_widget.insert("end", f"📦 {app['name']}\n", "app_name")
                text_widget.insert("end", f"   Catégorie: {app.get('category', 'N/A')}\n")
                text_widget.insert("end", f"   Description: {app.get('description', 'N/A')}\n")
                text_widget.insert("end", f"   Version: {app.get('version', 'N/A')}\n")
                text_widget.insert("end", f"   Chemin: {app.get('executable_path', 'N/A')}\n")
                size_mb = app.get('file_size', 0) / 1024 / 1024 if app.get('file_size') else 0
                text_widget.insert("end", f"   Taille: {size_mb:.2f} MB\n")
                text_widget.insert("end", "\n" + "-"*80 + "\n\n")
            
            text_widget.configure(state="disabled")
            
            # Bouton fermer
            ttk.Button(
                main_frame,
                text="❌ Fermer",
                command=dialog.destroy
            ).pack(pady=(10, 0))
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'affichage des apps: {e}")
            messagebox.showerror("Erreur", f"❌ Erreur:\n{e}")

    def verify_database_integrity(self, parent_dialog=None):
        """Vérifie l'intégrité de la base de données"""
        from tkinter import messagebox, scrolledtext
        import tkinter as tk
        from tkinter import ttk
        
        if not self.installer_manager or not self.installer_manager.portable_db:
            return
        
        try:
            db = self.installer_manager.portable_db
            issues = db.verify_integrity()
            
            if not issues:
                messagebox.showinfo(
                    "Vérification d'intégrité",
                    "✅ AUCUN PROBLÈME DÉTECTÉ\n\n"
                    "La base de données est intègre.\n"
                    "Tous les fichiers sont présents et non modifiés."
                )
            else:
                # Créer une fenêtre pour afficher les problèmes
                dialog = tk.Toplevel(parent_dialog or self.root)
                dialog.title(f"⚠️ Problèmes détectés ({len(issues)})")
                dialog.geometry("700x400")
                dialog.configure(bg=self.DARK_BG)
                
                main_frame = ttk.Frame(dialog)
                main_frame.pack(fill="both", expand=True, padx=10, pady=10)
                
                title_label = tk.Label(
                    main_frame,
                    text=f"⚠️ {len(issues)} PROBLÈME(S) DÉTECTÉ(S)",
                    font=('Segoe UI', 12, 'bold'),
                    bg=self.DARK_BG,
                    fg=self.ACCENT_RED
                )
                title_label.pack(pady=(0, 10))
                
                text_widget = scrolledtext.ScrolledText(
                    main_frame,
                    font=('Consolas', 9),
                    bg=self.DARK_BG2,
                    fg=self.DARK_FG
                )
                text_widget.pack(fill="both", expand=True)
                
                for issue in issues:
                    text_widget.insert("end", f"⚠️ {issue['app']}\n", "app_name")
                    text_widget.insert("end", f"   Problème: {issue['issue']}\n")
                    text_widget.insert("end", f"   Chemin: {issue['path']}\n\n")
                
                text_widget.configure(state="disabled")
                
                ttk.Button(main_frame, text="❌ Fermer", command=dialog.destroy).pack(pady=(10, 0))
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification: {e}")
            messagebox.showerror("Erreur", f"❌ Erreur:\n{e}")

    def export_database_json(self, parent_dialog=None):
        """Exporte la base de données vers un fichier JSON"""
        from tkinter import messagebox, filedialog
        from datetime import datetime
        
        if not self.installer_manager or not self.installer_manager.portable_db:
            return
        
        try:
            # Demander où sauvegarder
            default_name = f"portable_apps_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filename = filedialog.asksaveasfilename(
                parent=parent_dialog or self.root,
                title="Exporter la base de données",
                defaultextension=".json",
                initialfile=default_name,
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                db = self.installer_manager.portable_db
                success = db.export_to_json(filename)
                
                if success:
                    messagebox.showinfo(
                        "Export réussi",
                        f"✅ Base de données exportée avec succès!\n\n"
                        f"Fichier: {filename}"
                    )
                else:
                    messagebox.showerror(
                        "Erreur d'export",
                        "❌ Impossible d'exporter la base de données."
                    )
        except Exception as e:
            self.logger.error(f"Erreur lors de l'export: {e}")
            messagebox.showerror("Erreur", f"❌ Erreur:\n{e}")


def create_gui_manager(root, installer_manager=None, config_manager=None):
    """Crée et retourne le GUI Manager complet"""
    return NiTriteGUIComplet(root, installer_manager, config_manager)
