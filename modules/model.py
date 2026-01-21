"""
Description: Model portion of MVC design pattern.
"""

from __future__ import annotations

__author__ = "John DeBoard"
__email__ = "john.deboard@gmail.com"
__date__ = "2023-10-18"
__modified__ = "2026-01-21"
__version__ = "2.0.0.0"

import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot

from modules.logger import setup_logger

if TYPE_CHECKING:
    from modules.controller import Controller

logger = setup_logger(__name__)


class Model(QObject):
    """Model class for MVC design pattern.

    The model responds to the controller and is updated by the controller.
    Handles data persistence via SQLite database.
    """

    data_sig = Signal(str)
    updated_sig = Signal(str)
    check_data = Signal()

    def __init__(self, parent=None, db_path: str | Path | None = None):
        """Initialize the Model.

        Args:
            parent: Optional parent QObject.
            db_path: Path to SQLite database. If None, uses 'mvc.db' in the
                     same directory as the main script.
        """
        super().__init__(parent)

        self.incr: int = 0
        self.data: str = "default"
        self._controller: Controller | None = None

        # Determine database path
        if db_path is None:
            db_path = Path(__file__).parent.parent / "mvc.db"
        self._db_path = Path(db_path)

        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

        self.check_data.connect(self.data_check)
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database connection and schema."""
        try:
            self.conn = sqlite3.connect(str(self._db_path))
            self.cursor = self.conn.cursor()

            # Check if migration is needed
            self._migrate_database()

            logger.info(f"Database initialized at {self._db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def _migrate_database(self) -> None:
        """Migrate database schema if needed."""
        try:
            # Check current schema
            self.cursor.execute("PRAGMA table_info(mvc)")
            columns = {row[1] for row in self.cursor.fetchall()}

            if not columns:
                # Table doesn't exist, create with new schema
                self.cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS mvc (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lastdata TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                self.conn.commit()
                logger.info("Created new database schema")
            elif "id" not in columns:
                # Old schema exists, migrate
                logger.info("Migrating database schema...")
                self.cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS mvc_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lastdata TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                self.cursor.execute(
                    """
                    INSERT INTO mvc_new (lastdata)
                    SELECT lastdata FROM mvc
                """
                )
                self.cursor.execute("DROP TABLE mvc")
                self.cursor.execute("ALTER TABLE mvc_new RENAME TO mvc")
                self.conn.commit()
                logger.info("Database migration completed")
        except sqlite3.Error as e:
            logger.error(f"Database migration failed: {e}")
            raise

    @Slot()
    def data_check(self) -> None:
        """Check if data exists in database and load the most recent entry."""
        logger.debug("Checking for existing data")

        try:
            self.cursor.execute("SELECT lastdata FROM mvc ORDER BY id DESC LIMIT 1")
            row = self.cursor.fetchone()
            if row:
                self.data = row[0]
                logger.debug(f"Loaded data from database: {self.data}")
                self.updated_sig.emit(self.data)
                self.data_sig.emit(self.data)
        except sqlite3.Error as e:
            logger.error(f"Error checking data: {e}")

    def set_controller(self, ctrl: Controller) -> None:
        """Set the controller reference and establish connections.

        Args:
            ctrl: The Controller instance to connect to.
        """
        self._controller = ctrl
        self.updated_sig.connect(self._controller.model_updated)
        self.check_data.emit()

    @Slot(str)
    def update_data(self, arg: str) -> None:
        """Process new data from controller.

        Args:
            arg: The new data string to process.
        """
        self.incr += 1
        self.data = f"{self.incr}:{arg}"
        logger.debug(f"Model data set to: {self.data}")

        self.data_sig.emit(self.data)
        self.updated_sig.emit(self.data)

        try:
            self.cursor.execute(
                "INSERT INTO mvc (lastdata) VALUES (?)", (self.data,)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error saving data: {e}")

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            try:
                self.conn.close()
                logger.debug("Database connection closed")
            except sqlite3.Error as e:
                logger.error(f"Error closing database: {e}")
            finally:
                self.conn = None
                self.cursor = None

    def __del__(self):
        """Destructor to ensure database is closed."""
        self.close()
