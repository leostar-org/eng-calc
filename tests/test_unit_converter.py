"""
Tests for UnitConverter class.

This module contains comprehensive tests for the UnitConverter class,
covering all unit categories and edge cases.
"""

import math
import pytest

from eng_calc.utilities import UnitConverter, UnitConversionError, UnitCategory


@pytest.fixture
def converter():
    """Create a UnitConverter instance for testing."""
    return UnitConverter()


class TestConvertMethod:
    """Tests for the convert() method."""

    # ============ Length Conversions ============

    def test_convert_meters_to_feet(self, converter):
        """Test converting meters to feet."""
        result = converter.convert(1, "m", "ft")
        assert math.isclose(result, 3.280839895, rel_tol=1e-6)

    def test_convert_feet_to_meters(self, converter):
        """Test converting feet to meters."""
        result = converter.convert(1, "ft", "m")
        assert math.isclose(result, 0.3048, rel_tol=1e-9)

    def test_convert_inches_to_millimeters(self, converter):
        """Test converting inches to millimeters."""
        result = converter.convert(1, "in", "mm")
        assert math.isclose(result, 25.4, rel_tol=1e-9)

    def test_convert_miles_to_kilometers(self, converter):
        """Test converting miles to kilometers."""
        result = converter.convert(1, "mi", "km")
        assert math.isclose(result, 1.609344, rel_tol=1e-6)

    def test_convert_cm_to_in(self, converter):
        """Test converting centimeters to inches."""
        result = converter.convert(2.54, "cm", "in")
        assert math.isclose(result, 1.0, rel_tol=1e-9)

    # ============ Area Conversions ============

    def test_convert_m2_to_ft2(self, converter):
        """Test converting square meters to square feet."""
        result = converter.convert(1, "m2", "ft2")
        assert math.isclose(result, 10.76391042, rel_tol=1e-6)

    def test_convert_in2_to_mm2(self, converter):
        """Test converting square inches to square millimeters."""
        result = converter.convert(1, "in2", "mm2")
        assert math.isclose(result, 645.16, rel_tol=1e-6)

    # ============ Volume Conversions ============

    def test_convert_liters_to_gallons(self, converter):
        """Test converting liters to US gallons."""
        result = converter.convert(1, "L", "gal")
        assert math.isclose(result, 0.264172052, rel_tol=1e-6)

    def test_convert_cubic_meters_to_liters(self, converter):
        """Test converting cubic meters to liters."""
        result = converter.convert(1, "m3", "L")
        assert math.isclose(result, 1000, rel_tol=1e-9)

    def test_convert_cubic_inches_to_cubic_centimeters(self, converter):
        """Test converting cubic inches to cubic centimeters."""
        result = converter.convert(1, "in3", "cm3")
        assert math.isclose(result, 16.387064, rel_tol=1e-6)

    # ============ Mass Conversions ============

    def test_convert_kg_to_lb(self, converter):
        """Test converting kilograms to pounds."""
        result = converter.convert(1, "kg", "lb")
        assert math.isclose(result, 2.20462262, rel_tol=1e-6)

    def test_convert_lb_to_kg(self, converter):
        """Test converting pounds to kilograms."""
        result = converter.convert(1, "lb", "kg")
        assert math.isclose(result, 0.45359237, rel_tol=1e-9)

    def test_convert_tons_to_kg(self, converter):
        """Test converting metric tons to kilograms."""
        result = converter.convert(1, "t", "kg")
        assert math.isclose(result, 1000, rel_tol=1e-9)

    def test_convert_slug_to_kg(self, converter):
        """Test converting slugs to kilograms."""
        result = converter.convert(1, "slug", "kg")
        assert math.isclose(result, 14.593903, rel_tol=1e-6)

    # ============ Force Conversions ============

    def test_convert_newtons_to_lbf(self, converter):
        """Test converting newtons to pound-force."""
        result = converter.convert(1, "N", "lbf")
        assert math.isclose(result, 0.224808943, rel_tol=1e-6)

    def test_convert_kip_to_kN(self, converter):
        """Test converting kilopounds to kilonewtons."""
        result = converter.convert(1, "kip", "kN")
        assert math.isclose(result, 4.4482216, rel_tol=1e-6)

    def test_convert_kgf_to_N(self, converter):
        """Test converting kilogram-force to newtons."""
        result = converter.convert(1, "kgf", "N")
        assert math.isclose(result, 9.80665, rel_tol=1e-9)

    # ============ Pressure/Stress Conversions ============

    def test_convert_psi_to_MPa(self, converter):
        """Test converting psi to megapascals."""
        result = converter.convert(1, "psi", "MPa")
        assert math.isclose(result, 0.006894757, rel_tol=1e-6)

    def test_convert_MPa_to_psi(self, converter):
        """Test converting megapascals to psi."""
        result = converter.convert(1, "MPa", "psi")
        assert math.isclose(result, 145.03773773, rel_tol=1e-5)

    def test_convert_ksi_to_MPa(self, converter):
        """Test converting ksi to megapascals."""
        result = converter.convert(1, "ksi", "MPa")
        assert math.isclose(result, 6.894757, rel_tol=1e-5)

    def test_convert_bar_to_psi(self, converter):
        """Test converting bar to psi."""
        result = converter.convert(1, "bar", "psi")
        assert math.isclose(result, 14.5037738, rel_tol=1e-5)

    def test_convert_atm_to_kPa(self, converter):
        """Test converting atmospheres to kilopascals."""
        result = converter.convert(1, "atm", "kPa")
        assert math.isclose(result, 101.325, rel_tol=1e-6)

    def test_convert_GPa_to_ksi(self, converter):
        """Test converting gigapascals to ksi."""
        result = converter.convert(1, "GPa", "ksi")
        assert math.isclose(result, 145.0377, rel_tol=1e-4)

    # ============ Torque Conversions ============

    def test_convert_Nm_to_lbf_ft(self, converter):
        """Test converting newton-meters to pound-force feet."""
        result = converter.convert(1, "N.m", "lbf.ft")
        assert math.isclose(result, 0.7375621, rel_tol=1e-5)

    def test_convert_kN_m_to_lbf_in(self, converter):
        """Test converting kilonewton-meters to pound-force inches."""
        result = converter.convert(1, "kN.m", "lbf.in")
        assert math.isclose(result, 8850.7457, rel_tol=1e-4)

    # ============ Energy Conversions ============

    def test_convert_joules_to_BTU(self, converter):
        """Test converting joules to BTU."""
        result = converter.convert(1, "J", "BTU")
        assert math.isclose(result, 0.000947817, rel_tol=1e-5)

    def test_convert_kWh_to_MJ(self, converter):
        """Test converting kilowatt-hours to megajoules."""
        result = converter.convert(1, "kWh", "MJ")
        assert math.isclose(result, 3.6, rel_tol=1e-9)

    def test_convert_cal_to_J(self, converter):
        """Test converting calories to joules."""
        result = converter.convert(1, "cal", "J")
        assert math.isclose(result, 4.184, rel_tol=1e-9)

    def test_convert_ft_lbf_to_J(self, converter):
        """Test converting foot-pound force to joules."""
        result = converter.convert(1, "ft.lbf", "J")
        assert math.isclose(result, 1.3558179, rel_tol=1e-6)

    # ============ Power Conversions ============

    def test_convert_hp_to_kW(self, converter):
        """Test converting horsepower to kilowatts."""
        result = converter.convert(1, "hp", "kW")
        assert math.isclose(result, 0.7456999, rel_tol=1e-5)

    def test_convert_kW_to_hp(self, converter):
        """Test converting kilowatts to horsepower."""
        result = converter.convert(1, "kW", "hp")
        assert math.isclose(result, 1.34102209, rel_tol=1e-5)

    def test_convert_MW_to_BTU_h(self, converter):
        """Test converting megawatts to BTU per hour."""
        result = converter.convert(1, "MW", "BTU/h")
        assert math.isclose(result, 3412141.6, rel_tol=1e-4)

    # ============ Velocity Conversions ============

    def test_convert_m_s_to_mph(self, converter):
        """Test converting meters per second to miles per hour."""
        result = converter.convert(1, "m/s", "mph")
        assert math.isclose(result, 2.23693629, rel_tol=1e-5)

    def test_convert_km_h_to_mph(self, converter):
        """Test converting kilometers per hour to miles per hour."""
        result = converter.convert(100, "km/h", "mph")
        assert math.isclose(result, 62.1371192, rel_tol=1e-5)

    def test_convert_knot_to_m_s(self, converter):
        """Test converting knots to meters per second."""
        result = converter.convert(1, "knot", "m/s")
        assert math.isclose(result, 0.514444444, rel_tol=1e-6)

    # ============ Acceleration Conversions ============

    def test_convert_g0_to_m_s2(self, converter):
        """Test converting standard gravity to m/s^2."""
        result = converter.convert(1, "g0", "m/s2")
        assert math.isclose(result, 9.80665, rel_tol=1e-9)

    def test_convert_ft_s2_to_m_s2(self, converter):
        """Test converting ft/s^2 to m/s^2."""
        result = converter.convert(1, "ft/s2", "m/s2")
        assert math.isclose(result, 0.3048, rel_tol=1e-9)

    # ============ Angular Velocity Conversions ============

    def test_convert_rpm_to_rad_s(self, converter):
        """Test converting RPM to radians per second."""
        result = converter.convert(60, "rpm", "rad/s")
        assert math.isclose(result, 6.28318530718, rel_tol=1e-6)

    def test_convert_Hz_to_rpm(self, converter):
        """Test converting Hertz to RPM."""
        result = converter.convert(1, "Hz", "rpm")
        assert math.isclose(result, 60, rel_tol=1e-6)

    def test_convert_deg_s_to_rad_s(self, converter):
        """Test converting degrees per second to radians per second."""
        result = converter.convert(180, "deg/s", "rad/s")
        assert math.isclose(result, math.pi, rel_tol=1e-6)

    # ============ Density Conversions ============

    def test_convert_kg_m3_to_lb_ft3(self, converter):
        """Test converting kg/m^3 to lb/ft^3."""
        result = converter.convert(1000, "kg/m3", "lb/ft3")
        assert math.isclose(result, 62.4279606, rel_tol=1e-5)

    def test_convert_g_cm3_to_kg_m3(self, converter):
        """Test converting g/cm^3 to kg/m^3."""
        result = converter.convert(1, "g/cm3", "kg/m3")
        assert math.isclose(result, 1000, rel_tol=1e-9)

    # ============ Time Conversions ============

    def test_convert_hours_to_seconds(self, converter):
        """Test converting hours to seconds."""
        result = converter.convert(1, "h", "s")
        assert math.isclose(result, 3600, rel_tol=1e-9)

    def test_convert_minutes_to_ms(self, converter):
        """Test converting minutes to milliseconds."""
        result = converter.convert(1, "min", "ms")
        assert math.isclose(result, 60000, rel_tol=1e-9)

    # ============ Angle Conversions ============

    def test_convert_degrees_to_radians(self, converter):
        """Test converting degrees to radians."""
        result = converter.convert(180, "deg", "rad")
        assert math.isclose(result, math.pi, rel_tol=1e-9)

    def test_convert_radians_to_degrees(self, converter):
        """Test converting radians to degrees."""
        result = converter.convert(math.pi, "rad", "deg")
        assert math.isclose(result, 180, rel_tol=1e-9)

    def test_convert_revolution_to_degrees(self, converter):
        """Test converting revolutions to degrees."""
        result = converter.convert(1, "rev", "deg")
        assert math.isclose(result, 360, rel_tol=1e-6)

    # ============ Moment of Inertia Conversions ============

    def test_convert_mm4_to_in4(self, converter):
        """Test converting mm^4 to in^4."""
        result = converter.convert(1e6, "mm4", "in4")
        assert math.isclose(result, 2.40251, rel_tol=1e-4)

    def test_convert_cm4_to_mm4(self, converter):
        """Test converting cm^4 to mm^4."""
        result = converter.convert(1, "cm4", "mm4")
        assert math.isclose(result, 10000, rel_tol=1e-9)

    # ============ Same Unit Conversion ============

    def test_convert_same_unit_returns_same_value(self, converter):
        """Test that converting to the same unit returns the same value."""
        result = converter.convert(42.5, "m", "m")
        assert result == 42.5

    def test_convert_same_unit_pressure(self, converter):
        """Test same unit conversion for pressure."""
        result = converter.convert(100.0, "MPa", "MPa")
        assert result == 100.0

    # ============ Zero and Negative Values ============

    def test_convert_zero_value(self, converter):
        """Test converting zero value."""
        result = converter.convert(0, "m", "ft")
        assert result == 0

    def test_convert_negative_value(self, converter):
        """Test converting negative value."""
        result = converter.convert(-10, "m", "ft")
        assert math.isclose(result, -32.80839895, rel_tol=1e-6)

    def test_convert_very_small_value(self, converter):
        """Test converting very small values."""
        result = converter.convert(1e-10, "m", "mm")
        assert math.isclose(result, 1e-7, rel_tol=1e-9)

    def test_convert_very_large_value(self, converter):
        """Test converting very large values."""
        result = converter.convert(1e10, "mm", "km")
        assert math.isclose(result, 10000, rel_tol=1e-9)


class TestConvertMethodErrors:
    """Tests for error handling in convert() method."""

    def test_convert_unknown_from_unit(self, converter):
        """Test that converting from an unknown unit raises an error."""
        with pytest.raises(UnitConversionError) as excinfo:
            converter.convert(1, "xyz", "m")
        assert "Unknown unit" in str(excinfo.value)
        assert "xyz" in str(excinfo.value)

    def test_convert_unknown_to_unit(self, converter):
        """Test that converting to an unknown unit raises an error."""
        with pytest.raises(UnitConversionError) as excinfo:
            converter.convert(1, "m", "abc")
        assert "Unknown unit" in str(excinfo.value)
        assert "abc" in str(excinfo.value)

    def test_convert_incompatible_units(self, converter):
        """Test that converting between incompatible units raises an error."""
        with pytest.raises(UnitConversionError) as excinfo:
            converter.convert(1, "m", "kg")
        assert "Cannot convert between different categories" in str(excinfo.value)
        assert "LENGTH" in str(excinfo.value)
        assert "MASS" in str(excinfo.value)

    def test_convert_force_to_pressure_error(self, converter):
        """Test that converting force to pressure raises an error."""
        with pytest.raises(UnitConversionError) as excinfo:
            converter.convert(1, "N", "Pa")
        assert "Cannot convert between different categories" in str(excinfo.value)

    def test_convert_non_numeric_value(self, converter):
        """Test that converting a non-numeric value raises an error."""
        with pytest.raises(UnitConversionError) as excinfo:
            converter.convert("not a number", "m", "ft")
        assert "must be a number" in str(excinfo.value)

    def test_convert_none_value(self, converter):
        """Test that converting None raises an error."""
        with pytest.raises(UnitConversionError):
            converter.convert(None, "m", "ft")


class TestGetConversionFactor:
    """Tests for the get_conversion_factor() method."""

    def test_get_factor_m_to_ft(self, converter):
        """Test getting conversion factor from meters to feet."""
        factor = converter.get_conversion_factor("m", "ft")
        assert math.isclose(factor, 3.280839895, rel_tol=1e-6)

    def test_get_factor_ft_to_m(self, converter):
        """Test getting conversion factor from feet to meters."""
        factor = converter.get_conversion_factor("ft", "m")
        assert math.isclose(factor, 0.3048, rel_tol=1e-9)

    def test_get_factor_same_unit(self, converter):
        """Test that factor for same unit is 1."""
        factor = converter.get_conversion_factor("m", "m")
        assert factor == 1.0

    def test_get_factor_psi_to_MPa(self, converter):
        """Test getting conversion factor from psi to MPa."""
        factor = converter.get_conversion_factor("psi", "MPa")
        assert math.isclose(factor, 0.006894757, rel_tol=1e-6)

    def test_get_factor_kN_to_lbf(self, converter):
        """Test getting conversion factor from kN to lbf."""
        factor = converter.get_conversion_factor("kN", "lbf")
        assert math.isclose(factor, 224.8089431, rel_tol=1e-5)

    def test_get_factor_unknown_unit_raises_error(self, converter):
        """Test that getting factor for unknown unit raises an error."""
        with pytest.raises(UnitConversionError):
            converter.get_conversion_factor("xyz", "m")

    def test_get_factor_incompatible_units_raises_error(self, converter):
        """Test that getting factor for incompatible units raises an error."""
        with pytest.raises(UnitConversionError):
            converter.get_conversion_factor("m", "kg")

    def test_factor_times_value_equals_convert(self, converter):
        """Test that multiplying by factor gives same result as convert()."""
        value = 42.5
        factor = converter.get_conversion_factor("psi", "kPa")
        factor_result = value * factor
        convert_result = converter.convert(value, "psi", "kPa")
        assert math.isclose(factor_result, convert_result, rel_tol=1e-9)


class TestListUnits:
    """Tests for the list_units() method."""

    def test_list_all_units(self, converter):
        """Test listing all units without category filter."""
        units = converter.list_units()
        assert len(units) > 60  # We have 65+ units
        assert all(hasattr(u, "symbol") for u in units)
        assert all(hasattr(u, "category") for u in units)

    def test_list_units_by_category_enum(self, converter):
        """Test listing units by category enum."""
        units = converter.list_units(UnitCategory.LENGTH)
        assert len(units) == 8  # m, mm, cm, km, in, ft, yd, mi
        assert all(u.category == UnitCategory.LENGTH for u in units)

    def test_list_units_by_category_string(self, converter):
        """Test listing units by category string."""
        units = converter.list_units("length")
        assert len(units) == 8
        assert all(u.category == UnitCategory.LENGTH for u in units)

    def test_list_units_by_category_string_uppercase(self, converter):
        """Test listing units by uppercase category string."""
        units = converter.list_units("LENGTH")
        assert len(units) == 8

    def test_list_units_by_category_string_mixed_case(self, converter):
        """Test listing units by mixed case category string."""
        units = converter.list_units("LeNgTh")
        assert len(units) == 8

    def test_list_force_units(self, converter):
        """Test listing force units."""
        units = converter.list_units(UnitCategory.FORCE)
        symbols = [u.symbol for u in units]
        assert "N" in symbols
        assert "kN" in symbols
        assert "lbf" in symbols
        assert "kip" in symbols

    def test_list_pressure_units(self, converter):
        """Test listing pressure units."""
        units = converter.list_units(UnitCategory.PRESSURE)
        symbols = [u.symbol for u in units]
        assert "Pa" in symbols
        assert "MPa" in symbols
        assert "psi" in symbols
        assert "bar" in symbols

    def test_list_units_invalid_category_string(self, converter):
        """Test that listing with invalid category string raises error."""
        with pytest.raises(UnitConversionError) as excinfo:
            converter.list_units("invalid_category")
        assert "Unknown category" in str(excinfo.value)

    def test_list_units_contains_expected_categories(self, converter):
        """Test that key engineering categories have units defined."""
        # Categories that must have units
        required_categories = [
            UnitCategory.LENGTH,
            UnitCategory.AREA,
            UnitCategory.VOLUME,
            UnitCategory.MASS,
            UnitCategory.FORCE,
            UnitCategory.PRESSURE,
            UnitCategory.TORQUE,
            UnitCategory.ENERGY,
            UnitCategory.POWER,
            UnitCategory.VELOCITY,
            UnitCategory.ACCELERATION,
            UnitCategory.ANGULAR_VELOCITY,
            UnitCategory.DENSITY,
            UnitCategory.TIME,
            UnitCategory.ANGLE,
            UnitCategory.MOMENT_OF_INERTIA,
        ]
        for category in required_categories:
            units = converter.list_units(category)
            assert len(units) > 0, f"Category {category.name} has no units"

    def test_list_units_empty_categories(self, converter):
        """Test that some categories may be empty (reserved for future use)."""
        # STRESS and TEMPERATURE are defined but not yet populated
        # This is expected as PRESSURE covers stress units and
        # temperature conversion requires offset handling
        empty_categories = [UnitCategory.STRESS, UnitCategory.TEMPERATURE]
        for category in empty_categories:
            units = converter.list_units(category)
            # These may be empty until implemented
            assert isinstance(units, list)


class TestGetUnitInfo:
    """Tests for the get_unit_info() method."""

    def test_get_unit_info_meter(self, converter):
        """Test getting info for meter."""
        info = converter.get_unit_info("m")
        assert info.symbol == "m"
        assert info.name == "meter"
        assert info.category == UnitCategory.LENGTH
        assert info.to_si_factor == 1.0

    def test_get_unit_info_psi(self, converter):
        """Test getting info for psi."""
        info = converter.get_unit_info("psi")
        assert info.symbol == "psi"
        assert info.name == "pound per square inch"
        assert info.category == UnitCategory.PRESSURE

    def test_get_unit_info_unknown_unit(self, converter):
        """Test that getting info for unknown unit raises error."""
        with pytest.raises(UnitConversionError) as excinfo:
            converter.get_unit_info("xyz")
        assert "Unknown unit" in str(excinfo.value)


class TestGetCategories:
    """Tests for the get_categories() method."""

    def test_get_categories_returns_all(self, converter):
        """Test that get_categories returns all categories."""
        categories = converter.get_categories()
        assert UnitCategory.LENGTH in categories
        assert UnitCategory.MASS in categories
        assert UnitCategory.FORCE in categories
        assert UnitCategory.PRESSURE in categories
        assert UnitCategory.ENERGY in categories
        assert UnitCategory.POWER in categories

    def test_get_categories_count(self, converter):
        """Test that the correct number of categories is returned."""
        categories = converter.get_categories()
        assert len(categories) == len(UnitCategory)


class TestIsValidUnit:
    """Tests for the is_valid_unit() method."""

    def test_is_valid_unit_known(self, converter):
        """Test that known units are valid."""
        assert converter.is_valid_unit("m") is True
        assert converter.is_valid_unit("ft") is True
        assert converter.is_valid_unit("psi") is True
        assert converter.is_valid_unit("MPa") is True

    def test_is_valid_unit_unknown(self, converter):
        """Test that unknown units are invalid."""
        assert converter.is_valid_unit("xyz") is False
        assert converter.is_valid_unit("unknown") is False
        assert converter.is_valid_unit("") is False


class TestAreCompatible:
    """Tests for the are_compatible() method."""

    def test_are_compatible_same_category(self, converter):
        """Test that units in the same category are compatible."""
        assert converter.are_compatible("m", "ft") is True
        assert converter.are_compatible("psi", "MPa") is True
        assert converter.are_compatible("N", "lbf") is True

    def test_are_compatible_different_category(self, converter):
        """Test that units in different categories are not compatible."""
        assert converter.are_compatible("m", "kg") is False
        assert converter.are_compatible("N", "Pa") is False
        assert converter.are_compatible("W", "J") is False

    def test_are_compatible_unknown_unit_raises_error(self, converter):
        """Test that checking compatibility with unknown unit raises error."""
        with pytest.raises(UnitConversionError):
            converter.are_compatible("m", "xyz")


class TestRoundTripConversions:
    """Tests for round-trip conversion accuracy."""

    def test_round_trip_length(self, converter):
        """Test round-trip conversion for length."""
        original = 123.456
        converted = converter.convert(original, "m", "ft")
        back = converter.convert(converted, "ft", "m")
        assert math.isclose(back, original, rel_tol=1e-10)

    def test_round_trip_pressure(self, converter):
        """Test round-trip conversion for pressure."""
        original = 100.0
        converted = converter.convert(original, "MPa", "psi")
        back = converter.convert(converted, "psi", "MPa")
        assert math.isclose(back, original, rel_tol=1e-10)

    def test_round_trip_energy(self, converter):
        """Test round-trip conversion for energy."""
        original = 5000.0
        converted = converter.convert(original, "J", "BTU")
        back = converter.convert(converted, "BTU", "J")
        assert math.isclose(back, original, rel_tol=1e-10)

    def test_round_trip_angular_velocity(self, converter):
        """Test round-trip conversion for angular velocity."""
        original = 3600.0
        converted = converter.convert(original, "rpm", "rad/s")
        back = converter.convert(converted, "rad/s", "rpm")
        assert math.isclose(back, original, rel_tol=1e-10)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_integer_input(self, converter):
        """Test that integer input works correctly."""
        result = converter.convert(1, "m", "mm")
        assert result == 1000.0

    def test_float_input(self, converter):
        """Test that float input works correctly."""
        result = converter.convert(1.5, "m", "mm")
        assert result == 1500.0

    def test_scientific_notation_input(self, converter):
        """Test that scientific notation input works correctly."""
        result = converter.convert(1e-3, "m", "mm")
        assert math.isclose(result, 1.0, rel_tol=1e-9)

    def test_very_precise_conversion(self, converter):
        """Test conversion with high precision requirements."""
        # 1 inch = exactly 25.4 mm
        result = converter.convert(1, "in", "mm")
        assert result == 25.4

    def test_chain_of_conversions(self, converter):
        """Test a chain of conversions maintains accuracy."""
        value = 100.0
        # m -> cm -> mm -> in -> ft -> yd -> m
        v1 = converter.convert(value, "m", "cm")
        v2 = converter.convert(v1, "cm", "mm")
        v3 = converter.convert(v2, "mm", "in")
        v4 = converter.convert(v3, "in", "ft")
        v5 = converter.convert(v4, "ft", "yd")
        v6 = converter.convert(v5, "yd", "m")
        assert math.isclose(v6, value, rel_tol=1e-9)
