"""Calculator widgets."""

from typing import Callable, Optional

from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from eng_calc.calculators.force_calculator import ForceCalculator
from eng_calc.calculators.stress_calculator import StressCalculator
from eng_calc.utilities.unit_converter import UnitConverter
from eng_calc.utilities.units import UnitCategory, get_units_by_category


class CalculatorWidget(QWidget):
    """Base class for calculator widgets."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._status_callback: Optional[Callable[[str], None]] = None
        self._setup_ui()

    def set_status_callback(self, callback: Callable[[str], None]) -> None:
        self._status_callback = callback

    def _show_status(self, message: str) -> None:
        if self._status_callback:
            self._status_callback(message)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(8)
        layout.addLayout(self.form_layout)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self._on_calculate)
        layout.addWidget(self.calculate_button)

        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setMaximumHeight(150)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.results_display)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)
        layout.addWidget(clear_button)

        layout.addStretch()

        self._create_inputs()

    def _create_inputs(self) -> None:
        pass

    def get_inputs(self) -> dict:
        return {}

    def perform_calculation(self) -> str:
        return "Not implemented"

    def display_results(self, results: str) -> None:
        self.results_display.setText(results)

    def clear(self) -> None:
        self.results_display.clear()
        self._clear_inputs()

    def _clear_inputs(self) -> None:
        pass

    def _on_calculate(self) -> None:
        try:
            results = self.perform_calculation()
            self.display_results(results)
            self._show_status("Calculation completed")
        except ValueError as e:
            error_msg = f"Input Error: {str(e)}"
            self.display_results(error_msg)
            self._show_status(error_msg)
        except Exception as e:
            error_msg = f"Calculation Error: {str(e)}"
            self.display_results(error_msg)
            self._show_status(error_msg)


class StressCalculatorWidget(CalculatorWidget):
    """Widget for Stress Calculator."""

    def _create_inputs(self) -> None:
        self.force_input = QDoubleSpinBox()
        self.force_input.setRange(0, 1_000_000)
        self.force_input.setValue(1000)
        self.force_input.setDecimals(2)
        self.form_layout.addRow("Force (N):", self.force_input)

        self.area_input = QDoubleSpinBox()
        self.area_input.setRange(0.001, 1_000_000)
        self.area_input.setValue(100)
        self.area_input.setDecimals(4)
        self.form_layout.addRow("Area (m²):", self.area_input)

    def get_inputs(self) -> dict:
        return {
            "force": self.force_input.value(),
            "area": self.area_input.value(),
        }

    def perform_calculation(self) -> str:
        inputs = self.get_inputs()
        calc = StressCalculator()
        result = calc.calculate_tensile_stress(inputs["force"], inputs["area"])
        # Extract value from CalculationResult object
        stress_value = result.value if hasattr(result, 'value') else float(result)

        return (
            f"<b>Stress Calculation Results</b><br>"
            f"Force: {inputs['force']:.2f} N<br>"
            f"Area: {inputs['area']:.4f} m²<br>"
            f"<b>Stress: {stress_value:.4f} Pa</b>"
        )

    def _clear_inputs(self) -> None:
        self.force_input.setValue(1000)
        self.area_input.setValue(100)


class ForceCalculatorWidget(CalculatorWidget):
    """Widget for Force Calculator."""

    def _create_inputs(self) -> None:
        self.force1_input = QDoubleSpinBox()
        self.force1_input.setRange(-10_000, 10_000)
        self.force1_input.setValue(100)
        self.force1_input.setDecimals(2)
        self.form_layout.addRow("Force 1 (N):", self.force1_input)

        self.force2_input = QDoubleSpinBox()
        self.force2_input.setRange(-10_000, 10_000)
        self.force2_input.setValue(50)
        self.force2_input.setDecimals(2)
        self.form_layout.addRow("Force 2 (N):", self.force2_input)

    def get_inputs(self) -> dict:
        return {
            "force1": self.force1_input.value(),
            "force2": self.force2_input.value(),
        }

    def perform_calculation(self) -> str:
        inputs = self.get_inputs()
        calc = ForceCalculator()
        calc.set_force_vectors([(inputs["force1"], inputs["force2"])])
        result = calc.calculate("resultant_force")
        # Extract value from CalculationResult object
        resultant_value = result.value if hasattr(result, 'value') else float(result)

        return (
            f"<b>Force Calculation Results</b><br>"
            f"Force X: {inputs['force1']:.2f} N<br>"
            f"Force Y: {inputs['force2']:.2f} N<br>"
            f"<b>Resultant: {resultant_value:.2f} N</b>"
        )

    def _clear_inputs(self) -> None:
        self.force1_input.setValue(100)
        self.force2_input.setValue(50)


class UnitConverterWidget(CalculatorWidget):
    """Widget for Unit Converter."""

    def _create_inputs(self) -> None:
        self.category_combo = QComboBox()
        categories = [cat.name for cat in UnitCategory]
        self.category_combo.addItems(categories)
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        self.form_layout.addRow("Category:", self.category_combo)

        self.value_input = QDoubleSpinBox()
        self.value_input.setRange(-1e10, 1e10)
        self.value_input.setValue(1.0)
        self.value_input.setDecimals(6)
        self.form_layout.addRow("Value:", self.value_input)

        self.from_unit_combo = QComboBox()
        self.form_layout.addRow("From:", self.from_unit_combo)

        self.to_unit_combo = QComboBox()
        self.form_layout.addRow("To:", self.to_unit_combo)

        self._on_category_changed()

    def _on_category_changed(self) -> None:
        category_str = self.category_combo.currentText()
        try:
            category = UnitCategory[category_str]
            units = [u.symbol for u in get_units_by_category(category)]
        except (ValueError, KeyError):
            units = []

        self.from_unit_combo.clear()
        self.from_unit_combo.addItems(units)

        self.to_unit_combo.clear()
        self.to_unit_combo.addItems(units)

        if len(units) > 1:
            self.to_unit_combo.setCurrentIndex(1)

    def get_inputs(self) -> dict:
        return {
            "category": self.category_combo.currentText(),
            "value": self.value_input.value(),
            "from_unit": self.from_unit_combo.currentText(),
            "to_unit": self.to_unit_combo.currentText(),
        }

    def perform_calculation(self) -> str:
        inputs = self.get_inputs()
        converter = UnitConverter()

        result = converter.convert(
            inputs["value"],
            inputs["from_unit"],
            inputs["to_unit"],
        )

        return (
            f"<b>Unit Conversion Results</b><br>"
            f"Category: {inputs['category']}<br>"
            f"{inputs['value']:.6f} {inputs['from_unit']}<br>"
            f"<b>= {result:.6f} {inputs['to_unit']}</b>"
        )

    def _clear_inputs(self) -> None:
        self.value_input.setValue(1.0)
