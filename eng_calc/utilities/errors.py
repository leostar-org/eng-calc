"""
Custom Exceptions Module

Defines custom exception classes for the eng_calc package.
These exceptions provide specific error types for different
failure scenarios in the application.
"""


class EngCalcError(Exception):
    """
    Base exception class for all eng_calc errors.

    All custom exceptions in this package inherit from this class,
    allowing for broad exception catching when needed.
    """

    def __init__(self, message: str = "An error occurred in eng_calc") -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error description
        """
        self.message = message
        super().__init__(self.message)


class ValidationError(EngCalcError):
    """
    Raised when input validation fails.

    This exception is raised when input values do not meet
    the required constraints (type, range, physical validity, etc.).

    Attributes:
        field_name: Name of the field that failed validation
        value: The invalid value that was provided
        constraint: Description of the constraint that was violated
    """

    def __init__(
        self,
        message: str,
        field_name: str | None = None,
        value: float | str | None = None,
        constraint: str | None = None,
    ) -> None:
        """
        Initialize the validation error.

        Args:
            message: Human-readable error description
            field_name: Name of the field that failed validation
            value: The invalid value
            constraint: Description of the constraint violated
        """
        self.field_name = field_name
        self.value = value
        self.constraint = constraint
        super().__init__(message)

    def __str__(self) -> str:
        """Return a detailed error message."""
        parts = [self.message]
        if self.field_name:
            parts.append(f"Field: {self.field_name}")
        if self.value is not None:
            parts.append(f"Value: {self.value}")
        if self.constraint:
            parts.append(f"Constraint: {self.constraint}")
        return " | ".join(parts)


class UnitConversionError(EngCalcError):
    """
    Raised when unit conversion fails.

    This exception is raised when attempting to convert between
    incompatible units or when a unit is not recognized.

    Attributes:
        from_unit: The source unit
        to_unit: The target unit
    """

    def __init__(
        self,
        message: str,
        from_unit: str | None = None,
        to_unit: str | None = None,
    ) -> None:
        """
        Initialize the unit conversion error.

        Args:
            message: Human-readable error description
            from_unit: The source unit
            to_unit: The target unit
        """
        self.from_unit = from_unit
        self.to_unit = to_unit
        super().__init__(message)

    def __str__(self) -> str:
        """Return a detailed error message."""
        if self.from_unit and self.to_unit:
            return f"{self.message} (from '{self.from_unit}' to '{self.to_unit}')"
        return self.message


class CalculationError(EngCalcError):
    """
    Raised when a calculation fails.

    This exception is raised when a calculation cannot be completed
    due to mathematical errors (division by zero, overflow, etc.)
    or invalid intermediate results.

    Attributes:
        calculation_name: Name of the calculation that failed
        inputs: Dictionary of input values that caused the failure
    """

    def __init__(
        self,
        message: str,
        calculation_name: str | None = None,
        inputs: dict | None = None,
    ) -> None:
        """
        Initialize the calculation error.

        Args:
            message: Human-readable error description
            calculation_name: Name of the failed calculation
            inputs: Input values that caused the failure
        """
        self.calculation_name = calculation_name
        self.inputs = inputs or {}
        super().__init__(message)

    def __str__(self) -> str:
        """Return a detailed error message."""
        parts = [self.message]
        if self.calculation_name:
            parts.append(f"Calculation: {self.calculation_name}")
        if self.inputs:
            inputs_str = ", ".join(f"{k}={v}" for k, v in self.inputs.items())
            parts.append(f"Inputs: {inputs_str}")
        return " | ".join(parts)


class MaterialNotFoundError(EngCalcError):
    """
    Raised when a requested material is not found in the database.

    Attributes:
        material_name: Name of the material that was not found
    """

    def __init__(self, material_name: str) -> None:
        """
        Initialize the material not found error.

        Args:
            material_name: Name of the material that was not found
        """
        self.material_name = material_name
        message = f"Material '{material_name}' not found in database"
        super().__init__(message)
