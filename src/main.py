#!/usr/bin/env python3
"""
Arch Universal Toolbox - GUI application for Arch Linux package management
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.config import load_settings
from src.i18n import set_language


def main():
    """Main entry point"""
    set_language(load_settings().get("language", "en_US"))
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
