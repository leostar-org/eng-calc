"""
Main window for Engineering Calculator.

This module provides the main application window with menu bar,
toolbar, status bar, and central widget layout.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QMainWindow,
    QMenuBar,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from eng_calc.gui.widgets import (
    ForceCalculatorWidget,
    StressCalculatorWidget,
    UnitConverterWidget,
)


class MainWindow(QMainWindow):
    """
    Main application window for Engineering Calculator.

    This window provides the primary interface including:
    - Menu bar with File, Edit, and Help menus
    - Toolbar with common actions
    - Status bar for displaying messages
    - Central widget area for calculator views
    """

    # Window dimensions
    DEFAULT_WIDTH = 1024
    DEFAULT_HEIGHT = 768
    MIN_WIDTH = 800
    MIN_HEIGHT = 600

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self._setup_window()
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_status_bar()
        self._setup_central_widget()

    def _setup_window(self) -> None:
        """Configure window properties."""
        self.setWindowTitle("Engineering Calculator")
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.resize(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)

    def _setup_menu_bar(self) -> None:
        """Create and configure the menu bar."""
        menu_bar = self.menuBar()
        if menu_bar is None:
            menu_bar = QMenuBar(self)
            self.setMenuBar(menu_bar)

        self._create_file_menu(menu_bar)
        self._create_edit_menu(menu_bar)
        self._create_help_menu(menu_bar)

    def _create_file_menu(self, menu_bar: QMenuBar) -> None:
        """Create the File menu."""
        file_menu = menu_bar.addMenu("&File")
        if file_menu is None:
            return

        # New action
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip("Create a new calculation")
        new_action.triggered.connect(self._on_new)
        file_menu.addAction(new_action)

        # Open action
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Open a saved calculation")
        open_action.triggered.connect(self._on_open)
        file_menu.addAction(open_action)

        # Save action
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip("Save the current calculation")
        save_action.triggered.connect(self._on_save)
        file_menu.addAction(save_action)

        # Save As action
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip("Save the calculation with a new name")
        save_as_action.triggered.connect(self._on_save_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        # Export action
        export_action = QAction("&Export...", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.setStatusTip("Export calculation results")
        export_action.triggered.connect(self._on_export)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Store actions for toolbar access
        self._new_action = new_action
        self._open_action = open_action
        self._save_action = save_action

    def _create_edit_menu(self, menu_bar: QMenuBar) -> None:
        """Create the Edit menu."""
        edit_menu = menu_bar.addMenu("&Edit")
        if edit_menu is None:
            return

        # Undo action
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.setStatusTip("Undo the last action")
        undo_action.triggered.connect(self._on_undo)
        edit_menu.addAction(undo_action)

        # Redo action
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.setStatusTip("Redo the last undone action")
        redo_action.triggered.connect(self._on_redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        # Clear action
        clear_action = QAction("&Clear", self)
        clear_action.setShortcut(QKeySequence("Ctrl+L"))
        clear_action.setStatusTip("Clear all inputs")
        clear_action.triggered.connect(self._on_clear)
        edit_menu.addAction(clear_action)

        edit_menu.addSeparator()

        # Preferences action
        preferences_action = QAction("&Preferences...", self)
        preferences_action.setShortcut(QKeySequence.StandardKey.Preferences)
        preferences_action.setStatusTip("Configure application settings")
        preferences_action.triggered.connect(self._on_preferences)
        edit_menu.addAction(preferences_action)

    def _create_help_menu(self, menu_bar: QMenuBar) -> None:
        """Create the Help menu."""
        help_menu = menu_bar.addMenu("&Help")
        if help_menu is None:
            return

        # Documentation action
        docs_action = QAction("&Documentation", self)
        docs_action.setShortcut(QKeySequence.StandardKey.HelpContents)
        docs_action.setStatusTip("Open documentation")
        docs_action.triggered.connect(self._on_documentation)
        help_menu.addAction(docs_action)

        help_menu.addSeparator()

        # About action
        about_action = QAction("&About", self)
        about_action.setStatusTip("About Engineering Calculator")
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _setup_toolbar(self) -> None:
        """Create and configure the toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # Add actions to toolbar
        if hasattr(self, "_new_action"):
            toolbar.addAction(self._new_action)
        if hasattr(self, "_open_action"):
            toolbar.addAction(self._open_action)
        if hasattr(self, "_save_action"):
            toolbar.addAction(self._save_action)

        toolbar.addSeparator()

        # Calculator selector
        selector_label = QLabel("Calculator: ")
        toolbar.addWidget(selector_label)

        self._calculator_combo = QComboBox()
        self._calculator_combo.addItems(
            ["Stress Calculator", "Force Calculator", "Unit Converter"]
        )
        self._calculator_combo.currentIndexChanged.connect(
            self._on_calculator_changed
        )
        toolbar.addWidget(self._calculator_combo)

        self._toolbar = toolbar

    def _setup_status_bar(self) -> None:
        """Create and configure the status bar."""
        status_bar = self.statusBar()
        if status_bar is None:
            status_bar = QStatusBar(self)
            self.setStatusBar(status_bar)

        status_bar.showMessage("Ready")

        # Permanent widgets for status bar
        self._unit_system_label = QLabel("SI Units")
        status_bar.addPermanentWidget(self._unit_system_label)

    def _setup_central_widget(self) -> None:
        """Create and configure the central widget."""
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Stacked widget for calculator views
        self._stacked_widget = QStackedWidget()

        # Create calculator widgets
        self._stress_widget = StressCalculatorWidget()
        self._stress_widget.set_status_callback(self.show_message)

        self._force_widget = ForceCalculatorWidget()
        self._force_widget.set_status_callback(self.show_message)

        self._converter_widget = UnitConverterWidget()
        self._converter_widget.set_status_callback(self.show_message)

        # Add to stacked widget
        self._stacked_widget.addWidget(self._stress_widget)
        self._stacked_widget.addWidget(self._force_widget)
        self._stacked_widget.addWidget(self._converter_widget)

        layout.addWidget(self._stacked_widget)

        self._central_layout = layout

    # --- Slot Methods (Placeholders) ---

    def _on_new(self) -> None:
        """Handle New action."""
        self.statusBar().showMessage("New calculation", 3000)

    def _on_open(self) -> None:
        """Handle Open action."""
        self.statusBar().showMessage("Open calculation", 3000)

    def _on_save(self) -> None:
        """Handle Save action."""
        self.statusBar().showMessage("Save calculation", 3000)

    def _on_save_as(self) -> None:
        """Handle Save As action."""
        self.statusBar().showMessage("Save As...", 3000)

    def _on_export(self) -> None:
        """Handle Export action."""
        self.statusBar().showMessage("Export...", 3000)

    def _on_undo(self) -> None:
        """Handle Undo action."""
        self.statusBar().showMessage("Undo", 3000)

    def _on_redo(self) -> None:
        """Handle Redo action."""
        self.statusBar().showMessage("Redo", 3000)

    def _on_clear(self) -> None:
        """Handle Clear action."""
        if hasattr(self, "_stacked_widget"):
            current_widget = self._stacked_widget.currentWidget()
            if current_widget and hasattr(current_widget, "clear"):
                current_widget.clear()
        self.statusBar().showMessage("Cleared", 3000)

    def _on_calculator_changed(self, index: int) -> None:
        """Handle calculator selection change."""
        if hasattr(self, "_stacked_widget"):
            self._stacked_widget.setCurrentIndex(index)
        self.show_message("Switched calculator", 2000)

    def _on_preferences(self) -> None:
        """Handle Preferences action."""
        self.statusBar().showMessage("Preferences...", 3000)

    def _on_documentation(self) -> None:
        """Handle Documentation action."""
        self.statusBar().showMessage("Opening documentation...", 3000)

    def _on_about(self) -> None:
        """Handle About action."""
        from PyQt6.QtWidgets import QMessageBox

        from eng_calc import __version__

        QMessageBox.about(
            self,
            "About Engineering Calculator",
            f"<h3>Engineering Calculator</h3>"
            f"<p>Version {__version__}</p>"
            f"<p>A comprehensive engineering calculation tool.</p>"
            f"<p>Licensed under MIT License.</p>",
        )

    def show_message(self, message: str, timeout: int = 3000) -> None:
        """
        Display a message in the status bar.

        Args:
            message: The message to display.
            timeout: Duration in milliseconds (0 for permanent).
        """
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage(message, timeout)
