"""
Tests for ForceCalculator class.

This module contains comprehensive tests for the ForceCalculator class,
covering all calculation methods, unit conversions, and edge cases.
"""

import math
import pytest

from eng_calc.calculators import ForceCalculator, CalculationResult
from eng_calc.utilities import ValidationError


@pytest.fixture
def calculator():
    """Create a ForceCalculator instance for testing."""
    return ForceCalculator()


class TestForceCalculatorProperties:
    """Tests for ForceCalculator properties."""

    def test_name(self, calculator):
        """Test that the calculator has the correct name."""
        assert calculator.name == "Force & Equilibrium Calculator"

    def test_description(self, calculator):
        """Test that the calculator has a description."""
        assert "force" in calculator.description.lower()
        assert "equilibrium" in calculator.description.lower()

    def test_available_calculations(self, calculator):
        """Test that all expected calculations are available."""
        expected = ["resultant_force", "force_components", "moment", "equilibrium"]
        assert calculator.available_calculations == expected

    def test_required_inputs_for_resultant_force(self, calculator):
        """Test required inputs for resultant force calculation."""
        required = calculator.get_required_inputs_for("resultant_force")
        assert "forces" in required

    def test_required_inputs_for_force_components(self, calculator):
        """Test required inputs for force components calculation."""
        required = calculator.get_required_inputs_for("force_components")
        assert "force" in required
        assert "angle" in required

    def test_required_inputs_for_moment(self, calculator):
        """Test required inputs for moment calculation."""
        required = calculator.get_required_inputs_for("moment")
        assert "force" in required
        assert "moment_arm" in required

    def test_required_inputs_for_equilibrium(self, calculator):
        """Test required inputs for equilibrium calculation."""
        required = calculator.get_required_inputs_for("equilibrium")
        assert "forces" in required
        assert "moments" in required


class TestResultantForceCalculation:
    """Tests for resultant force calculation (R = sqrt(Fx^2 + Fy^2))."""

    def test_single_force_horizontal(self, calculator):
        """Test resultant of a single horizontal force."""
        calculator.set_force_vectors([(100, 0)])
        result = calculator.calculate("resultant_force")

        assert result.name == "resultant_force"
        assert math.isclose(result.value, 100, rel_tol=1e-9)
        assert result.unit == "N"

    def test_single_force_vertical(self, calculator):
        """Test resultant of a single vertical force."""
        calculator.set_force_vectors([(0, 100)])
        result = calculator.calculate("resultant_force")

        assert math.isclose(result.value, 100, rel_tol=1e-9)
        assert math.isclose(result.inputs["resultant_angle_deg"], 90, rel_tol=1e-9)

    def test_two_perpendicular_forces(self, calculator):
        """Test resultant of two perpendicular forces (3-4-5 triangle)."""
        # 300 N horizontal + 400 N vertical = 500 N resultant
        calculator.set_force_vectors([(300, 0), (0, 400)])
        result = calculator.calculate("resultant_force")

        assert math.isclose(result.value, 500, rel_tol=1e-9)
        # Angle should be atan2(400, 300) ≈ 53.13°
        expected_angle = math.degrees(math.atan2(400, 300))
        assert math.isclose(
            result.inputs["resultant_angle_deg"], expected_angle, rel_tol=1e-6
        )

    def test_opposing_forces(self, calculator):
        """Test resultant of opposing forces."""
        # 100 N right + 60 N left = 40 N right
        calculator.set_force_vectors([(100, 0), (-60, 0)])
        result = calculator.calculate("resultant_force")

        assert math.isclose(result.value, 40, rel_tol=1e-9)
        assert math.isclose(result.inputs["resultant_angle_deg"], 0, rel_tol=1e-9)

    def test_multiple_forces(self, calculator):
        """Test resultant of multiple forces."""
        # F1 = (100, 0), F2 = (50, 50), F3 = (-30, 40)
        # Sum = (120, 90) → R = sqrt(120² + 90²) = 150
        calculator.set_force_vectors([(100, 0), (50, 50), (-30, 40)])
        result = calculator.calculate("resultant_force")

        assert math.isclose(result.value, 150, rel_tol=1e-9)

    def test_resultant_force_with_unit_conversion(self, calculator):
        """Test resultant force with unit conversion for inputs."""
        # 1 kN horizontal + 1 kN vertical = sqrt(2) kN ≈ 1.414 kN = 1414.21 N
        calculator.set_force_vectors([(1, 0), (0, 1)], "kN")
        result = calculator.calculate("resultant_force")

        expected = math.sqrt(2) * 1000  # Convert kN to N
        assert math.isclose(result.value, expected, rel_tol=1e-6)

    def test_resultant_force_with_output_conversion(self, calculator):
        """Test resultant force with output unit conversion."""
        calculator.set_force_vectors([(1000, 0), (0, 1000)], "N")
        calculator.set_output_unit("resultant_force", "kN")
        result = calculator.calculate("resultant_force")

        expected = math.sqrt(2)  # kN
        assert math.isclose(result.value, expected, rel_tol=1e-6)
        assert result.unit == "kN"

    def test_resultant_force_convenience_method(self, calculator):
        """Test the convenience method for resultant force."""
        result = calculator.calculate_resultant_force(
            forces=[(300, 0), (0, 400)],
            force_unit="N",
            output_unit="N",
        )

        assert math.isclose(result.value, 500, rel_tol=1e-9)

    def test_resultant_force_result_contains_inputs(self, calculator):
        """Test that result includes input values."""
        forces = [(100, 0), (0, 100)]
        calculator.set_force_vectors(forces, "N")
        result = calculator.calculate("resultant_force")

        assert result.inputs["forces"] == forces
        assert result.inputs["forces_unit"] == "N"
        assert "sum_fx" in result.inputs
        assert "sum_fy" in result.inputs

    def test_balanced_forces_zero_resultant(self, calculator):
        """Test that balanced forces give zero resultant."""
        # Four forces in a cross pattern that cancel out
        calculator.set_force_vectors([(100, 0), (-100, 0), (0, 100), (0, -100)])
        result = calculator.calculate("resultant_force")

        assert math.isclose(result.value, 0, abs_tol=1e-9)


class TestForceComponentsCalculation:
    """Tests for force components calculation (Fx = F*cos(θ), Fy = F*sin(θ))."""

    def test_force_at_zero_degrees(self, calculator):
        """Test force components at 0 degrees (all horizontal)."""
        calculator.set_input("force", 100)
        calculator.set_input("angle", 0)
        result = calculator.calculate("force_components")

        assert result.name == "force_components"
        assert math.isclose(result.value, 100, rel_tol=1e-9)  # Fx
        assert math.isclose(result.inputs["fx"], 100, rel_tol=1e-9)
        assert math.isclose(result.inputs["fy"], 0, abs_tol=1e-9)

    def test_force_at_90_degrees(self, calculator):
        """Test force components at 90 degrees (all vertical)."""
        calculator.set_input("force", 100)
        calculator.set_input("angle", 90)
        result = calculator.calculate("force_components")

        assert math.isclose(result.inputs["fx"], 0, abs_tol=1e-9)
        assert math.isclose(result.inputs["fy"], 100, rel_tol=1e-9)

    def test_force_at_45_degrees(self, calculator):
        """Test force components at 45 degrees (equal components)."""
        calculator.set_input("force", 100)
        calculator.set_input("angle", 45)
        result = calculator.calculate("force_components")

        expected = 100 * math.cos(math.radians(45))
        assert math.isclose(result.inputs["fx"], expected, rel_tol=1e-9)
        assert math.isclose(result.inputs["fy"], expected, rel_tol=1e-9)

    def test_force_at_30_degrees(self, calculator):
        """Test force components at 30 degrees."""
        calculator.set_input("force", 100)
        calculator.set_input("angle", 30)
        result = calculator.calculate("force_components")

        # cos(30°) ≈ 0.866, sin(30°) = 0.5
        assert math.isclose(result.inputs["fx"], 100 * math.sqrt(3) / 2, rel_tol=1e-6)
        assert math.isclose(result.inputs["fy"], 50, rel_tol=1e-6)

    def test_force_at_180_degrees(self, calculator):
        """Test force components at 180 degrees (negative x)."""
        calculator.set_input("force", 100)
        calculator.set_input("angle", 180)
        result = calculator.calculate("force_components")

        assert math.isclose(result.inputs["fx"], -100, rel_tol=1e-9)
        assert math.isclose(result.inputs["fy"], 0, abs_tol=1e-9)

    def test_force_components_with_radians(self, calculator):
        """Test force components with angle in radians."""
        calculator.set_input("force", 100, "N")
        calculator.set_input("angle", math.pi / 4, "rad")  # 45 degrees
        result = calculator.calculate("force_components")

        expected = 100 / math.sqrt(2)
        assert math.isclose(result.inputs["fx"], expected, rel_tol=1e-9)
        assert math.isclose(result.inputs["fy"], expected, rel_tol=1e-9)

    def test_force_components_with_unit_conversion(self, calculator):
        """Test force components with unit conversion."""
        calculator.set_input("force", 1, "kN")  # 1000 N
        calculator.set_input("angle", 60, "deg")
        result = calculator.calculate("force_components")

        # Fx = 1000 * cos(60°) = 500 N
        # Fy = 1000 * sin(60°) ≈ 866 N
        assert math.isclose(result.inputs["fx"], 500, rel_tol=1e-6)
        assert math.isclose(result.inputs["fy"], 1000 * math.sqrt(3) / 2, rel_tol=1e-6)

    def test_force_components_convenience_method(self, calculator):
        """Test the convenience method for force components."""
        result = calculator.calculate_force_components(
            force=100,
            angle=45,
            force_unit="N",
            angle_unit="deg",
        )

        expected = 100 / math.sqrt(2)
        assert math.isclose(result.inputs["fx"], expected, rel_tol=1e-9)
        assert math.isclose(result.inputs["fy"], expected, rel_tol=1e-9)

    def test_force_components_with_output_conversion(self, calculator):
        """Test force components with output unit conversion."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("angle", 0, "deg")
        calculator.set_output_unit("force_components", "kN")
        result = calculator.calculate("force_components")

        assert math.isclose(result.value, 1, rel_tol=1e-6)
        assert result.unit == "kN"


class TestMomentCalculation:
    """Tests for moment calculation (M = F × d)."""

    def test_basic_moment(self, calculator):
        """Test basic moment calculation (perpendicular force)."""
        # M = 100 N × 2 m = 200 N·m
        calculator.set_input("force", 100)
        calculator.set_input("moment_arm", 2)
        result = calculator.calculate("moment")

        assert result.name == "moment"
        assert math.isclose(result.value, 200, rel_tol=1e-9)
        assert result.unit == "N.m"
        assert "F × d" in result.formula

    def test_moment_with_angle(self, calculator):
        """Test moment with non-perpendicular force."""
        # M = 100 N × 2 m × sin(30°) = 100 N·m
        calculator.set_input("force", 100)
        calculator.set_input("moment_arm", 2)
        calculator.set_input("angle", 30)
        result = calculator.calculate("moment")

        assert math.isclose(result.value, 100, rel_tol=1e-6)

    def test_moment_at_90_degrees(self, calculator):
        """Test moment at 90 degrees (perpendicular - maximum)."""
        calculator.set_input("force", 100)
        calculator.set_input("moment_arm", 2)
        calculator.set_input("angle", 90)
        result = calculator.calculate("moment")

        assert math.isclose(result.value, 200, rel_tol=1e-9)

    def test_moment_at_zero_degrees(self, calculator):
        """Test moment at 0 degrees (parallel - zero moment)."""
        calculator.set_input("force", 100)
        calculator.set_input("moment_arm", 2)
        calculator.set_input("angle", 0)
        result = calculator.calculate("moment")

        assert math.isclose(result.value, 0, abs_tol=1e-9)

    def test_moment_with_unit_conversion(self, calculator):
        """Test moment with unit conversion."""
        # 1 kN × 500 mm = 0.5 kN·m = 500 N·m
        calculator.set_input("force", 1, "kN")
        calculator.set_input("moment_arm", 500, "mm")
        result = calculator.calculate("moment")

        assert math.isclose(result.value, 500, rel_tol=1e-6)

    def test_moment_with_output_conversion(self, calculator):
        """Test moment with output unit conversion."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("moment_arm", 1, "m")
        calculator.set_output_unit("moment", "kN.m")
        result = calculator.calculate("moment")

        assert math.isclose(result.value, 1, rel_tol=1e-6)
        assert result.unit == "kN.m"

    def test_moment_convenience_method(self, calculator):
        """Test the convenience method for moment."""
        result = calculator.calculate_moment(
            force=100,
            moment_arm=2,
            force_unit="N",
            moment_arm_unit="m",
        )

        assert math.isclose(result.value, 200, rel_tol=1e-9)

    def test_moment_convenience_method_with_angle(self, calculator):
        """Test the convenience method for moment with angle."""
        result = calculator.calculate_moment(
            force=100,
            moment_arm=2,
            angle=30,
            angle_unit="deg",
        )

        assert math.isclose(result.value, 100, rel_tol=1e-6)

    def test_moment_negative_force(self, calculator):
        """Test moment with negative force (opposite direction)."""
        calculator.set_input("force", -100)
        calculator.set_input("moment_arm", 2)
        result = calculator.calculate("moment")

        assert math.isclose(result.value, -200, rel_tol=1e-9)

    def test_moment_imperial_units(self, calculator):
        """Test moment with imperial units."""
        # 100 lbf × 1 ft = 100 lbf·ft
        calculator.set_input("force", 100, "lbf")
        calculator.set_input("moment_arm", 1, "ft")
        calculator.set_output_unit("moment", "lbf.ft")
        result = calculator.calculate("moment")

        assert math.isclose(result.value, 100, rel_tol=1e-4)
        assert result.unit == "lbf.ft"


class TestEquilibriumCalculation:
    """Tests for equilibrium check (ΣFx=0, ΣFy=0, ΣM=0)."""

    def test_simple_equilibrium(self, calculator):
        """Test simple force equilibrium."""
        # Two equal and opposite forces
        calculator.set_force_vectors([(100, 0), (-100, 0)])
        result = calculator.calculate("equilibrium")

        assert result.name == "equilibrium"
        assert result.value == 1.0  # In equilibrium
        assert result.inputs["is_in_equilibrium"] is True

    def test_equilibrium_with_moments(self, calculator):
        """Test equilibrium with balanced moments."""
        calculator.set_force_vectors([(100, 0), (-100, 0)])
        calculator.set_moments([50, -50])
        result = calculator.calculate("equilibrium")

        assert result.value == 1.0
        assert result.inputs["is_in_equilibrium"] is True
        assert math.isclose(result.inputs["sum_m"], 0, abs_tol=1e-9)

    def test_force_not_in_equilibrium(self, calculator):
        """Test detection of force imbalance."""
        calculator.set_force_vectors([(100, 0), (-50, 0)])
        result = calculator.calculate("equilibrium")

        assert result.value == 0.0  # Not in equilibrium
        assert result.inputs["is_in_equilibrium"] is False
        assert result.inputs["fx_equilibrium"] is False

    def test_moment_not_in_equilibrium(self, calculator):
        """Test detection of moment imbalance."""
        calculator.set_force_vectors([(100, 0), (-100, 0)])
        calculator.set_moments([50, -30])  # Net moment of 20
        result = calculator.calculate("equilibrium")

        assert result.value == 0.0
        assert result.inputs["is_in_equilibrium"] is False
        assert result.inputs["m_equilibrium"] is False

    def test_complex_equilibrium(self, calculator):
        """Test complex equilibrium with multiple forces."""
        # Rectangle in equilibrium: forces at corners that sum to zero
        forces = [
            (100, 50),
            (-100, 50),
            (-100, -50),
            (100, -50),
        ]
        calculator.set_force_vectors(forces)
        result = calculator.calculate("equilibrium")

        assert result.value == 1.0
        assert result.inputs["is_in_equilibrium"] is True

    def test_equilibrium_convenience_method(self, calculator):
        """Test the convenience method for equilibrium check."""
        result = calculator.check_equilibrium(
            forces=[(100, 0), (-100, 0)],
            moments=[50, -50],
        )

        assert result.value == 1.0
        assert result.inputs["is_in_equilibrium"] is True

    def test_equilibrium_without_moments(self, calculator):
        """Test equilibrium check without moments (only force balance)."""
        result = calculator.check_equilibrium(
            forces=[(100, 100), (-100, -100)],
        )

        assert result.value == 1.0
        assert result.inputs["m_equilibrium"] is True

    def test_equilibrium_result_contains_residuals(self, calculator):
        """Test that equilibrium result contains residual values."""
        calculator.set_force_vectors([(100, 50), (-90, -50)])
        result = calculator.calculate("equilibrium")

        assert "sum_fx" in result.inputs
        assert "sum_fy" in result.inputs
        assert "sum_m" in result.inputs
        assert math.isclose(result.inputs["sum_fx"], 10, rel_tol=1e-9)

    def test_equilibrium_with_unit_conversion(self, calculator):
        """Test equilibrium with unit conversion."""
        # 1 kN = 1000 N
        calculator.set_force_vectors([(1, 0), (-1, 0)], "kN")
        calculator.set_moments([1, -1], "kN.m")
        result = calculator.calculate("equilibrium")

        assert result.value == 1.0
        assert result.inputs["is_in_equilibrium"] is True


class TestValidation:
    """Tests for input validation."""

    def test_empty_forces_raises_error(self, calculator):
        """Test that empty force list raises validation error."""
        calculator.set_force_vectors([])
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("resultant_force")
        assert "force" in str(excinfo.value).lower()

    def test_missing_forces_raises_error(self, calculator):
        """Test that missing forces raises validation error."""
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("resultant_force")
        assert "force" in str(excinfo.value).lower()

    def test_invalid_force_tuple_raises_error(self, calculator):
        """Test that invalid force tuple raises validation error."""
        calculator._inputs["forces"] = [(100,)]  # Only one component
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("resultant_force")
        assert "tuple" in str(excinfo.value).lower()

    def test_nan_force_raises_error(self, calculator):
        """Test that NaN force component raises validation error."""
        calculator.set_force_vectors([(float("nan"), 0)])
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("resultant_force")
        assert "nan" in str(excinfo.value).lower()

    def test_infinite_force_raises_error(self, calculator):
        """Test that infinite force component raises validation error."""
        calculator.set_force_vectors([(float("inf"), 0)])
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("resultant_force")
        assert "infinite" in str(excinfo.value).lower()

    def test_missing_force_for_components(self, calculator):
        """Test that missing force raises error for components calculation."""
        calculator.set_input("angle", 45)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("force_components")
        assert "force" in str(excinfo.value).lower()

    def test_missing_angle_for_components(self, calculator):
        """Test that missing angle raises error for components calculation."""
        calculator.set_input("force", 100)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("force_components")
        assert "angle" in str(excinfo.value).lower()

    def test_negative_force_for_components_raises_error(self, calculator):
        """Test that negative force magnitude raises error."""
        calculator.set_input("force", -100)
        calculator.set_input("angle", 45)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("force_components")
        assert "force" in str(excinfo.value).lower()

    def test_missing_moment_arm_raises_error(self, calculator):
        """Test that missing moment arm raises error."""
        calculator.set_input("force", 100)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("moment")
        assert "moment_arm" in str(excinfo.value).lower()

    def test_negative_moment_arm_raises_error(self, calculator):
        """Test that negative moment arm raises error."""
        calculator.set_input("force", 100)
        calculator.set_input("moment_arm", -2)
        with pytest.raises(ValidationError) as excinfo:
            calculator.calculate("moment")
        assert "moment_arm" in str(excinfo.value).lower()

    def test_unknown_calculation_raises_error(self, calculator):
        """Test that unknown calculation name raises error."""
        calculator.set_force_vectors([(100, 0)])
        with pytest.raises(ValueError) as excinfo:
            calculator.calculate("unknown_calculation")
        assert "unknown_calculation" in str(excinfo.value).lower()

    def test_validate_inputs_method(self, calculator):
        """Test the validate_inputs method."""
        calculator.set_input("force", 100)
        calculator.set_input("angle", 45)
        is_valid, error = calculator.validate_inputs()
        assert is_valid is True
        assert error == ""

    def test_validate_for_method(self, calculator):
        """Test the validate_for method."""
        calculator.set_force_vectors([(100, 0)])
        is_valid, error = calculator.validate_for("resultant_force")
        assert is_valid is True
        assert error == ""

    def test_validate_for_invalid_inputs(self, calculator):
        """Test validate_for with invalid inputs."""
        calculator.set_input("force", -100)  # Invalid for components
        calculator.set_input("angle", 45)
        is_valid, error = calculator.validate_for("force_components")
        assert is_valid is False
        assert "force" in error.lower()


class TestUnitConversion:
    """Tests for unit conversion functionality."""

    def test_force_kn_to_n(self, calculator):
        """Test force conversion from kN to N."""
        calculator.set_force_vectors([(1, 0)], "kN")
        result = calculator.calculate("resultant_force")

        assert math.isclose(result.value, 1000, rel_tol=1e-6)

    def test_force_lbf_conversion(self, calculator):
        """Test force conversion from lbf."""
        calculator.set_force_vectors([(100, 0)], "lbf")
        result = calculator.calculate("resultant_force")

        # 100 lbf ≈ 444.82 N
        assert math.isclose(result.value, 444.82216, rel_tol=1e-4)

    def test_moment_arm_mm_to_m(self, calculator):
        """Test moment arm conversion from mm to m."""
        calculator.set_input("force", 1000, "N")
        calculator.set_input("moment_arm", 500, "mm")  # 0.5 m
        result = calculator.calculate("moment")

        # 1000 N × 0.5 m = 500 N·m
        assert math.isclose(result.value, 500, rel_tol=1e-6)

    def test_angle_radians(self, calculator):
        """Test angle conversion with radians."""
        calculator.set_input("force", 100, "N")
        calculator.set_input("angle", math.pi / 3, "rad")  # 60 degrees
        result = calculator.calculate("force_components")

        # Fx = 100 * cos(60°) = 50
        assert math.isclose(result.inputs["fx"], 50, rel_tol=1e-6)

    def test_output_to_kn(self, calculator):
        """Test output conversion to kN."""
        calculator.set_force_vectors([(1000, 0)], "N")
        calculator.set_output_unit("resultant_force", "kN")
        result = calculator.calculate("resultant_force")

        assert math.isclose(result.value, 1, rel_tol=1e-6)
        assert result.unit == "kN"

    def test_moment_output_to_knm(self, calculator):
        """Test moment output conversion to kN·m."""
        calculator.set_input("force", 10000, "N")
        calculator.set_input("moment_arm", 1, "m")
        calculator.set_output_unit("moment", "kN.m")
        result = calculator.calculate("moment")

        assert math.isclose(result.value, 10, rel_tol=1e-6)
        assert result.unit == "kN.m"


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_zero_force(self, calculator):
        """Test with zero force."""
        calculator.set_force_vectors([(0, 0)])
        result = calculator.calculate("resultant_force")

        assert math.isclose(result.value, 0, abs_tol=1e-9)

    def test_zero_force_components(self, calculator):
        """Test force components with zero force."""
        calculator.set_input("force", 0)
        calculator.set_input("angle", 45)
        result = calculator.calculate("force_components")

        assert math.isclose(result.inputs["fx"], 0, abs_tol=1e-9)
        assert math.isclose(result.inputs["fy"], 0, abs_tol=1e-9)

    def test_zero_moment_arm(self, calculator):
        """Test moment with zero moment arm."""
        calculator.set_input("force", 100)
        calculator.set_input("moment_arm", 0)
        result = calculator.calculate("moment")

        assert math.isclose(result.value, 0, abs_tol=1e-9)

    def test_very_small_forces(self, calculator):
        """Test with very small force values."""
        calculator.set_force_vectors([(1e-9, 0), (0, 1e-9)])
        result = calculator.calculate("resultant_force")

        expected = math.sqrt(2) * 1e-9
        assert math.isclose(result.value, expected, rel_tol=1e-6)

    def test_very_large_forces(self, calculator):
        """Test with very large force values."""
        calculator.set_force_vectors([(1e12, 0), (0, 1e12)])
        result = calculator.calculate("resultant_force")

        expected = math.sqrt(2) * 1e12
        assert math.isclose(result.value, expected, rel_tol=1e-6)

    def test_negative_angle(self, calculator):
        """Test force components with negative angle."""
        calculator.set_input("force", 100)
        calculator.set_input("angle", -45)
        result = calculator.calculate("force_components")

        expected_fx = 100 * math.cos(math.radians(-45))
        expected_fy = 100 * math.sin(math.radians(-45))
        assert math.isclose(result.inputs["fx"], expected_fx, rel_tol=1e-9)
        assert math.isclose(result.inputs["fy"], expected_fy, rel_tol=1e-9)

    def test_angle_greater_than_360(self, calculator):
        """Test force components with angle > 360 degrees."""
        calculator.set_input("force", 100)
        calculator.set_input("angle", 405)  # Same as 45 degrees
        result = calculator.calculate("force_components")

        expected = 100 / math.sqrt(2)
        assert math.isclose(result.inputs["fx"], expected, rel_tol=1e-6)
        assert math.isclose(result.inputs["fy"], expected, rel_tol=1e-6)

    def test_calculate_all(self, calculator):
        """Test calculate_all method."""
        # Set inputs for multiple calculations
        calculator.set_force_vectors([(100, 0), (-100, 0)])
        calculator.set_moments([50, -50])
        calculator.set_input("force", 100)
        calculator.set_input("angle", 45)
        calculator.set_input("moment_arm", 2)

        results = calculator.calculate_all()

        # Should get results for calculations that have sufficient inputs
        names = [r.name for r in results]
        assert "resultant_force" in names
        assert "equilibrium" in names

    def test_clear_inputs(self, calculator):
        """Test that clear_inputs works correctly."""
        calculator.set_force_vectors([(100, 0)])
        calculator.set_input("force", 100)
        calculator.clear_inputs()

        assert calculator.get_input("force") is None
        assert len(calculator._force_vectors) == 0

    def test_set_inputs_batch(self, calculator):
        """Test set_inputs for batch setting."""
        calculator.set_inputs({"force": 100, "angle": 45})
        result = calculator.calculate("force_components")

        expected = 100 / math.sqrt(2)
        assert math.isclose(result.inputs["fx"], expected, rel_tol=1e-9)


class TestFormulas:
    """Tests for formula retrieval."""

    def test_get_resultant_force_formula(self, calculator):
        """Test getting resultant force formula."""
        formula = calculator.get_formula("resultant_force")
        assert "R" in formula
        assert "√" in formula or "sqrt" in formula.lower()

    def test_get_force_components_formula(self, calculator):
        """Test getting force components formula."""
        formula = calculator.get_formula("force_components")
        assert "Fx" in formula
        assert "Fy" in formula
        assert "cos" in formula
        assert "sin" in formula

    def test_get_moment_formula(self, calculator):
        """Test getting moment formula."""
        formula = calculator.get_formula("moment")
        assert "M" in formula
        assert "F" in formula
        assert "d" in formula

    def test_get_equilibrium_formula(self, calculator):
        """Test getting equilibrium formula."""
        formula = calculator.get_formula("equilibrium")
        assert "ΣFx" in formula or "Fx" in formula
        assert "0" in formula

    def test_get_all_formulas(self, calculator):
        """Test getting all formulas."""
        formulas = calculator.get_all_formulas()

        assert "resultant_force" in formulas
        assert "force_components" in formulas
        assert "moment" in formulas
        assert "equilibrium" in formulas

    def test_unknown_formula_raises_error(self, calculator):
        """Test that unknown formula name raises error."""
        with pytest.raises(ValueError) as excinfo:
            calculator.get_formula("unknown")
        assert "unknown" in str(excinfo.value).lower()


class TestCalculationResult:
    """Tests for CalculationResult dataclass."""

    def test_result_string_representation(self, calculator):
        """Test string representation of CalculationResult."""
        calculator.set_force_vectors([(100, 0)])
        result = calculator.calculate("resultant_force")

        result_str = str(result)
        assert "resultant_force" in result_str
        assert "N" in result_str

    def test_result_attributes(self, calculator):
        """Test CalculationResult attributes."""
        calculator.set_force_vectors([(100, 0)])
        result = calculator.calculate("resultant_force")

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
        assert "ForceCalculator" in repr_str
        assert "Force" in repr_str


class TestRoundTripAccuracy:
    """Tests for calculation accuracy with round-trip conversions."""

    def test_force_unit_round_trip(self, calculator):
        """Test force calculation with round-trip unit conversions."""
        # Start with lbf, convert through the system
        calculator.set_force_vectors([(100, 0), (0, 100)], "lbf")
        calculator.set_output_unit("resultant_force", "lbf")
        result = calculator.calculate("resultant_force")

        # Should get back sqrt(2) * 100 ≈ 141.42 lbf
        expected = 100 * math.sqrt(2)
        assert math.isclose(result.value, expected, rel_tol=1e-4)

    def test_moment_unit_round_trip(self, calculator):
        """Test moment calculation with round-trip unit conversions."""
        # Calculate in imperial, output in imperial
        calculator.set_input("force", 100, "lbf")
        calculator.set_input("moment_arm", 1, "ft")
        calculator.set_output_unit("moment", "lbf.ft")
        result = calculator.calculate("moment")

        # Should get back ~100 lbf·ft
        assert math.isclose(result.value, 100, rel_tol=1e-4)

    def test_components_verify_magnitude(self, calculator):
        """Test that force components recreate original magnitude."""
        original_force = 250
        angle = 37  # degrees

        calculator.set_input("force", original_force)
        calculator.set_input("angle", angle)
        result = calculator.calculate("force_components")

        fx = result.inputs["fx"]
        fy = result.inputs["fy"]

        # Verify magnitude: sqrt(fx² + fy²) should equal original force
        reconstructed = math.sqrt(fx**2 + fy**2)
        assert math.isclose(reconstructed, original_force, rel_tol=1e-9)


class TestPhysicalScenarios:
    """Tests for realistic physical scenarios."""

    def test_beam_equilibrium(self, calculator):
        """Test simply supported beam equilibrium."""
        # A 10m beam with 1000N load at center
        # Reactions: R1 = R2 = 500N (upward)
        # Sum of forces: 500 + 500 - 1000 = 0
        result = calculator.check_equilibrium(
            forces=[
                (0, 500),    # Left reaction
                (0, 500),    # Right reaction
                (0, -1000),  # Applied load
            ],
        )
        assert result.inputs["is_in_equilibrium"] is True

    def test_bracket_force_analysis(self, calculator):
        """Test force analysis for an angled bracket."""
        # 45-degree bracket with 1000N vertical load
        # Horizontal and vertical reactions needed
        angle = 45
        load = 1000

        result = calculator.calculate_force_components(
            force=load,
            angle=angle,
        )

        # Both components should be equal for 45 degrees
        assert math.isclose(result.inputs["fx"], result.inputs["fy"], rel_tol=1e-9)

    def test_crane_moment(self, calculator):
        """Test moment calculation for a crane arm."""
        # Crane arm: 5m long, 10kN load at tip
        result = calculator.calculate_moment(
            force=10,
            moment_arm=5,
            force_unit="kN",
            moment_arm_unit="m",
            output_unit="kN.m",
        )

        assert math.isclose(result.value, 50, rel_tol=1e-6)
        assert result.unit == "kN.m"

    def test_truss_joint_equilibrium(self, calculator):
        """Test equilibrium at a truss joint."""
        # Three forces meeting at a joint
        # 100N horizontal, 100N at 120°, 100N at 240° (should sum to zero)
        f1 = (100, 0)
        f2 = (100 * math.cos(math.radians(120)), 100 * math.sin(math.radians(120)))
        f3 = (100 * math.cos(math.radians(240)), 100 * math.sin(math.radians(240)))

        result = calculator.check_equilibrium(forces=[f1, f2, f3])

        assert result.inputs["is_in_equilibrium"] is True
