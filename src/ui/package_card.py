from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.package_store import PackageInfo


class PackageCard(QWidget):
    install_requested = pyqtSignal(str)

    def __init__(self, package: PackageInfo, parent=None):
        super().__init__(parent)
        self.package = package
        layout = QHBoxLayout(self)
        icon = QLabel()
        icon.setPixmap(QIcon(package.display_icon).pixmap(40, 40))
        layout.addWidget(icon)

        details = QVBoxLayout()
        title = QLabel(f"<b>{package.name}</b> {package.version}")
        description = QLabel(package.description or "No description available")
        description.setWordWrap(True)
        details.addWidget(title)
        details.addWidget(QLabel(f"{package.repository}"))
        details.addWidget(description)
        layout.addLayout(details, 1)

        install = QPushButton("Install")
        install.clicked.connect(lambda: self.install_requested.emit(package.name))
        layout.addWidget(install)
