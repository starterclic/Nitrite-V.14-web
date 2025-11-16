#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NiTriTe V13.1 - Définition des couleurs
Module séparé pour éviter les imports circulaires
"""


class ModernColors:
    """Palette de couleurs moderne Noir & Orange Premium - Alignée sur la version web"""
    # Backgrounds (matching web version)
    BG_DARK = "#1a1a1a"  # Primary background (--bg-primary)
    BG_MEDIUM = "#2d2d2d"  # Secondary background (--bg-secondary)
    BG_LIGHT = "#3a3a3a"  # Tertiary background (--bg-tertiary)
    BG_CARD = "#252525"  # Card background (--bg-card)
    BG_HOVER = "#333333"  # Hover state (--bg-hover)

    # Orange accents (matching web version)
    ORANGE_PRIMARY = "#FF6B35"  # Primary orange (--primary-color)
    ORANGE_LIGHT = "#FF8C5A"  # Light orange (--primary-light)
    ORANGE_DARK = "#E85A28"  # Dark orange (--primary-dark)
    ORANGE_GLOW = "#FF6B35"  # Glow effect
    ORANGE_SECONDARY = "#F7931E"  # Secondary orange (--secondary-color)

    # Textes (matching web version)
    TEXT_PRIMARY = "#ffffff"  # Primary text (--text-primary)
    TEXT_SECONDARY = "#b0b0b0"  # Secondary text (--text-secondary)
    TEXT_MUTED = "#808080"  # Tertiary text (--text-tertiary)

    # Borders (matching web version)
    BORDER_COLOR = "#404040"  # Primary border (--border-color)
    BORDER_LIGHT = "#505050"  # Light border (--border-light)

    # Accents (matching web version)
    GREEN_SUCCESS = "#4CAF50"  # Success color (--success-color)
    RED_ERROR = "#F44336"  # Error color (--error-color)
    BLUE_INFO = "#2196F3"  # Info color
    PURPLE_PREMIUM = "#9C27B0"  # Premium color
    YELLOW_WARNING = "#FFA726"  # Warning color (--warning-color)


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
