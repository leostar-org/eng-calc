"""
Physical Constants Module

Defines commonly used physical constants for engineering calculations.
All constants are provided in SI units unless otherwise noted.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PhysicalConstants:
    """
    Physical constants used in engineering calculations.

    All values are in SI units:
    - Length: meters (m)
    - Mass: kilograms (kg)
    - Time: seconds (s)
    - Force: Newtons (N)
    - Pressure: Pascals (Pa)
    - Temperature: Kelvin (K)
    """

    # Gravitational acceleration (m/s^2)
    GRAVITY_STANDARD: float = 9.80665

    # Speed of light in vacuum (m/s)
    SPEED_OF_LIGHT: float = 299792458.0

    # Planck constant (J·s)
    PLANCK_CONSTANT: float = 6.62607015e-34

    # Boltzmann constant (J/K)
    BOLTZMANN_CONSTANT: float = 1.380649e-23

    # Avogadro constant (1/mol)
    AVOGADRO_CONSTANT: float = 6.02214076e23

    # Universal gas constant (J/(mol·K))
    GAS_CONSTANT: float = 8.314462618

    # Stefan-Boltzmann constant (W/(m^2·K^4))
    STEFAN_BOLTZMANN: float = 5.670374419e-8

    # Standard atmospheric pressure (Pa)
    ATMOSPHERIC_PRESSURE: float = 101325.0

    # Absolute zero in Celsius
    ABSOLUTE_ZERO_CELSIUS: float = -273.15

    # Water properties at standard conditions
    WATER_DENSITY_20C: float = 998.2  # kg/m^3 at 20°C
    WATER_SPECIFIC_HEAT: float = 4186.0  # J/(kg·K)

    # Air properties at standard conditions
    AIR_DENSITY_SEA_LEVEL: float = 1.225  # kg/m^3 at 15°C, 101.325 kPa
    AIR_SPECIFIC_HEAT_CP: float = 1005.0  # J/(kg·K) at constant pressure

    # Mathematical constants
    PI: float = 3.141592653589793
    E: float = 2.718281828459045

    @classmethod
    def gravity_at_latitude(cls, latitude_degrees: float) -> float:
        """
        Calculate gravitational acceleration at a given latitude.

        Uses the International Gravity Formula (1980).

        Args:
            latitude_degrees: Latitude in degrees

        Returns:
            Gravitational acceleration in m/s^2
        """
        import math

        lat_rad = math.radians(latitude_degrees)
        sin_lat = math.sin(lat_rad)
        sin_2lat = math.sin(2 * lat_rad)

        # International Gravity Formula 1980
        g = 9.780327 * (1 + 0.0053024 * sin_lat**2 - 0.0000058 * sin_2lat**2)
        return g

    @classmethod
    def celsius_to_kelvin(cls, celsius: float) -> float:
        """
        Convert temperature from Celsius to Kelvin.

        Args:
            celsius: Temperature in degrees Celsius

        Returns:
            Temperature in Kelvin
        """
        return celsius - cls.ABSOLUTE_ZERO_CELSIUS

    @classmethod
    def kelvin_to_celsius(cls, kelvin: float) -> float:
        """
        Convert temperature from Kelvin to Celsius.

        Args:
            kelvin: Temperature in Kelvin

        Returns:
            Temperature in degrees Celsius
        """
        return kelvin + cls.ABSOLUTE_ZERO_CELSIUS


# Convenience access to constants
GRAVITY = PhysicalConstants.GRAVITY_STANDARD
PI = PhysicalConstants.PI
