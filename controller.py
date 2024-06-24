"""'
  Description: Controller portion of MVC design pattern
"""

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2024-06-21"
__version__ = "1.0.0.0"

from PySide2.QtCore import Signal, Slot, QObject
import view
import model


class Controller(QObject):
    """controller class for MVC pattern"""

    data_sig = Signal(str)

    def __init__(self, aview, amod, parent=None):
        """constructor"""
        super().__init__(parent)

        self.view: view.View
        self.model: model.Model
        self.view = aview
        self.model = amod

        self.data_sig.connect(self.model.update_data)

    @Slot(str)
    def button_action(self, arg):
        """View button clicked signal emitted"""
        if len(arg):
            # emit for model
            # but only if the string has a length
            self.data_sig.emit(arg)
