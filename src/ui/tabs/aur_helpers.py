from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QMessageBox, QProgressDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from src.i18n import t
from src.system import PackageManager


class InstallWorker(QThread):
    """Worker thread for package installation"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    
    def __init__(self, helper: str):
        super().__init__()
        self.helper = helper
    
    def run(self):
        try:
            if self.helper == "paru":
                success, msg = PackageManager.install_paru()
            elif self.helper == "yay":
                success, msg = PackageManager.install_yay()
            else:
                success, msg = False, "Unknown helper"
            
            if success:
                self.success.emit(msg)
            else:
                self.error.emit(msg)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()


class UninstallWorker(QThread):
    """Worker thread for package uninstallation"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    
    def __init__(self, package: str):
        super().__init__()
        self.package = package
    
    def run(self):
        try:
            success, msg = PackageManager.uninstall_package(self.package)
            if success:
                self.success.emit(msg)
            else:
                self.error.emit(msg)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()


class AURHelpersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_status()
    
    def init_ui(self):
        """Initialize the AUR Helpers tab"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(t("aur_helpers"))
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Paru group
        paru_group = self.create_helper_group("paru", t("paru"))
        layout.addWidget(paru_group)
        
        # Yay group
        yay_group = self.create_helper_group("yay", t("yay"))
        layout.addWidget(yay_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_helper_group(self, helper_name: str, display_name: str) -> QGroupBox:
        """Create a group box for an AUR helper"""
        group = QGroupBox(display_name)
        layout = QHBoxLayout()
        
        # Status label
        self.status_label = QLabel(t("loading"))
        self.status_label.setObjectName(f"status_{helper_name}")
        self.status_label.setFont(QFont("Arial", 10))
        
        # Install button
        install_btn = QPushButton(t("install"))
        install_btn.clicked.connect(lambda: self.install_helper(helper_name))
        install_btn.setObjectName(f"install_{helper_name}")
        
        # Uninstall button
        uninstall_btn = QPushButton(t("uninstall"))
        uninstall_btn.clicked.connect(lambda: self.uninstall_helper(helper_name))
        uninstall_btn.setObjectName(f"uninstall_{helper_name}")
        
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(install_btn)
        layout.addWidget(uninstall_btn)
        
        group.setLayout(layout)
        group.setObjectName(f"group_{helper_name}")
        
        return group
    
    def update_status(self):
        """Update the installation status of AUR helpers"""
        paru_installed = PackageManager.is_aur_helper_installed("paru")
        yay_installed = PackageManager.is_aur_helper_installed("yay")
        
        paru_status = self.findChild(QLabel, "status_paru")
        yay_status = self.findChild(QLabel, "status_yay")
        
        if paru_status:
            paru_status.setText(
                f"{t('paru')}: {t('installed') if paru_installed else t('not_installed')}"
            )
        
        if yay_status:
            yay_status.setText(
                f"{t('yay')}: {t('installed') if yay_installed else t('not_installed')}"
            )
    
    def install_helper(self, helper: str):
        """Install an AUR helper"""
        reply = QMessageBox.question(
            self,
            t("confirm"),
            f"{t('install')} {helper}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            worker = InstallWorker(helper)
            worker.success.connect(
                lambda msg: self.show_success(msg)
            )
            worker.error.connect(
                lambda msg: self.show_error(msg)
            )
            worker.finished.connect(
                lambda: self.update_status()
            )
            worker.start()
    
    def uninstall_helper(self, helper: str):
        """Uninstall an AUR helper"""
        reply = QMessageBox.question(
            self,
            t("confirm"),
            f"{t('uninstall')} {helper}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            worker = UninstallWorker(helper)
            worker.success.connect(
                lambda msg: self.show_success(msg)
            )
            worker.error.connect(
                lambda msg: self.show_error(msg)
            )
            worker.finished.connect(
                lambda: self.update_status()
            )
            worker.start()
    
    def show_success(self, message: str):
        """Show success message"""
        QMessageBox.information(self, t("success"), message)
    
    def show_error(self, message: str):
        """Show error message"""
        QMessageBox.critical(self, t("error"), message)
