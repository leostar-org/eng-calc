"""
Unit Definitions Module

Defines unit categories, unit definitions, and conversion factors
for use in engineering calculations.
"""

from dataclasses import dataclass
from enum import Enum, auto


class UnitCategory(Enum):
    """Categories of physical units."""

    LENGTH = auto()
    AREA = auto()
    VOLUME = auto()
    MASS = auto()
    FORCE = auto()
    PRESSURE = auto()
    STRESS = auto()
    TORQUE = auto()
    ENERGY = auto()
    POWER = auto()
    VELOCITY = auto()
    ACCELERATION = auto()
    ANGULAR_VELOCITY = auto()
    DENSITY = auto()
    TEMPERATURE = auto()
    TIME = auto()
    ANGLE = auto()
    MOMENT_OF_INERTIA = auto()


@dataclass(frozen=True)
class UnitDefinition:
    """
    Definition of a unit with its conversion factor to SI base unit.

    Attributes:
        symbol: The unit symbol (e.g., "m", "ft", "Pa")
        name: Full name of the unit (e.g., "meter", "foot", "pascal")
        category: The physical quantity category
        to_si_factor: Multiplication factor to convert to SI base unit
        to_si_offset: Additive offset for conversion (used for temperature)
    """

    symbol: str
    name: str
    category: UnitCategory
    to_si_factor: float
    to_si_offset: float = 0.0

    def to_si(self, value: float) -> float:
        """
        Convert a value from this unit to SI.

        Args:
            value: Value in this unit

        Returns:
            Value in SI base unit
        """
        return value * self.to_si_factor + self.to_si_offset

    def from_si(self, value: float) -> float:
        """
        Convert a value from SI to this unit.

        Args:
            value: Value in SI base unit

        Returns:
            Value in this unit
        """
        return (value - self.to_si_offset) / self.to_si_factor


# Unit definitions organized by category
# Conversion factors are relative to SI base units

UNIT_DEFINITIONS: dict[str, UnitDefinition] = {
    # Length (base: meter)
    "m": UnitDefinition("m", "meter", UnitCategory.LENGTH, 1.0),
    "mm": UnitDefinition("mm", "millimeter", UnitCategory.LENGTH, 1e-3),
    "cm": UnitDefinition("cm", "centimeter", UnitCategory.LENGTH, 1e-2),
    "km": UnitDefinition("km", "kilometer", UnitCategory.LENGTH, 1e3),
    "in": UnitDefinition("in", "inch", UnitCategory.LENGTH, 0.0254),
    "ft": UnitDefinition("ft", "foot", UnitCategory.LENGTH, 0.3048),
    "yd": UnitDefinition("yd", "yard", UnitCategory.LENGTH, 0.9144),
    "mi": UnitDefinition("mi", "mile", UnitCategory.LENGTH, 1609.344),
    # Area (base: m^2)
    "m2": UnitDefinition("m2", "square meter", UnitCategory.AREA, 1.0),
    "mm2": UnitDefinition("mm2", "square millimeter", UnitCategory.AREA, 1e-6),
    "cm2": UnitDefinition("cm2", "square centimeter", UnitCategory.AREA, 1e-4),
    "in2": UnitDefinition("in2", "square inch", UnitCategory.AREA, 6.4516e-4),
    "ft2": UnitDefinition("ft2", "square foot", UnitCategory.AREA, 0.09290304),
    # Volume (base: m^3)
    "m3": UnitDefinition("m3", "cubic meter", UnitCategory.VOLUME, 1.0),
    "mm3": UnitDefinition("mm3", "cubic millimeter", UnitCategory.VOLUME, 1e-9),
    "cm3": UnitDefinition("cm3", "cubic centimeter", UnitCategory.VOLUME, 1e-6),
    "L": UnitDefinition("L", "liter", UnitCategory.VOLUME, 1e-3),
    "mL": UnitDefinition("mL", "milliliter", UnitCategory.VOLUME, 1e-6),
    "in3": UnitDefinition("in3", "cubic inch", UnitCategory.VOLUME, 1.6387064e-5),
    "ft3": UnitDefinition("ft3", "cubic foot", UnitCategory.VOLUME, 0.028316846592),
    "gal": UnitDefinition("gal", "US gallon", UnitCategory.VOLUME, 3.785411784e-3),
    # Mass (base: kg)
    "kg": UnitDefinition("kg", "kilogram", UnitCategory.MASS, 1.0),
    "g": UnitDefinition("g", "gram", UnitCategory.MASS, 1e-3),
    "mg": UnitDefinition("mg", "milligram", UnitCategory.MASS, 1e-6),
    "t": UnitDefinition("t", "metric ton", UnitCategory.MASS, 1e3),
    "lb": UnitDefinition("lb", "pound", UnitCategory.MASS, 0.45359237),
    "oz": UnitDefinition("oz", "ounce", UnitCategory.MASS, 0.028349523125),
    "slug": UnitDefinition("slug", "slug", UnitCategory.MASS, 14.593903),
    # Force (base: N)
    "N": UnitDefinition("N", "newton", UnitCategory.FORCE, 1.0),
    "kN": UnitDefinition("kN", "kilonewton", UnitCategory.FORCE, 1e3),
    "MN": UnitDefinition("MN", "meganewton", UnitCategory.FORCE, 1e6),
    "mN": UnitDefinition("mN", "millinewton", UnitCategory.FORCE, 1e-3),
    "lbf": UnitDefinition("lbf", "pound-force", UnitCategory.FORCE, 4.4482216152605),
    "kip": UnitDefinition("kip", "kilopound-force", UnitCategory.FORCE, 4448.2216152605),
    "kgf": UnitDefinition("kgf", "kilogram-force", UnitCategory.FORCE, 9.80665),
    # Pressure/Stress (base: Pa)
    "Pa": UnitDefinition("Pa", "pascal", UnitCategory.PRESSURE, 1.0),
    "kPa": UnitDefinition("kPa", "kilopascal", UnitCategory.PRESSURE, 1e3),
    "MPa": UnitDefinition("MPa", "megapascal", UnitCategory.PRESSURE, 1e6),
    "GPa": UnitDefinition("GPa", "gigapascal", UnitCategory.PRESSURE, 1e9),
    "bar": UnitDefinition("bar", "bar", UnitCategory.PRESSURE, 1e5),
    "psi": UnitDefinition("psi", "pound per square inch", UnitCategory.PRESSURE, 6894.757293168),
    "ksi": UnitDefinition("ksi", "kilopound per square inch", UnitCategory.PRESSURE, 6894757.293168),
    "atm": UnitDefinition("atm", "atmosphere", UnitCategory.PRESSURE, 101325.0),
    # Torque (base: N·m)
    "N.m": UnitDefinition("N.m", "newton-meter", UnitCategory.TORQUE, 1.0),
    "N.mm": UnitDefinition("N.mm", "newton-millimeter", UnitCategory.TORQUE, 1e-3),
    "kN.m": UnitDefinition("kN.m", "kilonewton-meter", UnitCategory.TORQUE, 1e3),
    "lbf.ft": UnitDefinition("lbf.ft", "pound-force foot", UnitCategory.TORQUE, 1.3558179483314),
    "lbf.in": UnitDefinition("lbf.in", "pound-force inch", UnitCategory.TORQUE, 0.1129848290276167),
    # Energy (base: J)
    "J": UnitDefinition("J", "joule", UnitCategory.ENERGY, 1.0),
    "kJ": UnitDefinition("kJ", "kilojoule", UnitCategory.ENERGY, 1e3),
    "MJ": UnitDefinition("MJ", "megajoule", UnitCategory.ENERGY, 1e6),
    "cal": UnitDefinition("cal", "calorie", UnitCategory.ENERGY, 4.184),
    "kcal": UnitDefinition("kcal", "kilocalorie", UnitCategory.ENERGY, 4184.0),
    "BTU": UnitDefinition("BTU", "British thermal unit", UnitCategory.ENERGY, 1055.05585262),
    "Wh": UnitDefinition("Wh", "watt-hour", UnitCategory.ENERGY, 3600.0),
    "kWh": UnitDefinition("kWh", "kilowatt-hour", UnitCategory.ENERGY, 3.6e6),
    "ft.lbf": UnitDefinition("ft.lbf", "foot-pound force", UnitCategory.ENERGY, 1.3558179483314),
    # Power (base: W)
    "W": UnitDefinition("W", "watt", UnitCategory.POWER, 1.0),
    "kW": UnitDefinition("kW", "kilowatt", UnitCategory.POWER, 1e3),
    "MW": UnitDefinition("MW", "megawatt", UnitCategory.POWER, 1e6),
    "mW": UnitDefinition("mW", "milliwatt", UnitCategory.POWER, 1e-3),
    "hp": UnitDefinition("hp", "horsepower", UnitCategory.POWER, 745.69987158227),
    "BTU/h": UnitDefinition("BTU/h", "BTU per hour", UnitCategory.POWER, 0.29307107017222),
    # Velocity (base: m/s)
    "m/s": UnitDefinition("m/s", "meter per second", UnitCategory.VELOCITY, 1.0),
    "km/h": UnitDefinition("km/h", "kilometer per hour", UnitCategory.VELOCITY, 1 / 3.6),
    "ft/s": UnitDefinition("ft/s", "foot per second", UnitCategory.VELOCITY, 0.3048),
    "mph": UnitDefinition("mph", "mile per hour", UnitCategory.VELOCITY, 0.44704),
    "knot": UnitDefinition("knot", "knot", UnitCategory.VELOCITY, 0.514444444),
    # Acceleration (base: m/s^2)
    "m/s2": UnitDefinition("m/s2", "meter per second squared", UnitCategory.ACCELERATION, 1.0),
    "ft/s2": UnitDefinition("ft/s2", "foot per second squared", UnitCategory.ACCELERATION, 0.3048),
    "g0": UnitDefinition("g0", "standard gravity", UnitCategory.ACCELERATION, 9.80665),
    # Angular velocity (base: rad/s)
    "rad/s": UnitDefinition("rad/s", "radian per second", UnitCategory.ANGULAR_VELOCITY, 1.0),
    "deg/s": UnitDefinition("deg/s", "degree per second", UnitCategory.ANGULAR_VELOCITY, 0.017453292519943),
    "rpm": UnitDefinition("rpm", "revolutions per minute", UnitCategory.ANGULAR_VELOCITY, 0.10471975511966),
    "Hz": UnitDefinition("Hz", "hertz", UnitCategory.ANGULAR_VELOCITY, 6.283185307179586),
    # Density (base: kg/m^3)
    "kg/m3": UnitDefinition("kg/m3", "kilogram per cubic meter", UnitCategory.DENSITY, 1.0),
    "g/cm3": UnitDefinition("g/cm3", "gram per cubic centimeter", UnitCategory.DENSITY, 1e3),
    "lb/ft3": UnitDefinition("lb/ft3", "pound per cubic foot", UnitCategory.DENSITY, 16.01846337396),
    "lb/in3": UnitDefinition("lb/in3", "pound per cubic inch", UnitCategory.DENSITY, 27679.904710191),
    # Time (base: s)
    "s": UnitDefinition("s", "second", UnitCategory.TIME, 1.0),
    "ms": UnitDefinition("ms", "millisecond", UnitCategory.TIME, 1e-3),
    "us": UnitDefinition("us", "microsecond", UnitCategory.TIME, 1e-6),
    "min": UnitDefinition("min", "minute", UnitCategory.TIME, 60.0),
    "h": UnitDefinition("h", "hour", UnitCategory.TIME, 3600.0),
    # Angle (base: rad)
    "rad": UnitDefinition("rad", "radian", UnitCategory.ANGLE, 1.0),
    "deg": UnitDefinition("deg", "degree", UnitCategory.ANGLE, 0.017453292519943),
    "rev": UnitDefinition("rev", "revolution", UnitCategory.ANGLE, 6.283185307179586),
    # Second moment of area (base: m^4)
    "m4": UnitDefinition("m4", "meter to the fourth", UnitCategory.MOMENT_OF_INERTIA, 1.0),
    "mm4": UnitDefinition("mm4", "millimeter to the fourth", UnitCategory.MOMENT_OF_INERTIA, 1e-12),
    "cm4": UnitDefinition("cm4", "centimeter to the fourth", UnitCategory.MOMENT_OF_INERTIA, 1e-8),
    "in4": UnitDefinition("in4", "inch to the fourth", UnitCategory.MOMENT_OF_INERTIA, 4.162314256e-7),
}


def get_units_by_category(category: UnitCategory) -> list[UnitDefinition]:
    """
    Get all unit definitions for a given category.

    Args:
        category: The unit category to filter by

    Returns:
        List of UnitDefinition objects in that category
    """
    return [unit for unit in UNIT_DEFINITIONS.values() if unit.category == category]


def get_unit(symbol: str) -> UnitDefinition | None:
    """
    Get a unit definition by its symbol.

    Args:
        symbol: The unit symbol (e.g., "m", "Pa", "psi")

    Returns:
        UnitDefinition if found, None otherwise
    """
    return UNIT_DEFINITIONS.get(symbol)
