"""
Algebra Helper Dialog for symbolic manipulation and equation solving
"""

from ..core.imports import *

class AlgebraHelperDialog(QDialog):
    """Dialog for algebra operations with symbolic variables"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Algebra Helper")
        self.setModal(False)
        self.setMinimumSize(700, 600)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the algebra helper interface"""
        layout = QVBoxLayout(self)
        
        # Create tab widget for different algebra operations
        self.tabs = QTabWidget()
        
        # Tab 1: Symbolic Variables
        self.setup_variables_tab()
        
        # Tab 2: Expression Manipulation
        self.setup_manipulation_tab()
        
        # Tab 3: Equation Solving
        self.setup_solving_tab()
        
        # Tab 4: Quick Reference
        self.setup_reference_tab()
        
        layout.addWidget(self.tabs)
        
        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.close)
        layout.addWidget(button_box)
        
    def setup_variables_tab(self):
        """Setup tab for creating symbolic variables"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Info label
        info = QLabel("Create symbolic variables for algebraic manipulation:")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Variable creation section
        var_group = QGroupBox("Create Symbolic Variables")
        var_layout = QVBoxLayout()
        
        # Single variable
        single_layout = QHBoxLayout()
        single_layout.addWidget(QLabel("Single variable:"))
        self.single_var_input = QLineEdit()
        self.single_var_input.setPlaceholderText("e.g., x")
        single_layout.addWidget(self.single_var_input)
        create_single_btn = QPushButton("Create")
        create_single_btn.clicked.connect(self.create_single_variable)
        single_layout.addWidget(create_single_btn)
        var_layout.addLayout(single_layout)
        
        # Multiple variables
        multi_layout = QHBoxLayout()
        multi_layout.addWidget(QLabel("Multiple variables:"))
        self.multi_var_input = QLineEdit()
        self.multi_var_input.setPlaceholderText("e.g., x y z or a,b,c")
        multi_layout.addWidget(self.multi_var_input)
        create_multi_btn = QPushButton("Create")
        create_multi_btn.clicked.connect(self.create_multiple_variables)
        multi_layout.addWidget(create_multi_btn)
        var_layout.addLayout(multi_layout)
        
        # Imaginary/Complex variables
        complex_layout = QHBoxLayout()
        complex_layout.addWidget(QLabel("Complex variables:"))
        self.complex_var_input = QLineEdit()
        self.complex_var_input.setPlaceholderText("e.g., z1 z2")
        complex_layout.addWidget(self.complex_var_input)
        self.complex_var_checkbox = QCheckBox("Real")
        complex_layout.addWidget(self.complex_var_checkbox)
        create_complex_btn = QPushButton("Create")
        create_complex_btn.clicked.connect(self.create_complex_variables)
        complex_layout.addWidget(create_complex_btn)
        var_layout.addLayout(complex_layout)
        
        var_group.setLayout(var_layout)
        layout.addWidget(var_group)
        
        # Output area
        self.var_output = QTextEdit()
        self.var_output.setReadOnly(True)
        self.var_output.setMaximumHeight(150)
        layout.addWidget(QLabel("Command to copy:"))
        layout.addWidget(self.var_output)
        
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.var_output.toPlainText()))
        layout.addWidget(copy_btn)
        
        layout.addStretch()
        
        self.tabs.addTab(tab, "Variables")
        
    def setup_manipulation_tab(self):
        """Setup tab for expression manipulation"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Info
        info = QLabel("Manipulate and simplify algebraic expressions:")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Expression input
        expr_layout = QHBoxLayout()
        expr_layout.addWidget(QLabel("Expression:"))
        self.expr_input = QLineEdit()
        self.expr_input.setPlaceholderText("e.g., (x + y)**2 or x**2 + 2*x*y + y**2")
        expr_layout.addWidget(self.expr_input)
        layout.addLayout(expr_layout)
        
        # Operations grid
        ops_group = QGroupBox("Operations")
        ops_layout = QVBoxLayout()
        
        # Row 1: Basic operations
        row1 = QHBoxLayout()
        expand_btn = QPushButton("Expand")
        expand_btn.clicked.connect(lambda: self.apply_operation("expand"))
        row1.addWidget(expand_btn)
        
        factor_btn = QPushButton("Factor")
        factor_btn.clicked.connect(lambda: self.apply_operation("factor"))
        row1.addWidget(factor_btn)
        
        simplify_btn = QPushButton("Simplify")
        simplify_btn.clicked.connect(lambda: self.apply_operation("simplify"))
        row1.addWidget(simplify_btn)
        ops_layout.addLayout(row1)
        
        # Row 2: Advanced simplification
        row2 = QHBoxLayout()
        collect_btn = QPushButton("Collect Terms")
        collect_btn.clicked.connect(lambda: self.apply_operation("collect"))
        row2.addWidget(collect_btn)
        
        together_btn = QPushButton("Together")
        together_btn.clicked.connect(lambda: self.apply_operation("together"))
        row2.addWidget(together_btn)
        
        apart_btn = QPushButton("Apart")
        apart_btn.clicked.connect(lambda: self.apply_operation("apart"))
        row2.addWidget(apart_btn)
        ops_layout.addLayout(row2)
        
        # Row 3: Trigonometric
        row3 = QHBoxLayout()
        trigsimp_btn = QPushButton("Trig Simplify")
        trigsimp_btn.clicked.connect(lambda: self.apply_operation("trigsimp"))
        row3.addWidget(trigsimp_btn)
        
        expand_trig_btn = QPushButton("Expand Trig")
        expand_trig_btn.clicked.connect(lambda: self.apply_operation("expand_trig"))
        row3.addWidget(expand_trig_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(lambda: self.apply_operation("cancel"))
        row3.addWidget(cancel_btn)
        ops_layout.addLayout(row3)
        
        # Row 4: Power and log
        row4 = QHBoxLayout()
        powsimp_btn = QPushButton("Power Simplify")
        powsimp_btn.clicked.connect(lambda: self.apply_operation("powsimp"))
        row4.addWidget(powsimp_btn)
        
        expand_log_btn = QPushButton("Expand Log")
        expand_log_btn.clicked.connect(lambda: self.apply_operation("expand_log"))
        row4.addWidget(expand_log_btn)
        
        ratsimp_btn = QPushButton("Rational Simplify")
        ratsimp_btn.clicked.connect(lambda: self.apply_operation("ratsimp"))
        row4.addWidget(ratsimp_btn)
        ops_layout.addLayout(row4)
        
        ops_group.setLayout(ops_layout)
        layout.addWidget(ops_group)
        
        # Collect variable input (for collect operation)
        collect_layout = QHBoxLayout()
        collect_layout.addWidget(QLabel("Variable to collect:"))
        self.collect_var_input = QLineEdit()
        self.collect_var_input.setPlaceholderText("e.g., x (for collect operation)")
        collect_layout.addWidget(self.collect_var_input)
        layout.addLayout(collect_layout)
        
        # Output
        self.manip_output = QTextEdit()
        self.manip_output.setReadOnly(True)
        self.manip_output.setMaximumHeight(120)
        layout.addWidget(QLabel("Result:"))
        layout.addWidget(self.manip_output)
        
        copy_manip_btn = QPushButton("Copy to Clipboard")
        copy_manip_btn.clicked.connect(lambda: self.copy_to_clipboard(self.manip_output.toPlainText()))
        layout.addWidget(copy_manip_btn)
        
        layout.addStretch()
        
        self.tabs.addTab(tab, "Manipulation")
        
    def setup_solving_tab(self):
        """Setup tab for equation solving"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Info
        info = QLabel("Solve equations and systems of equations:")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Equation input
        eq_group = QGroupBox("Equation(s)")
        eq_layout = QVBoxLayout()
        
        eq_input_layout = QHBoxLayout()
        eq_input_layout.addWidget(QLabel("Equation:"))
        self.eq_input = QLineEdit()
        self.eq_input.setPlaceholderText("e.g., x**2 - 4 or Eq(x**2, 4)")
        eq_input_layout.addWidget(self.eq_input)
        eq_layout.addLayout(eq_input_layout)
        
        # Additional equations for system
        self.eq_list = QListWidget()
        self.eq_list.setMaximumHeight(100)
        eq_layout.addWidget(QLabel("System of equations (one per line):"))
        eq_layout.addWidget(self.eq_list)
        
        eq_btn_layout = QHBoxLayout()
        add_eq_btn = QPushButton("Add Equation")
        add_eq_btn.clicked.connect(self.add_equation)
        eq_btn_layout.addWidget(add_eq_btn)
        
        clear_eq_btn = QPushButton("Clear List")
        clear_eq_btn.clicked.connect(self.eq_list.clear)
        eq_btn_layout.addWidget(clear_eq_btn)
        eq_layout.addLayout(eq_btn_layout)
        
        eq_group.setLayout(eq_layout)
        layout.addWidget(eq_group)
        
        # Variables to solve for
        var_layout = QHBoxLayout()
        var_layout.addWidget(QLabel("Variables to solve:"))
        self.solve_vars_input = QLineEdit()
        self.solve_vars_input.setPlaceholderText("e.g., x or x,y,z")
        var_layout.addWidget(self.solve_vars_input)
        layout.addLayout(var_layout)
        
        # Solve buttons
        solve_btn_layout = QHBoxLayout()
        
        solve_btn = QPushButton("Solve")
        solve_btn.clicked.connect(lambda: self.solve_equations("solve"))
        solve_btn_layout.addWidget(solve_btn)
        
        solveset_btn = QPushButton("Solve Set")
        solveset_btn.clicked.connect(lambda: self.solve_equations("solveset"))
        solve_btn_layout.addWidget(solveset_btn)
        
        linsolve_btn = QPushButton("Linear Solve")
        linsolve_btn.clicked.connect(lambda: self.solve_equations("linsolve"))
        solve_btn_layout.addWidget(linsolve_btn)
        
        layout.addLayout(solve_btn_layout)
        
        # Output
        self.solve_output = QTextEdit()
        self.solve_output.setReadOnly(True)
        self.solve_output.setMaximumHeight(150)
        layout.addWidget(QLabel("Solution:"))
        layout.addWidget(self.solve_output)
        
        copy_solve_btn = QPushButton("Copy to Clipboard")
        copy_solve_btn.clicked.connect(lambda: self.copy_to_clipboard(self.solve_output.toPlainText()))
        layout.addWidget(copy_solve_btn)
        
        layout.addStretch()
        
        self.tabs.addTab(tab, "Equation Solving")
        
    def setup_reference_tab(self):
        """Setup quick reference tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        ref_text = QTextBrowser()
        ref_text.setOpenExternalLinks(False)
        
        reference_content = """
        <h3>Algebra Helper Quick Reference</h3>
        
        <h4>Creating Symbolic Variables</h4>
        <ul>
            <li><b>Single variable:</b> <code>x = symbols('x')</code></li>
            <li><b>Multiple variables:</b> <code>x, y, z = symbols('x y z')</code></li>
            <li><b>Complex variables:</b> <code>z = symbols('z', complex=True)</code></li>
            <li><b>Real variables:</b> <code>x = symbols('x', real=True)</code></li>
            <li><b>Imaginary unit:</b> Use <code>I</code> (already available)</li>
        </ul>
        
        <h4>Expression Manipulation</h4>
        <ul>
            <li><b>expand():</b> Expand algebraic expressions: <code>expand((x+y)**2)</code> → x² + 2xy + y²</li>
            <li><b>factor():</b> Factor expressions: <code>factor(x**2 + 2*x + 1)</code> → (x+1)²</li>
            <li><b>simplify():</b> General simplification: <code>simplify((x**2 - 1)/(x - 1))</code> → x+1</li>
            <li><b>collect():</b> Collect terms: <code>collect(x*y + x - 3 + 2*x**2, x)</code></li>
            <li><b>together():</b> Combine fractions: <code>together(1/x + 1/y)</code></li>
            <li><b>apart():</b> Partial fractions: <code>apart(1/(x**2 - 1))</code></li>
            <li><b>cancel():</b> Cancel common factors: <code>cancel((x**2-1)/(x-1))</code></li>
        </ul>
        
        <h4>Equation Solving</h4>
        <ul>
            <li><b>solve():</b> General equation solver: <code>solve(x**2 - 4, x)</code> → [-2, 2]</li>
            <li><b>solveset():</b> Modern solver returning sets: <code>solveset(x**2 - 4, x)</code></li>
            <li><b>System of equations:</b> <code>solve([x + y - 5, x - y - 1], [x, y])</code></li>
            <li><b>Using Eq():</b> <code>solve(Eq(x**2, 4), x)</code></li>
        </ul>
        
        <h4>Working with Imaginary/Complex Numbers</h4>
        <ul>
            <li><b>Imaginary unit:</b> <code>I</code> (sympy's imaginary unit)</li>
            <li><b>Complex expressions:</b> <code>expand((x + I*y)**2)</code></li>
            <li><b>Separate real/imaginary:</b> <code>re(expr)</code>, <code>im(expr)</code></li>
            <li><b>Complex conjugate:</b> <code>conjugate(x + I*y)</code></li>
            <li><b>Expand complex:</b> <code>expand_complex(expr)</code></li>
        </ul>
        
        <h4>Examples</h4>
        <pre>
# Create symbolic variables
x, y, z = symbols('x y z')

# Expand a formula
expand((x + y + z)**2)
# Result: x² + 2xy + 2xz + y² + 2yz + z²

# Factor back
factor(x**2 + 2*x*y + 2*x*z + y**2 + 2*y*z + z**2)
# Result: (x + y + z)²

# Solve with imaginary solutions
solve(x**2 + 1, x)
# Result: [-I, I]

# Work with multiple imaginary variables
z1, z2 = symbols('z1 z2', complex=True)
expr = (z1 + z2)*(z1 - z2)
expand(expr)
# Result: z1² - z2²
        </pre>
        """
        
        ref_text.setHtml(reference_content)
        layout.addWidget(ref_text)
        
        self.tabs.addTab(tab, "Reference")
    
    def create_single_variable(self):
        """Create a single symbolic variable"""
        var_name = self.single_var_input.text().strip()
        if not var_name:
            self.var_output.setText("Please enter a variable name")
            return
        
        command = f"{var_name} = symbols('{var_name}')"
        self.var_output.setText(command)
        
        if self.parent:
            self.parent.insert_at_cursor(command)
    
    def create_multiple_variables(self):
        """Create multiple symbolic variables"""
        var_text = self.multi_var_input.text().strip()
        if not var_text:
            self.var_output.setText("Please enter variable names")
            return
        
        # Handle both space and comma separated
        vars_list = var_text.replace(',', ' ').split()
        vars_str = ' '.join(vars_list)
        vars_joined = ', '.join(vars_list)
        
        command = f"{vars_joined} = symbols('{vars_str}')"
        self.var_output.setText(command)
        
        if self.parent:
            self.parent.insert_at_cursor(command)
    
    def create_complex_variables(self):
        """Create complex/imaginary symbolic variables"""
        var_text = self.complex_var_input.text().strip()
        if not var_text:
            self.var_output.setText("Please enter variable names")
            return
        
        vars_list = var_text.replace(',', ' ').split()
        vars_str = ' '.join(vars_list)
        vars_joined = ', '.join(vars_list)
        
        is_real = self.complex_var_checkbox.isChecked()
        assumption = "real=True" if is_real else "complex=True"
        
        command = f"{vars_joined} = symbols('{vars_str}', {assumption})"
        self.var_output.setText(command)
        
        if self.parent:
            self.parent.insert_at_cursor(command)
    
    def apply_operation(self, operation):
        """Apply an operation to the expression"""
        expr_text = self.expr_input.text().strip()
        if not expr_text:
            self.manip_output.setText("Please enter an expression")
            return
        
        try:
            if not SYMPY_AVAILABLE:
                self.manip_output.setText("SymPy is not available")
                return
            
            # Parse the expression
            expr = sympify(expr_text)
            
            # Apply operation
            if operation == "collect":
                collect_var = self.collect_var_input.text().strip()
                if not collect_var:
                    self.manip_output.setText("Please specify a variable to collect")
                    return
                var_sym = symbols(collect_var)
                result = collect(expr, var_sym)
            elif operation == "expand":
                result = expand(expr)
            elif operation == "factor":
                result = factor(expr)
            elif operation == "simplify":
                result = simplify(expr)
            elif operation == "together":
                result = together(expr)
            elif operation == "apart":
                result = apart(expr)
            elif operation == "cancel":
                result = cancel(expr)
            elif operation == "trigsimp":
                result = trigsimp(expr)
            elif operation == "expand_trig":
                result = expand_trig(expr)
            elif operation == "powsimp":
                result = powsimp(expr)
            elif operation == "expand_log":
                result = expand_log(expr)
            elif operation == "ratsimp":
                result = ratsimp(expr)
            else:
                self.manip_output.setText(f"Unknown operation: {operation}")
                return
            
            output = f"{operation}({expr_text}) =\n{result}"
            self.manip_output.setText(output)
            
        except Exception as e:
            self.manip_output.setText(f"Error: {str(e)}")
    
    def add_equation(self):
        """Add equation to the list"""
        eq_text = self.eq_input.text().strip()
        if eq_text:
            self.eq_list.addItem(eq_text)
            self.eq_input.clear()
    
    def solve_equations(self, solver_type):
        """Solve equation(s)"""
        try:
            if not SYMPY_AVAILABLE:
                self.solve_output.setText("SymPy is not available")
                return
            
            # Get variables to solve for
            var_text = self.solve_vars_input.text().strip()
            if not var_text:
                self.solve_output.setText("Please specify variables to solve for")
                return
            
            vars_list = [v.strip() for v in var_text.replace(',', ' ').split()]
            vars_symbols = symbols(' '.join(vars_list))
            if not isinstance(vars_symbols, tuple):
                vars_symbols = (vars_symbols,)
            
            # Get equations
            equations = []
            
            # Add single equation if present
            eq_text = self.eq_input.text().strip()
            if eq_text:
                equations.append(eq_text)
            
            # Add equations from list
            for i in range(self.eq_list.count()):
                equations.append(self.eq_list.item(i).text())
            
            if not equations:
                self.solve_output.setText("Please enter at least one equation")
                return
            
            # Parse equations
            parsed_eqs = []
            for eq in equations:
                try:
                    # Check if it's already an Eq expression
                    if 'Eq(' in eq:
                        parsed_eqs.append(sympify(eq))
                    else:
                        # Assume it's an expression equal to 0
                        parsed_eqs.append(sympify(eq))
                except:
                    self.solve_output.setText(f"Error parsing equation: {eq}")
                    return
            
            # Solve based on type
            if solver_type == "solve":
                if len(parsed_eqs) == 1:
                    solution = solve(parsed_eqs[0], vars_symbols)
                else:
                    solution = solve(parsed_eqs, vars_symbols)
            elif solver_type == "solveset":
                if len(parsed_eqs) != 1:
                    self.solve_output.setText("solveset works with single equations only")
                    return
                solution = solveset(parsed_eqs[0], vars_symbols[0])
            elif solver_type == "linsolve":
                solution = linsolve(parsed_eqs, vars_symbols)
            else:
                self.solve_output.setText(f"Unknown solver: {solver_type}")
                return
            
            output = f"Solution:\n{solution}"
            self.solve_output.setText(output)
            
        except Exception as e:
            self.solve_output.setText(f"Error: {str(e)}\n\n{traceback.format_exc()}")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Copied", "Text copied to clipboard!")
