from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from src.i18n import t
from src import __version__


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the About tab"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(t("about"))
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # App name
        app_name = QLabel(t("app_title"))
        app_name.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(app_name)
        
        # Version
        version = QLabel(f"{t('app_version')}: {__version__}")
        version.setFont(QFont("Arial", 10))
        layout.addWidget(version)
        
        # Description
        desc = QLabel(
            "A universal GUI toolbox for Arch Linux package management.\n"
            "Easily install/uninstall AUR helpers and manage pacman mirrors."
        )
        desc.setFont(QFont("Arial", 10))
        desc.setStyleSheet("color: #666;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Author
        author = QLabel("Made with ❤️ for Arch Linux")
        author.setFont(QFont("Arial", 9))
        author.setStyleSheet("color: #999;")
        layout.addWidget(author)
        
        layout.addStretch()
        self.setLayout(layout)
