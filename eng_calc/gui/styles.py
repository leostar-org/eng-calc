"""
Stylesheet definitions for Engineering Calculator GUI.

This module provides the styling for the PyQt6 application.
"""

# Main application stylesheet
MAIN_STYLESHEET = """
/* Main Window */
QMainWindow {
    background-color: #f5f5f5;
}

/* Menu Bar */
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    padding: 2px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 6px 12px;
}

QMenuBar::item:selected {
    background-color: #e8f0fe;
    border-radius: 4px;
}

QMenuBar::item:pressed {
    background-color: #d2e3fc;
}

/* Dropdown Menus */
QMenu {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 4px 0px;
}

QMenu::item {
    padding: 8px 32px 8px 16px;
}

QMenu::item:selected {
    background-color: #e8f0fe;
}

QMenu::separator {
    height: 1px;
    background-color: #e0e0e0;
    margin: 4px 8px;
}

/* Toolbar */
QToolBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    spacing: 4px;
    padding: 4px;
}

QToolBar::separator {
    width: 1px;
    background-color: #e0e0e0;
    margin: 4px 8px;
}

QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 6px;
}

QToolButton:hover {
    background-color: #e8f0fe;
}

QToolButton:pressed {
    background-color: #d2e3fc;
}

/* Status Bar */
QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e0e0e0;
    color: #666666;
}

QStatusBar::item {
    border: none;
}

/* Central Widget */
QWidget#centralWidget {
    background-color: #f5f5f5;
}

/* Labels */
QLabel {
    color: #333333;
}

/* Push Buttons */
QPushButton {
    background-color: #1a73e8;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #1557b0;
}

QPushButton:pressed {
    background-color: #104080;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #888888;
}

/* Secondary Buttons */
QPushButton.secondary {
    background-color: transparent;
    color: #1a73e8;
    border: 1px solid #dadce0;
}

QPushButton.secondary:hover {
    background-color: #e8f0fe;
    border-color: #1a73e8;
}

/* Line Edits */
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 4px;
    padding: 8px 12px;
    selection-background-color: #e8f0fe;
}

QLineEdit:focus {
    border-color: #1a73e8;
    border-width: 2px;
    padding: 7px 11px;
}

/* Combo Boxes */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 4px;
    padding: 8px 12px;
    min-width: 80px;
}

QComboBox:focus {
    border-color: #1a73e8;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    selection-background-color: #e8f0fe;
}

/* Group Boxes */
QGroupBox {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px;
    font-weight: 500;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 8px;
    color: #333333;
}

/* Scroll Areas */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: transparent;
    width: 12px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #c1c1c1;
    border-radius: 6px;
    min-height: 30px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a8a8a8;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 12px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #c1c1c1;
    border-radius: 6px;
    min-width: 30px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #a8a8a8;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: #ffffff;
}

QTabBar::tab {
    background-color: transparent;
    border: none;
    padding: 10px 16px;
    color: #666666;
}

QTabBar::tab:selected {
    color: #1a73e8;
    border-bottom: 2px solid #1a73e8;
}

QTabBar::tab:hover:!selected {
    background-color: #f5f5f5;
}
"""


def get_stylesheet() -> str:
    """
    Get the main application stylesheet.

    Returns:
        The complete CSS stylesheet string.
    """
    return MAIN_STYLESHEET
