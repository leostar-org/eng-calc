"""
Tests for GUI widgets.

Tests calculator widget implementations and their integration.
"""

import pytest
from PyQt6.QtWidgets import QApplication

from eng_calc.gui.widgets import (
    ForceCalculatorWidget,
    StressCalculatorWidget,
    UnitConverterWidget,
)


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication for testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


class TestStressCalculatorWidget:
    """Tests for StressCalculatorWidget."""

    def test_widget_creation(self, qapp):
        """Test widget can be created."""
        widget = StressCalculatorWidget()
        assert widget is not None
        assert widget.force_input is not None
        assert widget.area_input is not None

    def test_get_inputs(self, qapp):
        """Test getting input values."""
        widget = StressCalculatorWidget()
        widget.force_input.setValue(2000)
        widget.area_input.setValue(50)

        inputs = widget.get_inputs()
        assert inputs["force"] == 2000
        assert inputs["area"] == 50

    def test_calculation(self, qapp):
        """Test stress calculation."""
        widget = StressCalculatorWidget()
        widget.force_input.setValue(1000)
        widget.area_input.setValue(100)

        result = widget.perform_calculation()
        assert "1000.00" in result
        assert "100.0000" in result
        assert "Stress" in result

    def test_clear(self, qapp):
        """Test clearing inputs."""
        widget = StressCalculatorWidget()
        widget.force_input.setValue(5000)
        widget.area_input.setValue(200)

        widget.clear()

        assert widget.force_input.value() == 1000  # default
        assert widget.area_input.value() == 100  # default
        assert widget.results_display.toPlainText() == ""


class TestForceCalculatorWidget:
    """Tests for ForceCalculatorWidget."""

    def test_widget_creation(self, qapp):
        """Test widget can be created."""
        widget = ForceCalculatorWidget()
        assert widget is not None
        assert widget.force1_input is not None
        assert widget.force2_input is not None

    def test_get_inputs(self, qapp):
        """Test getting input values."""
        widget = ForceCalculatorWidget()
        widget.force1_input.setValue(150)
        widget.force2_input.setValue(75)

        inputs = widget.get_inputs()
        assert inputs["force1"] == 150
        assert inputs["force2"] == 75

    def test_calculation(self, qapp):
        """Test force calculation."""
        widget = ForceCalculatorWidget()
        widget.force1_input.setValue(100)
        widget.force2_input.setValue(50)

        result = widget.perform_calculation()
        assert "100.00" in result
        assert "50.00" in result
        assert "Resultant" in result
        assert "150.00" in result

    def test_clear(self, qapp):
        """Test clearing inputs."""
        widget = ForceCalculatorWidget()
        widget.force1_input.setValue(500)
        widget.force2_input.setValue(250)

        widget.clear()

        assert widget.force1_input.value() == 100  # default
        assert widget.force2_input.value() == 50  # default


class TestUnitConverterWidget:
    """Tests for UnitConverterWidget."""

    def test_widget_creation(self, qapp):
        """Test widget can be created."""
        widget = UnitConverterWidget()
        assert widget is not None
        assert widget.category_combo is not None
        assert widget.value_input is not None
        assert widget.from_unit_combo is not None
        assert widget.to_unit_combo is not None

    def test_category_change(self, qapp):
        """Test category selection updates units."""
        widget = UnitConverterWidget()

        # Initially should have a category
        initial_category = widget.category_combo.currentText()
        assert initial_category is not None

        # Units should be populated
        assert widget.from_unit_combo.count() > 0
        assert widget.to_unit_combo.count() > 0

    def test_conversion(self, qapp):
        """Test unit conversion."""
        widget = UnitConverterWidget()
        widget.category_combo.setCurrentText("Length")
        widget.from_unit_combo.setCurrentText("m")
        widget.to_unit_combo.setCurrentText("cm")
        widget.value_input.setValue(1.0)

        result = widget.perform_calculation()
        assert "Length" in result
        assert "1.000000" in result
        assert "m" in result
        assert "cm" in result

    def test_clear(self, qapp):
        """Test clearing inputs."""
        widget = UnitConverterWidget()
        widget.value_input.setValue(100.5)

        widget.clear()

        assert widget.value_input.value() == 1.0  # default


class TestStatusCallback:
    """Tests for status callback functionality."""

    def test_status_callback(self, qapp):
        """Test status callback is invoked."""
        widget = StressCalculatorWidget()
        status_messages = []

        def capture_status(msg):
            status_messages.append(msg)

        widget.set_status_callback(capture_status)
        widget.calculate_button.click()

        assert len(status_messages) > 0
        assert "Calculation completed" in status_messages

    def test_error_callback(self, qapp):
        """Test error status callback."""
        widget = StressCalculatorWidget()
        status_messages = []

        def capture_status(msg):
            status_messages.append(msg)

        widget.set_status_callback(capture_status)

        # Set invalid values that might cause issues
        widget.area_input.setValue(0)  # Zero area
        widget.calculate_button.click()

        # Should have error message
        assert any("Error" in msg for msg in status_messages)
