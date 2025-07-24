"""'
  Description: Controller portion of MVC design pattern
"""

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2025-07-18"
__version__ = "1.0.0.2"

from PySide6.QtCore import Signal, Slot, QObject
import view
import model


class Controller(QObject):
    """controller class for MVC pattern"""

    init_comps_sig = Signal()
    data_sig = Signal(str)
    view_update = Signal(str)

    def __init__(self, aview, amod, parent=None):
        """constructor"""
        super().__init__(parent)

        self.view: view.View
        self.model: model.Model
        self.view = aview
        self.model = amod

        self.init_comps_sig.connect(self.init_components)
        # this signal should be handles outside of __init__
        self.init_comps_sig.emit()

    @Slot()
    def init_components(self):
        print("controller: init_components")
        self.view.set_controller(self)
        self.view_update.connect(self.view.update_data)
        self.model.set_controller(self)
        self.data_sig.connect(self.model.update_data)

    @Slot(str)
    def button_action(self, arg):
        """View button clicked signal emitted"""
        print("Controller: view button clicked")
        if len(arg):
            # emit for model
            # but only if the string has a length
            self.data_sig.emit(arg)

    @Slot(str)
    def model_updated(self, arg):
        # model data --> controller signal
        print("Controller: model data updated to: " + arg)
        # controller --> view
        self.view_update.emit(arg)

