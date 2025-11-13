"""
Méthodes GUI pour la gestion de la base de données portable
À inclure dans gui_manager.py
"""

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
        from tkinter import messagebox
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
        from tkinter import messagebox
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
