"""
Tests for StressCalculator class.

This module contains comprehensive tests for the StressCalculator class,
covering all calculation methods, unit conversions, and edge cases.
"""

import math
import pytest

from eng_calc.calculators import StressCalculator, CalculationResult
from eng_calc.utilities import ValidationError, CalculationError


@pytest.fixture
def calculator():
    """Create a StressCalculator instance for testing."""
    return StressCalculator()


class TestStressCalculatorProperties:
    """Tests for StressCalculator properties."""

    def test_name(self, calculator):
        """Test that the calculator has the correct name."""
        assert calculator.name == "Stress & Strain Calculator"

    def test_description(self, calculator):
        """Test that the calculator has a description."""
        assert "stress" in calculator.description.lower()
        assert "strain" in calculator.description.lower()

    def test_available_calculations(self, calculator):
        """Test that all expected calculations are available."""
        expected = ["tensile_stress", "shear_stress", "normal_strain", "youngs_modulus"]
        assert calculator.available_calculations == expected

    def test_required_inputs_for_tensile_stress(self, calculator):
        """Test required inputs for tensile stress calculation."""
        required = calculator.get_required_inputs_for("tensile_stress")
        assert "force" in required
        assert "area" in required

    def test_required_inputs_for_shear_stress(self, calculator):
        """Test required inputs for shear stress calculation."""
        required = calculator.get_required_inputs_for("shear_stress")
        assert "force" in required
        assert "area" in required

    def test_required_inputs_for_normal_strain(self, calculator):
        """Test required inputs for normal strain calculation."""
        required = calculator.get_required_inputs_for("normal_strain")
        assert "original_length" in required
        assert "change_in_length" in required

    def test_required_inputs_for_youngs_modulus(self, calculator):
        """Test required inputs for Young's modulus calculation."""
        required = calculator.get_required_inputs_for("youngs_modulus")
        assert "stress" in required
        assert "strain" in required


class TestTensileStressCalculation:
    """Tests for tensile stress calculation (σ = F/A)."""

    def test_basic_tensile_stress(self, calculator):
        """Test basic tensile stress calculation in SI units."""
        # Force = 1000 N, Area = 0.001 m² → σ = 1,000,000 Pa = 1 MPa
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0.001)
        result = calculator.calculate("tensile_stress")

        assert result.name == "tensile_stress"
        assert math.isclose(result.value, 1000000, rel_tol=1e-9)
        assert result.unit == "Pa"
        assert result.formula == "σ = F / A"

    def test_tensile_stress_with_explicit_units(self, calculator):
        """Test tensile stress with explicit SI units."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("area", 0.001, "m2")
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1000000, rel_tol=1e-9)
        assert result.unit == "Pa"

    def test_tensile_stress_with_unit_conversion(self, calculator):
        """Test tensile stress with unit conversion for inputs."""
        # 1 kN = 1000 N, 1000 mm² = 0.001 m²
        calculator.set_input("force", 1, "kN")
        calculator.set_input("area", 1000, "mm2")
        result = calculator.calculate("tensile_stress")

        # 1000 N / 0.001 m² = 1,000,000 Pa
        assert math.isclose(result.value, 1000000, rel_tol=1e-6)

    def test_tensile_stress_with_output_unit_conversion(self, calculator):
        """Test tensile stress with output unit conversion."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("area", 0.001, "m2")
        calculator.set_output_unit("tensile_stress", "MPa")
        result = calculator.calculate("tensile_stress")

        # 1,000,000 Pa = 1 MPa
        assert math.isclose(result.value, 1.0, rel_tol=1e-6)
        assert result.unit == "MPa"

    def test_tensile_stress_imperial_units(self, calculator):
        """Test tensile stress with imperial units."""
        # 1000 lbf / 1 in² = 1000 psi
        calculator.set_input("force", 1000, "lbf")
        calculator.set_input("area", 1, "in2")
        calculator.set_output_unit("tensile_stress", "psi")
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1000, rel_tol=1e-4)
        assert result.unit == "psi"

    def test_tensile_stress_convenience_method(self, calculator):
        """Test the convenience method for tensile stress."""
        result = calculator.calculate_tensile_stress(
            force=1000,
            area=0.001,
            force_unit="N",
            area_unit="m2",
            output_unit="MPa",
        )

        assert math.isclose(result.value, 1.0, rel_tol=1e-6)
        assert result.unit == "MPa"

    def test_tensile_stress_result_contains_inputs(self, calculator):
        """Test that result includes input values."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("area", 0.001, "m2")
        result = calculator.calculate("tensile_stress")

        assert result.inputs["force"] == 1000
        assert result.inputs["area"] == 0.001
        assert result.inputs["force_unit"] == "N"
        assert result.inputs["area_unit"] == "m2"

    def test_tensile_stress_large_values(self, calculator):
        """Test tensile stress with large engineering values."""
        # Steel yield stress ~250 MPa
        # 250 MN force over 1 m² = 250 MPa = 250e6 Pa
        calculator.set_input("force", 250, "MN")
        calculator.set_input("area", 1, "m2")
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 250e6, rel_tol=1e-6)

    def test_tensile_stress_small_values(self, calculator):
        """Test tensile stress with small values."""
        calculator.set_input("force", 0.001, "N")  # 1 mN
        calculator.set_input("area", 0.000001, "m2")  # 1 mm²
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1000, rel_tol=1e-6)


class TestShearStressCalculation:
    """Tests for shear stress calculation (τ = F/A)."""

    def test_basic_shear_stress(self, calculator):
        """Test basic shear stress calculation."""
        calculator.set_input("force", 500)
        calculator.set_input("area", 0.0005)
        result = calculator.calculate("shear_stress")

        assert result.name == "shear_stress"
        assert math.isclose(result.value, 1000000, rel_tol=1e-9)
        assert result.unit == "Pa"
        assert result.formula == "τ = F / A"

    def test_shear_stress_with_units(self, calculator):
        """Test shear stress with unit conversion."""
        calculator.set_input("force", 10, "kN")
        calculator.set_input("area", 100, "mm2")
        calculator.set_output_unit("shear_stress", "MPa")
        result = calculator.calculate("shear_stress")

        # 10000 N / 0.0001 m² = 100 MPa
        assert math.isclose(result.value, 100, rel_tol=1e-4)

    def test_shear_stress_convenience_method(self, calculator):
        """Test the convenience method for shear stress."""
        result = calculator.calculate_shear_stress(
            force=10,
            area=100,
            force_unit="kN",
            area_unit="mm2",
            output_unit="MPa",
        )

        assert math.isclose(result.value, 100, rel_tol=1e-4)


class TestNormalStrainCalculation:
    """Tests for normal strain calculation (ε = ΔL/L₀)."""

    def test_basic_normal_strain(self, calculator):
        """Test basic normal strain calculation."""
        # 10 mm elongation on 1000 mm = 0.01 strain
        calculator.set_input("original_length", 1000)
        calculator.set_input("change_in_length", 10)
        result = calculator.calculate("normal_strain")

        assert result.name == "normal_strain"
        assert math.isclose(result.value, 0.01, rel_tol=1e-9)
        assert result.unit == ""  # Dimensionless
        assert result.formula == "ε = ΔL / L₀"

    def test_strain_with_units(self, calculator):
        """Test strain calculation with units."""
        calculator.set_input("original_length", 1, "m")
        calculator.set_input("change_in_length", 10, "mm")
        result = calculator.calculate("normal_strain")

        # 0.01 m / 1 m = 0.01
        assert math.isclose(result.value, 0.01, rel_tol=1e-6)

    def test_strain_compressive(self, calculator):
        """Test strain with compressive (negative) change."""
        calculator.set_input("original_length", 100, "mm")
        calculator.set_input("change_in_length", -5, "mm")
        result = calculator.calculate("normal_strain")

        assert math.isclose(result.value, -0.05, rel_tol=1e-9)

    def test_strain_convenience_method(self, calculator):
        """Test the convenience method for normal strain."""
        result = calculator.calculate_normal_strain(
            original_length=1000,
            change_in_length=2,
            length_unit="mm",
        )

        assert math.isclose(result.value, 0.002, rel_tol=1e-9)

    def test_strain_result_contains_inputs(self, calculator):
        """Test that strain result includes input values."""
        calculator.set_input("original_length", 100, "mm")
        calculator.set_input("change_in_length", 1, "mm")
        result = calculator.calculate("normal_strain")

        assert result.inputs["original_length"] == 100
        assert result.inputs["change_in_length"] == 1

    def test_strain_typical_steel_value(self, calculator):
        """Test strain at typical steel yield point."""
        # Steel yield strain ~0.002 (0.2%)
        calculator.set_input("original_length", 1000, "mm")
        calculator.set_input("change_in_length", 2, "mm")
        result = calculator.calculate("normal_strain")

        assert math.isclose(result.value, 0.002, rel_tol=1e-9)


class TestYoungsModulusCalculation:
    """Tests for Young's modulus calculation (E = σ/ε)."""

    def test_basic_youngs_modulus(self, calculator):
        """Test basic Young's modulus calculation."""
        # Steel: E ≈ 200 GPa
        # σ = 200 MPa, ε = 0.001 → E = 200 GPa
        calculator.set_input("stress", 200e6)  # 200 MPa in Pa
        calculator.set_input("strain", 0.001)
        result = calculator.calculate("youngs_modulus")

        assert result.name == "youngs_modulus"
        assert math.isclose(result.value, 200e9, rel_tol=1e-9)
        assert result.unit == "Pa"
        assert result.formula == "E = σ / ε"

    def test_youngs_modulus_with_units(self, calculator):
        """Test Young's modulus with unit conversion."""
        calculator.set_input("stress", 200, "MPa")
        calculator.set_input("strain", 0.001)
        calculator.set_output_unit("youngs_modulus", "GPa")
        result = calculator.calculate("youngs_modulus")

        assert math.isclose(result.value, 200, rel_tol=1e-4)
        assert result.unit == "GPa"

    def test_youngs_modulus_convenience_method(self, calculator):
        """Test the convenience method for Young's modulus."""
        result = calculator.calculate_youngs_modulus(
            stress=200,
            strain=0.001,
            stress_unit="MPa",
            output_unit="GPa",
        )

        assert math.isclose(result.value, 200, rel_tol=1e-4)

    def test_youngs_modulus_aluminum(self, calculator):
        """Test Young's modulus for aluminum (~70 GPa)."""
        calculator.set_input("stress", 70, "MPa")
        calculator.set_input("strain", 0.001)
        calculator.set_output_unit("youngs_modulus", "GPa")
        result = calculator.calculate("youngs_modulus")

        assert math.isclose(result.value, 70, rel_tol=1e-4)

    def test_youngs_modulus_negative_strain(self, calculator):
        """Test Young's modulus with compressive stress/strain."""
        # Compressive stress and strain (both negative)
        calculator.set_input("stress", -200e6)
        calculator.set_input("strain", -0.001)
        result = calculator.calculate("youngs_modulus")

        # E is still positive
        assert math.isclose(result.value, 200e9, rel_tol=1e-9)


class TestValidation:
    """Tests for input validation."""

    def test_missing_force_for_stress(self, calculator):
        """Test that missing force raises validation error."""
        calculator.set_input("area", 0.001)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("tensile_stress")
        assert "force" in str(excinfo.value).lower()

    def test_missing_area_for_stress(self, calculator):
        """Test that missing area raises validation error."""
        calculator.set_input("force", 1000)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("tensile_stress")
        assert "area" in str(excinfo.value).lower()

    def test_zero_area_raises_error(self, calculator):
        """Test that zero area raises validation error."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("tensile_stress")
        assert "area" in str(excinfo.value).lower()
        assert "positive" in str(excinfo.value).lower()

    def test_negative_area_raises_error(self, calculator):
        """Test that negative area raises validation error."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", -0.001)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("tensile_stress")
        assert "area" in str(excinfo.value).lower()

    def test_zero_original_length_raises_error(self, calculator):
        """Test that zero original length raises validation error."""
        calculator.set_input("original_length", 0)
        calculator.set_input("change_in_length", 1)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("normal_strain")
        assert "original_length" in str(excinfo.value).lower()

    def test_zero_strain_raises_error(self, calculator):
        """Test that zero strain raises error for Young's modulus."""
        calculator.set_input("stress", 200e6)
        calculator.set_input("strain", 0)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("youngs_modulus")
        assert "strain" in str(excinfo.value).lower()
        assert "zero" in str(excinfo.value).lower()

    def test_nan_input_raises_error(self, calculator):
        """Test that NaN input raises validation error."""
        calculator.set_input("force", float("nan"))
        calculator.set_input("area", 0.001)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("tensile_stress")
        assert "nan" in str(excinfo.value).lower()

    def test_infinite_input_raises_error(self, calculator):
        """Test that infinite input raises validation error."""
        calculator.set_input("force", float("inf"))
        calculator.set_input("area", 0.001)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("tensile_stress")
        assert "infinite" in str(excinfo.value).lower()

    def test_unknown_calculation_raises_error(self, calculator):
        """Test that unknown calculation name raises error."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0.001)
        with pytest.raises(ValueError) as excinfo:
            calculator.calculate("unknown_calculation")
        assert "unknown_calculation" in str(excinfo.value).lower()

    def test_validate_inputs_method(self, calculator):
        """Test the validate_inputs method."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0.001)
        is_valid, error = calculator.validate_inputs()
        assert is_valid is True
        assert error == ""

    def test_validate_for_method(self, calculator):
        """Test the validate_for method."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0.001)
        is_valid, error = calculator.validate_for("tensile_stress")
        assert is_valid is True
        assert error == ""

    def test_validate_for_invalid_inputs(self, calculator):
        """Test validate_for with invalid inputs."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", -0.001)  # Invalid
        is_valid, error = calculator.validate_for("tensile_stress")
        assert is_valid is False
        assert "area" in error.lower()


class TestUnitConversion:
    """Tests for unit conversion functionality."""

    def test_force_kn_to_n(self, calculator):
        """Test force conversion from kN to N."""
        calculator.set_input("force", 1, "kN")  # 1000 N
        calculator.set_input("area", 0.001, "m2")
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1e6, rel_tol=1e-6)

    def test_force_lbf_conversion(self, calculator):
        """Test force conversion from lbf."""
        calculator.set_input("force", 100, "lbf")  # ~444.82 N
        calculator.set_input("area", 0.001, "m2")
        result = calculator.calculate("tensile_stress")

        # 444.82 N / 0.001 m² ≈ 444822 Pa
        assert math.isclose(result.value, 444822.16, rel_tol=1e-4)

    def test_area_mm2_to_m2(self, calculator):
        """Test area conversion from mm² to m²."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("area", 1e6, "mm2")  # 1 m²
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1000, rel_tol=1e-6)

    def test_area_in2_conversion(self, calculator):
        """Test area conversion from in²."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("area", 1, "in2")  # 0.00064516 m²
        result = calculator.calculate("tensile_stress")

        # 1000 N / 0.00064516 m² ≈ 1,550,003 Pa
        assert math.isclose(result.value, 1550003.1, rel_tol=1e-4)

    def test_output_to_mpa(self, calculator):
        """Test output conversion to MPa."""
        calculator.set_input("force", 1000000, "N")
        calculator.set_input("area", 1, "m2")
        calculator.set_output_unit("tensile_stress", "MPa")
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1, rel_tol=1e-6)
        assert result.unit == "MPa"

    def test_output_to_gpa(self, calculator):
        """Test output conversion to GPa."""
        calculator.set_input("force", 1e9, "N")
        calculator.set_input("area", 1, "m2")
        calculator.set_output_unit("tensile_stress", "GPa")
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1, rel_tol=1e-6)
        assert result.unit == "GPa"

    def test_output_to_psi(self, calculator):
        """Test output conversion to psi."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("area", 0.001, "m2")
        calculator.set_output_unit("tensile_stress", "psi")
        result = calculator.calculate("tensile_stress")

        # 1 MPa ≈ 145.038 psi
        assert math.isclose(result.value, 145.038, rel_tol=1e-3)

    def test_length_mm_to_m(self, calculator):
        """Test length conversion for strain calculation."""
        calculator.set_input("original_length", 1000, "mm")  # 1 m
        calculator.set_input("change_in_length", 10, "mm")  # 0.01 m
        result = calculator.calculate("normal_strain")

        assert math.isclose(result.value, 0.01, rel_tol=1e-6)

    def test_stress_unit_for_youngs_modulus(self, calculator):
        """Test stress unit conversion for Young's modulus."""
        calculator.set_input("stress", 200, "MPa")  # 200e6 Pa
        calculator.set_input("strain", 0.001)
        result = calculator.calculate("youngs_modulus")

        # E = 200 GPa in Pa
        assert math.isclose(result.value, 200e9, rel_tol=1e-4)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_very_small_area(self, calculator):
        """Test calculation with very small area."""
        calculator.set_input("force", 1, "N")
        calculator.set_input("area", 1e-12, "m2")  # 1 μm²
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1e12, rel_tol=1e-6)

    def test_very_large_force(self, calculator):
        """Test calculation with very large force."""
        calculator.set_input("force", 1e12, "N")  # 1 TN
        calculator.set_input("area", 1, "m2")
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1e12, rel_tol=1e-6)

    def test_negative_force_compression(self, calculator):
        """Test that negative force (compression) is allowed."""
        calculator.set_input("force", -1000, "N")
        calculator.set_input("area", 0.001, "m2")
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, -1e6, rel_tol=1e-9)

    def test_very_small_strain(self, calculator):
        """Test Young's modulus with very small strain."""
        calculator.set_input("stress", 1e6, "Pa")
        calculator.set_input("strain", 1e-6)
        result = calculator.calculate("youngs_modulus")

        assert math.isclose(result.value, 1e12, rel_tol=1e-6)

    def test_calculate_all(self, calculator):
        """Test calculate_all method."""
        # Set inputs for multiple calculations
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0.001)
        calculator.set_input("original_length", 1000)
        calculator.set_input("change_in_length", 10)
        calculator.set_input("stress", 200e6)
        calculator.set_input("strain", 0.001)

        results = calculator.calculate_all()

        # Should get results for all 4 calculations
        names = [r.name for r in results]
        assert "tensile_stress" in names
        assert "shear_stress" in names
        assert "normal_strain" in names
        assert "youngs_modulus" in names

    def test_clear_inputs(self, calculator):
        """Test that clear_inputs works correctly."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0.001)
        calculator.clear_inputs()

        assert calculator.get_input("force") is None
        assert calculator.get_input("area") is None

    def test_set_inputs_batch(self, calculator):
        """Test set_inputs for batch setting."""
        calculator.set_inputs({"force": 1000, "area": 0.001})
        result = calculator.calculate("tensile_stress")

        assert math.isclose(result.value, 1e6, rel_tol=1e-9)


class TestFormulas:
    """Tests for formula retrieval."""

    def test_get_tensile_stress_formula(self, calculator):
        """Test getting tensile stress formula."""
        formula = calculator.get_formula("tensile_stress")
        assert "σ" in formula
        assert "F" in formula
        assert "A" in formula

    def test_get_shear_stress_formula(self, calculator):
        """Test getting shear stress formula."""
        formula = calculator.get_formula("shear_stress")
        assert "τ" in formula
        assert "F" in formula
        assert "A" in formula

    def test_get_normal_strain_formula(self, calculator):
        """Test getting normal strain formula."""
        formula = calculator.get_formula("normal_strain")
        assert "ε" in formula
        assert "ΔL" in formula
        assert "L" in formula

    def test_get_youngs_modulus_formula(self, calculator):
        """Test getting Young's modulus formula."""
        formula = calculator.get_formula("youngs_modulus")
        assert "E" in formula
        assert "σ" in formula
        assert "ε" in formula

    def test_get_all_formulas(self, calculator):
        """Test getting all formulas."""
        formulas = calculator.get_all_formulas()

        assert "tensile_stress" in formulas
        assert "shear_stress" in formulas
        assert "normal_strain" in formulas
        assert "youngs_modulus" in formulas

    def test_unknown_formula_raises_error(self, calculator):
        """Test that unknown formula name raises error."""
        with pytest.raises(ValueError) as excinfo:
            calculator.get_formula("unknown")
        assert "unknown" in str(excinfo.value).lower()


class TestCalculationResult:
    """Tests for CalculationResult dataclass."""

    def test_result_string_representation(self, calculator):
        """Test string representation of CalculationResult."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0.001)
        result = calculator.calculate("tensile_stress")

        result_str = str(result)
        assert "tensile_stress" in result_str
        assert "Pa" in result_str

    def test_result_attributes(self, calculator):
        """Test CalculationResult attributes."""
        calculator.set_input("force", 1000)
        calculator.set_input("area", 0.001)
        result = calculator.calculate("tensile_stress")

        assert isinstance(result, CalculationResult)
        assert hasattr(result, "name")
        assert hasattr(result, "value")
        assert hasattr(result, "unit")
        assert hasattr(result, "formula")
        assert hasattr(result, "inputs")


class TestRepr:
    """Tests for string representations."""

    def test_calculator_repr(self, calculator):
        """Test calculator __repr__ method."""
        repr_str = repr(calculator)
        assert "StressCalculator" in repr_str
        assert "Stress" in repr_str


class TestRoundTripAccuracy:
    """Tests for calculation accuracy with round-trip conversions."""

    def test_stress_unit_round_trip(self, calculator):
        """Test stress calculation with round-trip unit conversions."""
        # Start with psi, convert through the system
        calculator.set_input("force", 1000, "lbf")
        calculator.set_input("area", 1, "in2")
        calculator.set_output_unit("tensile_stress", "psi")
        result = calculator.calculate("tensile_stress")

        # Should get back ~1000 psi
        assert math.isclose(result.value, 1000, rel_tol=1e-4)

    def test_length_unit_round_trip(self, calculator):
        """Test strain calculation with different length units."""
        # 100 ft with 1 in change
        calculator.set_input("original_length", 100, "ft")
        calculator.set_input("change_in_length", 1, "in")
        result = calculator.calculate("normal_strain")

        # 1 in / 1200 in = 0.000833...
        expected_strain = 1 / (100 * 12)
        assert math.isclose(result.value, expected_strain, rel_tol=1e-4)

    def test_modulus_unit_round_trip(self, calculator):
        """Test Young's modulus with round-trip units."""
        # Input in psi, output in GPa, should still be accurate
        calculator.set_input("stress", 29000, "psi")  # ~200 MPa
        calculator.set_input("strain", 0.001)
        calculator.set_output_unit("youngs_modulus", "GPa")
        result = calculator.calculate("youngs_modulus")

        # 29000 psi = 199.948 MPa, E ≈ 200 GPa
        assert math.isclose(result.value, 199.948, rel_tol=1e-3)
