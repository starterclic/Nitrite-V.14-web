#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de traduction pour NiTriTe V13.1
Support: Français, English
"""

TRANSLATIONS = {
    "fr": {
        # Navigation
        "applications": "Applications",
        "tools": "Outils Système",
        "master_install": "Master Installation",
        "updates": "Mises à Jour",
        "backup": "Backup & Restore",
        "optimizations": "Optimisations",
        "diagnostic": "Diagnostic",
        "settings": "Paramètres",

        # Applications page
        "apps_available": "apps disponibles",
        "tools_available": "boutons utiles",
        "search_placeholder": "Rechercher...",
        "install_selected": "INSTALLER SÉLECTION",
        "select_all": "Tout sélectionner",
        "deselect_all": "Tout désélectionner",

        # Diagnostic page
        "pc_health_score": "Score de Santé PC",
        "system_info": "Informations Système",
        "current_performance": "Performance Actuelle",
        "benchmark": "Benchmark & Tests",
        "refresh": "Rafraîchir",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "Disque",
        "gpu": "Carte Graphique",
        "os_version": "Version OS",
        "processor": "Processeur",
        "graphics_card": "Carte Graphique",
        "disk_type": "Type de Disque",
        "excellent": "Excellent",
        "good": "Bon",
        "average": "Moyen",
        "poor": "Faible",

        # Settings page
        "settings_themes": "Paramètres & Thèmes",
        "available_themes": "Thèmes disponibles",
        "preferences": "Préférences",
        "language": "Langue",
        "appearance": "Apparence",
        "dark_mode": "Mode Sombre",
        "light_mode": "Mode Clair",
        "french": "Français",
        "english": "English",
        "apply": "Appliquer",
        "save": "Sauvegarder",
        "cancel": "Annuler",

        # Optimizations page
        "windows_optimizations": "Optimisations Windows",
        "privacy_telemetry": "Confidentialité & Télémétrie",
        "services_management": "Gestion des Services",
        "startup_management": "Gestion du Démarrage",
        "registry_cleanup": "Nettoyage du Registre",
        "disable_telemetry": "Désactiver Télémétrie",
        "disable_cortana": "Désactiver Cortana",
        "disable_tracking": "Désactiver Tracking",

        # Backup page
        "backup_restore": "Backup & Restauration",
        "create_restore_point": "Créer Point de Restauration",
        "backup_drivers": "Backup Drivers",
        "backup_app_list": "Sauvegarder Liste Apps",

        # Updates page
        "updates_checks": "Vérifications & Mises à Jour",
        "detect_apps": "Détecter Apps Installées",
        "check_updates": "Vérifier Updates",
        "generate_script": "Générer Script",

        # Master Windows
        "master_windows": "Master Windows",
        "quick_actions": "Actions Rapides",
        "system_info_cmd": "Informations Système",
        "windows_version": "Version Windows (winver)",
    },
    "en": {
        # Navigation
        "applications": "Applications",
        "tools": "System Tools",
        "master_install": "Master Installation",
        "updates": "Updates",
        "backup": "Backup & Restore",
        "optimizations": "Optimizations",
        "diagnostic": "Diagnostic",
        "settings": "Settings",

        # Applications page
        "apps_available": "apps available",
        "tools_available": "useful buttons",
        "search_placeholder": "Search...",
        "install_selected": "INSTALL SELECTION",
        "select_all": "Select All",
        "deselect_all": "Deselect All",

        # Diagnostic page
        "pc_health_score": "PC Health Score",
        "system_info": "System Information",
        "current_performance": "Current Performance",
        "benchmark": "Benchmark & Tests",
        "refresh": "Refresh",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "Disk",
        "gpu": "Graphics Card",
        "os_version": "OS Version",
        "processor": "Processor",
        "graphics_card": "Graphics Card",
        "disk_type": "Disk Type",
        "excellent": "Excellent",
        "good": "Good",
        "average": "Average",
        "poor": "Poor",

        # Settings page
        "settings_themes": "Settings & Themes",
        "available_themes": "Available Themes",
        "preferences": "Preferences",
        "language": "Language",
        "appearance": "Appearance",
        "dark_mode": "Dark Mode",
        "light_mode": "Light Mode",
        "french": "Français",
        "english": "English",
        "apply": "Apply",
        "save": "Save",
        "cancel": "Cancel",

        # Optimizations page
        "windows_optimizations": "Windows Optimizations",
        "privacy_telemetry": "Privacy & Telemetry",
        "services_management": "Services Management",
        "startup_management": "Startup Management",
        "registry_cleanup": "Registry Cleanup",
        "disable_telemetry": "Disable Telemetry",
        "disable_cortana": "Disable Cortana",
        "disable_tracking": "Disable Tracking",

        # Backup page
        "backup_restore": "Backup & Restore",
        "create_restore_point": "Create Restore Point",
        "backup_drivers": "Backup Drivers",
        "backup_app_list": "Backup App List",

        # Updates page
        "updates_checks": "Updates & Checks",
        "detect_apps": "Detect Installed Apps",
        "check_updates": "Check Updates",
        "generate_script": "Generate Script",

        # Master Windows
        "master_windows": "Master Windows",
        "quick_actions": "Quick Actions",
        "system_info_cmd": "System Information",
        "windows_version": "Windows Version (winver)",
    }
}

# Langue par défaut
CURRENT_LANGUAGE = "fr"

def set_language(lang_code):
    """Définir la langue de l'application"""
    global CURRENT_LANGUAGE
    if lang_code in TRANSLATIONS:
        CURRENT_LANGUAGE = lang_code
        return True
    return False

def get_text(key):
    """Obtenir le texte traduit pour une clé"""
    return TRANSLATIONS.get(CURRENT_LANGUAGE, {}).get(key, key)

def _(key):
    """Alias court pour get_text()"""
    return get_text(key)
