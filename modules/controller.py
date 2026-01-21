"""
Description: Controller portion of MVC design pattern.
"""

from __future__ import annotations

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2026-01-21"
__version__ = "2.0.0.0"

from PySide6.QtCore import QObject, Signal, Slot

from modules.logger import setup_logger
from modules.model import Model
from modules.view import View

logger = setup_logger(__name__)


class Controller(QObject):
    """Controller class for MVC pattern.

    Orchestrates communication between View and Model components.
    """

    init_comps_sig = Signal()
    data_sig = Signal(str)
    view_update = Signal(str)

    def __init__(self, aview: View, amod: Model, parent=None):
        """Initialize the Controller.

        Args:
            aview: The View instance to control.
            amod: The Model instance to control.
            parent: Optional parent QObject.
        """
        super().__init__(parent)

        self.view: View = aview
        self.model: Model = amod

        self.init_comps_sig.connect(self.init_components)
        self.init_comps_sig.emit()

    @Slot()
    def init_components(self) -> None:
        """Initialize component connections."""
        logger.debug("Initializing components")
        self.view.set_controller(self)
        self.view_update.connect(self.view.update_data)
        self.model.set_controller(self)
        self.data_sig.connect(self.model.update_data)

    @Slot(str)
    def button_action(self, arg: str) -> None:
        """Handle view button click signal.

        Args:
            arg: The text from the view's entry field.
        """
        logger.debug("View button clicked")
        if arg:
            self.data_sig.emit(arg)

    @Slot(str)
    def model_updated(self, arg: str) -> None:
        """Handle model data update signal.

        Args:
            arg: The updated data from the model.
        """
        logger.debug(f"Model data updated to: {arg}")
        self.view_update.emit(arg)
