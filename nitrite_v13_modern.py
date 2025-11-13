#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NiTriTe V13.0 - Lanceur Principal
Interface Moderne pour Techniciens de Maintenance Informatique
"""

import sys
import os
import threading

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import splash screen and main GUI
from splash_screen import SplashScreen
from gui_modern_v13 import main


def launch_with_splash():
    """Launch application with splash screen"""

    # Create splash screen
    splash = SplashScreen()
    splash.show()

    # Variable to hold main app
    main_app = [None]

    def load_main_app():
        """Load main application after splash"""
        # Destroy splash
        splash.close()

        # Launch main application
        main()

    # Run loading sequence
    splash.run_loading_sequence(callback=load_main_app)

    # Start splash mainloop
    splash.mainloop()


if __name__ == "__main__":
    launch_with_splash()
