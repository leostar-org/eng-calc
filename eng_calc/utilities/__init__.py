"""
eng_calc.utilities - Utility Modules

This package contains utility modules for:
- Custom exceptions and error handling
- Physical constants
- Unit definitions and conversion
- Input validation
"""

from eng_calc.utilities.errors import (
    EngCalcError,
    ValidationError,
    UnitConversionError,
    CalculationError,
    MaterialNotFoundError,
)
from eng_calc.utilities.constants import PhysicalConstants
from eng_calc.utilities.units import UnitCategory, UnitDefinition, UNIT_DEFINITIONS
from eng_calc.utilities.validators import Validator

__all__ = [
    "EngCalcError",
    "ValidationError",
    "UnitConversionError",
    "CalculationError",
    "MaterialNotFoundError",
    "PhysicalConstants",
    "UnitCategory",
    "UnitDefinition",
    "UNIT_DEFINITIONS",
    "Validator",
]
