#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion de l'ordre personnalisé des éléments
Permet de réorganiser les applications, outils et catégories
Sauvegarde l'ordre dans un fichier JSON
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
import logging

# Import du module de chemins portables
try:
    from .portable_paths import get_portable_config_dir
except ImportError:
    try:
        from portable_paths import get_portable_config_dir
    except ImportError:
        # Fallback si pas disponible
        def get_portable_config_dir():
            return Path.home() / '.nitrite'

logger = logging.getLogger(__name__)


class LayoutManager:
    """Gestionnaire de l'ordre personnalisé des éléments"""

    def __init__(self):
        """Initialiser le gestionnaire"""
        self.config_dir = get_portable_config_dir()
        self.layout_file = self.config_dir / 'custom_layout.json'
        self.layouts = self._load_layouts()

    def _load_layouts(self) -> Dict[str, Any]:
        """Charger les layouts personnalisés depuis le fichier"""
        if not self.layout_file.exists():
            logger.info("Aucun layout personnalisé trouvé, utilisation des valeurs par défaut")
            return {}

        try:
            with open(self.layout_file, 'r', encoding='utf-8') as f:
                layouts = json.load(f)
            logger.info(f"Layouts personnalisés chargés depuis {self.layout_file}")
            return layouts
        except Exception as e:
            logger.error(f"Erreur lors du chargement des layouts: {e}")
            return {}

    def _save_layouts(self):
        """Sauvegarder les layouts personnalisés dans le fichier"""
        try:
            # Créer le dossier si nécessaire
            self.config_dir.mkdir(parents=True, exist_ok=True)

            with open(self.layout_file, 'w', encoding='utf-8') as f:
                json.dump(self.layouts, f, indent=2, ensure_ascii=False)

            logger.info(f"Layouts personnalisés sauvegardés dans {self.layout_file}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des layouts: {e}")

    def get_category_order(self, page_name: str) -> List[str]:
        """Obtenir l'ordre des catégories pour une page"""
        return self.layouts.get(f"{page_name}_categories", [])

    def set_category_order(self, page_name: str, categories: List[str]):
        """Définir l'ordre des catégories pour une page"""
        self.layouts[f"{page_name}_categories"] = categories
        self._save_layouts()
        logger.info(f"Ordre des catégories pour {page_name} sauvegardé")

    def get_items_order(self, page_name: str, category: str) -> List[str]:
        """Obtenir l'ordre des éléments dans une catégorie"""
        key = f"{page_name}_{category}_items"
        return self.layouts.get(key, [])

    def set_items_order(self, page_name: str, category: str, items: List[str]):
        """Définir l'ordre des éléments dans une catégorie"""
        key = f"{page_name}_{category}_items"
        self.layouts[key] = items
        self._save_layouts()
        logger.info(f"Ordre des éléments pour {page_name}/{category} sauvegardé")

    def move_category_up(self, page_name: str, current_categories: List[str], category: str):
        """Déplacer une catégorie vers le haut"""
        if category not in current_categories:
            return current_categories

        index = current_categories.index(category)
        if index > 0:
            # Échanger avec l'élément précédent
            current_categories[index], current_categories[index - 1] = \
                current_categories[index - 1], current_categories[index]
            self.set_category_order(page_name, current_categories)

        return current_categories

    def move_category_down(self, page_name: str, current_categories: List[str], category: str):
        """Déplacer une catégorie vers le bas"""
        if category not in current_categories:
            return current_categories

        index = current_categories.index(category)
        if index < len(current_categories) - 1:
            # Échanger avec l'élément suivant
            current_categories[index], current_categories[index + 1] = \
                current_categories[index + 1], current_categories[index]
            self.set_category_order(page_name, current_categories)

        return current_categories

    def move_item_up(self, page_name: str, category: str, current_items: List[str], item: str):
        """Déplacer un élément vers le haut dans sa catégorie"""
        if item not in current_items:
            return current_items

        index = current_items.index(item)
        if index > 0:
            # Échanger avec l'élément précédent
            current_items[index], current_items[index - 1] = \
                current_items[index - 1], current_items[index]
            self.set_items_order(page_name, category, current_items)

        return current_items

    def move_item_down(self, page_name: str, category: str, current_items: List[str], item: str):
        """Déplacer un élément vers le bas dans sa catégorie"""
        if item not in current_items:
            return current_items

        index = current_items.index(item)
        if index < len(current_items) - 1:
            # Échanger avec l'élément suivant
            current_items[index], current_items[index + 1] = \
                current_items[index + 1], current_items[index]
            self.set_items_order(page_name, category, current_items)

        return current_items

    def apply_order(self, page_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Appliquer l'ordre personnalisé à un dictionnaire de données

        Args:
            page_name: Nom de la page (ex: "applications", "tools")
            data: Dictionnaire avec clés = catégories, valeurs = éléments

        Returns:
            Dictionnaire réorganisé selon l'ordre personnalisé
        """
        # Obtenir l'ordre des catégories
        custom_category_order = self.get_category_order(page_name)

        if not custom_category_order:
            # Pas d'ordre personnalisé, retourner tel quel
            return data

        # Réorganiser les catégories
        ordered_data = {}

        # D'abord les catégories dans l'ordre personnalisé
        for category in custom_category_order:
            if category in data:
                # Obtenir l'ordre des éléments pour cette catégorie
                custom_items_order = self.get_items_order(page_name, category)

                if custom_items_order and isinstance(data[category], dict):
                    # Réorganiser les éléments de la catégorie
                    ordered_items = {}
                    for item_name in custom_items_order:
                        if item_name in data[category]:
                            ordered_items[item_name] = data[category][item_name]

                    # Ajouter les éléments non présents dans l'ordre personnalisé
                    for item_name, item_data in data[category].items():
                        if item_name not in ordered_items:
                            ordered_items[item_name] = item_data

                    ordered_data[category] = ordered_items
                else:
                    ordered_data[category] = data[category]

        # Ajouter les catégories non présentes dans l'ordre personnalisé
        for category, items in data.items():
            if category not in ordered_data:
                ordered_data[category] = items

        return ordered_data

    def reset_layout(self, page_name: str = None):
        """
        Réinitialiser l'ordre personnalisé

        Args:
            page_name: Nom de la page à réinitialiser, ou None pour tout réinitialiser
        """
        if page_name is None:
            # Réinitialiser tout
            self.layouts = {}
            logger.info("Tous les layouts ont été réinitialisés")
        else:
            # Réinitialiser une page spécifique
            keys_to_remove = [k for k in self.layouts.keys() if k.startswith(page_name)]
            for key in keys_to_remove:
                del self.layouts[key]
            logger.info(f"Layout de {page_name} réinitialisé")

        self._save_layouts()


# Instance globale
_layout_manager = None


def get_layout_manager() -> LayoutManager:
    """Obtenir l'instance globale du gestionnaire de layout"""
    global _layout_manager
    if _layout_manager is None:
        _layout_manager = LayoutManager()
    return _layout_manager
