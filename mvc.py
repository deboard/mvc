#!/usr/bin/env python3

"""'
  Description: MVC main for Model View Controller design pattern.
"""

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2024-06-21"
__version__ = "1.0.0.0"

import sys
from PySide2.QtWidgets import QApplication

## import MVC design pattern modules
import view
import model
import controller

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # setup MVC objects

    ## View needs a Controller, set later in process
    my_view = view.View()
    my_model = model.Model(my_view)
    my_ctrl = controller.Controller(my_view, my_model)
    my_view.set_controller(my_ctrl)

    my_view.show()

    sys.exit(app.exec_())
