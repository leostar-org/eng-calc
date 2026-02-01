"""
Stress & Strain Calculator Module

Provides calculations for mechanical stress, strain, and material properties.
Implements the BaseCalculator interface with methods for:
- Tensile stress (σ = F/A)
- Shear stress (τ = F/A)
- Normal strain (ε = ΔL/L)
- Young's modulus (E = σ/ε)
"""

from eng_calc.calculators.base_calculator import BaseCalculator, CalculationResult
from eng_calc.utilities import (
    CalculationError,
    UnitCategory,
    UnitConverter,
    ValidationError,
    Validator,
)


class StressCalculator(BaseCalculator):
    """
    Calculator for stress and strain analysis.

    Provides methods for calculating mechanical stress, strain, and
    elastic modulus. Supports unit conversion for both inputs and outputs.

    Available calculations:
        - tensile_stress: Calculate tensile stress (σ = F/A)
        - shear_stress: Calculate shear stress (τ = F/A)
        - normal_strain: Calculate normal strain (ε = ΔL/L)
        - youngs_modulus: Calculate Young's modulus (E = σ/ε)

    Example:
        >>> calc = StressCalculator()
        >>> calc.set_input("force", 1000, "N")
        >>> calc.set_input("area", 0.001, "m2")
        >>> result = calc.calculate("tensile_stress")
        >>> print(result)
        tensile_stress: 1e+06 Pa
    """

    # Default SI units for each input type
    DEFAULT_INPUT_UNITS = {
        "force": "N",
        "area": "m2",
        "original_length": "m",
        "change_in_length": "m",
        "stress": "Pa",
        "strain": None,  # Strain is dimensionless
    }

    # Formulas for each calculation
    FORMULAS = {
        "tensile_stress": "σ = F / A",
        "shear_stress": "τ = F / A",
        "normal_strain": "ε = ΔL / L₀",
        "youngs_modulus": "E = σ / ε",
    }

    def __init__(self) -> None:
        """Initialize the StressCalculator."""
        super().__init__()
        self._converter = UnitConverter()

    @property
    def name(self) -> str:
        """Return the display name of the calculator."""
        return "Stress & Strain Calculator"

    @property
    def description(self) -> str:
        """Return a brief description of the calculator's purpose."""
        return (
            "Calculate mechanical stress, strain, and elastic properties "
            "for structural analysis."
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
        return ["tensile_stress", "shear_stress", "normal_strain", "youngs_modulus"]

    def get_required_inputs_for(self, calculation_name: str) -> list[str]:
        """
        Get the required inputs for a specific calculation.

        Args:
            calculation_name: Name of the calculation

        Returns:
            List of required input parameter names
        """
        requirements = {
            "tensile_stress": ["force", "area"],
            "shear_stress": ["force", "area"],
            "normal_strain": ["original_length", "change_in_length"],
            "youngs_modulus": ["stress", "strain"],
        }
        return requirements.get(calculation_name, [])

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
                if value is not None:
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
            required = self.get_required_inputs_for(calculation_name)
            Validator.validate_required_inputs(self._inputs, required)

            if calculation_name == "tensile_stress":
                self._validate_stress_inputs("tensile_stress")
            elif calculation_name == "shear_stress":
                self._validate_stress_inputs("shear_stress")
            elif calculation_name == "normal_strain":
                self._validate_strain_inputs()
            elif calculation_name == "youngs_modulus":
                self._validate_youngs_modulus_inputs()
            else:
                raise CalculationError(
                    f"Unknown calculation: {calculation_name}",
                    calculation_name=calculation_name,
                )

            return True, ""
        except (ValidationError, CalculationError) as e:
            return False, str(e)

    def _validate_stress_inputs(self, calc_name: str) -> None:
        """Validate inputs for stress calculations."""
        force = self._inputs.get("force")
        area = self._inputs.get("area")

        Validator.validate_number(force, "force")
        Validator.validate_number(area, "area")
        Validator.validate_finite(force, "force")
        Validator.validate_finite(area, "area")

        # Force can be any real number (compression is negative)
        # Area must be positive
        Validator.validate_positive(area, "area")

        # Validate units if provided
        if "force" in self._input_units:
            Validator.validate_unit(
                self._input_units["force"], UnitCategory.FORCE, "force unit"
            )
        if "area" in self._input_units:
            Validator.validate_unit(
                self._input_units["area"], UnitCategory.AREA, "area unit"
            )

    def _validate_strain_inputs(self) -> None:
        """Validate inputs for strain calculation."""
        original_length = self._inputs.get("original_length")
        change_in_length = self._inputs.get("change_in_length")

        Validator.validate_number(original_length, "original_length")
        Validator.validate_number(change_in_length, "change_in_length")
        Validator.validate_finite(original_length, "original_length")
        Validator.validate_finite(change_in_length, "change_in_length")

        # Original length must be positive
        Validator.validate_positive(original_length, "original_length")

        # change_in_length can be positive (tension) or negative (compression)

        # Validate units if provided
        if "original_length" in self._input_units:
            Validator.validate_unit(
                self._input_units["original_length"],
                UnitCategory.LENGTH,
                "original_length unit",
            )
        if "change_in_length" in self._input_units:
            Validator.validate_unit(
                self._input_units["change_in_length"],
                UnitCategory.LENGTH,
                "change_in_length unit",
            )

    def _validate_youngs_modulus_inputs(self) -> None:
        """Validate inputs for Young's modulus calculation."""
        stress = self._inputs.get("stress")
        strain = self._inputs.get("strain")

        Validator.validate_number(stress, "stress")
        Validator.validate_number(strain, "strain")
        Validator.validate_finite(stress, "stress")
        Validator.validate_finite(strain, "strain")

        # Strain cannot be zero (division by zero)
        Validator.validate_non_zero(strain, "strain")

        # Validate unit if provided
        if "stress" in self._input_units:
            Validator.validate_unit(
                self._input_units["stress"], UnitCategory.PRESSURE, "stress unit"
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
        if calculation_name == "tensile_stress":
            return self._calculate_tensile_stress()
        elif calculation_name == "shear_stress":
            return self._calculate_shear_stress()
        elif calculation_name == "normal_strain":
            return self._calculate_normal_strain()
        elif calculation_name == "youngs_modulus":
            return self._calculate_youngs_modulus()
        else:
            raise CalculationError(
                f"Calculation '{calculation_name}' not implemented",
                calculation_name=calculation_name,
            )

    def _calculate_tensile_stress(self) -> CalculationResult:
        """
        Calculate tensile stress (σ = F/A).

        Tensile stress is the force per unit area acting perpendicular
        to the cross-section in the direction that tends to stretch
        (elongate) the material.

        Returns:
            CalculationResult with stress value in Pa (or desired output unit)
        """
        # Get and convert inputs to SI
        force = self._convert_to_si(self._inputs["force"], "force")
        area = self._convert_to_si(self._inputs["area"], "area")

        # Calculate stress: σ = F / A
        stress = force / area

        # Convert output if needed
        result_value, result_unit = self._convert_from_si(
            stress, "tensile_stress", "Pa"
        )

        return CalculationResult(
            name="tensile_stress",
            value=result_value,
            unit=result_unit,
            formula=self.FORMULAS["tensile_stress"],
            inputs={
                "force": self._inputs["force"],
                "force_unit": self._input_units.get("force", "N"),
                "area": self._inputs["area"],
                "area_unit": self._input_units.get("area", "m2"),
            },
        )

    def _calculate_shear_stress(self) -> CalculationResult:
        """
        Calculate shear stress (τ = F/A).

        Shear stress is the force per unit area acting parallel
        (tangential) to the cross-section.

        Returns:
            CalculationResult with stress value in Pa (or desired output unit)
        """
        # Get and convert inputs to SI
        force = self._convert_to_si(self._inputs["force"], "force")
        area = self._convert_to_si(self._inputs["area"], "area")

        # Calculate shear stress: τ = F / A
        stress = force / area

        # Convert output if needed
        result_value, result_unit = self._convert_from_si(stress, "shear_stress", "Pa")

        return CalculationResult(
            name="shear_stress",
            value=result_value,
            unit=result_unit,
            formula=self.FORMULAS["shear_stress"],
            inputs={
                "force": self._inputs["force"],
                "force_unit": self._input_units.get("force", "N"),
                "area": self._inputs["area"],
                "area_unit": self._input_units.get("area", "m2"),
            },
        )

    def _calculate_normal_strain(self) -> CalculationResult:
        """
        Calculate normal strain (ε = ΔL/L₀).

        Normal strain is the ratio of change in length to original length.
        It is dimensionless.

        Returns:
            CalculationResult with strain value (dimensionless)
        """
        # Get and convert inputs to SI (meters)
        original_length = self._convert_to_si(
            self._inputs["original_length"], "original_length"
        )
        change_in_length = self._convert_to_si(
            self._inputs["change_in_length"], "change_in_length"
        )

        # Calculate strain: ε = ΔL / L₀
        strain = change_in_length / original_length

        return CalculationResult(
            name="normal_strain",
            value=strain,
            unit="",  # Strain is dimensionless
            formula=self.FORMULAS["normal_strain"],
            inputs={
                "original_length": self._inputs["original_length"],
                "original_length_unit": self._input_units.get("original_length", "m"),
                "change_in_length": self._inputs["change_in_length"],
                "change_in_length_unit": self._input_units.get("change_in_length", "m"),
            },
        )

    def _calculate_youngs_modulus(self) -> CalculationResult:
        """
        Calculate Young's modulus (E = σ/ε).

        Young's modulus (elastic modulus) is the ratio of stress to strain
        in the linear elastic region. It represents the stiffness of a material.

        Returns:
            CalculationResult with modulus value in Pa (or desired output unit)
        """
        # Get and convert stress to SI
        stress = self._convert_to_si(self._inputs["stress"], "stress")
        strain = self._inputs["strain"]  # Dimensionless, no conversion needed

        # Calculate Young's modulus: E = σ / ε
        modulus = stress / strain

        # Convert output if needed
        result_value, result_unit = self._convert_from_si(
            modulus, "youngs_modulus", "Pa"
        )

        return CalculationResult(
            name="youngs_modulus",
            value=result_value,
            unit=result_unit,
            formula=self.FORMULAS["youngs_modulus"],
            inputs={
                "stress": self._inputs["stress"],
                "stress_unit": self._input_units.get("stress", "Pa"),
                "strain": self._inputs["strain"],
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

    def calculate_tensile_stress(
        self,
        force: float,
        area: float,
        force_unit: str = "N",
        area_unit: str = "m2",
        output_unit: str | None = None,
    ) -> CalculationResult:
        """
        Calculate tensile stress directly with parameters.

        Args:
            force: Applied force
            area: Cross-sectional area
            force_unit: Unit of force (default: N)
            area_unit: Unit of area (default: m2)
            output_unit: Desired output unit (default: Pa)

        Returns:
            CalculationResult with tensile stress
        """
        self.clear_inputs()
        self.set_input("force", force, force_unit)
        self.set_input("area", area, area_unit)
        if output_unit:
            self.set_output_unit("tensile_stress", output_unit)
        return self.calculate("tensile_stress")

    def calculate_shear_stress(
        self,
        force: float,
        area: float,
        force_unit: str = "N",
        area_unit: str = "m2",
        output_unit: str | None = None,
    ) -> CalculationResult:
        """
        Calculate shear stress directly with parameters.

        Args:
            force: Applied shear force
            area: Area parallel to force
            force_unit: Unit of force (default: N)
            area_unit: Unit of area (default: m2)
            output_unit: Desired output unit (default: Pa)

        Returns:
            CalculationResult with shear stress
        """
        self.clear_inputs()
        self.set_input("force", force, force_unit)
        self.set_input("area", area, area_unit)
        if output_unit:
            self.set_output_unit("shear_stress", output_unit)
        return self.calculate("shear_stress")

    def calculate_normal_strain(
        self,
        original_length: float,
        change_in_length: float,
        length_unit: str = "m",
    ) -> CalculationResult:
        """
        Calculate normal strain directly with parameters.

        Args:
            original_length: Original length of the material
            change_in_length: Change in length (positive for extension)
            length_unit: Unit of both lengths (default: m)

        Returns:
            CalculationResult with normal strain (dimensionless)
        """
        self.clear_inputs()
        self.set_input("original_length", original_length, length_unit)
        self.set_input("change_in_length", change_in_length, length_unit)
        return self.calculate("normal_strain")

    def calculate_youngs_modulus(
        self,
        stress: float,
        strain: float,
        stress_unit: str = "Pa",
        output_unit: str | None = None,
    ) -> CalculationResult:
        """
        Calculate Young's modulus directly with parameters.

        Args:
            stress: Applied stress
            strain: Resulting strain (dimensionless)
            stress_unit: Unit of stress (default: Pa)
            output_unit: Desired output unit (default: Pa)

        Returns:
            CalculationResult with Young's modulus
        """
        self.clear_inputs()
        self.set_input("stress", stress, stress_unit)
        self.set_input("strain", strain)
        if output_unit:
            self.set_output_unit("youngs_modulus", output_unit)
        return self.calculate("youngs_modulus")
