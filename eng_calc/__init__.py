"""
eng_calc - Engineering Mechanics Calculator

A professional-grade Python engineering calculator for mechanical engineering
calculations including stress, strain, torque, forces, beams, energy, and more.

This package provides:
- Multiple calculation modules for different engineering domains
- Unit conversion support (SI, Imperial)
- Material property database
- Input validation and error handling
- PyQt6-based graphical user interface
"""

__version__ = "0.1.0"
__author__ = "eng-calc contributors"
__license__ = "MIT"

from eng_calc.utilities.errors import (
    EngCalcError,
    ValidationError,
    UnitConversionError,
    CalculationError,
)

__all__ = [
    "__version__",
    "EngCalcError",
    "ValidationError",
    "UnitConversionError",
    "CalculationError",
]
