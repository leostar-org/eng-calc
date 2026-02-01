"""
Main application class for Engineering Calculator.

This module provides the QApplication wrapper with proper initialization
and configuration for the PyQt6 application.
"""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from eng_calc import __version__
from eng_calc.gui import MainWindow
from eng_calc.gui.styles import get_stylesheet


class EngCalcApp:
    """
    Engineering Calculator application wrapper.

    This class encapsulates the QApplication and MainWindow setup,
    providing a clean interface for running the application.

    Attributes:
        app: The PyQt6 QApplication instance.
        main_window: The main application window.
    """

    APP_NAME = "Engineering Calculator"
    ORG_NAME = "eng-calc"
    ORG_DOMAIN = "eng-calc.local"

    def __init__(self, args: list[str] | None = None) -> None:
        """
        Initialize the application.

        Args:
            args: Command-line arguments. If None, uses sys.argv.
        """
        if args is None:
            args = sys.argv

        self._app = QApplication(args)
        self._configure_app()
        self._main_window = MainWindow()

    def _configure_app(self) -> None:
        """Configure application properties and settings."""
        self._app.setApplicationName(self.APP_NAME)
        self._app.setApplicationVersion(__version__)
        self._app.setOrganizationName(self.ORG_NAME)
        self._app.setOrganizationDomain(self.ORG_DOMAIN)

        # Apply stylesheet
        self._app.setStyleSheet(get_stylesheet())

        # High DPI settings are automatic in PyQt6

    @property
    def app(self) -> QApplication:
        """Get the QApplication instance."""
        return self._app

    @property
    def main_window(self) -> MainWindow:
        """Get the main window instance."""
        return self._main_window

    def run(self) -> int:
        """
        Run the application event loop.

        Returns:
            Exit code from the application.
        """
        self._main_window.show()
        return self._app.exec()


def create_app(args: list[str] | None = None) -> EngCalcApp:
    """
    Factory function to create the application.

    Args:
        args: Command-line arguments.

    Returns:
        Configured EngCalcApp instance.
    """
    return EngCalcApp(args)
