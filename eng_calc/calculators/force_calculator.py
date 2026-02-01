"""
Force & Equilibrium Calculator Module

Provides calculations for force analysis and static equilibrium.
Implements the BaseCalculator interface with methods for:
- Resultant force (2D vector addition)
- Force components (resolve into x/y)
- Moment calculation (M = F × d)
- Equilibrium check (ΣF=0, ΣM=0)
"""

import math
from typing import Any

from eng_calc.calculators.base_calculator import BaseCalculator, CalculationResult
from eng_calc.utilities import (
    CalculationError,
    UnitCategory,
    UnitConverter,
    ValidationError,
    Validator,
)


class ForceCalculator(BaseCalculator):
    """
    Calculator for force analysis and static equilibrium.

    Provides methods for calculating resultant forces, force components,
    moments, and checking equilibrium conditions. Supports unit conversion
    for both inputs and outputs.

    Available calculations:
        - resultant_force: Calculate resultant of multiple 2D force vectors
        - force_components: Resolve a force into x/y components
        - moment: Calculate moment about a point (M = F × d)
        - equilibrium: Check static equilibrium (ΣF=0, ΣM=0)

    Example:
        >>> calc = ForceCalculator()
        >>> result = calc.calculate_resultant_force(
        ...     forces=[(100, 0), (0, 100)],  # Two perpendicular forces
        ...     force_unit="N"
        ... )
        >>> print(result)
        resultant_force: 141.421 N
    """

    # Default SI units for each input type
    DEFAULT_INPUT_UNITS = {
        "force": "N",
        "force_x": "N",
        "force_y": "N",
        "distance": "m",
        "moment_arm": "m",
        "angle": "deg",
    }

    # Formulas for each calculation
    FORMULAS = {
        "resultant_force": "R = √(ΣFx² + ΣFy²), θ = atan2(ΣFy, ΣFx)",
        "force_components": "Fx = F·cos(θ), Fy = F·sin(θ)",
        "moment": "M = F × d = F·d·sin(θ)",
        "equilibrium": "ΣFx = 0, ΣFy = 0, ΣM = 0",
    }

    def __init__(self) -> None:
        """Initialize the ForceCalculator."""
        super().__init__()
        self._converter = UnitConverter()
        # Storage for force vectors (list of (fx, fy) tuples)
        self._force_vectors: list[tuple[float, float]] = []
        # Storage for moments (list of moment values)
        self._moments: list[float] = []

    @property
    def name(self) -> str:
        """Return the display name of the calculator."""
        return "Force & Equilibrium Calculator"

    @property
    def description(self) -> str:
        """Return a brief description of the calculator's purpose."""
        return (
            "Calculate resultant forces, force components, moments, "
            "and check static equilibrium conditions."
        )

    @property
    def required_inputs(self) -> list[str]:
        """
        Return a list of required input parameter names.

        Note: Required inputs vary by calculation. This returns the
        base required inputs. Use get_required_inputs_for() for
        calculation-specific requirements.
        """
        return []  # Varies by calculation

    @property
    def available_calculations(self) -> list[str]:
        """Return a list of available calculation methods."""
        return ["resultant_force", "force_components", "moment", "equilibrium"]

    def get_required_inputs_for(self, calculation_name: str) -> list[str]:
        """
        Get the required inputs for a specific calculation.

        Args:
            calculation_name: Name of the calculation

        Returns:
            List of required input parameter names
        """
        requirements = {
            "resultant_force": ["forces"],  # List of force vectors
            "force_components": ["force", "angle"],
            "moment": ["force", "moment_arm"],
            "equilibrium": ["forces", "moments"],  # Lists of forces and moments
        }
        return requirements.get(calculation_name, [])

    def set_force_vectors(
        self, forces: list[tuple[float, float]], unit: str = "N"
    ) -> None:
        """
        Set the force vectors for resultant or equilibrium calculations.

        Args:
            forces: List of (fx, fy) tuples representing force components
            unit: Unit of force values (default: N)
        """
        self._force_vectors = forces
        self._input_units["forces"] = unit
        self._inputs["forces"] = forces

    def set_moments(self, moments: list[float], unit: str = "N.m") -> None:
        """
        Set the moments for equilibrium calculation.

        Args:
            moments: List of moment values (positive = counterclockwise)
            unit: Unit of moment values (default: N.m)
        """
        self._moments = moments
        self._input_units["moments"] = unit
        self._inputs["moments"] = moments

    def clear_inputs(self) -> None:
        """Clear all input values including force vectors and moments."""
        super().clear_inputs()
        self._force_vectors = []
        self._moments = []

    def validate_inputs(self) -> tuple[bool, str]:
        """
        Validate the current input values.

        This performs basic validation on all set inputs.
        For calculation-specific validation, use validate_for().

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Validate all numeric inputs are finite and valid
            for name, value in self._inputs.items():
                if value is not None and not isinstance(value, (list, tuple)):
                    Validator.validate_number(value, name)
                    Validator.validate_finite(value, name)
            return True, ""
        except ValidationError as e:
            return False, str(e)

    def validate_for(self, calculation_name: str) -> tuple[bool, str]:
        """
        Validate inputs for a specific calculation.

        Args:
            calculation_name: Name of the calculation to validate for

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if calculation_name == "resultant_force":
                self._validate_resultant_force_inputs()
            elif calculation_name == "force_components":
                self._validate_force_components_inputs()
            elif calculation_name == "moment":
                self._validate_moment_inputs()
            elif calculation_name == "equilibrium":
                self._validate_equilibrium_inputs()
            else:
                raise CalculationError(
                    f"Unknown calculation: {calculation_name}",
                    calculation_name=calculation_name,
                )

            return True, ""
        except (ValidationError, CalculationError) as e:
            return False, str(e)

    def _validate_resultant_force_inputs(self) -> None:
        """Validate inputs for resultant force calculation."""
        forces = self._inputs.get("forces")

        if forces is None or len(forces) == 0:
            raise ValidationError(
                "At least one force vector is required",
                field_name="forces",
                constraint="must provide at least one force",
            )

        for i, force in enumerate(forces):
            if not isinstance(force, (list, tuple)) or len(force) != 2:
                raise ValidationError(
                    f"Force at index {i} must be a (fx, fy) tuple",
                    field_name=f"forces[{i}]",
                    value=force,
                    constraint="must be (fx, fy) tuple",
                )
            fx, fy = force
            Validator.validate_number(fx, f"forces[{i}].fx")
            Validator.validate_number(fy, f"forces[{i}].fy")
            Validator.validate_finite(fx, f"forces[{i}].fx")
            Validator.validate_finite(fy, f"forces[{i}].fy")

        # Validate unit if provided
        if "forces" in self._input_units:
            Validator.validate_unit(
                self._input_units["forces"], UnitCategory.FORCE, "forces unit"
            )

    def _validate_force_components_inputs(self) -> None:
        """Validate inputs for force components calculation."""
        force = self._inputs.get("force")
        angle = self._inputs.get("angle")

        Validator.validate_number(force, "force")
        Validator.validate_number(angle, "angle")
        Validator.validate_finite(force, "force")
        Validator.validate_finite(angle, "angle")

        # Force magnitude must be non-negative
        Validator.validate_positive(force, "force", allow_zero=True)

        # Validate units if provided
        if "force" in self._input_units:
            Validator.validate_unit(
                self._input_units["force"], UnitCategory.FORCE, "force unit"
            )
        if "angle" in self._input_units:
            Validator.validate_unit(
                self._input_units["angle"], UnitCategory.ANGLE, "angle unit"
            )

    def _validate_moment_inputs(self) -> None:
        """Validate inputs for moment calculation."""
        force = self._inputs.get("force")
        moment_arm = self._inputs.get("moment_arm")

        Validator.validate_number(force, "force")
        Validator.validate_number(moment_arm, "moment_arm")
        Validator.validate_finite(force, "force")
        Validator.validate_finite(moment_arm, "moment_arm")

        # Moment arm must be non-negative
        Validator.validate_positive(moment_arm, "moment_arm", allow_zero=True)

        # Check for optional angle input
        angle = self._inputs.get("angle")
        if angle is not None:
            Validator.validate_number(angle, "angle")
            Validator.validate_finite(angle, "angle")
            if "angle" in self._input_units:
                Validator.validate_unit(
                    self._input_units["angle"], UnitCategory.ANGLE, "angle unit"
                )

        # Validate units if provided
        if "force" in self._input_units:
            Validator.validate_unit(
                self._input_units["force"], UnitCategory.FORCE, "force unit"
            )
        if "moment_arm" in self._input_units:
            Validator.validate_unit(
                self._input_units["moment_arm"], UnitCategory.LENGTH, "moment_arm unit"
            )

    def _validate_equilibrium_inputs(self) -> None:
        """Validate inputs for equilibrium check."""
        forces = self._inputs.get("forces")

        if forces is None or len(forces) == 0:
            raise ValidationError(
                "At least one force vector is required for equilibrium check",
                field_name="forces",
                constraint="must provide at least one force",
            )

        # Validate each force vector
        for i, force in enumerate(forces):
            if not isinstance(force, (list, tuple)) or len(force) != 2:
                raise ValidationError(
                    f"Force at index {i} must be a (fx, fy) tuple",
                    field_name=f"forces[{i}]",
                    value=force,
                    constraint="must be (fx, fy) tuple",
                )
            fx, fy = force
            Validator.validate_number(fx, f"forces[{i}].fx")
            Validator.validate_number(fy, f"forces[{i}].fy")
            Validator.validate_finite(fx, f"forces[{i}].fx")
            Validator.validate_finite(fy, f"forces[{i}].fy")

        # Validate moments if provided
        moments = self._inputs.get("moments")
        if moments is not None:
            for i, moment in enumerate(moments):
                Validator.validate_number(moment, f"moments[{i}]")
                Validator.validate_finite(moment, f"moments[{i}]")

        # Validate units if provided
        if "forces" in self._input_units:
            Validator.validate_unit(
                self._input_units["forces"], UnitCategory.FORCE, "forces unit"
            )
        if "moments" in self._input_units:
            Validator.validate_unit(
                self._input_units["moments"], UnitCategory.TORQUE, "moments unit"
            )

    def _convert_to_si(self, value: float, input_name: str) -> float:
        """
        Convert an input value to SI units.

        Args:
            value: The input value
            input_name: Name of the input (to look up its unit)

        Returns:
            Value converted to SI units
        """
        if input_name not in self._input_units:
            return value  # Assume already in SI

        input_unit = self._input_units[input_name]
        default_unit = self.DEFAULT_INPUT_UNITS.get(input_name)

        if default_unit is None or input_unit == default_unit:
            return value

        return self._converter.convert(value, input_unit, default_unit)

    def _convert_angle_to_radians(self, angle: float, input_name: str = "angle") -> float:
        """
        Convert an angle to radians.

        Args:
            angle: The angle value
            input_name: Name of the angle input

        Returns:
            Angle in radians
        """
        if input_name not in self._input_units:
            # Default is degrees
            return math.radians(angle)

        input_unit = self._input_units[input_name]
        if input_unit == "rad":
            return angle
        elif input_unit == "deg":
            return math.radians(angle)
        elif input_unit == "rev":
            return angle * 2 * math.pi
        else:
            # Use converter for other angle units
            return self._converter.convert(angle, input_unit, "rad")

    def _convert_from_si(
        self, value: float, output_name: str, si_unit: str
    ) -> tuple[float, str]:
        """
        Convert an output value from SI to the desired output unit.

        Args:
            value: The value in SI units
            output_name: Name of the output (to look up desired unit)
            si_unit: The SI unit of the value

        Returns:
            Tuple of (converted_value, unit_string)
        """
        if output_name not in self._output_units:
            return value, si_unit

        target_unit = self._output_units[output_name]
        converted = self._converter.convert(value, si_unit, target_unit)
        return converted, target_unit

    def calculate(self, calculation_name: str) -> CalculationResult:
        """
        Perform a specific calculation.

        Args:
            calculation_name: Name of the calculation to perform

        Returns:
            CalculationResult containing the computed value and metadata

        Raises:
            ValidationError: If inputs are invalid
            CalculationError: If the calculation fails
            ValueError: If calculation_name is not recognized
        """
        if calculation_name not in self.available_calculations:
            raise ValueError(
                f"Unknown calculation: '{calculation_name}'. "
                f"Available: {self.available_calculations}"
            )

        # Validate inputs for this calculation
        valid, error = self.validate_for(calculation_name)
        if not valid:
            raise ValidationError(error)

        # Dispatch to specific calculation method
        if calculation_name == "resultant_force":
            return self._calculate_resultant_force()
        elif calculation_name == "force_components":
            return self._calculate_force_components()
        elif calculation_name == "moment":
            return self._calculate_moment()
        elif calculation_name == "equilibrium":
            return self._calculate_equilibrium()
        else:
            raise CalculationError(
                f"Calculation '{calculation_name}' not implemented",
                calculation_name=calculation_name,
            )

    def _calculate_resultant_force(self) -> CalculationResult:
        """
        Calculate resultant force from multiple 2D force vectors.

        R = √(ΣFx² + ΣFy²)
        θ = atan2(ΣFy, ΣFx)

        Returns:
            CalculationResult with resultant magnitude and angle
        """
        forces = self._inputs["forces"]
        force_unit = self._input_units.get("forces", "N")

        # Convert forces to SI if needed
        conversion_factor = 1.0
        if force_unit != "N":
            conversion_factor = self._converter.convert(1, force_unit, "N")

        # Sum components
        sum_fx = 0.0
        sum_fy = 0.0
        for fx, fy in forces:
            sum_fx += fx * conversion_factor
            sum_fy += fy * conversion_factor

        # Calculate resultant magnitude
        resultant_magnitude = math.sqrt(sum_fx**2 + sum_fy**2)

        # Calculate resultant angle (in radians, then convert to degrees)
        resultant_angle_rad = math.atan2(sum_fy, sum_fx)
        resultant_angle_deg = math.degrees(resultant_angle_rad)

        # Convert output if needed
        result_value, result_unit = self._convert_from_si(
            resultant_magnitude, "resultant_force", "N"
        )

        return CalculationResult(
            name="resultant_force",
            value=result_value,
            unit=result_unit,
            formula=self.FORMULAS["resultant_force"],
            inputs={
                "forces": forces,
                "forces_unit": force_unit,
                "sum_fx": sum_fx,
                "sum_fy": sum_fy,
                "resultant_angle_deg": resultant_angle_deg,
            },
        )

    def _calculate_force_components(self) -> CalculationResult:
        """
        Resolve a force into x and y components.

        Fx = F·cos(θ)
        Fy = F·sin(θ)

        Returns:
            CalculationResult with force components
        """
        force = self._convert_to_si(self._inputs["force"], "force")
        angle_rad = self._convert_angle_to_radians(self._inputs["angle"], "angle")

        # Calculate components
        fx = force * math.cos(angle_rad)
        fy = force * math.sin(angle_rad)

        # Convert output if needed
        fx_result, result_unit = self._convert_from_si(fx, "force_components", "N")
        fy_result, _ = self._convert_from_si(fy, "force_components", "N")

        return CalculationResult(
            name="force_components",
            value=fx_result,  # Primary value is Fx
            unit=result_unit,
            formula=self.FORMULAS["force_components"],
            inputs={
                "force": self._inputs["force"],
                "force_unit": self._input_units.get("force", "N"),
                "angle": self._inputs["angle"],
                "angle_unit": self._input_units.get("angle", "deg"),
                "fx": fx_result,
                "fy": fy_result,
            },
        )

    def _calculate_moment(self) -> CalculationResult:
        """
        Calculate moment about a point.

        M = F × d = F·d·sin(θ)

        If no angle is provided, assumes perpendicular (θ = 90°).
        Positive moment is counterclockwise.

        Returns:
            CalculationResult with moment value
        """
        force = self._convert_to_si(self._inputs["force"], "force")
        moment_arm = self._convert_to_si(self._inputs["moment_arm"], "moment_arm")

        # Check for optional angle (default: perpendicular = 90°)
        angle = self._inputs.get("angle")
        if angle is not None:
            angle_rad = self._convert_angle_to_radians(angle, "angle")
            sin_factor = math.sin(angle_rad)
        else:
            sin_factor = 1.0  # sin(90°) = 1

        # Calculate moment: M = F × d
        moment = force * moment_arm * sin_factor

        # Convert output if needed
        result_value, result_unit = self._convert_from_si(moment, "moment", "N.m")

        inputs_dict: dict[str, Any] = {
            "force": self._inputs["force"],
            "force_unit": self._input_units.get("force", "N"),
            "moment_arm": self._inputs["moment_arm"],
            "moment_arm_unit": self._input_units.get("moment_arm", "m"),
        }
        if angle is not None:
            inputs_dict["angle"] = angle
            inputs_dict["angle_unit"] = self._input_units.get("angle", "deg")

        return CalculationResult(
            name="moment",
            value=result_value,
            unit=result_unit,
            formula=self.FORMULAS["moment"],
            inputs=inputs_dict,
        )

    def _calculate_equilibrium(self) -> CalculationResult:
        """
        Check static equilibrium conditions.

        ΣFx = 0 (sum of horizontal forces)
        ΣFy = 0 (sum of vertical forces)
        ΣM = 0 (sum of moments)

        Returns:
            CalculationResult with equilibrium status and residuals
        """
        forces = self._inputs["forces"]
        moments = self._inputs.get("moments", [])
        force_unit = self._input_units.get("forces", "N")
        moment_unit = self._input_units.get("moments", "N.m")

        # Convert forces to SI if needed
        force_conversion = 1.0
        if force_unit != "N":
            force_conversion = self._converter.convert(1, force_unit, "N")

        moment_conversion = 1.0
        if moment_unit != "N.m":
            moment_conversion = self._converter.convert(1, moment_unit, "N.m")

        # Sum force components
        sum_fx = 0.0
        sum_fy = 0.0
        for fx, fy in forces:
            sum_fx += fx * force_conversion
            sum_fy += fy * force_conversion

        # Sum moments
        sum_m = 0.0
        for m in moments:
            sum_m += m * moment_conversion

        # Check equilibrium with tolerance
        tolerance = 1e-9
        fx_equilibrium = abs(sum_fx) < tolerance
        fy_equilibrium = abs(sum_fy) < tolerance
        m_equilibrium = abs(sum_m) < tolerance if moments else True

        is_in_equilibrium = fx_equilibrium and fy_equilibrium and m_equilibrium

        return CalculationResult(
            name="equilibrium",
            value=1.0 if is_in_equilibrium else 0.0,
            unit="",  # Boolean result
            formula=self.FORMULAS["equilibrium"],
            inputs={
                "forces": forces,
                "forces_unit": force_unit,
                "moments": moments,
                "moments_unit": moment_unit,
                "sum_fx": sum_fx,
                "sum_fy": sum_fy,
                "sum_m": sum_m,
                "is_in_equilibrium": is_in_equilibrium,
                "fx_equilibrium": fx_equilibrium,
                "fy_equilibrium": fy_equilibrium,
                "m_equilibrium": m_equilibrium,
            },
        )

    def get_formula(self, calculation_name: str) -> str:
        """
        Get the formula string for a specific calculation.

        Args:
            calculation_name: Name of the calculation

        Returns:
            Human-readable formula string

        Raises:
            ValueError: If calculation_name is not recognized
        """
        if calculation_name not in self.FORMULAS:
            raise ValueError(
                f"Unknown calculation: '{calculation_name}'. "
                f"Available: {list(self.FORMULAS.keys())}"
            )
        return self.FORMULAS[calculation_name]

    # Convenience methods for direct calculations

    def calculate_resultant_force(
        self,
        forces: list[tuple[float, float]],
        force_unit: str = "N",
        output_unit: str | None = None,
    ) -> CalculationResult:
        """
        Calculate resultant force directly with parameters.

        Args:
            forces: List of (fx, fy) tuples representing force components
            force_unit: Unit of force values (default: N)
            output_unit: Desired output unit (default: N)

        Returns:
            CalculationResult with resultant force magnitude and angle
        """
        self.clear_inputs()
        self.set_force_vectors(forces, force_unit)
        if output_unit:
            self.set_output_unit("resultant_force", output_unit)
        return self.calculate("resultant_force")

    def calculate_force_components(
        self,
        force: float,
        angle: float,
        force_unit: str = "N",
        angle_unit: str = "deg",
        output_unit: str | None = None,
    ) -> CalculationResult:
        """
        Resolve a force into x and y components directly.

        Args:
            force: Force magnitude
            angle: Angle from positive x-axis
            force_unit: Unit of force (default: N)
            angle_unit: Unit of angle (default: deg)
            output_unit: Desired output unit (default: N)

        Returns:
            CalculationResult with force components (fx in value, fy in inputs)
        """
        self.clear_inputs()
        self.set_input("force", force, force_unit)
        self.set_input("angle", angle, angle_unit)
        if output_unit:
            self.set_output_unit("force_components", output_unit)
        return self.calculate("force_components")

    def calculate_moment(
        self,
        force: float,
        moment_arm: float,
        force_unit: str = "N",
        moment_arm_unit: str = "m",
        angle: float | None = None,
        angle_unit: str = "deg",
        output_unit: str | None = None,
    ) -> CalculationResult:
        """
        Calculate moment directly with parameters.

        Args:
            force: Force magnitude
            moment_arm: Perpendicular distance from force to pivot
            force_unit: Unit of force (default: N)
            moment_arm_unit: Unit of moment arm (default: m)
            angle: Angle between force and moment arm (default: 90°)
            angle_unit: Unit of angle (default: deg)
            output_unit: Desired output unit (default: N.m)

        Returns:
            CalculationResult with moment value
        """
        self.clear_inputs()
        self.set_input("force", force, force_unit)
        self.set_input("moment_arm", moment_arm, moment_arm_unit)
        if angle is not None:
            self.set_input("angle", angle, angle_unit)
        if output_unit:
            self.set_output_unit("moment", output_unit)
        return self.calculate("moment")

    def check_equilibrium(
        self,
        forces: list[tuple[float, float]],
        moments: list[float] | None = None,
        force_unit: str = "N",
        moment_unit: str = "N.m",
    ) -> CalculationResult:
        """
        Check static equilibrium conditions directly.

        Args:
            forces: List of (fx, fy) tuples representing force components
            moments: List of moment values (positive = counterclockwise)
            force_unit: Unit of force values (default: N)
            moment_unit: Unit of moment values (default: N.m)

        Returns:
            CalculationResult with equilibrium status (1.0 if in equilibrium)
        """
        self.clear_inputs()
        self.set_force_vectors(forces, force_unit)
        if moments is not None:
            self.set_moments(moments, moment_unit)
        return self.calculate("equilibrium")
