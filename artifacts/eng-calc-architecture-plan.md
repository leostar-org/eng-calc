# Engineering Calculator (eng-calc) - Architecture Plan

**Project:** Python-based Mechanical Engineering Calculator with GUI  
**Date Created:** February 1, 2026  
**Purpose:** Comprehensive architecture and design document for eng-calc project

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Core Functional Modules](#core-functional-modules)
3. [GUI Framework Analysis](#gui-framework-analysis)
4. [Architecture Design](#architecture-design)
5. [File Structure](#file-structure)
6. [Class Design](#class-design)
7. [Files to Create](#files-to-create)
8. [Dependencies & Requirements](#dependencies--requirements)

---

## Project Overview

### Objectives
- Create an extensible mechanical engineering calculator for quick computations
- Provide an intuitive GUI for users to perform complex calculations
- Support multiple calculation domains (stress, strain, torque, forces, energy, etc.)
- Enable unit conversions and standardized engineering calculations
- Allow users to save/load calculation history and results

### Target Users
- Mechanical engineers
- Students in mechanical engineering programs
- Engineering technicians
- Anyone needing quick mechanical engineering calculations

### Key Features
- Multiple calculation modules for different mechanical engineering domains
- Real-time calculation and result display
- Unit conversion support (SI, Imperial)
- Calculation history tracking
- Save/export results
- Help and documentation features

---

## Core Functional Modules

### 1. **Stress & Strain Module**
**Purpose:** Calculate stress, strain, and related material properties

**Calculations:**
- Tensile/Compressive stress: σ = F/A
- Shear stress: τ = F/A
- Normal strain: ε = ΔL/L
- Shear strain: γ = Δx/h
- Young's Modulus: E = σ/ε
- Poisson's Ratio calculations
- Stress concentration factors
- Combined stress analysis (Mohr's Circle)
- Von Mises equivalent stress
- Principal stresses

**Inputs:** Force, Area, Length, Displacement, Material properties

---

### 2. **Torque & Torsion Module**
**Purpose:** Calculate torque, angular velocity, and torsional properties

**Calculations:**
- Torque: τ = F × r
- Angular velocity: ω = θ/t
- Polar moment of inertia (I_p) for various cross-sections
- Shear stress in circular shafts: τ = (τ × r)/I_p
- Angle of twist: θ = (τ × L)/(G × I_p)
- Power transmission: P = τ × ω
- Critical torque (buckling analysis)
- Torsional rigidity

**Inputs:** Force, Radius, Angle, Length, Material shear modulus

---

### 3. **Force & Equilibrium Module**
**Purpose:** Analyze forces and equilibrium conditions

**Calculations:**
- Resultant force (2D/3D vector addition)
- Component resolution
- Equilibrium check (ΣF = 0, ΣM = 0)
- Force polygon analysis
- Moment about a point: M = F × d
- Couple forces analysis
- Free body diagram calculations
- Support reactions (beams, frames)
- Truss analysis (method of joints)

**Inputs:** Force magnitudes, directions, distances, geometry

---

### 4. **Bending & Beam Analysis Module**
**Purpose:** Calculate stresses and deflections in beams

**Calculations:**
- Bending moment: M = F × L
- Shear force diagrams
- Bending stress: σ = (M × y)/I
- Second moment of area (I) for standard sections
- Beam deflection (simple formulas for standard cases)
- Slope calculations
- Reaction forces and moments
- Maximum stress locations
- Support types handling (cantilever, simply supported, fixed, etc.)

**Inputs:** Load type, span, section geometry, material properties

---

### 5. **Energy & Work Module**
**Purpose:** Calculate mechanical energy and work

**Calculations:**
- Work: W = F × d × cos(θ)
- Kinetic energy: KE = ½mv²
- Potential energy: PE = mgh
- Elastic strain energy: U = ½σ²/E × V
- Power: P = W/t
- Efficiency calculations
- Energy conservation problems
- Impact and collision analysis

**Inputs:** Force, displacement, mass, velocity, height

---

### 6. **Motion & Kinematics Module**
**Purpose:** Calculate motion parameters and dynamics

**Calculations:**
- Linear motion: s = ut + ½at²
- Velocity: v = u + at
- Acceleration: a = F/m
- Circular motion: a_c = v²/r = ω²r
- Angular kinematics
- Centripetal force: F_c = mv²/r
- Momentum: p = mv
- Conservation of momentum
- Rotational inertia (I) calculations

**Inputs:** Mass, force, velocity, acceleration, radius, time

---

### 7. **Material Properties & Database Module**
**Purpose:** Provide standardized material data and lookup

**Data:**
- Density, Young's modulus, Shear modulus, Poisson's ratio
- Yield strength, Ultimate tensile strength
- Common materials (steel alloys, aluminum, copper, etc.)
- Material selection tools
- Temperature effects on properties

**Functionality:**
- Material lookup by name or designation
- Property interpolation
- Custom material definition
- Material comparison

---

### 8. **Unit Conversion Module**
**Purpose:** Handle unit conversions across systems

**Supported Systems:**
- SI (Metric)
- Imperial (US/UK)
- CGS (where relevant)

**Conversion Categories:**
- Length: m, cm, mm, in, ft, etc.
- Force: N, kN, lbf, kips, etc.
- Stress: Pa, MPa, GPa, psi, ksi, etc.
- Torque: N⋅m, lbf⋅ft, lbf⋅in, etc.
- Power: W, kW, hp, etc.
- Temperature: °C, °F, K
- Area, Volume, Density, etc.

---

### 9. **Calculation History & Memory Module**
**Purpose:** Track and manage calculation history

**Functionality:**
- Store recent calculations
- Tag and organize calculations
- Search history
- Export calculation results
- Load saved calculations
- Batch calculations
- Undo/Redo functionality

---

### 10. **Validation & Error Handling Module**
**Purpose:** Ensure data integrity and provide meaningful feedback

**Features:**
- Input validation (type, range, physics constraints)
- Unit compatibility checking
- Physical feasibility verification
- Error messages with suggestions
- Warnings for edge cases
- Numerical stability checks

---

## GUI Framework Analysis

### Option 1: Tkinter

**Pros:**
- Built-in with Python (no additional installation required)
- Lightweight and fast startup time
- Simple learning curve
- Good for traditional desktop applications
- Cross-platform (Windows, macOS, Linux)
- Minimal dependencies

**Cons:**
- Limited styling capabilities (dated appearance)
- Harder to create modern, polished UIs
- Fewer built-in widgets
- Limited support for advanced layouts
- Challenging for complex applications
- Less suitable for professional-looking applications

**Best for:** Simple calculators, quick prototypes, educational projects

---

### Option 2: PyQt6

**Pros:**
- Professional, modern appearance
- Rich set of widgets and UI components
- Advanced layout management (QLayouts)
- Excellent for complex, scalable applications
- Native look-and-feel on each platform
- Extensive styling with stylesheets (CSS-like)
- Excellent documentation and community support
- Better performance for large applications
- Built-in support for threads and signals/slots
- Packaging and distribution support

**Cons:**
- Larger package size
- Steeper learning curve
- Licensing (Community License for open-source)
- Slightly slower startup time
- Requires external dependency

**Best for:** Professional applications, complex UIs, large-scale projects

---

### **Recommendation: PyQt6**

**Rationale:**
- Engineering calculator is a tool for professionals/engineers
- Need modern, polished UI for credibility
- Extensibility and maintainability are important
- Complex calculations warrant robust framework
- Professional appearance increases adoption
- Signal/slot architecture supports modularity
- Better suited for future enhancements (graphs, real-time updates)

---

## Architecture Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        GUI Layer (PyQt6)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Main Window | Dialogs | Widgets | Views              │   │
│  │ (UI Components, Event Handling)                       │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Calculation Engine | Calculation Modules             │   │
│  │ (Stress, Strain, Torque, etc.)                       │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                     Utility Layer                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Unit Conversion | Material DB | Validation           │   │
│  │ History Management | Error Handling                   │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### Design Patterns

1. **Model-View-Controller (MVC)**
   - **Model:** Calculation modules, Material database, History
   - **View:** PyQt6 GUI components
   - **Controller:** Application logic bridging GUI and models

2. **Strategy Pattern**
   - Each calculation module implements a common interface
   - Easy to add new calculation types
   - Polymorphic execution of calculations

3. **Factory Pattern**
   - Factory for creating calculators
   - Factory for unit conversion
   - Material factory for database lookups

4. **Singleton Pattern**
   - Shared material database instance
   - Unit conversion manager
   - Application settings

5. **Observer Pattern**
   - PyQt6 signals/slots for GUI updates
   - History updates on new calculations
   - Real-time validation feedback

---

## File Structure

```
eng-calc/
├── README.md                          # Project overview
├── LICENSE                            # License file
├── requirements.txt                   # Python dependencies
├── setup.py                           # Package setup configuration
├── .gitignore                         # Git ignore rules
│
├── eng_calc/                          # Main package directory
│   ├── __init__.py                    # Package initialization
│   ├── main.py                        # Application entry point
│   ├── app.py                         # Main application class
│   │
│   ├── gui/                           # GUI components (PyQt6)
│   │   ├── __init__.py
│   │   ├── main_window.py             # Main window class
│   │   ├── dialogs.py                 # Dialog windows
│   │   ├── widgets.py                 # Custom widgets
│   │   ├── styles.py                  # Stylesheets and themes
│   │   ├── calculator_view.py         # Main calculator interface
│   │   ├── history_view.py            # Calculation history view
│   │   ├── material_view.py           # Material database view
│   │   └── settings_view.py           # Application settings
│   │
│   ├── calculators/                   # Calculation modules (Business Logic)
│   │   ├── __init__.py
│   │   ├── base_calculator.py         # Abstract base class
│   │   ├── stress_calculator.py       # Stress & strain calculations
│   │   ├── torque_calculator.py       # Torque & torsion calculations
│   │   ├── force_calculator.py        # Force & equilibrium calculations
│   │   ├── beam_calculator.py         # Bending & beam analysis
│   │   ├── energy_calculator.py       # Energy & work calculations
│   │   ├── kinematics_calculator.py   # Motion & kinematics calculations
│   │   └── calculator_factory.py      # Factory for creating calculators
│   │
│   ├── utilities/                     # Utility modules
│   │   ├── __init__.py
│   │   ├── unit_converter.py          # Unit conversion engine
│   │   ├── units.py                   # Unit definitions and constants
│   │   ├── materials.py               # Material database and lookup
│   │   ├── validators.py              # Input validation
│   │   ├── constants.py               # Physical constants
│   │   └── errors.py                  # Custom exceptions
│   │
│   ├── models/                        # Data models
│   │   ├── __init__.py
│   │   ├── calculation.py             # Calculation result model
│   │   ├── material.py                # Material property model
│   │   ├── formula.py                 # Formula and calculation metadata
│   │   └── history.py                 # History management model
│   │
│   ├── services/                      # Business logic services
│   │   ├── __init__.py
│   │   ├── calculation_service.py     # High-level calculation service
│   │   ├── history_service.py         # History management service
│   │   ├── export_service.py          # Export/save functionality
│   │   └── config_service.py          # Configuration management
│   │
│   ├── data/                          # Data files
│   │   ├── materials.json             # Material properties database
│   │   ├── formulas.json              # Formula definitions
│   │   └── defaults.json              # Default configurations
│   │
│   └── resources/                     # Static resources
│       ├── icons/                     # Application icons
│       ├── images/                    # Images and graphics
│       └── styles/                    # CSS stylesheets
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── test_calculators.py            # Unit tests for calculators
│   ├── test_unit_converter.py         # Unit converter tests
│   ├── test_materials.py              # Material database tests
│   ├── test_validators.py             # Validation tests
│   ├── test_gui.py                    # GUI integration tests
│   └── fixtures/                      # Test data and fixtures
│
├── docs/                              # Documentation
│   ├── API.md                         # API documentation
│   ├── USAGE.md                       # User guide
│   ├── DEVELOPMENT.md                 # Development guide
│   ├── ARCHITECTURE.md                # Architecture details
│   └── FORMULAS.md                    # Engineering formulas reference
│
├── examples/                          # Example scripts
│   ├── basic_calculations.py          # Basic usage examples
│   └── advanced_scenarios.py          # Advanced use cases
│
└── CHANGELOG.md                       # Version history
```

---

## Class Design

### Core Calculator Architecture

#### **BaseCalculator (Abstract Base Class)**
```
BaseCalculator
├── Attributes:
│   - inputs: dict
│   - outputs: dict
│   - description: str
│   - formulas: list
│
├── Methods:
│   - validate_inputs() -> bool
│   - calculate() -> dict (abstract)
│   - get_formula_description() -> str
│   - set_units(input_units, output_units) -> None
```

#### **Concrete Calculators**

**StressCalculator**
```
StressCalculator(BaseCalculator)
├── Methods:
│   - calculate_tensile_stress() -> float
│   - calculate_shear_stress() -> float
│   - calculate_strain() -> float
│   - calculate_youngs_modulus() -> float
│   - calculate_von_mises_stress() -> float
│   - calculate_mohr_circle() -> dict
```

**TorqueCalculator**
```
TorqueCalculator(BaseCalculator)
├── Methods:
│   - calculate_torque() -> float
│   - calculate_power_transmission() -> float
│   - calculate_polar_moment() -> float
│   - calculate_angle_of_twist() -> float
│   - calculate_shear_stress_shaft() -> float
```

**ForceCalculator**
```
ForceCalculator(BaseCalculator)
├── Methods:
│   - calculate_resultant_force() -> float
│   - calculate_components() -> tuple
│   - calculate_moment() -> float
│   - analyze_equilibrium() -> bool
│   - resolve_forces_2d() -> tuple
│   - resolve_forces_3d() -> tuple
```

**BeamCalculator**
```
BeamCalculator(BaseCalculator)
├── Methods:
│   - calculate_bending_stress() -> float
│   - calculate_second_moment() -> float
│   - calculate_deflection() -> float
│   - calculate_support_reactions() -> dict
│   - generate_shear_diagram() -> list
│   - generate_moment_diagram() -> list
```

**EnergyCalculator**
```
EnergyCalculator(BaseCalculator)
├── Methods:
│   - calculate_kinetic_energy() -> float
│   - calculate_potential_energy() -> float
│   - calculate_strain_energy() -> float
│   - calculate_work() -> float
│   - calculate_power() -> float
│   - analyze_collision() -> dict
```

**KinematicsCalculator**
```
KinematicsCalculator(BaseCalculator)
├── Methods:
│   - calculate_displacement() -> float
│   - calculate_velocity() -> float
│   - calculate_acceleration() -> float
│   - circular_motion_analysis() -> dict
│   - calculate_momentum() -> float
│   - calculate_centripetal_force() -> float
```

### Utility Classes

**UnitConverter**
```
UnitConverter
├── Attributes:
│   - conversion_table: dict
│   - supported_systems: list
│
├── Methods:
│   - convert(value, from_unit, to_unit) -> float
│   - add_custom_unit(category, name, factor) -> None
│   - get_conversion_factor(from_unit, to_unit) -> float
│   - list_units(category) -> list
```

**MaterialDatabase**
```
MaterialDatabase (Singleton)
├── Attributes:
│   - materials: dict
│   - properties: dict
│
├── Methods:
│   - get_material(name) -> Material
│   - list_materials() -> list
│   - add_material(name, properties) -> None
│   - search_by_property(property, range) -> list
│   - get_property(material, property) -> value
```

**Validator**
```
Validator
├── Methods:
│   - validate_number(value, min=None, max=None) -> bool
│   - validate_positive(value) -> bool
│   - validate_unit(value, expected_unit) -> bool
│   - validate_physics(inputs, constraint) -> bool
│   - get_error_message() -> str
```

**HistoryManager**
```
HistoryManager
├── Attributes:
│   - history: list
│   - max_size: int
│
├── Methods:
│   - add_calculation(calculation) -> None
│   - get_history(limit) -> list
│   - search_history(criteria) -> list
│   - save_history(filepath) -> None
│   - load_history(filepath) -> None
│   - clear_history() -> None
│   - export_calculation(calculation, format) -> str
```

### Data Models

**Calculation**
```
Calculation
├── Attributes:
│   - calculator_type: str
│   - inputs: dict
│   - outputs: dict
│   - timestamp: datetime
│   - notes: str
│   - input_units: dict
│   - output_units: dict
```

**Material**
```
Material
├── Attributes:
│   - name: str
│   - designation: str
│   - properties: dict (E, G, ν, σ_y, σ_u, ρ, etc.)
│   - temperature_range: tuple
│   - source: str
```

**Formula**
```
Formula
├── Attributes:
│   - name: str
│   - equation: str
│   - description: str
│   - inputs: list[str]
│   - outputs: list[str]
│   - category: str
│   - assumptions: list[str]
```

### GUI Classes

**MainWindow**
```
MainWindow(QMainWindow)
├── Components:
│   - menu_bar: QMenuBar
│   - toolbar: QToolBar
│   - central_widget: QWidget
│   - calculator_view: CalculatorView
│   - history_panel: HistoryView
│   - status_bar: QStatusBar
│
├── Methods:
│   - setup_ui() -> None
│   - create_menus() -> None
│   - connect_signals() -> None
│   - on_calculate() -> None
│   - on_clear() -> None
│   - on_history_selected() -> None
│   - on_export() -> None
```

**CalculatorView**
```
CalculatorView(QWidget)
├── Components:
│   - calculator_selector: QComboBox
│   - input_fields: dict[str, QLineEdit]
│   - unit_selectors: dict[str, QComboBox]
│   - output_display: QTextEdit
│   - formula_display: QLabel
│   - calculate_button: QPushButton
│
├── Methods:
│   - load_calculator(calculator_type) -> None
│   - get_inputs() -> dict
│   - display_results(results) -> None
│   - update_formula_display() -> None
│   - validate_inputs() -> bool
```

---

## Files to Create

### Priority 1: Foundation (Core Architecture)

1. **eng_calc/__init__.py** - Package initialization
2. **eng_calc/main.py** - Application entry point
3. **eng_calc/app.py** - Main PyQt6 application class

### Priority 2: Base Classes & Utilities

4. **eng_calc/calculators/base_calculator.py** - Abstract base class
5. **eng_calc/utilities/errors.py** - Custom exceptions
6. **eng_calc/utilities/constants.py** - Physical constants
7. **eng_calc/utilities/units.py** - Unit definitions
8. **eng_calc/utilities/unit_converter.py** - Unit conversion engine
9. **eng_calc/utilities/validators.py** - Input validation

### Priority 3: Calculation Modules

10. **eng_calc/calculators/stress_calculator.py**
11. **eng_calc/calculators/torque_calculator.py**
12. **eng_calc/calculators/force_calculator.py**
13. **eng_calc/calculators/beam_calculator.py**
14. **eng_calc/calculators/energy_calculator.py**
15. **eng_calc/calculators/kinematics_calculator.py**
16. **eng_calc/calculators/calculator_factory.py**

### Priority 4: Data & Utilities

17. **eng_calc/utilities/materials.py** - Material database
18. **eng_calc/models/calculation.py** - Calculation model
19. **eng_calc/models/material.py** - Material model
20. **eng_calc/models/formula.py** - Formula model
21. **eng_calc/data/materials.json** - Material database file

### Priority 5: Services

22. **eng_calc/services/calculation_service.py**
23. **eng_calc/services/history_service.py**
24. **eng_calc/services/export_service.py**
25. **eng_calc/models/history.py** - History model

### Priority 6: GUI Components

26. **eng_calc/gui/main_window.py** - Main window
27. **eng_calc/gui/calculator_view.py** - Calculator interface
28. **eng_calc/gui/widgets.py** - Custom widgets
29. **eng_calc/gui/styles.py** - Stylesheets
30. **eng_calc/gui/dialogs.py** - Dialog windows
31. **eng_calc/gui/history_view.py** - History panel
32. **eng_calc/gui/material_view.py** - Material database view
33. **eng_calc/gui/settings_view.py** - Settings window

### Priority 7: Configuration & Documentation

34. **eng_calc/data/formulas.json** - Formula database
35. **eng_calc/data/defaults.json** - Default configurations
36. **eng_calc/services/config_service.py** - Configuration management

### Priority 8: Testing & Documentation

37. **tests/test_calculators.py** - Calculator unit tests
38. **tests/test_unit_converter.py** - Converter tests
39. **tests/test_validators.py** - Validation tests
40. **tests/fixtures/test_data.json** - Test data
41. **docs/API.md** - API documentation
42. **docs/USAGE.md** - User guide
43. **README.md** - Project readme
44. **requirements.txt** - Dependencies list
45. **setup.py** - Package setup

### Priority 9: Examples & Extended Features

46. **examples/basic_calculations.py** - Usage examples
47. **eng_calc/gui/help_dialog.py** - Help system
48. **CHANGELOG.md** - Version history

---

## Dependencies & Requirements

### Core Dependencies

```
PyQt6>=6.5.0              # GUI framework
PyQt6-sip>=13.5.0         # PyQt6 support package
numpy>=1.24.0             # Numerical calculations
scipy>=1.10.0             # Scientific computing
```

### Development Dependencies

```
pytest>=7.4.0             # Testing framework
pytest-cov>=4.1.0         # Coverage reporting
black>=23.7.0             # Code formatting
pylint>=2.17.0            # Linting
mypy>=1.4.0               # Type checking
sphinx>=7.1.0             # Documentation
```

### Optional Dependencies

```
matplotlib>=3.7.0         # Plotting (for diagrams)
pandas>=2.0.0             # Data handling
openpyxl>=3.1.0           # Excel export
reportlab>=4.0.0          # PDF generation
```

### Python Version
- **Minimum:** Python 3.9
- **Recommended:** Python 3.11+

### System Requirements
- **OS:** Windows 10+, macOS 10.14+, Linux (Ubuntu 20.04+)
- **RAM:** 512 MB minimum
- **Disk:** 100 MB for application + dependencies

---

## Implementation Roadmap

### Phase 1: MVP (Minimum Viable Product)
- **Duration:** 2-3 weeks
- **Scope:** Basic calculator with 3-4 main modules
- **Deliverables:**
  - Stress calculator
  - Force calculator
  - Basic GUI with PyQt6
  - Unit conversion
  - Simple validation

### Phase 2: Core Features
- **Duration:** 3-4 weeks
- **Scope:** Complete all main calculation modules
- **Deliverables:**
  - All 6 calculation modules complete
  - Material database
  - Calculation history
  - Enhanced validation

### Phase 3: Polish & Enhancement
- **Duration:** 2-3 weeks
- **Scope:** UI/UX improvements, testing
- **Deliverables:**
  - Professional styling
  - Help system
  - Comprehensive testing
  - Documentation

### Phase 4: Advanced Features
- **Duration:** 2+ weeks
- **Scope:** Export, visualization, advanced features
- **Deliverables:**
  - Export functionality (PDF, Excel)
  - Graphical diagrams (Mohr's circle, beam diagrams)
  - Batch calculations
  - Plugin system

---

## Key Design Considerations

### 1. Modularity
- Each calculator is independent and can be extended
- Easy to add new calculation types via Strategy pattern
- Clear separation of concerns (GUI, Business Logic, Utilities)

### 2. Extensibility
- Material database can be extended without code changes
- Unit system is flexible and customizable
- Formula database is external and editable

### 3. Maintainability
- Clear naming conventions
- Type hints throughout
- Comprehensive documentation
- Test coverage > 80%

### 4. User Experience
- Intuitive calculator interface
- Clear error messages
- Real-time validation feedback
- Quick access to history
- Export options

### 5. Performance
- Efficient calculation algorithms
- Lazy loading of material database
- Caching for unit conversions
- Responsive GUI (long calculations in threads)

### 6. Scalability
- Service layer allows for API exposure in future
- Database design supports large material libraries
- History management with configurable limits

---

## Conclusion

This architecture provides a solid foundation for building a professional-grade mechanical engineering calculator. The modular design allows for incremental development, comprehensive testing, and easy future enhancements. The choice of PyQt6 ensures a modern, professional interface that reflects the quality of the underlying calculations.

The clear separation between GUI, business logic, and utilities ensures maintainability and testability. The use of established design patterns (MVC, Strategy, Factory, Singleton) provides a framework that developers will find familiar and easy to extend.

---

**Document Version:** 1.0  
**Last Updated:** February 1, 2026  
**Status:** Ready for Implementation
