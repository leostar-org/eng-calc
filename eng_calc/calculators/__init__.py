"""
eng_calc.calculators - Calculation Modules

This package contains the business logic for engineering calculations.
Each calculator module implements the BaseCalculator interface and provides
specific calculation methods for its domain.

Available calculators:
- BaseCalculator: Abstract base class defining the calculator interface
- StressCalculator: Stress, strain, and elastic modulus calculations
- ForceCalculator: Force analysis and static equilibrium calculations
"""

from eng_calc.calculators.base_calculator import BaseCalculator, CalculationResult
from eng_calc.calculators.force_calculator import ForceCalculator
from eng_calc.calculators.stress_calculator import StressCalculator

__all__ = ["BaseCalculator", "CalculationResult", "ForceCalculator", "StressCalculator"]
