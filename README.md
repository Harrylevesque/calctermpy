# Advanced Scientific Calculator - Modular Structure

This project has been restructured into a modular architecture for better maintainability and organization.

## Project Structure

```
calctermpy/
├── main.py                     # Main entry point
├── requirements.txt            # Dependencies
├── src/                        # Source code
│   ├── __init__.py
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── imports.py          # Common imports and constants
│   │   ├── syntax_highlighter.py  # Python syntax highlighting
│   │   └── calculator.py       # Main calculator class
│   ├── widgets/                # UI widgets
│   │   ├── __init__.py
│   │   ├── code_editor.py      # Code editor with line numbers
│   │   └── graph_plot_widget.py # Graph plotting widget
│   ├── panels/                 # Dock panels
│   │   ├── __init__.py
│   │   ├── history_panel.py    # Calculation history
│   │   ├── custom_function_library.py  # Custom functions
│   │   └── variable_inspector.py  # Variable management
│   └── dialogs/                # Dialog boxes
│       ├── __init__.py
│       ├── help_dialog.py      # Help documentation
│       ├── custom_function_dialog.py  # Function editor
│       ├── unit_converter_dialog.py   # Unit conversions
│       ├── theme_customizer.py  # Theme customization
│       └── settings_dialog.py   # Application settings
```

## Features by Module

### Core (`src/core/`)
- **imports.py**: Centralized imports for all scientific libraries (NumPy, SciPy, SymPy, matplotlib)
- **syntax_highlighter.py**: Python syntax highlighting with VS Code-like themes
- **calculator.py**: Main application class with document management and calculation engine

### Widgets (`src/widgets/`)
- **code_editor.py**: Custom text editor with line numbers and inline result display
- **graph_plot_widget.py**: Mathematical function plotting using matplotlib

### Panels (`src/panels/`)
- **history_panel.py**: Calculation history with export functionality
- **custom_function_library.py**: User-defined function management
- **variable_inspector.py**: Variable viewing, editing, and deletion

### Dialogs (`src/dialogs/`)
- **algebra_helper_dialog.py**: Interactive symbolic algebra tool
- **help_dialog.py**: Comprehensive help with examples
- **custom_function_dialog.py**: Function creation and editing interface
- **unit_converter_dialog.py**: Multi-category unit conversion tool
- **theme_customizer.py**: Color scheme and font customization
- **settings_dialog.py**: Application preferences

## Key Features

### Mathematical Capabilities
- **Python math library**: Full access to trigonometric, logarithmic, and special functions
- **NumPy integration**: Array operations, linear algebra, statistics
- **SciPy support**: Optimization, integration, advanced statistics
- **SymPy symbolic math**: Algebraic manipulation, calculus, equation solving
- **Advanced algebra solving**: Formula condensing, expansion, factorization, multiple imaginary variables
- **Equation solving**: Solve single equations and systems with symbolic or numerical solutions
- **Complex number support**: Full complex arithmetic via cmath and SymPy imaginary variables

### User Interface
- **Multi-document interface**: Tabbed documents for different calculations
- **Dock panels**: Dockable and tabbable side panels
- **Syntax highlighting**: Python code highlighting with multiple themes
- **Inline results**: Real-time calculation results displayed next to code
- **Line numbers**: Professional code editor with line numbering

### Advanced Features
- **Algebra Helper**: Interactive dialog for symbolic algebra (expand, factor, solve equations)
- **Variable management**: Interactive variable inspector with editing
- **Function library**: Create and manage custom mathematical functions
- **Graph plotting**: 2D function plotting with customizable ranges
- **Unit conversion**: Multi-category unit converter (length, mass, temperature, etc.)
- **Theme customization**: Full color scheme and font customization
- **Calculation history**: Persistent history with export functionality

### Algebra Solving Features
The calculator now includes comprehensive symbolic algebra capabilities:
- **Symbolic variables**: Create single or multiple symbolic/complex variables
- **Formula condensing**: Collect terms, combine fractions, cancel common factors
- **Formula expansion**: Expand polynomials, trigonometric, logarithmic expressions
- **Simplification**: Multiple simplification methods (general, trig, rational, etc.)
- **Equation solving**: Solve single equations or systems with symbolic solutions
- **Multiple imaginary variables**: Full support for complex symbolic variables

See **ALGEBRA_GUIDE.md** for detailed documentation and **ALGEBRA_EXAMPLES.txt** for examples.

Access the Algebra Helper via: **Tools → Algebra Helper**

## Usage

### Running the Application
```bash
python main.py
```

### Basic Usage
1. Type mathematical expressions in the document editor
2. Results appear inline as you type
3. Use variables: `x = 5`, then `y = x * 2`
4. Access scientific functions: `math.sin(x)`, `np.array([1,2,3])`
5. Plot functions in the graph panel: `math.sin(x)`

### Advanced Features
- **Custom Functions**: Use the Functions panel to create reusable functions
- **Variable Inspector**: View and modify all variables in real-time
- **History**: Access previous calculations from the History panel
- **Unit Conversion**: Convert between different units using the Tools menu
- **Themes**: Customize colors and fonts via Tools → Theme Customizer

## Dependencies
- PySide6 (Qt6 bindings for Python)
- NumPy (optional, for advanced array operations)
- SciPy (optional, for scientific computing)
- SymPy (optional, for symbolic mathematics)
- Matplotlib (optional, for plotting)

## Installation
```bash
pip install -r requirements.txt
```

## Module Import Structure
Each module is designed to be self-contained with clear dependencies:

- `core.imports` provides all common imports
- Each widget/panel/dialog imports only what it needs
- The main calculator class ties everything together
- Circular dependencies are avoided through careful design

This modular structure makes the codebase much more maintainable, testable, and extensible.
