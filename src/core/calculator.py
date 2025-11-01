"""
Main calculator application class
"""

from .imports import *
from .syntax_highlighter import PythonSyntaxHighlighter
from .config_manager import ConfigManager
from ..widgets.code_editor import CodeEditor
from ..widgets.graph_plot_widget import GraphPlotWidget
from ..panels.history_panel import HistoryPanel
from ..panels.custom_function_library import CustomFunctionLibrary
from ..panels.variable_inspector import VariableInspector
from ..dialogs.help_dialog import HelpDialog
from ..dialogs.unit_converter_dialog import UnitConverterDialog
from ..dialogs.theme_customizer import ThemeCustomizer
from ..dialogs.settings_dialog import SettingsDialog
from ..dialogs.algebra_helper_dialog import AlgebraHelperDialog
from ..widgets.math_function_taskbar import MathFunctionTaskbar

class ScientificCalculator(QMainWindow):
    """Main calculator application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Scientific Calculator - Document Mode")
        self.setGeometry(100, 100, 1400, 800)
        
        # Initialize configuration manager
        self.config_manager = ConfigManager()
        
        # Initialize variables
        self.variables = {}
        self.calculation_history = []
        self.settings = QSettings("ScientificCalculator", "Settings")
        self.recent_files = []
        
        # Load configuration
        self.load_all_config()
        
        # Setup UI
        self.setup_ui()
        self.setup_calculation_namespace()
        self.setup_menu_bar()
        self.setup_toolbar()
        
        # Restore layout and apply styling
        self.restore_layout()
        self.apply_styling()
        
        # Auto-save timer
        self.setup_auto_save()

    def setup_calculation_namespace(self):
        """Prepare the safe evaluation namespace for calculations"""
        import math, random, statistics, cmath, decimal, fractions
        base_namespace = {
            # Core modules
            "math": math,
            "random": random,
            "statistics": statistics,
            "cmath": cmath,
            "decimal": decimal,
            "fractions": fractions,
            # Safe builtins
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "sum": sum,
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "int": int,
            "float": float,
            "complex": complex,
            "bool": bool,
            "str": str,
            "list": list,
            "tuple": tuple,
        }
        
        if NUMPY_AVAILABLE:
            base_namespace.update({
                "np": np,
                "array": np.array,
                "arange": np.arange,
                "linspace": np.linspace,
                "zeros": np.zeros,
                "ones": np.ones,
            })
        
        if SCIPY_AVAILABLE:
            base_namespace.update({
                "sp": sp,
                "linalg": linalg,
                "optimize": optimize,
                "integrate": integrate,
                "stats": stats,
            })
        
        if SYMPY_AVAILABLE:
            base_namespace.update({
                "sym": sym,
                # Core symbolic functions
                "symbols": symbols,
                "Symbol": Symbol,
                "sympify": sympify,
                "parse_expr": parse_expr,
                # Constants
                "I": sympy_I,  # Imaginary unit
                "E": E,  # Euler's number
                "pi": pi,
                "oo": oo,  # Infinity
                "zoo": zoo,  # Complex infinity
                # Algebraic operations (condensing/expanding formulas)
                "expand": expand,
                "factor": factor,
                "simplify": simplify,
                "collect": collect,
                "apart": apart,
                "together": together,
                "cancel": cancel,
                "trigsimp": trigsimp,
                "expand_trig": expand_trig,
                "powsimp": powsimp,
                "expand_log": expand_log,
                "expand_power_base": expand_power_base,
                "expand_power_exp": expand_power_exp,
                "expand_complex": expand_complex,
                # Simplification variants
                "nsimplify": nsimplify,
                "ratsimp": ratsimp,
                "radsimp": radsimp,
                "powdenest": powdenest,
                # Equation solving
                "solve": solve,
                "solveset": solveset,
                "linsolve": linsolve,
                "nonlinsolve": nonlinsolve,
                "solve_poly_system": solve_poly_system,
                # Calculus
                "diff": diff,
                "sym_integrate": sym_integrate,
                "limit": limit,
                "series": series,
                "summation": summation,
                "product": product,
                # Matrix operations
                "Matrix": Matrix,
                "eye": eye,
                "sym_zeros": sym_zeros,
                "sym_ones": sym_ones,
                "diag": diag,
                # Relations
                "Eq": Eq,
                "Ne": Ne,
                "Lt": Lt,
                "Le": Le,
                "Gt": Gt,
                "Ge": Ge,
                # Number theory
                "isprime": isprime,
                "factorint": factorint,
                "divisors": divisors,
                "gcd": gcd,
                "lcm": lcm,
                # Special functions
                "factorial": factorial,
                "binomial": binomial,
                "sqrt": sqrt,
                "cbrt": cbrt,
                "root": root,
                # Printing/display
                "latex": latex,
                "pretty": pretty,
                "pprint": pprint,
            })
        
        self.base_namespace = base_namespace
        self.namespace = self.base_namespace.copy()
        
    def setup_ui(self):
        """Setup the main user interface with new layout including tabs and dock widgets"""
        
        # Setup multi-document tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)
        
        # Create first document tab
        self.create_new_document()
        
        # Setup dock widgets for additional features
        self.setup_dock_widgets()
        
        # Initialize undo/redo stacks for each document
        self.document_undo_stacks = {}
        
        self.line_results = {}
        self.last_text = ""
        self.calculation_timer = None
    
    def setup_dock_widgets(self):
        """Setup dock widgets for additional features"""
        
        # 1. Graph plotting dock
        self.graph_dock = QDockWidget("Graph Plotter", self)
        self.graph_widget = GraphPlotWidget(self)
        self.graph_dock.setWidget(self.graph_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.graph_dock)
        
        # 2. History dock
        self.history_dock = QDockWidget("History", self)
        self.history_widget = HistoryPanel(self)
        self.history_dock.setWidget(self.history_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.history_dock)
        
        # 3. Custom functions dock
        self.functions_dock = QDockWidget("Custom Functions", self)
        self.functions_widget = CustomFunctionLibrary(self)
        self.functions_dock.setWidget(self.functions_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.functions_dock)
        
        # 4. Variable inspector dock
        self.variables_dock = QDockWidget("Variable Inspector", self)
        self.variables_widget = VariableInspector(self)
        self.variables_dock.setWidget(self.variables_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.variables_dock)
        
        # 5. Math function taskbar dock
        self.math_functions_dock = QDockWidget("Math Functions", self)
        self.math_functions_widget = MathFunctionTaskbar(self)
        self.math_functions_dock.setWidget(self.math_functions_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.math_functions_dock)
        self.tabifyDockWidget(self.functions_dock, self.math_functions_dock)
        
        # Tabify left docks
        self.tabifyDockWidget(self.history_dock, self.functions_dock)
        
        # Tabify right docks  
        self.tabifyDockWidget(self.graph_dock, self.variables_dock)
        
        # Set default active tabs
        self.history_dock.raise_()
        self.graph_dock.raise_()
    
    def create_new_document(self, title="Document"):
        """Create a new document tab"""
        # Create document widget
        doc_widget = QWidget()
        doc_layout = QVBoxLayout(doc_widget)
        doc_layout.setContentsMargins(10, 10, 10, 10)
        
        # Custom code editor with line numbers and inline results
        document_editor = CodeEditor()
        document_editor.setPlaceholderText("Type your mathematical expressions here...\nPress Enter at end of line to calculate\nClick anywhere to position cursor")
        document_editor.textChanged.connect(lambda: self.on_text_changed(document_editor))
        document_editor.cursorPositionChanged.connect(lambda: self.on_cursor_changed(document_editor))
        
        # Apply Python syntax highlighting
        highlighter = PythonSyntaxHighlighter(document_editor.document())
        
        doc_layout.addWidget(document_editor)
        
        # Button row
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear Document")
        clear_btn.clicked.connect(lambda: self.clear_current_document())
        
        clear_vars_btn = QPushButton("Clear Variables")
        clear_vars_btn.clicked.connect(self.clear_variables)
        
        recalc_btn = QPushButton("Recalculate All")
        recalc_btn.clicked.connect(lambda: self.recalculate_all(document_editor))
        
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(clear_vars_btn)
        button_layout.addWidget(recalc_btn)
        button_layout.addStretch()
        
        doc_layout.addLayout(button_layout)
        
        # Add tab
        tab_index = self.tab_widget.addTab(doc_widget, title)
        self.tab_widget.setCurrentIndex(tab_index)
        
        # Store editor reference
        doc_widget.editor = document_editor
        doc_widget.highlighter = highlighter
        
        return document_editor
    
    def get_current_editor(self):
        """Get the currently active document editor"""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, 'editor'):
            return current_widget.editor
        return None
    
    def close_tab(self, index):
        """Close a document tab"""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            # Don't close the last tab, just clear it
            current_widget = self.tab_widget.widget(index)
            if current_widget and hasattr(current_widget, 'editor'):
                current_widget.editor.clear()
    
    def clear_current_document(self):
        """Clear the current document"""
        editor = self.get_current_editor()
        if editor:
            editor.clear()
            editor.clear_line_results()
    
    def setup_menu_bar(self):
        """Setup the menu bar with all mathematical functions"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Document", self.new_document, "Ctrl+N")
        file_menu.addAction("Open...", self.open_file, "Ctrl+O")
        
        # Recent files submenu
        self.recent_files_menu = file_menu.addMenu("Recent Files")
        self.update_recent_files_menu()
        
        file_menu.addSeparator()
        file_menu.addAction("Save", self.save_file, "Ctrl+S")
        file_menu.addAction("Save As...", self.save_as_file, "Ctrl+Shift+S")
        file_menu.addSeparator()
        file_menu.addAction("Export Configuration...", self.export_config)
        file_menu.addAction("Import Configuration...", self.import_config)
        file_menu.addSeparator()
        file_menu.addAction("Print...", self.print_document, "Ctrl+P")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close, "Ctrl+Q")
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo", self.undo_action, "Ctrl+Z")
        edit_menu.addAction("Redo", self.redo_action, "Ctrl+Y")
        edit_menu.addSeparator()
        edit_menu.addAction("Settings...", self.open_settings, "Ctrl+,")
        edit_menu.addSeparator()
        edit_menu.addAction("Reset Configuration...", self.reset_config)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Algebra Helper", self.open_algebra_helper)
        tools_menu.addAction("Unit Converter", self.open_unit_converter)
        tools_menu.addAction("Theme Customizer", self.open_theme_customizer)
        tools_menu.addAction("Panel Layout Config", self.open_panel_layout_config)
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("History Panel", lambda: self.history_dock.setVisible(not self.history_dock.isVisible()))
        view_menu.addAction("Functions Panel", lambda: self.functions_dock.setVisible(not self.functions_dock.isVisible()))
        view_menu.addAction("Graph Panel", lambda: self.graph_dock.setVisible(not self.graph_dock.isVisible()))
        view_menu.addAction("Variables Panel", lambda: self.variables_dock.setVisible(not self.variables_dock.isVisible()))
        
        # Mathematical function menus
        self.setup_math_menu(menubar)
        self.setup_random_menu(menubar)
        self.setup_statistics_menu(menubar)
        self.setup_cmath_menu(menubar)
        self.setup_decimal_menu(menubar)
        self.setup_fractions_menu(menubar)
        self.setup_constants_menu(menubar)
        # Add a menu for each library/category with all its functions
        from ..widgets.math_function_taskbar import MATH_FUNCTIONS
        # Only show simple/common libraries in the top bar
        COMMON_LIBS = ["math", "random", "statistics", "cmath", "decimal", "fractions"]
        LIB_GROUPS = {
            "math": [
                ("Trigonometric", ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh"]),
                ("Logarithmic", ["log", "log10", "log1p", "log2", "expm1", "exp"]),
                ("Rounding", ["ceil", "floor", "trunc"]),
                ("Other", None),
            ],
            "random": [
                ("Random Generation", ["random", "randint", "randrange", "choice", "shuffle", "uniform", "gauss", "betavariate", "expovariate", "gammavariate", "lognormvariate", "normalvariate", "paretovariate", "randbytes", "vonmisesvariate", "weibullvariate"]),
                ("Other", None),
            ],
            "statistics": [
                ("Averages", ["mean", "fmean", "geometric_mean", "harmonic_mean", "median", "median_grouped", "median_high", "median_low"]),
                ("Spread", ["pstdev", "pvariance", "stdev", "variance"]),
                ("Other", None),
            ],
            "cmath": [
                ("Trigonometric", ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh"]),
                ("Logarithmic", ["log", "log10", "exp"]),
                ("Other", None),
            ],
        }
        # Example popularity order (replace with actual usage data if available)
        POPULARITY = {
            "math": ["sin", "cos", "tan", "log", "exp", "sqrt", "pow", "ceil", "floor", "abs", "round"],
            "random": ["random", "randint", "choice", "shuffle", "uniform"],
            "statistics": ["mean", "median", "stdev", "variance", "mode"],
            "cmath": ["sin", "cos", "tan", "exp", "log", "sqrt"],
            "decimal": ["Decimal", "getcontext", "setcontext"],
            "fractions": ["Fraction", "from_float", "from_decimal"],
        }
        for category in COMMON_LIBS:
            functions = MATH_FUNCTIONS.get(category, [])
            lib_menu = menubar.addMenu(category)
            groups = LIB_GROUPS.get(category, [(None, None)])
            used = set()
            # Sort functions in each group by popularity
            for group_name, group_funcs in groups:
                if group_funcs:
                    # Sort group_funcs by popularity if available
                    sorted_group = sorted(group_funcs, key=lambda f: (POPULARITY.get(category, []).index(f) if f in POPULARITY.get(category, []) else 9999))
                    for func in sorted_group:
                        if func in functions:
                            action = QAction(func, self)
                            action.triggered.connect(lambda checked, c=category, f=func: self.insert_function(f"{c}.{f}(") )
                            lib_menu.addAction(action)
                            used.add(func)
                    lib_menu.addSeparator()
            # Add remaining functions not in any group, sorted by popularity
            remaining = [func for func in functions if func not in used]
            sorted_remaining = sorted(remaining, key=lambda f: (POPULARITY.get(category, []).index(f) if f in POPULARITY.get(category, []) else 9999))
            for func in sorted_remaining:
                action = QAction(func, self)
                action.triggered.connect(lambda checked, c=category, f=func: self.insert_function(f"{c}.{f}(") )
                lib_menu.addAction(action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Help", self.show_help, "F1")
        help_menu.addAction("About", self.show_about)
    
    # ... (Continue with other methods)
    
    def on_text_changed(self, editor):
        """Handle text changes in a specific editor"""
        # Use a timer to avoid recalculating on every keystroke
        if hasattr(self, 'calculation_timer') and self.calculation_timer:
            self.calculation_timer.stop()
        
        self.calculation_timer = QTimer()
        self.calculation_timer.setSingleShot(True)
        self.calculation_timer.timeout.connect(lambda: self.recalculate_changed_lines(editor))
        self.calculation_timer.start(500)  # Wait 500ms after last keystroke
    
    def on_cursor_changed(self, editor):
        """Handle cursor position changes in a specific editor"""
        cursor = editor.textCursor()
        line_number = cursor.blockNumber()
        self.highlight_current_line_result(line_number)
    
    def recalculate_all(self, editor=None):
        """Recalculate all lines in the document"""
        if editor is None:
            editor = self.get_current_editor()
        if editor:
            self.recalculate_changed_lines(editor)
    
    def recalculate_changed_lines(self, editor):
        """Recalculate lines that have changed for a specific editor"""
        # Reset namespace to the predefined safe defaults before recalculation
        self.namespace = self.base_namespace.copy()
        
        current_text = editor.toPlainText()
        lines = current_text.split('\n')
        
        # Clear variables and recalculate from top
        self.variables.clear()
        self.line_results.clear()
        
        for i, line in enumerate(lines):
            if not line.strip() or line.strip().startswith('#'):
                continue
                
            try:
                # Simple expression evaluation for now
                if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
                    # Variable assignment
                    var_name, expression = line.split('=', 1)
                    var_name = var_name.strip()
                    expression = expression.strip()
                    
                    result = eval(expression, {"__builtins__": {}}, self.namespace)
                    self.variables[var_name] = result
                    self.namespace[var_name] = result
                    self.line_results[i] = f"{var_name} = {self.format_result(result)}"
                else:
                    # Expression evaluation
                    result = eval(line, {"__builtins__": {}}, self.namespace)
                    if result is not None:
                        self.line_results[i] = self.format_result(result)
                        
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.line_results[i] = error_msg
        
        # Update inline results in code editor
        self.update_inline_results(editor)
        self.update_variables_display()
    
    def format_result(self, result):
        """Format calculation result for display"""
        if result is None:
            return "None"
        
        # Handle SymPy types
        if SYMPY_AVAILABLE:
            # Check if it's a SymPy type
            if hasattr(result, '__class__') and hasattr(result.__class__, '__module__'):
                if result.__class__.__module__.startswith('sympy'):
                    # SymPy object - use pretty string representation
                    result_str = str(result)
                    if len(result_str) > 200:
                        return result_str[:200] + "..."
                    return result_str
        
        # Handle different types
        if isinstance(result, bool):
            return str(result)
        elif isinstance(result, (int, float)):
            if isinstance(result, float):
                # Use scientific notation for very large or very small numbers
                if abs(result) > 1e10 or (abs(result) < 1e-4 and result != 0):
                    return f"{result:.{self.decimal_precision}e}"
                else:
                    return f"{result:.{self.decimal_precision}g}"
            else:
                return str(result)
        elif isinstance(result, complex):
            if result.imag == 0:
                return self.format_result(result.real)
            elif result.real == 0:
                return f"{result.imag:.{self.decimal_precision}g}j"
            else:
                return f"({result.real:.{self.decimal_precision}g}{'+' if result.imag >= 0 else ''}{result.imag:.{self.decimal_precision}g}j)"
        else:
            # For other types, just convert to string
            result_str = str(result)
            if len(result_str) > 200:
                return result_str[:200] + "..."
            return result_str
    
    def update_inline_results(self, editor):
        """Update inline results in the specified code editor"""
        # Clear existing line results
        editor.clear_line_results()
        
        # Set results for each line
        for line_num, result in self.line_results.items():
            editor.set_line_result(line_num + 1, result)  # line_num is 0-based, display is 1-based
    
    def update_variables_display(self):
        """Update the variables display in the variable inspector"""
        self.variables_widget.update_variables(self.variables)
    
    # Additional menu setup methods would go here...
    def setup_math_menu(self, menubar):
        """Setup the Math Functions menu"""
        math_menu = menubar.addMenu("Math")
        
        # Add trig functions submenu
        trig_menu = math_menu.addMenu("Trigonometric")
        trig_functions = [
            ("sin(x)", "math.sin("),
            ("cos(x)", "math.cos("),
            ("tan(x)", "math.tan("),
            ("asin(x)", "math.asin("),
            ("acos(x)", "math.acos("),
            ("atan(x)", "math.atan("),
        ]
        for name, func in trig_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            trig_menu.addAction(action)
    
    def setup_random_menu(self, menubar):
        """Setup the Random menu"""
        random_menu = menubar.addMenu("Random")
        random_functions = [
            ("random()", "random.random()"),
            ("randint(a, b)", "random.randint("),
            ("randrange(start, stop)", "random.randrange("),
            ("choice(seq)", "random.choice("),
            ("shuffle(list)", "random.shuffle("),
            ("uniform(a, b)", "random.uniform("),
            ("gauss(mu, sigma)", "random.gauss("),
        ]
        for name, func in random_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            random_menu.addAction(action)
    
    def setup_statistics_menu(self, menubar):
        """Setup the Statistics menu"""
        stats_menu = menubar.addMenu("Statistics")
        
        # Basic statistics
        basic_stats = [
            ("mean(data)", "statistics.mean("),
            ("median(data)", "statistics.median("),
            ("mode(data)", "statistics.mode("),
            ("stdev(data)", "statistics.stdev("),
            ("variance(data)", "statistics.variance("),
        ]
        for name, func in basic_stats:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            stats_menu.addAction(action)
    
    def setup_cmath_menu(self, menubar):
        """Setup the Complex Math menu"""
        cmath_menu = menubar.addMenu("Complex Math")
        
        cmath_functions = [
            ("phase(z)", "cmath.phase("),
            ("polar(z)", "cmath.polar("),
            ("rect(r, phi)", "cmath.rect("),
            ("exp(z)", "cmath.exp("),
            ("log(z)", "cmath.log("),
            ("sqrt(z)", "cmath.sqrt("),
            ("sin(z)", "cmath.sin("),
            ("cos(z)", "cmath.cos("),
            ("tan(z)", "cmath.tan("),
        ]
        for name, func in cmath_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            cmath_menu.addAction(action)
    
    def setup_decimal_menu(self, menubar):
        """Setup the Decimal menu"""
        decimal_menu = menubar.addMenu("Decimal")
        
        decimal_functions = [
            ("Decimal(value)", "decimal.Decimal("),
            ("getcontext()", "decimal.getcontext()"),
            ("setcontext(ctx)", "decimal.setcontext("),
        ]
        for name, func in decimal_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            decimal_menu.addAction(action)
    
    def setup_fractions_menu(self, menubar):
        """Setup the Fractions menu"""
        fractions_menu = menubar.addMenu("Fractions")
        
        fraction_functions = [
            ("Fraction(numerator, denominator)", "fractions.Fraction("),
            ("Fraction.from_float(value)", "fractions.Fraction.from_float("),
            ("Fraction.from_decimal(value)", "fractions.Fraction.from_decimal("),
        ]
        for name, func in fraction_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            fractions_menu.addAction(action)
    
    def setup_constants_menu(self, menubar):
        """Setup the Constants menu"""
        constants_menu = menubar.addMenu("Constants")
        
        constants = [
            ("π (pi)", "math.pi"),
            ("e (Euler's number)", "math.e"),
            ("τ (tau)", "math.tau"),
            ("∞ (infinity)", "math.inf"),
            ("NaN", "math.nan"),
        ]
        for name, const in constants:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, c=const: self.insert_function(c))
            constants_menu.addAction(action)
    
    def setup_toolbar(self): pass
    
    # File operations
    def new_document(self): 
        """Create a new document tab"""
        tab_count = self.tab_widget.count()
        title = f"Document {tab_count + 1}"
        self.create_new_document(title)
    
    def open_file(self):
        """Open a calculation file"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open File",
            "",
            "Calculation Files (*.calc);;Text Files (*.txt);;All Files (*)"
        )
        if filepath:
            self.open_recent_file(filepath)
    
    def save_file(self):
        """Save current document"""
        editor = self.get_current_editor()
        if editor:
            current_tab_index = self.tab_widget.currentIndex()
            tab_title = self.tab_widget.tabText(current_tab_index)
            
            # Check if file has been saved before
            if hasattr(editor, 'filepath') and editor.filepath:
                filepath = editor.filepath
            else:
                # Show save as dialog
                self.save_as_file()
                return
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())
                
                # Update tab title to remove asterisk if modified
                self.tab_widget.setTabText(current_tab_index, os.path.basename(filepath))
                
                # Update recent files
                if filepath not in self.recent_files:
                    self.recent_files.insert(0, filepath)
                    self.recent_files = self.recent_files[:10]
                    self.config_manager.save_recent_files(self.recent_files)
                    self.update_recent_files_menu()
                
            except Exception as e:
                QMessageBox.warning(self, "Save Error", f"Failed to save file: {e}")
    
    def save_as_file(self):
        """Save current document with a new name"""
        editor = self.get_current_editor()
        if editor:
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Save As",
                "",
                "Calculation Files (*.calc);;Text Files (*.txt);;All Files (*)"
            )
            if filepath:
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(editor.toPlainText())
                    
                    # Store filepath in editor
                    editor.filepath = filepath
                    
                    # Update tab title
                    current_tab_index = self.tab_widget.currentIndex()
                    self.tab_widget.setTabText(current_tab_index, os.path.basename(filepath))
                    
                    # Update recent files
                    if filepath not in self.recent_files:
                        self.recent_files.insert(0, filepath)
                        self.recent_files = self.recent_files[:10]
                        self.config_manager.save_recent_files(self.recent_files)
                        self.update_recent_files_menu()
                    
                except Exception as e:
                    QMessageBox.warning(self, "Save Error", f"Failed to save file: {e}")
    
    def print_document(self):
        """Print current document"""
        editor = self.get_current_editor()
        if editor:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                editor.document().print(printer)
    
    # Edit operations
    def undo_action(self):
        """Undo last edit"""
        editor = self.get_current_editor()
        if editor:
            editor.undo()
    
    def redo_action(self):
        """Redo last undone edit"""
        editor = self.get_current_editor()
        if editor:
            editor.redo()
    
    # Tool operations
    def open_algebra_helper(self):
        """Open algebra helper dialog"""
        dialog = AlgebraHelperDialog(self)
        dialog.show()
    
    def open_unit_converter(self):
        """Open unit converter dialog"""
        dialog = UnitConverterDialog(self)
        dialog.exec()
    
    def open_theme_customizer(self):
        """Open theme customizer dialog"""
        dialog = ThemeCustomizer(self)
        dialog.exec()
    
    def open_panel_layout_config(self):
        """Open panel layout configuration dialog"""
        QMessageBox.information(
            self, 
            "Panel Layout", 
            "You can drag and drop dock panels to rearrange them.\n"
            "Right-click on panel title bars for more options.\n"
            "Your layout will be saved automatically."
        )
    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self)
        dialog.exec()
    
    # Utility methods
    def insert_function(self, function_text):
        """Insert function or constant into current editor"""
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.insertText(function_text)
            editor.setFocus()
    
    def insert_function_with_shift_support(self, function_text, category=None, func_name=None):
        """Insert function or create example document based on shift key state"""
        # Check if shift key is pressed
        modifiers = QApplication.keyboardModifiers()
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            # Shift is pressed - create new document with example
            self.create_function_example_document(function_text, category, func_name)
        else:
            # No shift - insert at cursor
            self.insert_function(function_text)
    
    def create_function_example_document(self, function_text, category=None, func_name=None):
        """Create a new document with an example of how to use the function"""
        # Generate example content based on the function
        example_content = self.generate_function_example(function_text, category, func_name)
        
        # Create new document
        title = f"Example: {func_name or function_text}"
        editor = self.create_new_document(title)
        editor.setPlainText(example_content)
    
    def generate_function_example(self, function_text, category=None, func_name=None):
        """Generate example code for a function"""
        # Dictionary of function examples
        examples = {
            # Math functions
            "math.sin": "# Sine function - calculates sin(x) where x is in radians\nimport math\n\n# Basic usage\nangle_rad = math.pi / 4  # 45 degrees in radians\nresult = math.sin(angle_rad)\nprint(f\"sin(π/4) = {result}\")  # ≈ 0.707\n\n# Convert degrees to radians first\nangle_deg = 45\nangle_rad = math.radians(angle_deg)\nresult = math.sin(angle_rad)\n\n# Common angles\nmath.sin(0)         # 0\nmath.sin(math.pi/6) # 0.5 (30°)\nmath.sin(math.pi/4) # √2/2 ≈ 0.707 (45°)\nmath.sin(math.pi/2) # 1 (90°)",
            
            "math.cos": "# Cosine function - calculates cos(x) where x is in radians\nimport math\n\n# Basic usage\nangle_rad = math.pi / 3  # 60 degrees\nresult = math.cos(angle_rad)\nprint(f\"cos(π/3) = {result}\")  # 0.5\n\n# Convert degrees to radians\nangle_deg = 60\nresult = math.cos(math.radians(angle_deg))\n\n# Common angles\nmath.cos(0)         # 1\nmath.cos(math.pi/4) # √2/2 ≈ 0.707 (45°)\nmath.cos(math.pi/2) # 0 (90°)\nmath.cos(math.pi)   # -1 (180°)",
            
            "math.tan": "# Tangent function - calculates tan(x) where x is in radians\nimport math\n\n# Basic usage\nangle_rad = math.pi / 4  # 45 degrees\nresult = math.tan(angle_rad)\nprint(f\"tan(π/4) = {result}\")  # 1.0\n\n# Tangent of common angles\nmath.tan(0)         # 0\nmath.tan(math.pi/4) # 1 (45°)\nmath.tan(math.pi/6) # ≈ 0.577 (30°)\n\n# Note: tan(π/2) is undefined (approaches infinity)",
            
            "math.sqrt": "# Square root function\nimport math\n\n# Basic usage\nresult = math.sqrt(16)\nprint(f\"√16 = {result}\")  # 4.0\n\n# More examples\nmath.sqrt(2)    # ≈ 1.414\nmath.sqrt(100)  # 10.0\nmath.sqrt(0.25) # 0.5\n\n# For negative numbers, use cmath\nimport cmath\nresult = cmath.sqrt(-4)  # 2j (imaginary)",
            
            "math.log": "# Natural logarithm (base e)\nimport math\n\n# Basic usage\nresult = math.log(math.e)\nprint(f\"ln(e) = {result}\")  # 1.0\n\n# Log of different values\nmath.log(1)     # 0\nmath.log(10)    # ≈ 2.303\nmath.log(100)   # ≈ 4.605\n\n# Log with different base\nmath.log(100, 10)  # log base 10: 2.0\nmath.log(8, 2)     # log base 2: 3.0",
            
            "math.exp": "# Exponential function (e^x)\nimport math\n\n# Basic usage\nresult = math.exp(1)\nprint(f\"e^1 = {result}\")  # ≈ 2.718\n\n# More examples\nmath.exp(0)   # 1\nmath.exp(2)   # ≈ 7.389\nmath.exp(-1)  # ≈ 0.368\n\n# Useful for growth/decay calculations\ninitial = 100\nrate = 0.05  # 5% growth\ntime = 10\nfinal = initial * math.exp(rate * time)",
            
            "math.pow": "# Power function\nimport math\n\n# Basic usage\nresult = math.pow(2, 3)\nprint(f\"2^3 = {result}\")  # 8.0\n\n# More examples\nmath.pow(10, 2)    # 100.0\nmath.pow(2, 0.5)   # √2 ≈ 1.414\nmath.pow(27, 1/3)  # cube root: 3.0\n\n# Alternative: use ** operator\n2 ** 3      # 8\n10 ** -2    # 0.01",
            
            "random.random": "# Generate random float between 0.0 and 1.0\nimport random\n\n# Basic usage\nresult = random.random()\nprint(f\"Random: {result}\")  # e.g., 0.574839\n\n# Generate multiple random numbers\nfor i in range(5):\n    print(random.random())\n\n# Scale to different range\n# Random between 0 and 10\nrandom.random() * 10\n\n# Random between 5 and 15\nrandom.random() * 10 + 5",
            
            "random.randint": "# Generate random integer in range [a, b] (inclusive)\nimport random\n\n# Basic usage - dice roll\nresult = random.randint(1, 6)\nprint(f\"Dice roll: {result}\")\n\n# Random year\nrandom.randint(1900, 2024)\n\n# Random percentage\nrandom.randint(0, 100)\n\n# Simulate 10 dice rolls\nfor i in range(10):\n    print(random.randint(1, 6))",
            
            "random.choice": "# Choose random element from a sequence\nimport random\n\n# Basic usage\ncolors = ['red', 'green', 'blue', 'yellow']\nresult = random.choice(colors)\nprint(f\"Chosen: {result}\")\n\n# More examples\nrandom.choice([1, 2, 3, 4, 5])\nrandom.choice('ABCDEFG')\n\n# Pick random element multiple times\nfor i in range(5):\n    print(random.choice(colors))",
            
            "statistics.mean": "# Calculate arithmetic mean (average)\nimport statistics\n\n# Basic usage\ndata = [1, 2, 3, 4, 5]\nresult = statistics.mean(data)\nprint(f\"Mean: {result}\")  # 3.0\n\n# More examples\nstatistics.mean([10, 20, 30, 40])  # 25.0\nstatistics.mean([2.5, 3.5, 4.5])   # 3.5\n\n# Test scores\nscores = [85, 92, 78, 90, 88]\naverage = statistics.mean(scores)\nprint(f\"Average score: {average}\")",
            
            "statistics.median": "# Calculate median (middle value)\nimport statistics\n\n# Basic usage\ndata = [1, 3, 5, 7, 9]\nresult = statistics.median(data)\nprint(f\"Median: {result}\")  # 5\n\n# Even number of values (average of middle two)\ndata = [1, 2, 3, 4]\nstatistics.median(data)  # 2.5\n\n# Median is less affected by outliers\nstatistics.median([1, 2, 3, 100])  # 2.5\nstatistics.mean([1, 2, 3, 100])    # 26.5",
            
            "statistics.stdev": "# Calculate standard deviation (sample)\nimport statistics\n\n# Basic usage\ndata = [2, 4, 4, 4, 5, 5, 7, 9]\nresult = statistics.stdev(data)\nprint(f\"Std Dev: {result}\")  # ≈ 2.14\n\n# More examples\nstatistics.stdev([1, 1, 1, 1])      # 0.0 (no variation)\nstatistics.stdev([1, 5, 1, 5])      # High variation\n\n# Test score consistency\nscores_a = [85, 86, 84, 87, 85]  # Consistent\nscores_b = [70, 95, 60, 100, 72] # Variable\nprint(f\"A: {statistics.stdev(scores_a)}\")\nprint(f\"B: {statistics.stdev(scores_b)}\")",
        }
        
        # If we have a specific example, use it
        full_func_key = f"{category}.{func_name}" if category and func_name else function_text.rstrip("(")
        if full_func_key in examples:
            return examples[full_func_key]
        
        # Generate generic example based on category
        if category == "math":
            return f"# Example: {function_text}\nimport math\n\n# Basic usage\nresult = {function_text})\nprint(result)\n\n# Try different values:\n# {function_text})"
        elif category == "random":
            return f"# Example: {function_text}\nimport random\n\n# Generate random values\nfor i in range(5):\n    result = {function_text})\n    print(f\"Random {{i+1}}: {{result}}\")"
        elif category == "statistics":
            return f"# Example: {function_text}\nimport statistics\n\n# Sample data\ndata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nresult = {function_text}data)\nprint(f\"Result: {{result}}\")"
        elif category == "cmath":
            return f"# Example: {function_text} (Complex Math)\nimport cmath\n\n# Complex number examples\nz = 3 + 4j  # Complex number\nresult = {function_text}z)\nprint(f\"Result: {{result}}\")\n\n# Try with different complex numbers\n# {function_text}1+2j)"
        elif category == "decimal":
            return f"# Example: {function_text}\nimport decimal\nfrom decimal import Decimal\n\n# High precision arithmetic\nresult = {function_text})\nprint(result)"
        elif category == "fractions":
            return f"# Example: {function_text}\nimport fractions\nfrom fractions import Fraction\n\n# Exact rational arithmetic\nresult = {function_text})\nprint(result)"
        else:
            # Generic example
            return f"# Example: {function_text}\n\n# Basic usage:\nresult = {function_text})\nprint(result)\n\n# Modify the parameters above and press Enter to calculate"
    
    def insert_at_cursor(self, text):
        """Insert text at cursor position (alias for insert_function)"""
        self.insert_function(text)
    
    def clear_variables(self):
        """Clear all variables"""
        self.variables.clear()
        self.namespace = self.base_namespace.copy()
        self.variables_widget.update_variables({})
        # Clear line results and recalculate
        editor = self.get_current_editor()
        if editor:
            self.recalculate_all(editor)
    
    def get_current_variables(self):
        """Get current variables for variable inspector"""
        return self.variables.copy()
    
    def delete_variable(self, var_name):
        """Delete a variable"""
        if var_name in self.variables:
            del self.variables[var_name]
            if var_name in self.namespace:
                del self.namespace[var_name]
            self.recalculate_all()
    
    def edit_variable(self, var_name, new_value_str):
        """Edit a variable value"""
        try:
            # Try to evaluate the new value
            new_value = eval(new_value_str, {"__builtins__": {}}, self.base_namespace)
            self.variables[var_name] = new_value
            self.namespace[var_name] = new_value
            self.recalculate_all()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid value: {e}")
    
    def restore_from_history(self, expression):
        """Restore calculation from history"""
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.insertText(expression + "\n")
            editor.setFocus()
    
    def insert_conversion_result(self, result):
        """Insert conversion result into current editor"""
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.insertText(result)
            editor.setFocus()
    
    def insert_custom_function(self, name, code):
        """Insert custom function into current editor"""
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.insertText(f"{name}(")
            editor.setFocus()
    
    def apply_custom_theme(self, theme_data):
        """Apply custom theme from theme customizer"""
        try:
            colors = theme_data['colors']
            font = theme_data['font']
            font_size = theme_data['font_size']
            
            # Update current settings
            self.text_font = font
            self.text_font.setPointSize(font_size)
            self.bg_color = colors['bg']
            self.text_color = colors['text']
            
            # Apply styling
            self.apply_styling()
            
        except Exception as e:
            print(f"Error applying custom theme: {e}")
            QMessageBox.warning(self, "Theme Error", f"Failed to apply theme: {e}")
    
    def highlight_current_line_result(self, line_number):
        """Highlight the result for the current line"""
        # This is a placeholder for highlighting functionality
        pass
    
    def load_panel_configuration(self):
        """Load and apply panel configuration on startup"""
        pass
    
    def save_settings(self):
        """Save current settings"""
        self.settings.setValue("font", self.text_font.toString())
        self.settings.setValue("textColor", self.text_color.name())
        self.settings.setValue("bgColor", self.bg_color.name())
        self.settings.setValue("precision", self.decimal_precision)
        self.settings.setValue("theme", self.theme)
        
    def load_settings(self):
        """Load saved settings"""
        font_str = self.settings.value("font", self.text_font.toString())
        self.text_font.fromString(font_str)
        
        self.text_color = QColor(self.settings.value("textColor", "#000000"))
        self.bg_color = QColor(self.settings.value("bgColor", "#ffffff"))
        self.decimal_precision = int(self.settings.value("precision", 6))
        self.theme = self.settings.value("theme", "Default")
        
        self.apply_styling()
    
    def apply_styling(self):
        """Apply current styling settings to the interface"""
        # Apply styling to all document editors
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if widget and hasattr(widget, 'editor'):
                editor = widget.editor
                editor.setFont(self.text_font)
                
                if self.theme == "dark":
                    editor.setStyleSheet(f"""
                        QPlainTextEdit {{
                            background-color: {self.bg_color.name()};
                            color: {self.text_color.name()};
                            border: none;
                        }}
                    """)
                else:
                    editor.setStyleSheet(f"""
                        QPlainTextEdit {{
                            background-color: {self.bg_color.name()};
                            color: {self.text_color.name()};
                            border: 1px solid #ccc;
                        }}
                    """)
    
    def show_help(self):
        """Show the help dialog"""
        help_dialog = HelpDialog(self)
        help_dialog.exec()
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About", 
                         "Advanced Scientific Calculator v2.0\n"
                         "A powerful calculator with support for Python, NumPy, SciPy, and SymPy\n"
                         "Built with PySide6")
    
    def load_all_config(self):
        """Load all configuration settings"""
        # Load theme configuration
        theme_config = self.config_manager.load_theme_config()
        if theme_config:
            self.apply_loaded_theme(theme_config)
        else:
            # Set default theme
            self.text_font = QFont("Consolas", 12)
            if not self.text_font.exactMatch():
                self.text_font = QFont("Monaco", 12)  # macOS monospace font
                if not self.text_font.exactMatch():
                    self.text_font = QFont("monospace", 12)  # generic fallback
            self.text_color = QColor(212, 212, 212)  # Light text for dark theme
            self.bg_color = QColor(30, 30, 30)  # Dark background
            self.decimal_precision = 6
            self.theme = "dark"
        
        # Load editor configuration
        self.editor_config = self.config_manager.load_editor_config()
        
        # Load calculation configuration
        self.calc_config = self.config_manager.load_calculation_config()
        self.decimal_precision = self.calc_config.get('decimal_precision', 6)
        
        # Load recent files
        self.recent_files = self.config_manager.load_recent_files()
    
    def apply_loaded_theme(self, theme_config):
        """Apply loaded theme configuration"""
        try:
            if 'font' in theme_config:
                self.text_font = theme_config['font']
            else:
                self.text_font = QFont("Consolas", theme_config.get('font_size', 12))
            
            if 'colors' in theme_config:
                colors = theme_config['colors']
                self.text_color = colors.get('text', QColor(212, 212, 212))
                self.bg_color = colors.get('bg', QColor(30, 30, 30))
            
            self.theme = theme_config.get('theme_name', 'dark')
            
        except Exception as e:
            print(f"Error applying theme: {e}")
            # Fall back to defaults
            self.text_font = QFont("Consolas", 12)
            self.text_color = QColor(212, 212, 212)
            self.bg_color = QColor(30, 30, 30)
            self.theme = "dark"
    
    def restore_layout(self):
        """Restore window layout and dock positions"""
        self.config_manager.restore_window_geometry(self)
        self.config_manager.restore_dock_layout(self)
    
    def save_layout(self):
        """Save current window layout and dock positions"""
        self.config_manager.save_window_geometry(self)
        self.config_manager.save_dock_layout(self)
    
    def setup_auto_save(self):
        """Setup auto-save timer for configuration"""
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_config)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
    
    def auto_save_config(self):
        """Auto-save configuration"""
        try:
            self.save_layout()
            # Save custom functions from the functions widget
            if hasattr(self, 'functions_widget'):
                self.config_manager.save_custom_functions(self.functions_widget.functions)
        except Exception as e:
            print(f"Error during auto-save: {e}")
    
    def update_recent_files_menu(self):
        """Update the Recent Files submenu in the File menu"""
        self.recent_files_menu.clear()
        for filepath in self.recent_files:
            action = QAction(os.path.basename(filepath), self)
            action.setToolTip(filepath)
            action.triggered.connect(lambda checked, fp=filepath: self.open_recent_file(fp))
            self.recent_files_menu.addAction(action)
        if not self.recent_files:
            self.recent_files_menu.addAction(QAction("No recent files", self))
    
    def export_config(self):
        """Export configuration to a file"""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Configuration", 
            "calculator_config.json", 
            "JSON Files (*.json)"
        )
        if filepath:
            if self.config_manager.export_config(filepath):
                QMessageBox.information(self, "Export Complete", f"Configuration exported to {filepath}")
            else:
                QMessageBox.warning(self, "Export Error", "Failed to export configuration")
    
    def import_config(self):
        """Import configuration from a file"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Import Configuration",
            "",
            "JSON Files (*.json)"
        )
        if filepath:
            if self.config_manager.import_config(filepath):
                QMessageBox.information(self, "Import Complete", "Configuration imported successfully. Please restart the application for all changes to take effect.")
                # Reload configuration
                self.load_all_config()
                self.apply_styling()
                self.restore_layout()
            else:
                QMessageBox.warning(self, "Import Error", "Failed to import configuration")
    
    def reset_config(self):
        """Reset configuration to defaults"""
        reply = QMessageBox.question(
            self, "Reset Configuration",
            "Are you sure you want to reset all configuration to defaults?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.config_manager.reset_config():
                QMessageBox.information(self, "Reset Complete", "Configuration reset to defaults. Please restart the application.")
                # Reload configuration
                self.load_all_config()
                self.apply_styling()
                self.restore_layout()
            else:
                QMessageBox.warning(self, "Reset Error", "Failed to reset configuration")
    
    def open_recent_file(self, filepath):
        """Open a file from the recent files list"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create new document with the file content
                editor = self.create_new_document(os.path.basename(filepath))
                editor.setPlainText(content)
                
                # Update recent files
                if filepath in self.recent_files:
                    self.recent_files.remove(filepath)
                self.recent_files.insert(0, filepath)
                self.recent_files = self.recent_files[:10]  # Keep only last 10
                self.config_manager.save_recent_files(self.recent_files)
                self.update_recent_files_menu()
                
            except Exception as e:
                QMessageBox.warning(self, "Open Error", f"Failed to open file: {e}")
        else:
            QMessageBox.warning(self, "File Not Found", f"File not found: {filepath}")
            # Remove from recent files
            if filepath in self.recent_files:
                self.recent_files.remove(filepath)
                self.config_manager.save_recent_files(self.recent_files)
                self.update_recent_files_menu()
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Save configuration and layout
        self.save_layout()
        if hasattr(self, 'functions_widget'):
            self.config_manager.save_custom_functions(self.functions_widget.functions)
        event.accept()
