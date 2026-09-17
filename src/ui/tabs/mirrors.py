from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.i18n import t
from src.system import PackageManager


class MirrorsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_mirrors()
    
    def init_ui(self):
        """Initialize the Mirrors tab"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(t("mirrors"))
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton(t("add_mirror"))
        add_btn.clicked.connect(self.add_mirror_dialog)
        
        remove_btn = QPushButton(t("remove_mirror"))
        remove_btn.clicked.connect(self.remove_selected_mirror)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_mirrors)
        
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(remove_btn)
        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # Mirrors table
        self.mirrors_table = QTableWidget()
        self.mirrors_table.setColumnCount(2)
        self.mirrors_table.setHorizontalHeaderLabels([t("mirror_name"), "URL"])
        self.mirrors_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.mirrors_table)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def load_mirrors(self):
        """Load mirrors from pacman.conf"""
        mirrors = PackageManager.get_pacman_mirrors()
        self.mirrors_table.setRowCount(0)
        
        for mirror in mirrors:
            row_position = self.mirrors_table.rowCount()
            self.mirrors_table.insertRow(row_position)
            
            # Parse mirror data
            parts = mirror.split("=")
            if len(parts) >= 2:
                name = parts[0].strip().replace("Server", "").strip()
                url = parts[1].strip()
                
                self.mirrors_table.setItem(row_position, 0, QTableWidgetItem(name or "Default"))
                self.mirrors_table.setItem(row_position, 1, QTableWidgetItem(url))
    
    def add_mirror_dialog(self):
        """Show dialog to add a new mirror"""
        dialog = QDialog(self)
        dialog.setWindowTitle(t("add_mirror"))
        dialog.setGeometry(200, 200, 400, 200)
        
        layout = QVBoxLayout()
        
        # Mirror name
        name_label = QLabel(t("mirror_name") + ":")
        name_input = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(name_input)
        
        # Mirror URL
        url_label = QLabel(t("mirror_url") + ":")
        url_input = QLineEdit()
        layout.addWidget(url_label)
        layout.addWidget(url_input)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton(t("save"))
        cancel_btn = QPushButton(t("cancel"))
        
        save_btn.clicked.connect(
            lambda: self.save_mirror(name_input.text(), url_input.text(), dialog)
        )
        cancel_btn.clicked.connect(dialog.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def save_mirror(self, name: str, url: str, dialog):
        """Save a new mirror"""
        if not name or not url:
            QMessageBox.warning(self, t("warning"), "Please fill all fields")
            return
        
        success, msg = PackageManager.add_mirror("custom", url)
        
        if success:
            QMessageBox.information(self, t("success"), msg)
            dialog.accept()
            self.load_mirrors()
        else:
            QMessageBox.critical(self, t("error"), msg)
    
    def remove_selected_mirror(self):
        """Remove the selected mirror"""
        current_row = self.mirrors_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, t("warning"), "Please select a mirror to remove")
            return
        
        reply = QMessageBox.question(
            self,
            t("confirm"),
            f"{t('remove_mirror')}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.mirrors_table.removeRow(current_row)
            QMessageBox.information(self, t("success"), "Mirror removed")
