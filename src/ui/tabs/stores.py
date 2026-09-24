from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.package_store import PackageInfo, search_aur, search_official
from src.system import PackageManager
from src.ui.package_card import PackageCard


class SearchWorker(QThread):
    completed = pyqtSignal(list)
    failed = pyqtSignal(str)

    def __init__(self, source, query):
        super().__init__()
        self.source = source
        self.query = query

    def run(self):
        try:
            finder = search_aur if self.source == "aur" else search_official
            self.completed.emit(finder(self.query))
        except (OSError, RuntimeError, ValueError) as error:
            self.failed.emit(str(error))


class InstallWorker(QThread):
    completed = pyqtSignal(bool, str)

    def __init__(self, package: str, source: str):
        super().__init__()
        self.package = package
        self.source = source

    def run(self):
        success, message = PackageManager.install_package(self.package, self.source)
        self.completed.emit(success, message)


class PackageStoreTab(QWidget):
    def __init__(self, source: str, parent=None):
        super().__init__(parent)
        self.source = source
        self.worker = None
        self.install_worker = None
        self.results = QVBoxLayout()
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search packages")
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        self.results.addWidget(self.query)
        self.results.addWidget(button)

        self.container = QWidget()
        self.cards = QVBoxLayout(self.container)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.container)
        self.results.addWidget(scroll)
        self.setLayout(self.results)

    def search(self):
        if self.worker and self.worker.isRunning():
            return
        self.worker = SearchWorker(self.source, self.query.text())
        self.worker.completed.connect(self.show_results)
        self.worker.failed.connect(self.show_error)
        self.worker.start()

    def show_results(self, packages):
        while self.cards.count():
            item = self.cards.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for package in packages:
            card = PackageCard(package)
            card.install_requested.connect(self.confirm_install)
            self.cards.addWidget(card)
        self.cards.addStretch()

    def confirm_install(self, package: str):
        source_name = "AUR" if self.source == "aur" else "official pacman"
        answer = QMessageBox.question(
            self,
            "Confirm installation",
            f"Install {package} from {source_name}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        if self.install_worker and self.install_worker.isRunning():
            return
        self.install_worker = InstallWorker(package, self.source)
        self.install_worker.completed.connect(self.install_finished)
        self.install_worker.start()

    def install_finished(self, success: bool, message: str):
        if success:
            QMessageBox.information(self, "Installation complete", message)
        else:
            QMessageBox.critical(self, "Installation failed", message)

    def show_error(self, message: str):
        QMessageBox.critical(self, "Search failed", message)
