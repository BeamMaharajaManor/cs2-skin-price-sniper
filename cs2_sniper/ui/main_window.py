"""Main window for the CS2 Skin Price Sniper desktop app."""
from __future__ import annotations

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

from cs2_sniper.config.settings import Settings
from cs2_sniper.services.sniper_engine import SniperEngine


class MainWindow(QMainWindow):
    def __init__(self, engine: SniperEngine, settings: Settings) -> None:
        super().__init__()
        self.engine = engine
        self.settings = settings
        self.setWindowTitle(f"CS2 Skin Price Sniper v{settings.version}")
        self.resize(960, 640)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.addWidget(QLabel("Watching marketplaces: " + ", ".join(engine.registry)))
        layout.addWidget(QLabel(f"Mode: {settings.mode}"))
        layout.addWidget(QLabel(f"Min discount: {settings.min_discount_percent}%"))
        self.setCentralWidget(root)

    def run(self) -> int:
        app = QApplication.instance() or QApplication([])
        self.show()
        return app.exec()