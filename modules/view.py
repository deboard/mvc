"""
Description: View portion of MVC design pattern.
"""

from __future__ import annotations

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2026-01-21"
__version__ = "2.0.0.0"

from typing import TYPE_CHECKING

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from modules.logger import setup_logger

if TYPE_CHECKING:
    from modules.controller import Controller

logger = setup_logger(__name__)


class View(QWidget):
    """View class of MVC pattern.

    Handles the graphical user interface and user interactions.
    """

    clicked_sig = Signal(str)

    def __init__(self, parent=None):
        """Initialize the View.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)

        self._controller: Controller | None = None

        self.setWindowTitle("MVC View")

        self.label = QLabel("No model data", self)
        self.entry = QLineEdit("", self)
        self.button = QPushButton("Click Me!", self)

        self.button.clicked.connect(self.btn_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.button)

    def btn_clicked(self) -> None:
        """Handle button click, emit signal with entry text."""
        self.clicked_sig.emit(self.entry.text())

    @Slot(str)
    def update_data(self, arg: str) -> None:
        """Update the view with new data from controller.

        Args:
            arg: The data string to display.
        """
        logger.debug(f"View update from controller: {arg}")
        self.label.setText(arg)

    def set_controller(self, ctrl: Controller) -> None:
        """Set the controller and establish signal connections.

        Args:
            ctrl: The Controller instance to connect to.
        """
        self._controller = ctrl
        self.clicked_sig.connect(self._controller.button_action)
