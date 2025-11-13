"""
Interface graphique NiTrite v2 avec support Winget
Mode sombre élégant avec installation via Winget
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from threading import Thread
from typing import Dict, List
from src.winget_manager import WingetManager

logger = logging.getLogger(__name__)


class NiTriteWingetGUI:
    """Interface graphique avec support Winget"""
    
    # Palette de couleurs sombre (VS Code inspired)
    COLORS = {
        'bg_primary': '#1e1e1e',
        'bg_secondary': '#252526',
        'bg_tertiary': '#2d2d30',
        'fg_primary': '#d4d4d4',
        'fg_secondary': '#969696',
        'accent_blue': '#007acc',
        'accent_green': '#4ec9b0',
        'accent_orange': '#ce9178',
        'accent_red': '#f48771',
        'border': '#3e3e42',
    }
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.winget_manager = WingetManager()
        self.programs = self.winget_manager.get_all_programs()
        self.checkboxes: Dict[str, tk.BooleanVar] = {}
        self.installation_completed = False  # Track si des installations ont été faites
        self.programs_installed_count = 0    # Nombre de programmes installés
        
        self._setup_window()
        self._apply_dark_theme()
        self._create_widgets()
        self._setup_close_handler()
        
        logger.info(f"✅ {self.winget_manager.get_program_count()} programmes chargés via Winget")
    
    def _setup_window(self):
        """Configure la fenêtre principale"""
        self.root.title("🌙 NiTrite v2 - Installation via Winget")
        self.root.configure(bg=self.COLORS['bg_primary'])
        
        # Taille et positionnement
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(1400, screen_width - 100)
        window_height = min(900, screen_height - 100)
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _apply_dark_theme(self):
        """Applique le thème sombre"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuration des styles
        style.configure('Dark.TFrame', background=self.COLORS['bg_primary'])
        style.configure('Secondary.TFrame', background=self.COLORS['bg_secondary'])
        
        style.configure(
            'Dark.TLabel',
            background=self.COLORS['bg_primary'],
            foreground=self.COLORS['fg_primary'],
            font=('Segoe UI', 10)
        )
        
        style.configure(
            'Title.TLabel',
            background=self.COLORS['bg_primary'],
            foreground=self.COLORS['accent_blue'],
            font=('Segoe UI', 14, 'bold')
        )
        
        style.configure(
            'Category.TLabel',
            background=self.COLORS['bg_secondary'],
            foreground=self.COLORS['accent_green'],
            font=('Segoe UI', 11, 'bold')
        )
        
        # Style spécial pour Outils OrdiPlus (orange vif)
        style.configure(
            'OrdiPlus.TLabel',
            background=self.COLORS['bg_secondary'],
            foreground='#FF6600',  # Orange vif
            font=('Segoe UI', 12, 'bold')
        )
        
        # Style pour Réparation Windows
        style.configure(
            'Repair.TLabel',
            background=self.COLORS['bg_secondary'],
            foreground='#FFD700',  # Or
            font=('Segoe UI', 11, 'bold')
        )
        
        # Style pour Paramètres Windows
        style.configure(
            'Settings.TLabel',
            background=self.COLORS['bg_secondary'],
            foreground='#00D4FF',  # Cyan/Bleu clair
            font=('Segoe UI', 11, 'bold')
        )
        
        style.configure(
            'Dark.TCheckbutton',
            background=self.COLORS['bg_secondary'],
            foreground=self.COLORS['fg_primary'],
            font=('Segoe UI', 9)
        )
        
        style.map(
            'Dark.TCheckbutton',
            background=[('active', self.COLORS['bg_tertiary'])]
        )
        
        style.configure(
            'Accent.TButton',
            background=self.COLORS['accent_blue'],
            foreground='white',
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0,
            focuscolor='none'
        )
        
        style.map(
            'Accent.TButton',
            background=[('active', '#005a9e')]
        )
        
        style.configure(
            'Dark.Horizontal.TProgressbar',
            background=self.COLORS['accent_green'],
            troughcolor=self.COLORS['bg_tertiary'],
            borderwidth=0,
            thickness=25
        )
    
    def _create_widgets(self):
        """Crée les widgets de l'interface"""
        # Container principal
        main_container = ttk.Frame(self.root, style='Dark.TFrame', padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # En-tête
        self._create_header(main_container)
        
        # Zone de programmes avec défilement
        programs_frame = self._create_scrollable_programs(main_container)
        programs_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        
        # Zone inférieure (boutons + progression)
        self._create_footer(main_container)
    
    def _create_header(self, parent):
        """Crée l'en-tête"""
        header = ttk.Frame(parent, style='Dark.TFrame')
        header.pack(fill=tk.X, pady=(0, 15))
        
        # Titre
        title = ttk.Label(
            header,
            text="🌙 NiTrite v2 - Installation via Winget",
            style='Title.TLabel'
        )
        title.pack(side=tk.LEFT)
        
        # Info Winget
        winget_status = "✅ Winget disponible" if self.winget_manager.winget_available else "❌ Winget non disponible"
        winget_label = ttk.Label(
            header,
            text=f"{winget_status} | {self.winget_manager.get_program_count()} programmes",
            style='Dark.TLabel'
        )
        winget_label.pack(side=tk.RIGHT)
    
    def _create_scrollable_programs(self, parent) -> ttk.Frame:
        """Crée la zone de programmes avec défilement"""
        # Frame conteneur
        container = ttk.Frame(parent, style='Secondary.TFrame')
        
        # Canvas pour le défilement
        canvas = tk.Canvas(
            container,
            bg=self.COLORS['bg_secondary'],
            highlightthickness=0
        )
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        
        # Frame scrollable
        scrollable_frame = ttk.Frame(canvas, style='Secondary.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Remplir avec les programmes
        self._populate_programs(scrollable_frame)
        
        # Placement
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Défilement à la molette
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return container
    
    def _populate_programs(self, parent):
        """Remplit la liste des programmes par catégorie"""
        for category_name, programs in self.programs.items():
            # Frame de catégorie
            category_frame = ttk.Frame(parent, style='Secondary.TFrame')
            category_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # En-tête de catégorie (cliquable pour expand/collapse)
            header_frame = ttk.Frame(category_frame, style='Secondary.TFrame')
            header_frame.pack(fill=tk.X, pady=(5, 5))
            
            # Variable pour suivre l'état expand/collapse
            is_expanded = tk.BooleanVar(value=True)
            
            # Déterminer le style en fonction de la catégorie
            if category_name == "Outils OrdiPlus":
                label_style = 'OrdiPlus.TLabel'
            elif "Réparation" in category_name or "🔧" in category_name:
                label_style = 'Repair.TLabel'
            elif "Paramètres" in category_name or "⚙️" in category_name:
                label_style = 'Settings.TLabel'
            else:
                label_style = 'Category.TLabel'
            
            # Label de catégorie
            category_label = ttk.Label(
                header_frame,
                text=f"▼ {category_name} ({len(programs)} programmes)",
                style=label_style,
                cursor='hand2'
            )
            category_label.pack(side=tk.LEFT)
            
            # Frame pour les programmes
            programs_container = ttk.Frame(category_frame, style='Secondary.TFrame')
            programs_container.pack(fill=tk.X, padx=20)
            
            # Toggle function
            def toggle_category(e, container=programs_container, label=category_label, 
                              expanded=is_expanded, cat=category_name, count=len(programs)):
                if expanded.get():
                    container.pack_forget()
                    label.config(text=f"▶ {cat} ({count} programmes)")
                    expanded.set(False)
                else:
                    container.pack(fill=tk.X, padx=20)
                    label.config(text=f"▼ {cat} ({count} programmes)")
                    expanded.set(True)
            
            category_label.bind("<Button-1>", toggle_category)
            
            # Vérifier si c'est une catégorie de commandes système
            is_system_category = any('command' in prog for prog in programs.values())
            
            if is_system_category:
                # Pour les commandes système : afficher des boutons "Ouvrir/Exécuter"
                row = 0
                for program_name, program_info in sorted(programs.items()):
                    # Frame pour chaque commande
                    cmd_frame = ttk.Frame(programs_container, style='Secondary.TFrame')
                    cmd_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W+tk.E, padx=10, pady=3)
                    
                    # Label avec le nom
                    name_label = ttk.Label(
                        cmd_frame,
                        text=program_name,
                        style='Status.TLabel',
                        width=35
                    )
                    name_label.pack(side=tk.LEFT, padx=(0, 10))
                    
                    # Description
                    desc_label = ttk.Label(
                        cmd_frame,
                        text=program_info.get('description', ''),
                        foreground=self.COLORS['fg_secondary'],
                        background=self.COLORS['bg_secondary'],
                        font=('Segoe UI', 8)
                    )
                    desc_label.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
                    
                    # Bouton pour exécuter la commande
                    is_repair = "Réparation" in category_name or "DISM" in program_name or "SFC" in program_name
                    btn_text = "📋 Exécuter" if is_repair else "⚙️ Ouvrir"
                    btn_color = '#FFD700' if is_repair else '#00D4FF'
                    
                    exec_btn = tk.Button(
                        cmd_frame,
                        text=btn_text,
                        command=lambda name=program_name, is_rep=is_repair: self._execute_system_command(name, is_rep),
                        bg=btn_color,
                        fg='#000000',
                        font=('Segoe UI', 9, 'bold'),
                        cursor='hand2',
                        relief=tk.RAISED,
                        borderwidth=2,
                        padx=15,
                        pady=5
                    )
                    exec_btn.pack(side=tk.RIGHT)
                    
                    row += 1
            else:
                # Pour les programmes normaux : garder le système de checkboxes
                row = 0
                col = 0
                max_cols = 5
                
                for program_name, program_info in sorted(programs.items()):
                    var = tk.BooleanVar()
                    self.checkboxes[program_name] = var
                    
                    cb = ttk.Checkbutton(
                        programs_container,
                        text=program_name,
                        variable=var,
                        style='Dark.TCheckbutton'
                    )
                    cb.grid(row=row, column=col, sticky=tk.W, padx=10, pady=3)
                    
                    # Tooltip avec description
                    self._create_tooltip(cb, program_info.get('description', ''))
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
    
    def _execute_system_command(self, command_name: str, is_repair: bool):
        """
        Exécute une commande système immédiatement
        
        Args:
            command_name: Nom de la commande à exécuter
            is_repair: True si c'est une commande de réparation (DISM/SFC)
        """
        import subprocess
        import os
        
        # Trouver la commande dans la base de données
        command_info = None
        for category, programs in self.programs.items():
            if command_name in programs:
                command_info = programs[command_name]
                break
        
        if not command_info or 'command' not in command_info:
            self.log_message(f"[ERROR] Commande '{command_name}' non trouvée")
            return
        
        command = command_info.get('command', '')
        admin_required = command_info.get('admin_required', False)
        
        try:
            if is_repair:
                # Pour DISM/SFC : Ouvrir un terminal admin et exécuter la commande
                self.log_message(f"[INFO] Ouverture terminal admin pour: {command_name}")
                
                # Créer un script PowerShell temporaire qui exécute la commande
                # et garde le terminal ouvert
                ps_script = f"""
                Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
                Write-Host "  {command_name}" -ForegroundColor Yellow
                Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
                Write-Host ""
                
                # Exécuter la commande
                {command}
                
                Write-Host ""
                Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
                Write-Host "  Terminé ! Appuyez sur une touche pour fermer..." -ForegroundColor Green
                Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                """
                
                # Sauvegarder le script temporaire
                temp_script = os.path.join(os.path.dirname(__file__), '..', 'temp_dism.ps1')
                with open(temp_script, 'w', encoding='utf-8') as f:
                    f.write(ps_script)
                
                # Lancer PowerShell en mode admin avec le script
                if admin_required:
                    # Utiliser Start-Process avec -Verb RunAs pour élévation admin
                    subprocess.Popen([
                        'powershell',
                        '-Command',
                        f"Start-Process powershell -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -NoExit -File \"{temp_script}\"'"
                    ])
                else:
                    # Sans admin
                    subprocess.Popen([
                        'powershell',
                        '-ExecutionPolicy', 'Bypass',
                        '-NoExit',
                        '-File', temp_script
                    ])
                
                self.log_message(f"[SUCCESS] Terminal lancé pour: {command_name}")
                
            else:
                # Pour les paramètres Windows : Redirection directe
                self.log_message(f"[INFO] Ouverture de: {command_name}")
                
                if command.startswith("start "):
                    # Commandes ms-settings:, windowsdefender:, shell:
                    setting_uri = command.replace('start ', '').strip()
                    subprocess.Popen(['powershell', '-Command', f'Start-Process "{setting_uri}"'])
                    
                else:
                    # Autres commandes (control, devmgmt.msc, sysdm.cpl, etc.)
                    subprocess.Popen(command, shell=True)
                
                self.log_message(f"[SUCCESS] ✅ {command_name} ouvert")
                
        except Exception as e:
            self.log_message(f"[ERROR] Erreur lors de l'exécution: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _create_tooltip(self, widget, text):
        """Crée un tooltip pour un widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background=self.COLORS['bg_tertiary'],
                foreground=self.COLORS['fg_primary'],
                relief=tk.SOLID,
                borderwidth=1,
                font=('Segoe UI', 9),
                padx=5,
                pady=3
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def _create_footer(self, parent):
        """Crée le pied de page avec boutons et progression"""
        footer = ttk.Frame(parent, style='Dark.TFrame')
        footer.pack(fill=tk.X, pady=(10, 0))
        
        # Boutons
        buttons_frame = ttk.Frame(footer, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Bouton Tout sélectionner
        select_all_btn = ttk.Button(
            buttons_frame,
            text="✓ Tout sélectionner",
            command=self.select_all,
            style='Accent.TButton'
        )
        select_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton Tout désélectionner
        deselect_all_btn = ttk.Button(
            buttons_frame,
            text="✗ Tout désélectionner",
            command=self.deselect_all,
            style='Accent.TButton'
        )
        deselect_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton Nettoyage
        cleanup_btn = ttk.Button(
            buttons_frame,
            text="🧹 Nettoyage",
            command=self._show_cleanup_dialog,
            style='Accent.TButton'
        )
        cleanup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton Installer
        self.install_btn = ttk.Button(
            buttons_frame,
            text="🚀 Installer les programmes sélectionnés",
            command=self.start_installation,
            style='Accent.TButton'
        )
        self.install_btn.pack(side=tk.RIGHT)
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            footer,
            variable=self.progress_var,
            maximum=100,
            style='Dark.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Zone de log
        log_frame = ttk.Frame(footer, style='Secondary.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg=self.COLORS['bg_tertiary'],
            fg=self.COLORS['fg_primary'],
            font=('Consolas', 9),
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar pour le log
        log_scroll = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scroll.set)
    
    def select_all(self):
        """Sélectionne tous les programmes"""
        for var in self.checkboxes.values():
            var.set(True)
        self.log_message("[INFO] Tous les programmes sélectionnés")
    
    def deselect_all(self):
        """Désélectionne tous les programmes"""
        for var in self.checkboxes.values():
            var.set(False)
        self.log_message("[INFO] Tous les programmes désélectionnés")
    
    def log_message(self, message: str):
        """Ajoute un message au log"""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        logger.info(message)
    
    def update_progress(self, value: float):
        """Met à jour la barre de progression"""
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def start_installation(self):
        """Démarre l'installation des programmes sélectionnés"""
        # Récupérer les programmes sélectionnés
        selected = [name for name, var in self.checkboxes.items() if var.get()]
        
        if not selected:
            messagebox.showwarning(
                "Aucune sélection",
                "Veuillez sélectionner au moins un programme à installer."
            )
            return
        
        if not self.winget_manager.winget_available:
            messagebox.showerror(
                "Winget non disponible",
                "Winget n'est pas disponible sur ce système.\n"
                "Veuillez installer App Installer depuis le Microsoft Store."
            )
            return
        
        # Confirmation
        response = messagebox.askyesno(
            "Confirmation",
            f"Installer {len(selected)} programme(s) ?\n\n"
            f"Les programmes seront installés via Winget."
        )
        
        if not response:
            return
        
        # Désactiver le bouton
        self.install_btn.config(state=tk.DISABLED)
        
        # Lancer l'installation dans un thread
        thread = Thread(
            target=self._install_thread,
            args=(selected,),
            daemon=True
        )
        thread.start()
    
    def _install_thread(self, selected: List[str]):
        """Thread d'installation"""
        self.log_message(f"[INFO] Traitement de {len(selected)} élément(s)...")
        
        # Séparer les programmes Winget et les commandes système (réparation + paramètres)
        programs_to_install = []
        system_commands = []
        
        for item in selected:
            if self.winget_manager.is_system_command(item):
                system_commands.append(item)
            else:
                programs_to_install.append(item)
        
        # Installer les programmes normaux
        if programs_to_install:
            self.log_message(f"[INFO] Installation de {len(programs_to_install)} programme(s) via Winget...")
            self.winget_manager.install_programs(
                programs_to_install,
                progress_callback=lambda p: self.update_progress(p * 0.7),  # 70% pour les installations
                log_callback=self.log_message,
                finished_callback=None
            )
        
        # Exécuter les commandes système (réparation Windows + paramètres)
        if system_commands:
            self.log_message(f"\n[INFO] Exécution de {len(system_commands)} commande(s) système...")
            
            for i, cmd_name in enumerate(system_commands, 1):
                base_progress = 70 if programs_to_install else 0
                progress_range = 30 if programs_to_install else 100
                
                def cmd_progress(p):
                    total_p = base_progress + (progress_range * ((i - 1) + p / 100) / len(system_commands))
                    self.update_progress(total_p)
                
                success = self.winget_manager.run_system_command(
                    cmd_name,
                    progress_callback=cmd_progress,
                    log_callback=self.log_message
                )
                
                if not success:
                    self.log_message(f"[WARNING] La commande '{cmd_name}' a échoué ou nécessite des privilèges admin")
        
        # Terminer
        self._on_installation_finished()
    
    def _on_installation_finished(self):
        """Appelé quand l'installation est terminée"""
        self.update_progress(100)
        self.install_btn.config(state=tk.NORMAL)
        self.installation_completed = True  # Marquer qu'une installation a été faite

        messagebox.showinfo(
            "Installation terminée",
            "L'installation des programmes est terminée !\n\n"
            "Consultez le log pour plus de détails."
        )
    
    def _setup_close_handler(self):
        """Configure le gestionnaire de fermeture de fenêtre"""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _on_closing(self):
        """Appelé quand l'utilisateur ferme la fenêtre"""
        # Toujours proposer le nettoyage (même sans installation)
        # Car l'utilisateur peut avoir utilisé l'app et vouloir nettoyer
        self._show_cleanup_dialog()
    
    def _show_cleanup_dialog(self):
        """Affiche la boîte de dialogue de nettoyage"""
        try:
            from src.cleanup_manager import NiTriteCleanup
            
            cleanup = NiTriteCleanup()
            items = cleanup.get_cleanup_items()
            total_size = cleanup.get_total_size()
            
            # Créer une fenêtre personnalisée pour le nettoyage
            cleanup_window = tk.Toplevel(self.root)
            cleanup_window.title("🧹 Nettoyage de NiTrite")
            cleanup_window.configure(bg=self.COLORS['bg_primary'])
            cleanup_window.geometry("600x500")
            cleanup_window.resizable(False, False)
            
            # Centrer la fenêtre
            cleanup_window.transient(self.root)
            cleanup_window.grab_set()
            
            # Titre
            title_frame = ttk.Frame(cleanup_window, style='Dark.TFrame', padding=20)
            title_frame.pack(fill=tk.X)
            
            title_label = ttk.Label(
                title_frame,
                text="🧹 Nettoyage de NiTrite",
                style='Title.TLabel'
            )
            title_label.pack()
            
            subtitle_label = ttk.Label(
                title_frame,
                text="Voulez-vous supprimer toutes les traces de l'application ?",
                style='Dark.TLabel'
            )
            subtitle_label.pack(pady=(5, 0))
            
            # Zone d'information
            info_frame = ttk.Frame(cleanup_window, style='Secondary.TFrame', padding=15)
            info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
            
            info_text = tk.Text(
                info_frame,
                height=15,
                bg=self.COLORS['bg_tertiary'],
                fg=self.COLORS['fg_primary'],
                font=('Segoe UI', 10),
                wrap=tk.WORD,
                relief=tk.FLAT,
                padx=10,
                pady=10
            )
            info_text.pack(fill=tk.BOTH, expand=True)
            
            # Ajouter les informations
            info_text.insert(tk.END, "📋 ÉLÉMENTS À SUPPRIMER :\n\n", "header")
            
            for name, path, size in items:
                info_text.insert(tk.END, f"• {name}\n", "item")
                info_text.insert(tk.END, f"  📁 {path}\n", "path")
                info_text.insert(tk.END, f"  💾 {size} Mo\n\n", "size")
            
            info_text.insert(tk.END, f"\n{'='*50}\n\n", "separator")
            info_text.insert(tk.END, f"💾 TAILLE TOTALE : {total_size} Mo\n\n", "total")
            
            info_text.insert(tk.END, "⚠️ ATTENTION :\n", "warning")
            info_text.insert(tk.END, "• Cette action est IRRÉVERSIBLE\n", "bullet")
            info_text.insert(tk.END, "• L'application sera complètement supprimée\n", "bullet")
            info_text.insert(tk.END, "• Python sera supprimé si installé localement\n", "bullet")
            info_text.insert(tk.END, "• Un script de nettoyage s'exécutera après fermeture\n", "bullet")
            
            # Configurer les tags
            info_text.tag_config("header", foreground=self.COLORS['accent_blue'], font=('Segoe UI', 11, 'bold'))
            info_text.tag_config("item", foreground=self.COLORS['accent_green'], font=('Segoe UI', 10, 'bold'))
            info_text.tag_config("path", foreground=self.COLORS['fg_secondary'], font=('Consolas', 9))
            info_text.tag_config("size", foreground=self.COLORS['accent_orange'])
            info_text.tag_config("separator", foreground=self.COLORS['border'])
            info_text.tag_config("total", foreground=self.COLORS['accent_green'], font=('Segoe UI', 11, 'bold'))
            info_text.tag_config("warning", foreground=self.COLORS['accent_red'], font=('Segoe UI', 10, 'bold'))
            info_text.tag_config("bullet", foreground=self.COLORS['fg_primary'])
            
            info_text.config(state=tk.DISABLED)
            
            # Boutons
            buttons_frame = ttk.Frame(cleanup_window, style='Dark.TFrame', padding=20)
            buttons_frame.pack(fill=tk.X)
            
            def on_cleanup():
                cleanup_window.destroy()
                
                # Confirmation finale
                response = messagebox.askyesno(
                    "⚠️ Confirmation finale",
                    f"Êtes-vous ABSOLUMENT SÛR ?\n\n"
                    f"• {total_size} Mo seront supprimés\n"
                    f"• L'application sera détruite\n"
                    f"• Action IRRÉVERSIBLE\n\n"
                    f"Continuer ?",
                    icon='warning'
                )
                
                if response:
                    # Exécuter le nettoyage
                    success = cleanup.execute_cleanup([path for _, path, _ in items])
                    
                    if success:
                        messagebox.showinfo(
                            "✅ Nettoyage lancé",
                            "Le script de nettoyage va s'exécuter après la fermeture.\n\n"
                            "L'application va maintenant se fermer."
                        )
                        self.root.destroy()
                    else:
                        messagebox.showerror(
                            "❌ Erreur",
                            "Impossible de lancer le nettoyage.\n"
                            "L'application va se fermer normalement."
                        )
                        self.root.destroy()
                else:
                    self.root.destroy()
            
            def on_skip():
                cleanup_window.destroy()
                self.root.destroy()
            
            # Bouton Nettoyer
            cleanup_btn = ttk.Button(
                buttons_frame,
                text=f"🧹 Nettoyer tout ({total_size} Mo)",
                command=on_cleanup,
                style='Accent.TButton'
            )
            cleanup_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
            
            # Bouton Ignorer
            skip_btn = ttk.Button(
                buttons_frame,
                text="❌ Non, fermer seulement",
                command=on_skip,
                style='Accent.TButton'
            )
            skip_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
        except Exception as e:
            logger.error(f"Erreur affichage dialogue nettoyage: {e}")
            # En cas d'erreur, fermer normalement
            self.root.destroy()


def create_gui(root: tk.Tk) -> NiTriteWingetGUI:
    """Crée l'interface graphique"""
    return NiTriteWingetGUI(root)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    root = tk.Tk()
    gui = create_gui(root)
    root.mainloop()
