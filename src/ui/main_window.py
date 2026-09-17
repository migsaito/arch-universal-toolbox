from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QComboBox, QLabel, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from src.i18n import t, set_language
from src.ui.tabs.aur_helpers import AURHelpersTab
from src.ui.tabs.mirrors import MirrorsTab
from src.ui.tabs.about import AboutTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main UI"""
        self.setWindowTitle(t("app_title"))
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(self.get_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Top bar with language selector
        top_layout = QHBoxLayout()
        lang_label = QLabel(t("lang_select") + ":")
        lang_label.setFont(QFont("Arial", 10))
        
        lang_combo = QComboBox()
        lang_combo.addItems(["English (US)", "Português (BR)"])
        lang_combo.currentTextChanged.connect(self.on_language_changed)
        
        top_layout.addStretch()
        top_layout.addWidget(lang_label)
        top_layout.addWidget(lang_combo)
        top_layout.setContentsMargins(10, 10, 10, 10)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(AURHelpersTab(), t("aur_helpers"))
        tabs.addTab(MirrorsTab(), t("mirrors"))
        tabs.addTab(AboutTab(), t("about"))
        
        # Add to main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(tabs)
        
        central_widget.setLayout(main_layout)
    
    def on_language_changed(self, text: str):
        """Handle language change"""
        if "Português" in text:
            set_language("pt_BR")
        else:
            set_language("en_US")
        
        # Refresh UI
        self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh all UI text after language change"""
        self.setWindowTitle(t("app_title"))
        # Note: This is a simple implementation. For a more robust solution,
        # consider using signals/slots for UI updates
    
    def get_stylesheet(self) -> str:
        """Return custom stylesheet"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QTabWidget {
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                margin-right: 2px;
                border-radius: 4px 4px 0px 0px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #0078d4;
            }
            
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #005a9e;
            }
            
            QPushButton:pressed {
                background-color: #004578;
            }
            
            QLabel {
                color: #333;
            }
            
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                background-color: white;
            }
            
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #0078d4;
            }
        """
