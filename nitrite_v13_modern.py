#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NiTriTe V13.0 - Lanceur Principal
Interface Moderne pour Techniciens de Maintenance Informatique
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Lancer l'interface moderne
from gui_modern_v13 import main

if __name__ == "__main__":
    main()
