#!/usr/bin/env python3
"""
Description: MVC main for Model View Controller design pattern.
"""

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2026-01-21"
__version__ = "2.0.0.0"

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from modules import Controller, Model, View

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Determine database path relative to script location
    db_path = Path(__file__).parent / "mvc.db"

    # Setup MVC objects
    my_view = View()
    my_model = Model(db_path=db_path)
    my_ctrl = Controller(my_view, my_model)

    my_view.show()

    sys.exit(app.exec())
