"""
Input Validation Module

Provides validation utilities for engineering calculation inputs.
Ensures data integrity and provides meaningful feedback for invalid inputs.
"""

from typing import Any

from eng_calc.utilities.errors import ValidationError
from eng_calc.utilities.units import UNIT_DEFINITIONS, UnitCategory


class Validator:
    """
    Utility class for validating engineering calculation inputs.

    Provides methods for validating numbers, ranges, units, and
    physical constraints. All validation methods raise ValidationError
    on failure or return True on success.
    """

    @staticmethod
    def validate_number(
        value: Any,
        field_name: str = "value",
    ) -> bool:
        """
        Validate that a value is a valid number.

        Args:
            value: The value to validate
            field_name: Name of the field for error messages

        Returns:
            True if valid

        Raises:
            ValidationError: If value is not a valid number
        """
        if value is None:
            raise ValidationError(
                f"{field_name} is required",
                field_name=field_name,
                value=value,
                constraint="must be a number",
            )

        try:
            float(value)
        except (TypeError, ValueError) as e:
            raise ValidationError(
                f"{field_name} must be a valid number",
                field_name=field_name,
                value=value,
                constraint="must be numeric",
            ) from e

        return True

    @staticmethod
    def validate_positive(
        value: float,
        field_name: str = "value",
        allow_zero: bool = False,
    ) -> bool:
        """
        Validate that a value is positive.

        Args:
            value: The value to validate
            field_name: Name of the field for error messages
            allow_zero: If True, zero is considered valid

        Returns:
            True if valid

        Raises:
            ValidationError: If value is not positive
        """
        Validator.validate_number(value, field_name)

        if allow_zero:
            if value < 0:
                raise ValidationError(
                    f"{field_name} must be non-negative",
                    field_name=field_name,
                    value=value,
                    constraint=">= 0",
                )
        else:
            if value <= 0:
                raise ValidationError(
                    f"{field_name} must be positive",
                    field_name=field_name,
                    value=value,
                    constraint="> 0",
                )

        return True

    @staticmethod
    def validate_non_zero(
        value: float,
        field_name: str = "value",
    ) -> bool:
        """
        Validate that a value is not zero.

        Args:
            value: The value to validate
            field_name: Name of the field for error messages

        Returns:
            True if valid

        Raises:
            ValidationError: If value is zero
        """
        Validator.validate_number(value, field_name)

        if value == 0:
            raise ValidationError(
                f"{field_name} cannot be zero",
                field_name=field_name,
                value=value,
                constraint="!= 0",
            )

        return True

    @staticmethod
    def validate_range(
        value: float,
        field_name: str = "value",
        min_value: float | None = None,
        max_value: float | None = None,
        inclusive_min: bool = True,
        inclusive_max: bool = True,
    ) -> bool:
        """
        Validate that a value is within a specified range.

        Args:
            value: The value to validate
            field_name: Name of the field for error messages
            min_value: Minimum allowed value (None for no minimum)
            max_value: Maximum allowed value (None for no maximum)
            inclusive_min: If True, min_value is included in valid range
            inclusive_max: If True, max_value is included in valid range

        Returns:
            True if valid

        Raises:
            ValidationError: If value is outside the range
        """
        Validator.validate_number(value, field_name)

        if min_value is not None:
            if inclusive_min:
                if value < min_value:
                    raise ValidationError(
                        f"{field_name} must be >= {min_value}",
                        field_name=field_name,
                        value=value,
                        constraint=f">= {min_value}",
                    )
            else:
                if value <= min_value:
                    raise ValidationError(
                        f"{field_name} must be > {min_value}",
                        field_name=field_name,
                        value=value,
                        constraint=f"> {min_value}",
                    )

        if max_value is not None:
            if inclusive_max:
                if value > max_value:
                    raise ValidationError(
                        f"{field_name} must be <= {max_value}",
                        field_name=field_name,
                        value=value,
                        constraint=f"<= {max_value}",
                    )
            else:
                if value >= max_value:
                    raise ValidationError(
                        f"{field_name} must be < {max_value}",
                        field_name=field_name,
                        value=value,
                        constraint=f"< {max_value}",
                    )

        return True

    @staticmethod
    def validate_unit(
        unit: str,
        expected_category: UnitCategory | None = None,
        field_name: str = "unit",
    ) -> bool:
        """
        Validate that a unit string is recognized.

        Args:
            unit: The unit symbol to validate
            expected_category: If provided, also check the unit belongs to this category
            field_name: Name of the field for error messages

        Returns:
            True if valid

        Raises:
            ValidationError: If unit is not recognized or wrong category
        """
        if unit not in UNIT_DEFINITIONS:
            raise ValidationError(
                f"Unknown unit: {unit}",
                field_name=field_name,
                value=unit,
                constraint="must be a recognized unit symbol",
            )

        if expected_category is not None:
            unit_def = UNIT_DEFINITIONS[unit]
            if unit_def.category != expected_category:
                raise ValidationError(
                    f"Unit '{unit}' is not a {expected_category.name.lower()} unit",
                    field_name=field_name,
                    value=unit,
                    constraint=f"must be a {expected_category.name.lower()} unit",
                )

        return True

    @staticmethod
    def validate_required_inputs(
        inputs: dict[str, Any],
        required: list[str],
    ) -> bool:
        """
        Validate that all required inputs are present and non-None.

        Args:
            inputs: Dictionary of input values
            required: List of required input names

        Returns:
            True if all required inputs are present

        Raises:
            ValidationError: If any required input is missing
        """
        missing = [name for name in required if inputs.get(name) is None]

        if missing:
            raise ValidationError(
                f"Missing required inputs: {', '.join(missing)}",
                field_name=missing[0],
                constraint="required",
            )

        return True

    @staticmethod
    def validate_finite(
        value: float,
        field_name: str = "value",
    ) -> bool:
        """
        Validate that a value is finite (not NaN or infinite).

        Args:
            value: The value to validate
            field_name: Name of the field for error messages

        Returns:
            True if valid

        Raises:
            ValidationError: If value is NaN or infinite
        """
        import math

        Validator.validate_number(value, field_name)

        if math.isnan(value):
            raise ValidationError(
                f"{field_name} is NaN (not a number)",
                field_name=field_name,
                value=value,
                constraint="must be finite",
            )

        if math.isinf(value):
            raise ValidationError(
                f"{field_name} is infinite",
                field_name=field_name,
                value=value,
                constraint="must be finite",
            )

        return True
