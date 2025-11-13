#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NiTriTe V13.1 - Définition des couleurs
Module séparé pour éviter les imports circulaires
"""


class ModernColors:
    """Palette de couleurs moderne Noir & Orange Premium"""
    # Backgrounds
    BG_DARK = "#0a0a0a"  # Noir profond
    BG_MEDIUM = "#141414"  # Noir moyen
    BG_LIGHT = "#1e1e1e"  # Gris foncé
    BG_CARD = "#252525"  # Cartes
    BG_HOVER = "#2f2f2f"  # Hover

    # Orange accents
    ORANGE_PRIMARY = "#ff6b00"  # Orange principal
    ORANGE_LIGHT = "#ff8533"  # Orange clair
    ORANGE_DARK = "#cc5500"  # Orange foncé
    ORANGE_GLOW = "#ff6b00"  # Effet glow

    # Textes
    TEXT_PRIMARY = "#ffffff"  # Blanc
    TEXT_SECONDARY = "#b8b8b8"  # Gris clair
    TEXT_MUTED = "#707070"  # Gris moyen

    # Accents
    GREEN_SUCCESS = "#00e676"  # Vert succès
    RED_ERROR = "#ff1744"  # Rouge erreur
    BLUE_INFO = "#00b0ff"  # Bleu info
    PURPLE_PREMIUM = "#7c4dff"  # Violet premium
    YELLOW_WARNING = "#ffd600"  # Jaune warning


def bind_mousewheel(canvas, scrollable_frame):
    """
    Bind mousewheel to canvas for smooth scrolling.
    Activates when mouse enters the area and deactivates when it leaves.
    """
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def bound_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def unbound_to_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    # Bind sur le canvas et le frame scrollable
    canvas.bind('<Enter>', bound_to_mousewheel)
    canvas.bind('<Leave>', unbound_to_mousewheel)
    scrollable_frame.bind('<Enter>', bound_to_mousewheel)
    scrollable_frame.bind('<Leave>', unbound_to_mousewheel)
