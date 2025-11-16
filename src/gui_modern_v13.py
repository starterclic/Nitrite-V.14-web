#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NiTriTe V13.0 - Interface Moderne avec Navigation 2 Pages
Architecture moderne pour techniciens de maintenance informatique
Design : Noir & Orange Premium avec animations fluides
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import sys
import webbrowser
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Import des couleurs (module séparé pour éviter imports circulaires)
try:
    from .modern_colors import ModernColors, bind_mousewheel
except ImportError:
    from modern_colors import ModernColors, bind_mousewheel

# Import des données complètes des outils
try:
    from .tools_data_complete import get_all_tools
except ImportError:
    try:
        from tools_data_complete import get_all_tools
    except ImportError:
        # Fallback si le module n'est pas trouvé
        def get_all_tools():
            return {}

# Import des pages avancées
try:
    from .advanced_pages import (
        SettingsPage, DiagnosticPage, BackupPage,
        OptimizationsPage, UpdatesPage, ThemeManager
    )
except ImportError:
    try:
        from advanced_pages import (
            SettingsPage, DiagnosticPage, BackupPage,
            OptimizationsPage, UpdatesPage, ThemeManager
        )
    except ImportError:
        # Si l'import échoue, créer des classes factices
        class SettingsPage:
            def __init__(self, *args, **kwargs):
                pass
        class DiagnosticPage:
            def __init__(self, *args, **kwargs):
                pass
        class BackupPage:
            def __init__(self, *args, **kwargs):
                pass
        class OptimizationsPage:
            def __init__(self, *args, **kwargs):
                pass
        class UpdatesPage:
            def __init__(self, *args, **kwargs):
                pass
        class ThemeManager:
            @staticmethod
            def load_theme_preference():
                return "dark_orange"
            @staticmethod
            def apply_theme(theme_id, root=None):
                return True

# Import du gestionnaire de layout
try:
    from .layout_manager import LayoutManager
except ImportError:
    try:
        from layout_manager import LayoutManager
    except ImportError:
        # Fallback si pas disponible
        class LayoutManager:
            def __init__(self):
                pass
            def set_category_order(self, page_name, categories):
                pass
            def get_category_order(self, page_name):
                return []

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ModernColors et bind_mousewheel sont maintenant importés depuis modern_colors.py


class AnimationEngine:
    """Moteur d'animations pour effets visuels fluides"""

    @staticmethod
    def fade_in(widget, duration=300, steps=20):
        """Animation de fondu entrant"""
        def animate(step=0):
            if step < steps:
                opacity = step / steps
                try:
                    widget.attributes('-alpha', opacity)
                except:
                    pass
                widget.after(duration // steps, lambda: animate(step + 1))
        animate()

    @staticmethod
    def slide_in(widget, direction='left', duration=300):
        """Animation de glissement"""
        # Implémentation simplifiée pour Tkinter
        widget.update_idletasks()

    @staticmethod
    def ripple_effect(widget, x, y):
        """Effet ripple Material Design"""
        # Simulé avec changement de couleur temporaire
        original_bg = widget.cget('background')
        widget.config(background=ModernColors.ORANGE_LIGHT)
        widget.after(100, lambda: widget.config(background=original_bg))

# bind_mousewheel est maintenant importé depuis modern_colors.py


class ModernSearchBar(tk.Frame):
    """Barre de recherche moderne avec suggestions"""

    def __init__(self, parent, on_search_callback):
        super().__init__(parent, bg=ModernColors.BG_CARD)
        self.on_search_callback = on_search_callback
        self._create_widgets()

    def _create_widgets(self):
        """Créer les widgets de la barre de recherche"""
        # Container avec padding
        container = tk.Frame(self, bg=ModernColors.BG_CARD)
        container.pack(fill=tk.X, padx=20, pady=15)

        # Icône de recherche
        search_icon = tk.Label(
            container,
            text="🔍",
            font=("Segoe UI", 16),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.ORANGE_PRIMARY
        )
        search_icon.pack(side=tk.LEFT, padx=(0, 10))

        # Champ de recherche
        self.search_entry = tk.Entry(
            container,
            font=("Segoe UI", 12),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY,
            insertbackground=ModernColors.ORANGE_PRIMARY,
            relief=tk.FLAT,
            bd=0
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, ipadx=10)
        self.search_entry.insert(0, "Rechercher une application ou un outil...")
        self.search_entry.bind('<FocusIn>', self._on_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_focus_out)
        self.search_entry.bind('<KeyRelease>', self._on_key_release)

        # Bouton effacer
        clear_btn = tk.Label(
            container,
            text="✕",
            font=("Segoe UI", 14, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_MUTED,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=(10, 0))
        clear_btn.bind('<Button-1>', self._clear_search)
        clear_btn.bind('<Enter>', lambda e: clear_btn.config(fg=ModernColors.ORANGE_PRIMARY))
        clear_btn.bind('<Leave>', lambda e: clear_btn.config(fg=ModernColors.TEXT_MUTED))

    def _on_focus_in(self, event):
        """Gérer le focus entrant"""
        if self.search_entry.get() == "Rechercher une application ou un outil...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=ModernColors.TEXT_PRIMARY)

    def _on_focus_out(self, event):
        """Gérer le focus sortant"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Rechercher une application ou un outil...")
            self.search_entry.config(fg=ModernColors.TEXT_MUTED)

    def _on_key_release(self, event):
        """Gérer la saisie clavier"""
        query = self.search_entry.get()
        if query != "Rechercher une application ou un outil...":
            self.on_search_callback(query)

    def _clear_search(self, event):
        """Effacer la recherche"""
        self.search_entry.delete(0, tk.END)
        self.search_entry.focus()
        self.on_search_callback("")


class ModernStatsCard(tk.Frame):
    """Carte de statistiques moderne"""

    def __init__(self, parent, title, value, icon, color):
        super().__init__(parent, bg=ModernColors.BG_CARD, relief=tk.FLAT)
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color
        self._create_widgets()
        self._add_hover_effect()

    def _create_widgets(self):
        """Créer les widgets de la carte"""
        # Padding interne
        container = tk.Frame(self, bg=ModernColors.BG_CARD)
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Icône
        icon_label = tk.Label(
            container,
            text=self.icon,
            font=("Segoe UI", 24),
            bg=ModernColors.BG_CARD,
            fg=self.color
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        # Texte
        text_container = tk.Frame(container, bg=ModernColors.BG_CARD)
        text_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            text_container,
            text=self.title,
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w'
        )
        title_label.pack(fill=tk.X)

        value_label = tk.Label(
            text_container,
            text=str(self.value),
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w'
        )
        value_label.pack(fill=tk.X)

    def _add_hover_effect(self):
        """Ajouter effet hover"""
        def on_enter(e):
            self.config(bg=ModernColors.BG_HOVER)
            for child in self.winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.config(bg=ModernColors.BG_HOVER)

        def on_leave(e):
            self.config(bg=ModernColors.BG_CARD)
            for child in self.winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.config(bg=ModernColors.BG_CARD)

        self.bind('<Enter>', on_enter)
        self.bind('<Leave>', on_leave)

    def update_value(self, new_value):
        """Mettre à jour la valeur"""
        self.value = new_value
        # Mettre à jour le label de valeur
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Frame):
                        for label in subchild.winfo_children():
                            if isinstance(label, tk.Label) and label.cget('font')[1] == 20:
                                label.config(text=str(new_value))


class ModernNavigationBar(tk.Frame):
    """Barre de navigation latérale moderne"""

    def __init__(self, parent, on_page_change):
        super().__init__(parent, bg=ModernColors.BG_MEDIUM, width=280)  # Web version uses 280px
        self.on_page_change = on_page_change
        self.current_page = "applications"
        self.nav_buttons = {}
        self._create_widgets()

    def _create_widgets(self):
        """Créer les widgets de navigation"""
        # Logo et titre - styled like web version with gradient box
        header = tk.Frame(self, bg=ModernColors.BG_MEDIUM)
        header.pack(fill=tk.X, padx=20, pady=(25, 20))

        # Container for logo + info (horizontal layout like web)
        logo_container = tk.Frame(header, bg=ModernColors.BG_MEDIUM)
        logo_container.pack(fill=tk.X)

        # Logo icon with gradient background (matching web .logo-icon)
        logo_frame = tk.Frame(
            logo_container,
            bg=ModernColors.ORANGE_PRIMARY,
            width=50,
            height=50
        )
        logo_frame.pack(side=tk.LEFT, padx=(0, 15))
        logo_frame.pack_propagate(False)

        logo_label = tk.Label(
            logo_frame,
            text="N",
            font=("Segoe UI", 28, "bold"),
            bg=ModernColors.ORANGE_PRIMARY,
            fg="white"
        )
        logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Logo info (title + version)
        info_frame = tk.Frame(logo_container, bg=ModernColors.BG_MEDIUM)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            info_frame,
            text="NiTriTe",
            font=("Segoe UI", 24, "bold"),
            bg=ModernColors.BG_MEDIUM,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w'
        )
        title_label.pack(fill=tk.X)

        version_label = tk.Label(
            info_frame,
            text="Version 13.0 Beta",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_MEDIUM,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w'
        )
        version_label.pack(fill=tk.X)

        # Séparateur (border-bottom like web)
        separator = tk.Frame(self, bg=ModernColors.BORDER_COLOR, height=1)
        separator.pack(fill=tk.X, pady=(0, 20))

        # Boutons de navigation
        nav_items = [
            ("applications", "📦", "Applications", "715 apps disponibles"),
            ("tools", "🛠️", "Outils Système", "553+ boutons utiles"),
            ("master_install", "🚀", "Master Installation", "Installation rapide Windows"),
            ("updates", "🔄", "Mises à Jour", "Détection & Updates"),
            ("backup", "💾", "Backup & Restore", "Sauvegarde système"),
            ("optimizations", "⚡", "Optimisations", "Tweaks Windows"),
            ("diagnostic", "🔍", "Diagnostic", "Benchmark & Santé PC"),
            ("settings", "⚙️", "Paramètres", "Thèmes & Configuration"),
        ]

        for page_id, icon, title, subtitle in nav_items:
            btn = self._create_nav_button(page_id, icon, title, subtitle)
            self.nav_buttons[page_id] = btn

        # Sélectionner la première page par défaut
        self._select_page("applications")

        # Spacer pour pousser le footer en bas
        spacer = tk.Frame(self, bg=ModernColors.BG_MEDIUM)
        spacer.pack(fill=tk.BOTH, expand=True)

        # Footer avec infos
        footer = tk.Frame(self, bg=ModernColors.BG_DARK)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        footer_text = tk.Label(
            footer,
            text="💼 OrdiPlus Tools\n🚀 Portable Edition",
            font=("Segoe UI", 8),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_MUTED,
            justify=tk.CENTER
        )
        footer_text.pack(pady=15)

    def _create_nav_button(self, page_id, icon, title, subtitle):
        """Créer un bouton de navigation - styled like web version"""
        container = tk.Frame(self, bg=ModernColors.BG_MEDIUM)
        container.pack(fill=tk.X, padx=10, pady=3)  # Reduced padding between buttons

        # Main button frame with rounded appearance
        btn = tk.Frame(
            container,
            bg=ModernColors.BG_MEDIUM,
            cursor="hand2",
            highlightthickness=0
        )
        btn.pack(fill=tk.X)

        # Content frame with proper padding (matching web: 14px 16px)
        content = tk.Frame(btn, bg=ModernColors.BG_MEDIUM)
        content.pack(fill=tk.BOTH, expand=True, padx=16, pady=14)

        # Horizontal layout: icon + text content
        icon_label = tk.Label(
            content,
            text=icon,
            font=("Segoe UI", 20),  # Slightly larger like web
            bg=ModernColors.BG_MEDIUM,
            fg=ModernColors.TEXT_SECONDARY
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 12))

        # Text container
        text_frame = tk.Frame(content, bg=ModernColors.BG_MEDIUM)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            text_frame,
            text=title,
            font=("Segoe UI", 15, "normal"),  # Matching web font-weight: 500
            bg=ModernColors.BG_MEDIUM,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w'
        )
        title_label.pack(fill=tk.X)

        # Store references for easy access
        btn.content = content
        btn.icon_label = icon_label
        btn.title_label = title_label
        btn.text_frame = text_frame
        btn.widgets = [btn, content, icon_label, title_label, text_frame]

        # Bind events
        for widget in btn.widgets:
            widget.bind('<Button-1>', lambda e, pid=page_id: self._on_nav_click(pid))
            widget.bind('<Enter>', lambda e, b=btn: self._on_nav_hover(b, True))
            widget.bind('<Leave>', lambda e, b=btn: self._on_nav_hover(b, False))

        return btn

    def _on_nav_click(self, page_id):
        """Gérer le clic sur un bouton de navigation"""
        self._select_page(page_id)
        # Afficher la page correspondante via le callback
        self.on_page_change(page_id)

    def _on_nav_hover(self, btn, is_enter):
        """Gérer le survol d'un bouton - matching web hover effect"""
        # Check if this button is active
        is_active = btn.cget('bg') == ModernColors.ORANGE_PRIMARY

        if not is_active:
            if is_enter:
                # Hover state: bg-hover color, text-primary
                for widget in btn.widgets:
                    widget.config(bg=ModernColors.BG_HOVER)
                btn.icon_label.config(fg=ModernColors.TEXT_PRIMARY)
                btn.title_label.config(fg=ModernColors.TEXT_PRIMARY)
            else:
                # Normal state: transparent, text-secondary
                for widget in btn.widgets:
                    widget.config(bg=ModernColors.BG_MEDIUM)
                btn.icon_label.config(fg=ModernColors.TEXT_SECONDARY)
                btn.title_label.config(fg=ModernColors.TEXT_SECONDARY)

    def _select_page(self, page_id):
        """Sélectionner une page - matching web active state with gradient"""
        # Deselect all buttons (reset to normal state)
        for pid, btn in self.nav_buttons.items():
            if pid != page_id:
                # Reset to normal state
                for widget in btn.widgets:
                    widget.config(bg=ModernColors.BG_MEDIUM)
                btn.icon_label.config(fg=ModernColors.TEXT_SECONDARY)
                btn.title_label.config(fg=ModernColors.TEXT_SECONDARY)

        # Select the new button (gradient background + white text)
        if page_id in self.nav_buttons:
            btn = self.nav_buttons[page_id]
            # Active state: gradient orange background with white text
            for widget in btn.widgets:
                widget.config(bg=ModernColors.ORANGE_PRIMARY)
            btn.icon_label.config(fg="white")
            btn.title_label.config(fg="white")
            self.current_page = page_id


class ModernAppCard(tk.Frame):
    """Carte moderne pour une application - styled like web version"""

    def __init__(self, parent, app_name, app_data, on_select, on_web_redirect):
        super().__init__(
            parent,
            bg=ModernColors.BG_CARD,
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightbackground=ModernColors.BORDER_COLOR,
            highlightcolor=ModernColors.BORDER_COLOR
        )
        self.app_name = app_name
        self.app_data = app_data
        self.on_select = on_select
        self.on_web_redirect = on_web_redirect
        self.is_selected = False
        self._create_widgets()
        self._add_hover_effect()

    def _create_widgets(self):
        """Créer les widgets de la carte"""
        # Container avec padding (web uses 20px, increased from 12px)
        container = tk.Frame(self, bg=ModernColors.BG_CARD)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header : checkbox + nom
        header = tk.Frame(container, bg=ModernColors.BG_CARD)
        header.pack(fill=tk.X)

        # Checkbox
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(
            header,
            variable=self.checkbox_var,
            bg=ModernColors.BG_CARD,
            fg=ModernColors.ORANGE_PRIMARY,
            selectcolor=ModernColors.BG_DARK,
            activebackground=ModernColors.BG_CARD,
            activeforeground=ModernColors.ORANGE_PRIMARY,
            command=self._on_checkbox_change,
            cursor="hand2"
        )
        self.checkbox.pack(side=tk.LEFT)

        # Nom de l'application
        name_label = tk.Label(
            header,
            text=self.app_name,
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w',
            cursor="hand2"
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        name_label.bind('<Button-1>', lambda e: self.checkbox.invoke())

        # Bouton web (si URL disponible)
        web_url = self.app_data.get('download_url') or self.app_data.get('web_url')
        if web_url:
            web_btn = tk.Label(
                header,
                text="🌐",
                font=("Segoe UI", 12),
                bg=ModernColors.BG_CARD,
                fg=ModernColors.BLUE_INFO,
                cursor="hand2"
            )
            web_btn.pack(side=tk.RIGHT, padx=(5, 0))
            web_btn.bind('<Button-1>', lambda e: self.on_web_redirect(web_url))
            web_btn.bind('<Enter>', lambda e: web_btn.config(fg=ModernColors.ORANGE_PRIMARY))
            web_btn.bind('<Leave>', lambda e: web_btn.config(fg=ModernColors.BLUE_INFO))

        # Description
        description = self.app_data.get('description', 'Aucune description')
        desc_label = tk.Label(
            container,
            text=description[:80] + "..." if len(description) > 80 else description,
            font=("Segoe UI", 9),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            justify=tk.LEFT,
            wraplength=250
        )
        desc_label.pack(fill=tk.X, pady=(5, 0))

        # Footer : badges
        footer = tk.Frame(container, bg=ModernColors.BG_CARD)
        footer.pack(fill=tk.X, pady=(8, 0))

        # Badge catégorie
        category = self.app_data.get('category', 'Autre')
        cat_badge = tk.Label(
            footer,
            text=f"📁 {category}",
            font=("Segoe UI", 8),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_MUTED,
            padx=6,
            pady=2
        )
        cat_badge.pack(side=tk.LEFT, padx=(0, 5))

        # Badge portable si applicable
        if self.app_data.get('portable'):
            port_badge = tk.Label(
                footer,
                text="💼 Portable",
                font=("Segoe UI", 8),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.GREEN_SUCCESS,
                padx=6,
                pady=2
            )
            port_badge.pack(side=tk.LEFT, padx=(0, 5))

        # Badge WinGet si disponible
        if self.app_data.get('winget_id'):
            winget_badge = tk.Label(
                footer,
                text="⚡ WinGet",
                font=("Segoe UI", 8),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.PURPLE_PREMIUM,
                padx=6,
                pady=2
            )
            winget_badge.pack(side=tk.LEFT)

    def _add_hover_effect(self):
        """Ajouter effet hover - matching web version"""
        def on_enter(e):
            if not self.is_selected:
                # Hover effect: orange border
                self.config(
                    highlightthickness=1,
                    highlightbackground=ModernColors.ORANGE_PRIMARY,
                    highlightcolor=ModernColors.ORANGE_PRIMARY
                )

        def on_leave(e):
            if not self.is_selected:
                # Reset to normal border
                self.config(
                    highlightthickness=1,
                    highlightbackground=ModernColors.BORDER_COLOR,
                    highlightcolor=ModernColors.BORDER_COLOR
                )

        self.bind('<Enter>', on_enter)
        self.bind('<Leave>', on_leave)

    def _on_checkbox_change(self):
        """Gérer le changement de checkbox - matching web selected state"""
        self.is_selected = self.checkbox_var.get()
        if self.is_selected:
            # Selected state: orange border + light orange background tint
            self.config(
                highlightthickness=1,
                highlightbackground=ModernColors.ORANGE_PRIMARY,
                highlightcolor=ModernColors.ORANGE_PRIMARY,
                bg="#2a1f1a"  # Approximation of rgba(255, 107, 53, 0.1) over dark bg
            )
            # Update container background
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg="#2a1f1a")
                    self._update_children_bg(child, "#2a1f1a")
        else:
            # Normal state: regular border + normal background
            self.config(
                highlightthickness=1,
                highlightbackground=ModernColors.BORDER_COLOR,
                highlightcolor=ModernColors.BORDER_COLOR,
                bg=ModernColors.BG_CARD
            )
            # Reset container background
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=ModernColors.BG_CARD)
                    self._update_children_bg(child, ModernColors.BG_CARD)
        self.on_select(self.app_name, self.is_selected)

    def _update_children_bg(self, widget, bg_color):
        """Recursively update background color of all children"""
        for child in widget.winfo_children():
            if isinstance(child, (tk.Frame, tk.Label)):
                child.config(bg=bg_color)
            if isinstance(child, tk.Frame):
                self._update_children_bg(child, bg_color)

    def set_selected(self, selected):
        """Définir la sélection"""
        self.checkbox_var.set(selected)
        self._on_checkbox_change()


class ModernToolButton(tk.Frame):
    """Bouton moderne pour un outil système"""

    def __init__(self, parent, name, action, icon="🔧"):
        super().__init__(parent, bg=ModernColors.BG_CARD, cursor="hand2")
        self.name = name
        self.action = action
        self.icon = icon
        self._create_widgets()
        self._add_hover_effect()

    def _create_widgets(self):
        """Créer les widgets du bouton"""
        # Container
        container = tk.Frame(self, bg=ModernColors.BG_CARD)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Icône
        icon_label = tk.Label(
            container,
            text=self.icon,
            font=("Segoe UI", 14),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.ORANGE_PRIMARY
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 8))

        # Nom
        name_label = tk.Label(
            container,
            text=self.name,
            font=("Segoe UI", 9),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w'
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Bind click
        for widget in [self, container, icon_label, name_label]:
            widget.bind('<Button-1>', lambda e: self._on_click())

    def _add_hover_effect(self):
        """Ajouter effet hover"""
        def on_enter(e):
            self.config(bg=ModernColors.BG_HOVER)
            for child in self.winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.config(bg=ModernColors.BG_HOVER)
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.Label):
                            subchild.config(bg=ModernColors.BG_HOVER)

        def on_leave(e):
            self.config(bg=ModernColors.BG_CARD)
            for child in self.winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.config(bg=ModernColors.BG_CARD)
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.Label):
                            subchild.config(bg=ModernColors.BG_CARD)

        self.bind('<Enter>', on_enter)
        self.bind('<Leave>', on_leave)

    def _on_click(self):
        """Gérer le clic"""
        try:
            # Effet visuel
            original_bg = self.cget('background')
            self.config(bg=ModernColors.ORANGE_PRIMARY)
            self.after(100, lambda: self.config(bg=original_bg))

            # Exécuter l'action
            if callable(self.action):
                self.action()
            elif isinstance(self.action, str):
                if self.action.startswith('http'):
                    webbrowser.open(self.action)
                else:
                    os.system(self.action)
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de {self.name}: {e}")
            messagebox.showerror("Erreur", f"Impossible d'exécuter {self.name}\n{str(e)}")


class ApplicationsPage(tk.Frame):
    """Page Applications avec cartes modernes"""

    def __init__(self, parent, programs_data):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self.programs_data = programs_data
        self.selected_apps = set()
        self.app_cards = {}
        self.filtered_programs = programs_data.copy()
        self.collapsed_sections = {}  # État collapsed de chaque section

        # Gestionnaire de layout pour sauvegarde ordre
        self.layout_manager = LayoutManager()

        # Charger l'ordre sauvegardé ou utiliser ordre par défaut
        saved_order = self.layout_manager.get_category_order("applications")
        if saved_order and all(cat in self.programs_data for cat in saved_order):
            self.section_order = saved_order
        else:
            self.section_order = list(self.programs_data.keys())
            # Mettre "Master Windows" en premier
            if "Master Windows" in self.section_order:
                self.section_order.remove("Master Windows")
                self.section_order.insert(0, "Master Windows")
            # Sauvegarder l'ordre initial
            self.layout_manager.set_category_order("applications", self.section_order)

        self.section_frames = {}  # Référence aux frames de chaque section
        self._create_widgets()

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Header avec stats et actions
        header = tk.Frame(self, bg=ModernColors.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        # Titre
        title_label = tk.Label(
            header,
            text="📦 Marketplace d'Applications",
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        # Spacer
        spacer = tk.Frame(header, bg=ModernColors.BG_DARK)
        spacer.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Boutons d'action
        actions_frame = tk.Frame(header, bg=ModernColors.BG_DARK)
        actions_frame.pack(side=tk.RIGHT)

        # Bouton Tout sélectionner
        select_all_btn = tk.Button(
            actions_frame,
            text="✓ Tout sélectionner",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_PRIMARY,
            activeforeground=ModernColors.TEXT_PRIMARY,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self._select_all
        )
        select_all_btn.pack(side=tk.LEFT, padx=5)

        # Bouton Tout désélectionner
        deselect_all_btn = tk.Button(
            actions_frame,
            text="✕ Tout désélectionner",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.RED_ERROR,
            activeforeground=ModernColors.TEXT_PRIMARY,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self._deselect_all
        )
        deselect_all_btn.pack(side=tk.LEFT, padx=5)

        # Barre de recherche
        self.search_bar = ModernSearchBar(self, self._on_search)
        self.search_bar.pack(fill=tk.X, padx=20, pady=(0, 10))

        # Stats cards
        stats_frame = tk.Frame(self, bg=ModernColors.BG_DARK)
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        total_apps = sum(len(apps) for apps in self.programs_data.values())
        total_categories = len(self.programs_data)

        self.stats_total = ModernStatsCard(
            stats_frame,
            "Applications",
            total_apps,
            "📦",
            ModernColors.ORANGE_PRIMARY
        )
        self.stats_total.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.stats_categories = ModernStatsCard(
            stats_frame,
            "Catégories",
            total_categories,
            "📁",
            ModernColors.BLUE_INFO
        )
        self.stats_categories.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.stats_selected = ModernStatsCard(
            stats_frame,
            "Sélectionnées",
            0,
            "✓",
            ModernColors.GREEN_SUCCESS
        )
        self.stats_selected.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Zone de scroll pour les applications
        scroll_frame = tk.Frame(self, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Canvas et scrollbar
        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        self.scrollable_frame = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mousewheel avec gestion intelligente
        bind_mousewheel(canvas, self.scrollable_frame)

        # Afficher les applications
        self._display_applications()

        # Bouton d'installation (fixe en bas)
        install_frame = tk.Frame(self, bg=ModernColors.BG_MEDIUM)
        install_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.install_btn = tk.Button(
            install_frame,
            text="🚀 INSTALLER LES APPLICATIONS SÉLECTIONNÉES",
            font=("Segoe UI", 12, "bold"),
            bg=ModernColors.ORANGE_PRIMARY,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            activeforeground=ModernColors.TEXT_PRIMARY,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=15,
            command=self._start_installation
        )
        self.install_btn.pack(fill=tk.X, padx=20, pady=15)

    def _display_applications(self):
        """Afficher les applications sous forme de cartes"""
        # Nettoyer le frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.app_cards.clear()
        self.section_frames.clear()

        # Afficher par catégorie dans l'ordre personnalisé
        for idx, category in enumerate(self.section_order):
            if category not in self.filtered_programs:
                continue

            apps = self.filtered_programs[category]

            # Header de catégorie avec collapse et reorder
            cat_header = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_MEDIUM)
            cat_header.pack(fill=tk.X, pady=(15, 10))

            # Bouton collapse/expand
            is_collapsed = self.collapsed_sections.get(category, False)
            collapse_icon = "▶" if is_collapsed else "▼"

            collapse_btn = tk.Label(
                cat_header,
                text=collapse_icon,
                font=("Segoe UI", 12),
                bg=ModernColors.BG_MEDIUM,
                fg=ModernColors.ORANGE_PRIMARY,
                cursor="hand2",
                padx=10,
                pady=10
            )
            collapse_btn.pack(side=tk.LEFT)
            collapse_btn.bind('<Button-1>', lambda e, c=category: self._toggle_section(c))

            # Label de catégorie
            cat_label = tk.Label(
                cat_header,
                text=f"📁 {category} ({len(apps)} apps)",
                font=("Segoe UI", 14, "bold"),
                bg=ModernColors.BG_MEDIUM,
                fg=ModernColors.ORANGE_PRIMARY,
                anchor='w',
                padx=5,
                pady=10
            )
            cat_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Boutons de réorganisation
            reorder_frame = tk.Frame(cat_header, bg=ModernColors.BG_MEDIUM)
            reorder_frame.pack(side=tk.RIGHT, padx=10)

            # Bouton Up
            if idx > 0:
                up_btn = tk.Label(
                    reorder_frame,
                    text="▲",
                    font=("Segoe UI", 10),
                    bg=ModernColors.BG_MEDIUM,
                    fg=ModernColors.TEXT_SECONDARY,
                    cursor="hand2",
                    padx=5
                )
                up_btn.pack(side=tk.LEFT, padx=2)
                up_btn.bind('<Button-1>', lambda e, c=category: self._move_section_up(c))
                up_btn.bind('<Enter>', lambda e, b=up_btn: b.config(fg=ModernColors.ORANGE_PRIMARY))
                up_btn.bind('<Leave>', lambda e, b=up_btn: b.config(fg=ModernColors.TEXT_SECONDARY))

            # Bouton Down
            if idx < len(self.section_order) - 1:
                down_btn = tk.Label(
                    reorder_frame,
                    text="▼",
                    font=("Segoe UI", 10),
                    bg=ModernColors.BG_MEDIUM,
                    fg=ModernColors.TEXT_SECONDARY,
                    cursor="hand2",
                    padx=5
                )
                down_btn.pack(side=tk.LEFT, padx=2)
                down_btn.bind('<Button-1>', lambda e, c=category: self._move_section_down(c))
                down_btn.bind('<Enter>', lambda e, b=down_btn: b.config(fg=ModernColors.ORANGE_PRIMARY))
                down_btn.bind('<Leave>', lambda e, b=down_btn: b.config(fg=ModernColors.TEXT_SECONDARY))

            # Grille de cartes (4 colonnes - compromis optimal)
            grid_frame = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_DARK)
            if not is_collapsed:
                grid_frame.pack(fill=tk.X, padx=5, pady=(0, 10))

            self.section_frames[category] = grid_frame

            # Si collapsed, ne pas afficher les applications
            if is_collapsed:
                continue

            row = 0
            col = 0
            for app_name, app_data in sorted(apps.items()):
                card = ModernAppCard(
                    grid_frame,
                    app_name,
                    app_data,
                    self._on_app_select,
                    self._on_web_redirect
                )
                card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                self.app_cards[app_name] = card

                col += 1
                if col >= 4:  # 4 colonnes
                    col = 0
                    row += 1

            # Configurer les colonnes pour expansion égale
            for i in range(4):  # 4 colonnes
                grid_frame.columnconfigure(i, weight=1, uniform="col")

    def _on_app_select(self, app_name, is_selected):
        """Gérer la sélection d'une application"""
        if is_selected:
            self.selected_apps.add(app_name)
        else:
            self.selected_apps.discard(app_name)

        # Mettre à jour les stats
        self.stats_selected.update_value(len(self.selected_apps))

    def _on_web_redirect(self, url):
        """Ouvrir l'URL dans le navigateur"""
        try:
            webbrowser.open(url)
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture de {url}: {e}")
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le lien\n{str(e)}")

    def _on_search(self, query):
        """Filtrer les applications par recherche"""
        if not query:
            self.filtered_programs = self.programs_data.copy()
        else:
            query_lower = query.lower()
            self.filtered_programs = {}

            for category, apps in self.programs_data.items():
                filtered_apps = {
                    name: data for name, data in apps.items()
                    if query_lower in name.lower() or
                       query_lower in data.get('description', '').lower()
                }
                if filtered_apps:
                    self.filtered_programs[category] = filtered_apps

        # Rafraîchir l'affichage
        self._display_applications()

    def _select_all(self):
        """Sélectionner toutes les applications visibles"""
        for card in self.app_cards.values():
            card.set_selected(True)

    def _deselect_all(self):
        """Désélectionner toutes les applications"""
        self.selected_apps.clear()
        for card in self.app_cards.values():
            card.set_selected(False)

    def _toggle_section(self, category):
        """Toggle l'état collapsed d'une section"""
        current_state = self.collapsed_sections.get(category, False)
        self.collapsed_sections[category] = not current_state
        self._display_applications()

    def _move_section_up(self, category):
        """Déplacer une section vers le haut"""
        idx = self.section_order.index(category)
        if idx > 0:
            # Échanger avec la section précédente
            self.section_order[idx], self.section_order[idx - 1] = \
                self.section_order[idx - 1], self.section_order[idx]
            # Sauvegarder l'ordre personnalisé
            self.layout_manager.set_category_order("applications", self.section_order)
            self._display_applications()

    def _move_section_down(self, category):
        """Déplacer une section vers le bas"""
        idx = self.section_order.index(category)
        if idx < len(self.section_order) - 1:
            # Échanger avec la section suivante
            self.section_order[idx], self.section_order[idx + 1] = \
                self.section_order[idx + 1], self.section_order[idx]
            # Sauvegarder l'ordre personnalisé
            self.layout_manager.set_category_order("applications", self.section_order)
            self._display_applications()

    def _start_installation(self):
        """Démarrer l'installation des applications sélectionnées"""
        if not self.selected_apps:
            messagebox.showwarning(
                "Aucune sélection",
                "Veuillez sélectionner au moins une application à installer."
            )
            return

        # Afficher confirmation
        count = len(self.selected_apps)
        response = messagebox.askyesno(
            "Confirmation d'installation",
            f"Vous êtes sur le point d'installer {count} application(s).\n\n"
            "Cette opération peut prendre plusieurs minutes.\n"
            "Continuer ?"
        )

        if response:
            # Afficher la fenêtre de progression
            self._show_installation_progress()

    def _show_installation_progress(self):
        """Afficher la fenêtre de progression d'installation"""
        # Créer une fenêtre modale
        progress_window = tk.Toplevel(self)
        progress_window.title("Installation en cours...")
        progress_window.geometry("600x400")
        progress_window.configure(bg=ModernColors.BG_DARK)
        progress_window.transient(self)
        progress_window.grab_set()

        # Titre
        title_label = tk.Label(
            progress_window,
            text="🚀 Installation en cours",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(pady=20)

        # Nombre d'apps
        count_label = tk.Label(
            progress_window,
            text=f"{len(self.selected_apps)} applications à installer",
            font=("Segoe UI", 11),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_SECONDARY
        )
        count_label.pack()

        # Barre de progression
        progress_frame = tk.Frame(progress_window, bg=ModernColors.BG_CARD)
        progress_frame.pack(fill=tk.X, padx=30, pady=20)

        progress_canvas = tk.Canvas(
            progress_frame,
            height=30,
            bg=ModernColors.BG_LIGHT,
            highlightthickness=0
        )
        progress_canvas.pack(fill=tk.X, padx=10, pady=10)

        # Zone de log
        log_frame = tk.Frame(progress_window, bg=ModernColors.BG_DARK)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))

        log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY,
            wrap=tk.WORD,
            height=10
        )
        log_text.pack(fill=tk.BOTH, expand=True)

        # Fonction de log
        def log_message(msg):
            log_text.insert(tk.END, f"{msg}\n")
            log_text.see(tk.END)
            log_text.update_idletasks()

        # Fonction de mise à jour de la progression
        def update_progress(current, total):
            percentage = (current / total) * 100
            width = progress_canvas.winfo_width()
            progress_width = int((width * percentage) / 100)

            progress_canvas.delete("all")
            # Fond
            progress_canvas.create_rectangle(
                0, 0, width, 30,
                fill=ModernColors.BG_LIGHT,
                outline=""
            )
            # Barre
            progress_canvas.create_rectangle(
                0, 0, progress_width, 30,
                fill=ModernColors.GREEN_SUCCESS,
                outline=""
            )
            # Texte
            progress_canvas.create_text(
                width // 2, 15,
                text=f"{int(percentage)}% - {current}/{total}",
                fill=ModernColors.TEXT_PRIMARY,
                font=("Segoe UI", 10, "bold")
            )

        # Bouton annuler
        cancel_btn = tk.Button(
            progress_window,
            text="✕ Annuler",
            font=("Segoe UI", 10),
            bg=ModernColors.RED_ERROR,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=lambda: progress_window.destroy()
        )
        cancel_btn.pack(pady=(0, 20))

        # Simuler l'installation (en attendant la vraie intégration)
        def simulate_installation():
            total = len(self.selected_apps)
            for i, app_name in enumerate(self.selected_apps, 1):
                log_message(f"[{i}/{total}] Installation de {app_name}...")
                update_progress(i, total)
                progress_window.update()

                # Simuler le temps d'installation
                import time
                time.sleep(0.5)  # Remplacer par vraie installation

                log_message(f"✓ {app_name} installé avec succès !")

            # Terminé
            log_message("\n✓ Installation terminée !")
            cancel_btn.config(text="✓ Fermer", bg=ModernColors.GREEN_SUCCESS)

        # Lancer l'installation dans un thread
        install_thread = threading.Thread(target=simulate_installation, daemon=True)
        install_thread.start()


class ToolsPage(tk.Frame):
    """Page Outils Système avec boutons organisés"""

    def __init__(self, parent):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self.tools_data = self._load_tools_data()
        self.filtered_tools = self.tools_data.copy()  # Outils filtrés (initialement tous)
        self.collapsed_sections = {}  # État collapsed de chaque section

        # Gestionnaire de layout pour sauvegarde ordre
        self.layout_manager = LayoutManager()

        # Charger l'ordre sauvegardé ou utiliser ordre par défaut
        saved_order = self.layout_manager.get_category_order("tools")
        if saved_order and all(cat in self.tools_data for cat in saved_order):
            self.section_order = saved_order
        else:
            self.section_order = list(self.tools_data.keys())
            # Sauvegarder l'ordre initial
            self.layout_manager.set_category_order("tools", self.section_order)

        self.section_frames = {}  # Référence aux frames de chaque section
        self._create_widgets()

    def _load_tools_data(self):
        """Charger les données complètes des outils système (548 outils)"""
        # Charger tous les outils depuis le module tools_data_complete
        all_tools = get_all_tools()

        # Convertir le format (name, action) vers (name, action, icon)
        # Les icônes sont déjà incluses dans les noms des outils
        converted_tools = {}
        for section_name, tools_list in all_tools.items():
            converted_tools[section_name] = []
            for tool_name, tool_action in tools_list:
                # Extraire l'icône du nom si elle existe (premier caractère emoji)
                icon = tool_name.split()[0] if tool_name else "🔧"
                converted_tools[section_name].append((tool_name, tool_action, icon))

        return converted_tools

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Header
        header = tk.Frame(self, bg=ModernColors.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        # Titre
        title_label = tk.Label(
            header,
            text="🛠️ Centre d'Outils Système",
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        # Stats
        total_tools = sum(len(tools) for tools in self.tools_data.values())
        stats_label = tk.Label(
            header,
            text=f"✨ {total_tools} outils disponibles",
            font=("Segoe UI", 12),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.ORANGE_PRIMARY
        )
        stats_label.pack(side=tk.RIGHT)

        # Barre de recherche
        self.search_bar = ModernSearchBar(self, self._on_search)
        self.search_bar.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Zone de scroll pour les outils
        scroll_frame = tk.Frame(self, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Canvas et scrollbar
        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        self.scrollable_frame = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mousewheel avec gestion intelligente
        bind_mousewheel(canvas, self.scrollable_frame)

        # Afficher les outils
        self._display_tools()

    def _display_tools(self):
        """Afficher les outils par section avec collapse et réorganisation"""
        # Nettoyer l'affichage actuel
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.section_frames.clear()

        # Afficher les sections dans l'ordre personnalisé (avec filtre appliqué)
        for idx, section_name in enumerate(self.section_order):
            if section_name not in self.filtered_tools:
                continue

            tools = self.filtered_tools[section_name]

            # Container pour la section complète
            section_container = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_DARK)
            section_container.pack(fill=tk.X, pady=(10, 0))

            # Header de section avec boutons
            section_header = tk.Frame(section_container, bg=ModernColors.BG_MEDIUM)
            section_header.pack(fill=tk.X)

            # Bouton collapse/expand
            is_collapsed = self.collapsed_sections.get(section_name, False)
            collapse_icon = "▶" if is_collapsed else "▼"

            collapse_btn = tk.Label(
                section_header,
                text=collapse_icon,
                font=("Segoe UI", 12),
                bg=ModernColors.BG_MEDIUM,
                fg=ModernColors.ORANGE_PRIMARY,
                cursor="hand2",
                padx=10,
                pady=10
            )
            collapse_btn.pack(side=tk.LEFT)
            collapse_btn.bind('<Button-1>', lambda e, s=section_name: self._toggle_section(s))

            # Nom de la section (aussi cliquable pour collapse)
            section_label = tk.Label(
                section_header,
                text=f"{section_name} ({len(tools)})",
                font=("Segoe UI", 14, "bold"),
                bg=ModernColors.BG_MEDIUM,
                fg=ModernColors.TEXT_PRIMARY,
                anchor='w',
                cursor="hand2"
            )
            section_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            section_label.bind('<Button-1>', lambda e, s=section_name: self._toggle_section(s))

            # Boutons de réorganisation
            reorder_frame = tk.Frame(section_header, bg=ModernColors.BG_MEDIUM)
            reorder_frame.pack(side=tk.RIGHT, padx=10)

            # Bouton Up
            if idx > 0:  # Pas de bouton Up pour le premier
                up_btn = tk.Label(
                    reorder_frame,
                    text="▲",
                    font=("Segoe UI", 10),
                    bg=ModernColors.BG_MEDIUM,
                    fg=ModernColors.TEXT_SECONDARY,
                    cursor="hand2",
                    padx=5
                )
                up_btn.pack(side=tk.LEFT, padx=2)
                up_btn.bind('<Button-1>', lambda e, s=section_name: self._move_section_up(s))
                up_btn.bind('<Enter>', lambda e, b=up_btn: b.config(fg=ModernColors.ORANGE_PRIMARY))
                up_btn.bind('<Leave>', lambda e, b=up_btn: b.config(fg=ModernColors.TEXT_SECONDARY))

            # Bouton Down
            if idx < len(self.section_order) - 1:  # Pas de bouton Down pour le dernier
                down_btn = tk.Label(
                    reorder_frame,
                    text="▼",
                    font=("Segoe UI", 10),
                    bg=ModernColors.BG_MEDIUM,
                    fg=ModernColors.TEXT_SECONDARY,
                    cursor="hand2",
                    padx=5
                )
                down_btn.pack(side=tk.LEFT, padx=2)
                down_btn.bind('<Button-1>', lambda e, s=section_name: self._move_section_down(s))
                down_btn.bind('<Enter>', lambda e, b=down_btn: b.config(fg=ModernColors.ORANGE_PRIMARY))
                down_btn.bind('<Leave>', lambda e, b=down_btn: b.config(fg=ModernColors.TEXT_SECONDARY))

            # Grille de boutons (visible seulement si pas collapsed)
            if not is_collapsed:
                grid_frame = tk.Frame(section_container, bg=ModernColors.BG_DARK)
                grid_frame.pack(fill=tk.X, padx=5, pady=(10, 10))

                row = 0
                col = 0
                for tool_name, tool_action, tool_icon in tools:
                    btn = ModernToolButton(grid_frame, tool_name, tool_action, tool_icon)
                    btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

                    col += 1
                    if col >= 6:  # 6 colonnes
                        col = 0
                        row += 1

                # Configurer les colonnes pour expansion égale
                for i in range(6):
                    grid_frame.columnconfigure(i, weight=1, uniform="col")

                self.section_frames[section_name] = grid_frame

    def _toggle_section(self, section_name):
        """Toggle l'état collapsed d'une section"""
        current_state = self.collapsed_sections.get(section_name, False)
        self.collapsed_sections[section_name] = not current_state
        self._display_tools()

    def _move_section_up(self, section_name):
        """Déplacer une section vers le haut"""
        idx = self.section_order.index(section_name)
        if idx > 0:
            # Échanger avec la section précédente
            self.section_order[idx], self.section_order[idx - 1] = \
                self.section_order[idx - 1], self.section_order[idx]
            # Sauvegarder l'ordre personnalisé
            self.layout_manager.set_category_order("tools", self.section_order)
            self._display_tools()

    def _move_section_down(self, section_name):
        """Déplacer une section vers le bas"""
        idx = self.section_order.index(section_name)
        if idx < len(self.section_order) - 1:
            # Échanger avec la section suivante
            self.section_order[idx], self.section_order[idx + 1] = \
                self.section_order[idx + 1], self.section_order[idx]
            # Sauvegarder l'ordre personnalisé
            self.layout_manager.set_category_order("tools", self.section_order)
            self._display_tools()

    def _on_search(self, query):
        """Filtrer les outils par recherche"""
        if not query or query.strip() == "":
            # Aucun filtre, afficher tout
            self.filtered_tools = self.tools_data.copy()
        else:
            # Filtrer les outils par nom (insensible à la casse)
            query_lower = query.lower().strip()
            self.filtered_tools = {}

            for section_name, tools in self.tools_data.items():
                # Filtrer les outils de cette section
                filtered = [
                    (name, action, icon) for name, action, icon in tools
                    if query_lower in name.lower()
                ]

                # N'ajouter la section que si elle contient des résultats
                if filtered:
                    self.filtered_tools[section_name] = filtered

        # Réafficher avec le filtre appliqué
        self._display_tools()


class MasterInstallationPage(tk.Frame):
    """Page Master Installation Windows - Installation rapide d'applications essentielles"""

    def __init__(self, parent):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self.selected_apps = set()
        self.app_checkboxes = {}
        self._create_widgets()

    def _get_master_apps(self):
        """Obtenir la liste des applications Master Installation"""
        return {
            "Adobe Acrobat Reader": {
                "url": "https://get.adobe.com/reader/",
                "portable": False,
                "description": "Lecteur PDF officiel d'Adobe"
            },
            "VLC Media Player": {
                "url": "https://www.videolan.org/vlc/",
                "portable": False,
                "description": "Lecteur multimédia universel"
            },
            "Pack Office 2007": {
                "url": "https://gravesoft.dev/office_c2r_links#2007",
                "portable": False,
                "description": "Suite bureautique Microsoft Office 2007"
            },
            "Pack Office 2024": {
                "url": "https://gravesoft.dev/office_c2r_links#2024",
                "portable": False,
                "description": "Suite bureautique Microsoft Office 2024"
            },
            "Spybot Search & Destroy": {
                "url": "https://www.safer-networking.org/download/",
                "portable": False,
                "description": "Anti-malware et protection système"
            },
            "AdwCleaner": {
                "url": "https://www.malwarebytes.com/adwcleaner",
                "portable": True,
                "exe_name": "adwcleaner.exe",
                "description": "Suppression des adwares (Portable)"
            },
            "AnyDesk": {
                "url": "https://anydesk.com/en/downloads/thank-you?dv=win_exe",
                "portable": True,
                "exe_name": "AnyDesk.exe",
                "description": "Contrôle à distance (Portable)"
            },
            "RustDesk": {
                "url": "https://github.com/rustdesk/rustdesk/releases/latest",
                "portable": True,
                "exe_name": "rustdesk.exe",
                "description": "Contrôle à distance open-source (Portable)"
            },
            "Wise Disk Cleaner": {
                "url": "https://www.wisecleaner.com/wise-disk-cleaner.html",
                "portable": False,
                "description": "Nettoyage et optimisation du disque"
            },
            "Malwarebytes": {
                "url": "https://www.malwarebytes.com/",
                "portable": False,
                "description": "Protection anti-malware avancée"
            },
            "Firefox": {
                "url": "https://www.mozilla.org/firefox/download/",
                "portable": False,
                "description": "Navigateur web Mozilla Firefox"
            },
        }

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Container principal avec disposition en 2 colonnes
        main_container = tk.Frame(self, bg=ModernColors.BG_DARK)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Colonne gauche : Applications
        left_column = tk.Frame(main_container, bg=ModernColors.BG_DARK)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header = tk.Frame(left_column, bg=ModernColors.BG_DARK)
        header.pack(fill=tk.X, pady=(0, 20))

        title_label = tk.Label(
            header,
            text="🚀 Master Installation Windows",
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        subtitle_label = tk.Label(
            header,
            text="Installation rapide des outils essentiels",
            font=("Segoe UI", 11),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_SECONDARY
        )
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0))

        # Boutons d'action rapide
        actions_frame = tk.Frame(left_column, bg=ModernColors.BG_DARK)
        actions_frame.pack(fill=tk.X, pady=(0, 20))

        select_all_btn = tk.Button(
            actions_frame,
            text="✓ Tout sélectionner",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_PRIMARY,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self._select_all
        )
        select_all_btn.pack(side=tk.LEFT, padx=(0, 10))

        deselect_all_btn = tk.Button(
            actions_frame,
            text="✕ Tout désélectionner",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.RED_ERROR,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self._deselect_all
        )
        deselect_all_btn.pack(side=tk.LEFT)

        # Zone de scroll pour les applications
        scroll_frame = tk.Frame(left_column, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Afficher les applications en grille 6 colonnes
        apps = self._get_master_apps()

        # Créer une grille pour les applications
        grid_frame = tk.Frame(scrollable_frame, bg=ModernColors.BG_DARK)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        row = 0
        col = 0
        for app_name, app_data in apps.items():
            card = self._create_app_card_grid(grid_frame, app_name, app_data)
            card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

            col += 1
            if col >= 6:  # 6 colonnes
                col = 0
                row += 1

        # Configurer les colonnes pour expansion égale
        for i in range(6):
            grid_frame.columnconfigure(i, weight=1, uniform="col")

        # Bouton d'installation
        install_btn = tk.Button(
            left_column,
            text="🚀 INSTALLER LES APPLICATIONS SÉLECTIONNÉES",
            font=("Segoe UI", 12, "bold"),
            bg=ModernColors.ORANGE_PRIMARY,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=15,
            command=self._start_installation
        )
        install_btn.pack(fill=tk.X, pady=(20, 0))

        # Colonne droite : Actions spéciales avec scrollbar
        right_column = tk.Frame(main_container, bg=ModernColors.BG_DARK, width=650)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 20), pady=20)
        right_column.pack_propagate(False)

        # Titre section droite
        right_title = tk.Label(
            right_column,
            text="⚡ Actions Rapides",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.ORANGE_PRIMARY
        )
        right_title.pack(pady=(0, 15))

        # Zone de scroll pour les boutons
        scroll_frame = tk.Frame(right_column, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        scrollable_buttons = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        scrollable_buttons.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_buttons, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mousewheel avec gestion intelligente
        bind_mousewheel(canvas, scrollable_buttons)

        # Grille 3 colonnes pour les boutons
        buttons_grid = tk.Frame(scrollable_buttons, bg=ModernColors.BG_DARK)
        buttons_grid.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configurer la grille 3 colonnes
        buttons_grid.columnconfigure(0, weight=1, uniform="col")
        buttons_grid.columnconfigure(1, weight=1, uniform="col")
        buttons_grid.columnconfigure(2, weight=1, uniform="col")

        # Fonction helper pour créer et placer les boutons
        def create_action_button(icon, title, description, color, command, row, col):
            card = tk.Frame(buttons_grid, bg=ModernColors.BG_CARD)
            card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

            content = tk.Frame(card, bg=ModernColors.BG_CARD)
            content.pack(fill=tk.BOTH, padx=12, pady=12)

            icon_label = tk.Label(
                content,
                text=icon,
                font=("Segoe UI", 20),
                bg=ModernColors.BG_CARD,
                fg=color
            )
            icon_label.pack()

            title_label = tk.Label(
                content,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_PRIMARY
            )
            title_label.pack(pady=(5, 0))

            if description:
                desc_label = tk.Label(
                    content,
                    text=description,
                    font=("Segoe UI", 8),
                    bg=ModernColors.BG_CARD,
                    fg=ModernColors.TEXT_SECONDARY,
                    justify=tk.CENTER
                )
                desc_label.pack()

            btn = tk.Button(
                content,
                text=title.split()[0],  # Premier mot comme texte du bouton
                font=("Segoe UI", 9),
                bg=color,
                fg=ModernColors.TEXT_PRIMARY,
                activebackground=ModernColors.ORANGE_PRIMARY,
                relief=tk.FLAT,
                cursor="hand2",
                padx=15,
                pady=6,
                command=command
            )
            btn.pack(pady=(8, 0))

            return card

        # Créer tous les boutons dans la grille 3 colonnes
        button_row = 0

        # Ligne 1
        create_action_button(
            "🔑", "MassGrave Scripts", "Activation Windows & Office",
            ModernColors.ORANGE_PRIMARY,
            lambda: webbrowser.open("https://massgrave.dev/"),
            button_row, 0
        )
        create_action_button(
            "⚡", "Activation Auto", "Script automatique\n(Bypass UAC)",
            ModernColors.GREEN_SUCCESS,
            self._run_activation_script,
            button_row, 1
        )
        create_action_button(
            "📁", "Outils Portables", "Créer dossier Bureau\n'Outils de Nettoyage'",
            ModernColors.BLUE_INFO,
            self._create_portable_folder,
            button_row, 2
        )
        button_row += 1

        # Ligne 2
        create_action_button(
            "📋", "Office FR", "Télécharger Office\nen français",
            ModernColors.PURPLE_PREMIUM,
            lambda: webbrowser.open("https://gravesoft.dev/office_c2r_links#french-fr-fr"),
            button_row, 0
        )
        create_action_button(
            "⚙️", "MSConfig", "Configuration système",
            ModernColors.YELLOW_WARNING,
            self._open_msconfig,
            button_row, 1
        )
        create_action_button(
            "🔄", "Windows Update", "Mises à jour Windows",
            ModernColors.BLUE_INFO,
            lambda: os.system("start ms-settings:windowsupdate"),
            button_row, 2
        )
        button_row += 1

        # Ligne 3 - Nouveaux outils système
        create_action_button(
            "💾", "Disque C:", "Ouvrir le disque C:",
            ModernColors.BLUE_INFO,
            lambda: os.system("explorer C:\\"),
            button_row, 0
        )
        create_action_button(
            "🚀", "Apps Démarrage", "Gestionnaire des tâches\nApplications de démarrage",
            ModernColors.PURPLE_PREMIUM,
            lambda: os.system("start ms-settings:startupapps"),
            button_row, 1
        )
        create_action_button(
            "⚡", "Terminal Admin", "PowerShell\nadministrateur",
            ModernColors.RED_ERROR,
            self._open_admin_terminal,
            button_row, 2
        )
        button_row += 1

        # Ligne 4 - Outils système supplémentaires
        create_action_button(
            "📋", "Rapport Système", "Générer rapport détaillé\nde configuration PC",
            ModernColors.GREEN_SUCCESS,
            self._generate_system_report,
            button_row, 0
        )
        create_action_button(
            "🪟", "Version Windows", "Afficher infos\nWindows (winver)",
            ModernColors.BLUE_INFO,
            lambda: os.system("winver"),
            button_row, 1
        )
        create_action_button(
            "ℹ️", "Infos Système", "Informations système\n(msinfo32)",
            ModernColors.PURPLE_PREMIUM,
            lambda: os.system("msinfo32"),
            button_row, 2
        )
        button_row += 1

        # Séparateur WinGet
        winget_separator = tk.Frame(buttons_grid, bg=ModernColors.ORANGE_PRIMARY, height=2)
        winget_separator.grid(row=button_row, column=0, columnspan=3, sticky='ew', pady=(15, 10))
        button_row += 1

        # Titre WinGet
        winget_title = tk.Label(
            buttons_grid,
            text="📦 WinGet Manager",
            font=("Segoe UI", 14, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.ORANGE_PRIMARY
        )
        winget_title.grid(row=button_row, column=0, columnspan=3, pady=(0, 10))
        button_row += 1

        # Ligne WinGet (2 boutons sur 3 colonnes)
        create_action_button(
            "⬆️", "Tout Mettre à Jour", "winget upgrade --all",
            ModernColors.GREEN_SUCCESS,
            lambda: os.system("start cmd /k winget upgrade --all"),
            button_row, 0
        )
        create_action_button(
            "📋", "Lister Mises à Jour", "winget upgrade",
            ModernColors.BLUE_INFO,
            lambda: os.system("start cmd /k winget upgrade"),
            button_row, 1
        )

    def _create_app_card_grid(self, parent, app_name, app_data):
        """Créer une carte compacte pour la grille"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD, relief=tk.FLAT, bd=0)

        container = tk.Frame(card, bg=ModernColors.BG_CARD)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Checkbox
        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(
            container,
            variable=checkbox_var,
            bg=ModernColors.BG_CARD,
            fg=ModernColors.ORANGE_PRIMARY,
            selectcolor=ModernColors.BG_DARK,
            activebackground=ModernColors.BG_CARD,
            command=lambda: self._on_app_select(app_name, checkbox_var.get())
        )
        checkbox.pack(anchor='w')
        self.app_checkboxes[app_name] = checkbox_var

        # Nom de l'app (plus petit pour la grille)
        name_label = tk.Label(
            container,
            text=app_name,
            font=("Segoe UI", 9, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w',
            wraplength=120
        )
        name_label.pack(fill=tk.X, pady=(3, 0))

        # Badge portable si applicable
        if app_data.get('portable'):
            portable_badge = tk.Label(
                container,
                text="💼",
                font=("Segoe UI", 10),
                bg=ModernColors.BG_CARD,
                fg=ModernColors.GREEN_SUCCESS
            )
            portable_badge.pack(anchor='w', pady=(2, 0))

        # Bouton web (petit)
        web_btn = tk.Label(
            container,
            text="🌐",
            font=("Segoe UI", 12),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.BLUE_INFO,
            cursor="hand2"
        )
        web_btn.pack(anchor='w', pady=(5, 0))
        web_btn.bind('<Button-1>', lambda e: webbrowser.open(app_data['url']))

        # Ajouter effet hover
        def on_enter(e):
            card.config(highlightthickness=2, highlightbackground=ModernColors.ORANGE_PRIMARY)

        def on_leave(e):
            card.config(highlightthickness=0)

        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)

        return card

    def _create_app_card(self, parent, app_name, app_data):
        """Créer une carte pour une application"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=5)

        container = tk.Frame(card, bg=ModernColors.BG_CARD)
        container.pack(fill=tk.X, padx=15, pady=12)

        # Checkbox et nom
        top_frame = tk.Frame(container, bg=ModernColors.BG_CARD)
        top_frame.pack(fill=tk.X)

        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(
            top_frame,
            variable=checkbox_var,
            bg=ModernColors.BG_CARD,
            fg=ModernColors.ORANGE_PRIMARY,
            selectcolor=ModernColors.BG_DARK,
            activebackground=ModernColors.BG_CARD,
            command=lambda: self._on_app_select(app_name, checkbox_var.get())
        )
        checkbox.pack(side=tk.LEFT)
        self.app_checkboxes[app_name] = checkbox_var

        name_label = tk.Label(
            top_frame,
            text=app_name,
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w'
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Badge portable si applicable
        if app_data.get('portable'):
            portable_badge = tk.Label(
                top_frame,
                text="💼 Portable",
                font=("Segoe UI", 8),
                bg=ModernColors.GREEN_SUCCESS,
                fg=ModernColors.TEXT_PRIMARY,
                padx=6,
                pady=2
            )
            portable_badge.pack(side=tk.RIGHT, padx=(5, 0))

        # Bouton web
        web_btn = tk.Label(
            top_frame,
            text="🌐",
            font=("Segoe UI", 12),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.BLUE_INFO,
            cursor="hand2"
        )
        web_btn.pack(side=tk.RIGHT, padx=(5, 0))
        web_btn.bind('<Button-1>', lambda e: webbrowser.open(app_data['url']))

        # Description
        desc_label = tk.Label(
            container,
            text=app_data['description'],
            font=("Segoe UI", 9),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            justify=tk.LEFT
        )
        desc_label.pack(fill=tk.X, padx=(26, 0), pady=(5, 0))

    def _on_app_select(self, app_name, is_selected):
        """Gérer la sélection d'une application"""
        if is_selected:
            self.selected_apps.add(app_name)
        else:
            self.selected_apps.discard(app_name)

    def _select_all(self):
        """Sélectionner toutes les applications"""
        for checkbox_var in self.app_checkboxes.values():
            checkbox_var.set(True)
        self.selected_apps = set(self.app_checkboxes.keys())

    def _deselect_all(self):
        """Désélectionner toutes les applications"""
        for checkbox_var in self.app_checkboxes.values():
            checkbox_var.set(False)
        self.selected_apps.clear()

    def _start_installation(self):
        """Démarrer l'installation des applications sélectionnées"""
        if not self.selected_apps:
            messagebox.showwarning(
                "Aucune sélection",
                "Veuillez sélectionner au moins une application à installer."
            )
            return

        count = len(self.selected_apps)
        apps = self._get_master_apps()

        # Construire le message avec les applications portables
        portable_apps = [name for name in self.selected_apps if apps[name].get('portable')]

        message = f"Vous êtes sur le point d'installer {count} application(s).\n\n"
        if portable_apps:
            message += f"⚠️  {len(portable_apps)} application(s) portable(s) seront copiées\n"
            message += f"dans le dossier 'Outils de Nettoyage' sur le Bureau.\n\n"

        message += "Les téléchargements seront ouverts dans votre navigateur.\n"
        message += "Continuer ?"

        response = messagebox.askyesno("Confirmation d'installation", message)

        if response:
            self._execute_installation()

    def _execute_installation(self):
        """Exécuter l'installation des applications"""
        apps = self._get_master_apps()

        for app_name in self.selected_apps:
            app_data = apps[app_name]
            # Ouvrir l'URL de téléchargement
            try:
                webbrowser.open(app_data['url'])
            except Exception as e:
                logger.error(f"Erreur lors de l'ouverture de {app_name}: {e}")

        messagebox.showinfo(
            "Installation lancée",
            f"{len(self.selected_apps)} pages de téléchargement ont été ouvertes.\n\n"
            "Téléchargez et installez les applications.\n"
            "Les applications portables peuvent être copiées dans\n"
            "le dossier 'Outils de Nettoyage' sur le Bureau."
        )

    def _open_msconfig(self):
        """Ouvrir MSConfig (Configuration système)"""
        try:
            # Exécuter msconfig directement
            os.system("msconfig")
            logger.info("MSConfig ouvert avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture de MSConfig: {e}")
            messagebox.showerror(
                "Erreur",
                f"Impossible d'ouvrir MSConfig.\n\n{str(e)}"
            )

    def _run_activation_script(self):
        """Exécuter le script d'activation Windows avec bypass UAC"""
        response = messagebox.askyesno(
            "Activation Windows",
            "⚠️  ATTENTION  ⚠️\n\n"
            "Ce script va exécuter les commandes d'activation Windows.\n"
            "Il nécessite des privilèges administrateur.\n\n"
            "Le script va :\n"
            "• Télécharger le script d'activation\n"
            "• L'exécuter automatiquement\n"
            "• Activer Windows et/ou Office\n\n"
            "Continuer ?"
        )

        if response:
            try:
                # Exécuter la commande PowerShell avec bypass UAC
                command = 'powershell -ExecutionPolicy Bypass -Command "irm https://get.activated.win | iex"'
                os.system(command)

                messagebox.showinfo(
                    "Script lancé",
                    "Le script d'activation a été lancé.\n"
                    "Suivez les instructions dans la fenêtre PowerShell."
                )
            except Exception as e:
                logger.error(f"Erreur lors de l'exécution du script d'activation: {e}")
                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'exécuter le script d'activation.\n\n{str(e)}"
                )

    def _create_portable_folder(self):
        """Créer le dossier 'Outils de Nettoyage' sur le Bureau"""
        try:
            # Obtenir le chemin du Bureau
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            if not os.path.exists(desktop):
                # Essayer avec le chemin français
                desktop = os.path.join(os.path.expanduser('~'), 'Bureau')

            # Créer le dossier
            tools_folder = os.path.join(desktop, 'Outils de Nettoyage')
            os.makedirs(tools_folder, exist_ok=True)

            # Créer un fichier README
            readme_path = os.path.join(tools_folder, 'README.txt')
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("=== OUTILS DE NETTOYAGE PORTABLES ===\n\n")
                f.write("Ce dossier contient des outils portables pour le nettoyage et la maintenance.\n\n")
                f.write("Applications portables recommandées :\n")
                f.write("• AdwCleaner - Suppression des adwares\n")
                f.write("• AnyDesk - Contrôle à distance\n")
                f.write("• RustDesk - Contrôle à distance open-source\n\n")
                f.write("Téléchargez ces applications et copiez les .exe dans ce dossier.\n")
                f.write("Elles pourront être exécutées sans installation.\n\n")
                f.write(f"Créé par NiTriTe V13.0 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

            messagebox.showinfo(
                "Dossier créé",
                f"Le dossier 'Outils de Nettoyage' a été créé sur le Bureau.\n\n"
                f"Chemin : {tools_folder}\n\n"
                f"Vous pouvez maintenant y copier vos applications portables."
            )

            # Ouvrir le dossier dans l'explorateur
            os.startfile(tools_folder)

        except Exception as e:
            logger.error(f"Erreur lors de la création du dossier portable: {e}")
            messagebox.showerror(
                "Erreur",
                f"Impossible de créer le dossier 'Outils de Nettoyage'.\n\n{str(e)}"
            )

    def _open_admin_terminal(self):
        """Ouvrir PowerShell en mode administrateur"""
        try:
            # Exécuter PowerShell en admin avec élévation UAC
            os.system('powershell -Command "Start-Process powershell -Verb RunAs"')
            logger.info("Terminal administrateur ouvert avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture du terminal admin: {e}")
            messagebox.showerror(
                "Erreur",
                f"Impossible d'ouvrir le terminal en mode administrateur.\n\n{str(e)}"
            )

    def _generate_system_report(self):
        """Générer un rapport détaillé de la configuration système"""
        try:
            # Obtenir le chemin du Bureau
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            if not os.path.exists(desktop):
                desktop = os.path.join(os.path.expanduser('~'), 'Bureau')

            # Nom du fichier rapport
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = os.path.join(desktop, f'Rapport_Systeme_{timestamp}.txt')

            # Créer le rapport avec systeminfo
            messagebox.showinfo(
                "Génération en cours",
                "Le rapport système est en cours de génération.\n"
                "Cela peut prendre quelques secondes...\n\n"
                "Le rapport sera sauvegardé sur le Bureau."
            )

            # Exécuter systeminfo et sauvegarder dans le fichier
            command = f'systeminfo > "{report_path}"'
            result = os.system(command)

            if result == 0 and os.path.exists(report_path):
                # Ajouter des informations supplémentaires au rapport
                with open(report_path, 'a', encoding='utf-8') as f:
                    f.write("\n\n" + "="*80 + "\n")
                    f.write("INFORMATIONS ADDITIONNELLES\n")
                    f.write("="*80 + "\n\n")
                    f.write(f"Rapport généré par NiTriTe V13.0\n")
                    f.write(f"Date et heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

                messagebox.showinfo(
                    "Rapport généré",
                    f"Le rapport système a été généré avec succès !\n\n"
                    f"Fichier : Rapport_Systeme_{timestamp}.txt\n"
                    f"Emplacement : Bureau\n\n"
                    f"Le rapport va s'ouvrir automatiquement."
                )

                # Ouvrir le fichier
                os.startfile(report_path)
            else:
                raise Exception("Échec de la génération du rapport")

        except Exception as e:
            logger.error(f"Erreur lors de la génération du rapport système: {e}")
            messagebox.showerror(
                "Erreur",
                f"Impossible de générer le rapport système.\n\n{str(e)}"
            )


class NiTriTeModernGUI:
    """Interface principale moderne de NiTriTe V13"""

    def __init__(self):
        # Charger et appliquer le thème préféré
        theme_id = ThemeManager.load_theme_preference()
        ThemeManager.apply_theme(theme_id, None)

        self.root = tk.Tk()
        self.root.title("NiTriTe V13.0 - Maintenance Informatique Pro")
        self.root.geometry("1400x900")
        self.root.configure(bg=ModernColors.BG_DARK)

        # Données
        self.programs_data = self._load_programs_data()

        # Pages
        self.current_page = None
        self.pages = {}

        self._setup_ui()
        self._show_page("applications")

        # Style
        self._configure_style()

    def _load_programs_data(self):
        """Charger les données des programmes"""
        try:
            # Déterminer le chemin du fichier programs.json
            if getattr(sys, 'frozen', False):
                # Mode exécutable
                base_path = sys._MEIPASS
            else:
                # Mode script
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            programs_file = os.path.join(base_path, 'data', 'programs.json')

            if not os.path.exists(programs_file):
                logger.warning(f"Fichier programs.json introuvable : {programs_file}")
                return self._get_sample_programs()

            with open(programs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.info(f"Chargé {sum(len(apps) for apps in data.values())} applications")
            return data

        except Exception as e:
            logger.error(f"Erreur lors du chargement des programmes : {e}")
            messagebox.showerror(
                "Erreur",
                f"Impossible de charger la liste des programmes\n{str(e)}"
            )
            return self._get_sample_programs()

    def _get_sample_programs(self):
        """Obtenir des programmes d'exemple"""
        return {
            "Exemple": {
                "Application Test": {
                    "description": "Application de test",
                    "category": "Test",
                    "download_url": "https://example.com",
                    "portable": False
                }
            }
        }

    def _setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Conteneur principal
        main_container = tk.Frame(self.root, bg=ModernColors.BG_DARK)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Barre de navigation latérale
        self.nav_bar = ModernNavigationBar(main_container, self._on_page_change)
        self.nav_bar.pack(side=tk.LEFT, fill=tk.Y)

        # Zone de contenu
        self.content_area = tk.Frame(main_container, bg=ModernColors.BG_DARK)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Créer les pages
        self.pages['applications'] = ApplicationsPage(self.content_area, self.programs_data)
        self.pages['tools'] = ToolsPage(self.content_area)
        self.pages['master_install'] = MasterInstallationPage(self.content_area)
        self.pages['updates'] = UpdatesPage(self.content_area, self.programs_data)
        self.pages['backup'] = BackupPage(self.content_area)
        self.pages['optimizations'] = OptimizationsPage(self.content_area)
        self.pages['diagnostic'] = DiagnosticPage(self.content_area)
        self.pages['settings'] = SettingsPage(self.content_area, self.root)

    def _configure_style(self):
        """Configurer les styles ttk"""
        style = ttk.Style()
        style.theme_use('clam')

        # Style de la scrollbar
        style.configure(
            "Vertical.TScrollbar",
            background=ModernColors.BG_CARD,
            troughcolor=ModernColors.BG_DARK,
            borderwidth=0,
            arrowcolor=ModernColors.ORANGE_PRIMARY
        )

    def _on_page_change(self, page_id):
        """Gérer le changement de page"""
        self._show_page(page_id)

    def _show_page(self, page_id):
        """Afficher une page"""
        # Cacher la page actuelle
        if self.current_page:
            self.pages[self.current_page].pack_forget()

        # Afficher la nouvelle page
        if page_id in self.pages:
            self.pages[page_id].pack(fill=tk.BOTH, expand=True)
            self.current_page = page_id

    def run(self):
        """Lancer l'application"""
        # Centrer la fenêtre
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        # Démarrer la boucle
        self.root.mainloop()


def main():
    """Point d'entrée principal"""
    try:
        app = NiTriTeModernGUI()
        app.run()
    except Exception as e:
        logger.error(f"Erreur fatale : {e}", exc_info=True)
        messagebox.showerror(
            "Erreur Fatale",
            f"Une erreur critique s'est produite :\n{str(e)}\n\n"
            "L'application va se fermer."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
