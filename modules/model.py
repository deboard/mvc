"""'
  Description: Model portion of MVC design pattern
"""

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2025-10-29"
__version__ = "1.0.2.0"

import os
import sqlite3
from PySide6.QtCore import Slot, Signal, QObject
from modules import controller


class Model(QObject):
    """
    model class for MVC design pattern
    model responds to controller
    model is updated by controller
    """

    data_sig = Signal(str)
    updated_sig = Signal(str)
    check_data = Signal()
    conn = None
    cursor = None

    def __init__(self, parent=None):
        """constructor"""
        super().__init__(parent)

        self.incr: int
        self.data: str
        self.cntrl: controller.Controller

        self.data_file = "data.txt"
        self.incr = 0
        self.data = "default"

        self.check_data.connect(self.data_check)

        self.conn = sqlite3.connect('mvc.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mvc (
                lastdata TEXT
            )''')

    @Slot()
    def data_check(self):
        """see if the data file is there and read it in if it is"""
        print("model.data_check")

        self.cursor.execute("SELECT * FROM mvc")
        rows = self.cursor.fetchall()
        if len(rows):
            self.data = rows[len(rows) - 1][0]
            print(f"self.data: {self.data}")
            self.updated_sig.emit(self.data)
            self.data_sig.emit(self.data)

    def set_controller(self, actrl):
        """self explainitory"""
        self.cntrl = actrl
        self.updated_sig.connect(self.cntrl.model_updated)
        self.check_data.emit()

    @Slot(str)
    def update_data(self, arg):
        """new data signal from controller"""
        self.data = arg
        self.incr = self.incr + 1
        print("Model data set to: " + self.data)

        self.data = str(self.incr) + ":" + self.data
        self.data_sig.emit(str(self.incr) + ":" + self.data)
        self.updated_sig.emit(self.data)

        self.cursor.execute("INSERT INTO mvc (lastdata) VALUES (?)", (arg,))
        self.conn.commit()
