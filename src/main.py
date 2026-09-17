#!/usr/bin/env python3
"""
Arch Universal Toolbox - GUI application for Arch Linux package management
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
