"""
eng_calc.calculators - Calculation Modules

This package contains the business logic for engineering calculations.
Each calculator module implements the BaseCalculator interface and provides
specific calculation methods for its domain.

Available calculators:
- BaseCalculator: Abstract base class defining the calculator interface
"""

from eng_calc.calculators.base_calculator import BaseCalculator

__all__ = ["BaseCalculator"]
