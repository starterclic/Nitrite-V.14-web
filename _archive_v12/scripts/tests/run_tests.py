#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement des tests unitaires
"""

import sys
from pathlib import Path

# Ajouter le répertoire du projet au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent  # scripts/tests/ -> racine))

if __name__ == '__main__':
    from tests import test_core_functionality
    sys.exit(0 if test_core_functionality.run_tests() else 1)
