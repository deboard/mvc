"""'
  Description: View portion of MVC design pattern.
"""

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2025-07-18"
__version__ = "1.0.0.0"

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout
from PySide6.QtCore import Signal, Slot

import controller

class View(QWidget):
    """View class of MVC pattern"""

    clicked_sig = Signal(str)
    controller: controller.Controller
    label: QLabel
    entry: QLineEdit
    button: QPushButton

    def __init__(self, ctrl=None):
        """constructor"""

        super().__init__()

        self.controller = ctrl

        self.setWindowTitle("MVC View")

        self.label = QLabel("No model data", self)
        self.entry = QLineEdit("", self)
        self.button = QPushButton("Click Me!", self)

        self.button.clicked.connect(self.btn_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.button)

    def btn_clicked(self):
        """clicked signal, send entry text to ctrlr"""
        self.clicked_sig.emit(self.entry.text())

    @Slot(str)
    def update_data(self, arg):
        """get updates from controller --> this.view"""
        print(f"View entry update from controller: {arg}")
        self.label.setText(arg)

    def set_controller(self, ctrl: controller.Controller):
        """
        set controller
        setup this.view --> controller event(s)
        """
        self.controller = ctrl
        self.clicked_sig.connect(self.controller.button_action)
