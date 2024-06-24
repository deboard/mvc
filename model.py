"""'
  Description: Model portion of MVC design pattern
"""

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2024-06-21"
__version__ = "1.0.0.0"

from PySide2.QtCore import Slot, Signal, QObject
import view

class Model(QObject):
    """
    model class for MVC design pattern
    model updates view
    model is updated by controller
    """

    data_sig = Signal(str)

    def __init__(self, aview, parent=None):
        """constructor"""
        super().__init__(parent)
       
        self.incr: int
        self.data: str
        self.mview: view.View

        self.mview = aview
        self.incr = 0
        self.data = "default"
        self.data_sig.connect(self.mview.update_data)

    @Slot(str)
    def update_data(self, arg):
        """new data signal from controller"""
        self.data = arg
        self.incr = self.incr + 1
        print("Model data set to: " + self.data)
        self.data_sig.emit(str(self.incr) + ":" + self.data)
