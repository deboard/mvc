"""
MVC Application Modules.

This package contains the Model, View, and Controller components.
"""

from modules.controller import Controller
from modules.logger import setup_logger
from modules.model import Model
from modules.view import View

__all__ = ["Model", "View", "Controller", "setup_logger"]
