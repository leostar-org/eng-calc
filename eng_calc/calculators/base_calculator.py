"""
Base Calculator Module

Defines the abstract base class for all engineering calculators.
All concrete calculator implementations must inherit from BaseCalculator
and implement the required abstract methods.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CalculationResult:
    """
    Represents the result of a calculation.

    Attributes:
        name: Name/identifier of the calculation performed
        value: The calculated numerical result
        unit: Unit of the result value
        formula: The formula used for the calculation
        inputs: Dictionary of input parameters used
    """
    name: str
    value: float
    unit: str
    formula: str
    inputs: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Return a formatted string representation of the result."""
        return f"{self.name}: {self.value:.6g} {self.unit}"


class BaseCalculator(ABC):
    """
    Abstract base class for all engineering calculators.

    This class defines the interface that all calculator modules must implement.
    It provides common functionality for input management, unit handling,
    and result formatting.

    Attributes:
        name: Display name of the calculator
        description: Brief description of what the calculator does
        _inputs: Dictionary storing current input values
        _input_units: Dictionary mapping input names to their units
        _output_units: Dictionary mapping output names to their units
    """

    def __init__(self) -> None:
        """Initialize the base calculator."""
        self._inputs: dict[str, Any] = {}
        self._input_units: dict[str, str] = {}
        self._output_units: dict[str, str] = {}

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the display name of the calculator."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of the calculator's purpose."""
        pass

    @property
    @abstractmethod
    def required_inputs(self) -> list[str]:
        """
        Return a list of required input parameter names.

        Returns:
            List of strings representing required input names
        """
        pass

    @property
    @abstractmethod
    def available_calculations(self) -> list[str]:
        """
        Return a list of available calculation methods.

        Returns:
            List of strings representing calculation method names
        """
        pass

    def set_input(self, name: str, value: float, unit: str | None = None) -> None:
        """
        Set an input parameter value.

        Args:
            name: Name of the input parameter
            value: Numerical value of the input
            unit: Optional unit of the input value

        Raises:
            ValueError: If the input name is not recognized
        """
        self._inputs[name] = value
        if unit is not None:
            self._input_units[name] = unit

    def get_input(self, name: str) -> float | None:
        """
        Get the value of an input parameter.

        Args:
            name: Name of the input parameter

        Returns:
            The input value, or None if not set
        """
        return self._inputs.get(name)

    def set_inputs(self, inputs: dict[str, float]) -> None:
        """
        Set multiple input parameters at once.

        Args:
            inputs: Dictionary mapping input names to values
        """
        for name, value in inputs.items():
            self.set_input(name, value)

    def clear_inputs(self) -> None:
        """Clear all input values."""
        self._inputs.clear()
        self._input_units.clear()

    def set_output_unit(self, output_name: str, unit: str) -> None:
        """
        Set the desired output unit for a calculation result.

        Args:
            output_name: Name of the output/calculation
            unit: Desired unit for the output
        """
        self._output_units[output_name] = unit

    @abstractmethod
    def validate_inputs(self) -> tuple[bool, str]:
        """
        Validate the current input values.

        Returns:
            Tuple of (is_valid, error_message)
            If valid, error_message is empty string
        """
        pass

    @abstractmethod
    def calculate(self, calculation_name: str) -> CalculationResult:
        """
        Perform a specific calculation.

        Args:
            calculation_name: Name of the calculation to perform

        Returns:
            CalculationResult containing the computed value and metadata

        Raises:
            ValidationError: If inputs are invalid
            CalculationError: If the calculation fails
            ValueError: If calculation_name is not recognized
        """
        pass

    def calculate_all(self) -> list[CalculationResult]:
        """
        Perform all available calculations with current inputs.

        Returns:
            List of CalculationResult objects for each calculation

        Raises:
            ValidationError: If inputs are invalid
        """
        results = []
        for calc_name in self.available_calculations:
            try:
                result = self.calculate(calc_name)
                results.append(result)
            except Exception:
                # Skip calculations that fail due to insufficient inputs
                continue
        return results

    @abstractmethod
    def get_formula(self, calculation_name: str) -> str:
        """
        Get the formula string for a specific calculation.

        Args:
            calculation_name: Name of the calculation

        Returns:
            Human-readable formula string
        """
        pass

    def get_all_formulas(self) -> dict[str, str]:
        """
        Get all formulas for this calculator.

        Returns:
            Dictionary mapping calculation names to formula strings
        """
        return {
            calc_name: self.get_formula(calc_name)
            for calc_name in self.available_calculations
        }

    def __repr__(self) -> str:
        """Return a string representation of the calculator."""
        return f"{self.__class__.__name__}(name='{self.name}')"
