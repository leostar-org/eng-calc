"""
Unit Converter Module

Provides the UnitConverter class for converting between different units
within the same physical category.
"""

from typing import Union

from eng_calc.utilities.errors import UnitConversionError
from eng_calc.utilities.units import (
    UNIT_DEFINITIONS,
    UnitCategory,
    UnitDefinition,
    get_unit,
    get_units_by_category,
)


class UnitConverter:
    """
    A utility class for converting values between different units.

    The UnitConverter uses the UNIT_DEFINITIONS from the units module
    to perform conversions between units in the same category.

    Example:
        >>> converter = UnitConverter()
        >>> converter.convert(1, "m", "ft")
        3.280839895013123
        >>> converter.convert(100, "psi", "MPa")
        0.6894757293168
    """

    def __init__(self) -> None:
        """Initialize the UnitConverter."""
        pass

    def convert(
        self,
        value: Union[int, float],
        from_unit: str,
        to_unit: str,
    ) -> float:
        """
        Convert a value from one unit to another.

        The conversion is performed by first converting the value to the
        SI base unit, then converting from SI to the target unit.

        Args:
            value: The numerical value to convert
            from_unit: The source unit symbol (e.g., "m", "ft", "psi")
            to_unit: The target unit symbol (e.g., "mm", "in", "MPa")

        Returns:
            The converted value in the target unit

        Raises:
            UnitConversionError: If either unit is not recognized or if
                the units are not in the same category
        """
        # Validate the value is numeric
        if not isinstance(value, (int, float)):
            raise UnitConversionError(
                f"Value must be a number, got {type(value).__name__}",
                from_unit=from_unit,
                to_unit=to_unit,
            )

        # Get unit definitions
        from_unit_def = self._get_unit_or_raise(from_unit)
        to_unit_def = self._get_unit_or_raise(to_unit)

        # Verify units are in the same category
        self._verify_same_category(from_unit_def, to_unit_def)

        # Convert: from_unit -> SI -> to_unit
        si_value = from_unit_def.to_si(value)
        result = to_unit_def.from_si(si_value)

        return result

    def get_conversion_factor(
        self,
        from_unit: str,
        to_unit: str,
    ) -> float:
        """
        Get the conversion factor between two units.

        This returns the factor by which you would multiply a value in
        from_unit to get the equivalent value in to_unit. This is only
        accurate for units without offset (not temperature).

        Args:
            from_unit: The source unit symbol
            to_unit: The target unit symbol

        Returns:
            The conversion factor (multiply from_unit value by this to get to_unit)

        Raises:
            UnitConversionError: If either unit is not recognized or if
                the units are not in the same category
        """
        from_unit_def = self._get_unit_or_raise(from_unit)
        to_unit_def = self._get_unit_or_raise(to_unit)

        self._verify_same_category(from_unit_def, to_unit_def)

        # Factor = from_unit's SI factor / to_unit's SI factor
        # This works because: value_in_to = value_in_from * factor
        # And: value_in_SI = value_in_from * from_factor
        #      value_in_to = value_in_SI / to_factor
        # So: value_in_to = value_in_from * (from_factor / to_factor)
        return from_unit_def.to_si_factor / to_unit_def.to_si_factor

    def list_units(
        self,
        category: Union[UnitCategory, str, None] = None,
    ) -> list[UnitDefinition]:
        """
        List all available units, optionally filtered by category.

        Args:
            category: Optional category to filter by. Can be a UnitCategory
                enum value or a string matching the category name (case-insensitive).
                If None, returns all units.

        Returns:
            List of UnitDefinition objects matching the filter

        Raises:
            UnitConversionError: If the category string is not recognized
        """
        if category is None:
            return list(UNIT_DEFINITIONS.values())

        # Handle string category names
        if isinstance(category, str):
            category = self._parse_category(category)

        return get_units_by_category(category)

    def get_unit_info(self, symbol: str) -> UnitDefinition:
        """
        Get detailed information about a unit.

        Args:
            symbol: The unit symbol to look up

        Returns:
            The UnitDefinition for the specified unit

        Raises:
            UnitConversionError: If the unit is not recognized
        """
        return self._get_unit_or_raise(symbol)

    def get_categories(self) -> list[UnitCategory]:
        """
        Get a list of all available unit categories.

        Returns:
            List of all UnitCategory enum values
        """
        return list(UnitCategory)

    def is_valid_unit(self, symbol: str) -> bool:
        """
        Check if a unit symbol is valid.

        Args:
            symbol: The unit symbol to check

        Returns:
            True if the unit exists, False otherwise
        """
        return get_unit(symbol) is not None

    def are_compatible(self, unit1: str, unit2: str) -> bool:
        """
        Check if two units are compatible (same category).

        Args:
            unit1: First unit symbol
            unit2: Second unit symbol

        Returns:
            True if the units are in the same category, False otherwise

        Raises:
            UnitConversionError: If either unit is not recognized
        """
        unit1_def = self._get_unit_or_raise(unit1)
        unit2_def = self._get_unit_or_raise(unit2)
        return unit1_def.category == unit2_def.category

    def _get_unit_or_raise(self, symbol: str) -> UnitDefinition:
        """
        Get a unit definition or raise an error if not found.

        Args:
            symbol: The unit symbol to look up

        Returns:
            The UnitDefinition for the specified unit

        Raises:
            UnitConversionError: If the unit is not recognized
        """
        unit_def = get_unit(symbol)
        if unit_def is None:
            raise UnitConversionError(
                f"Unknown unit: '{symbol}'",
                from_unit=symbol,
                to_unit=None,
            )
        return unit_def

    def _verify_same_category(
        self,
        from_unit: UnitDefinition,
        to_unit: UnitDefinition,
    ) -> None:
        """
        Verify that two units are in the same category.

        Args:
            from_unit: The source unit definition
            to_unit: The target unit definition

        Raises:
            UnitConversionError: If the units are in different categories
        """
        if from_unit.category != to_unit.category:
            raise UnitConversionError(
                f"Cannot convert between different categories: "
                f"{from_unit.category.name} and {to_unit.category.name}",
                from_unit=from_unit.symbol,
                to_unit=to_unit.symbol,
            )

    def _parse_category(self, category_name: str) -> UnitCategory:
        """
        Parse a category name string to a UnitCategory enum.

        Args:
            category_name: The category name (case-insensitive)

        Returns:
            The corresponding UnitCategory enum value

        Raises:
            UnitConversionError: If the category name is not recognized
        """
        try:
            return UnitCategory[category_name.upper()]
        except KeyError:
            valid_categories = [cat.name for cat in UnitCategory]
            raise UnitConversionError(
                f"Unknown category: '{category_name}'. "
                f"Valid categories: {', '.join(valid_categories)}"
            )
