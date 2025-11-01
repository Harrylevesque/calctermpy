#!/usr/bin/env python3
"""
Advanced Scientific Calculator with PyQt6
Supports Python math, numpy, scipy, and sympy functions
Features customizable text formatting and document-style calculation history
Includes AI chatbot for code assistance and debugging
"""

import sys
import math
import random
import statistics
import cmath
import decimal
import fractions
import traceback
import re
from typing import Dict, Any
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import AI libraries - Using Ollama instead of transformers
try:
    import requests
    import json
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Import libraries with error handling
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    np = None
    NUMPY_AVAILABLE = False

try:
    import scipy as sp
    from scipy import linalg, optimize, integrate, stats
    SCIPY_AVAILABLE = True
except ImportError:
    sp = None
    SCIPY_AVAILABLE = False

try:
    import sympy as sym
    from sympy import symbols, expand, factor, simplify, solve, diff, integrate as sym_integrate
    SYMPY_AVAILABLE = True
except ImportError:
    sym = None
    SYMPY_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    # Use the QtAgg backend compatible with Qt6/PySide6
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QTextEdit, QLineEdit, QPushButton, QSplitter, QMenuBar, QMenu,
    QDialog, QFormLayout, QSpinBox, QComboBox, QColorDialog,
    QFontDialog, QLabel, QDialogButtonBox, QMessageBox, QToolBar,
    QTextBrowser, QGroupBox, QScrollArea, QPlainTextEdit, QTabWidget,
    QDockWidget, QTreeWidget, QTreeWidgetItem, QHeaderView, QListWidget,
    QListWidgetItem, QFileDialog, QSlider, QCheckBox
)
from PySide6.QtCore import Qt, QSettings, QTimer, QRegularExpression, QSize
from PySide6.QtGui import (QFont, QColor, QAction, QTextCursor, QTextCharFormat, 
                          QSyntaxHighlighter, QTextDocument, QPainter)
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
import re


class GraphPlotWidget(QWidget):
    """Widget for plotting mathematical functions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Enter function (e.g., math.sin(x), x**2, np.exp(x))")
        self.plot_btn = QPushButton("Plot")
        self.clear_btn = QPushButton("Clear")
        
        control_layout.addWidget(QLabel("Function:"))
        control_layout.addWidget(self.function_input)
        control_layout.addWidget(self.plot_btn)
        control_layout.addWidget(self.clear_btn)
        
        layout.addLayout(control_layout)
        
        # Range controls
        range_layout = QHBoxLayout()
        self.x_min = QLineEdit("-10")
        self.x_max = QLineEdit("10")
        self.points = QLineEdit("1000")
        
        range_layout.addWidget(QLabel("X range:"))
        range_layout.addWidget(self.x_min)
        range_layout.addWidget(QLabel("to"))
        range_layout.addWidget(self.x_max)
        range_layout.addWidget(QLabel("Points:"))
        range_layout.addWidget(self.points)
        range_layout.addStretch()
        
        layout.addLayout(range_layout)
        
        # Plot canvas
        if MATPLOTLIB_AVAILABLE:
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)
            
            self.ax = self.figure.add_subplot(111)
            self.ax.grid(True)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
        else:
            layout.addWidget(QLabel("Matplotlib not available. Install with: pip install matplotlib"))
        
        # Connect signals
        self.plot_btn.clicked.connect(self.plot_function)
        self.clear_btn.clicked.connect(self.clear_plot)
        self.function_input.returnPressed.connect(self.plot_function)
        
    def plot_function(self):
        if not MATPLOTLIB_AVAILABLE:
            return
            
        try:
            func_text = self.function_input.text().strip()
            if not func_text:
                return
                
            x_min = float(self.x_min.text())
            x_max = float(self.x_max.text())
            num_points = int(self.points.text())
            
            if NUMPY_AVAILABLE:
                x = np.linspace(x_min, x_max, num_points)
            else:
                # Fallback without numpy
                step = (x_max - x_min) / (num_points - 1)
                x = [x_min + i * step for i in range(num_points)]
            
            # Prepare namespace for evaluation
            namespace = {
                'x': x,
                'math': math,
                'abs': abs,
                'pow': pow,
                'min': min,
                'max': max,
            }
            
            if NUMPY_AVAILABLE:
                namespace['np'] = np
                namespace['numpy'] = np
                
            if SCIPY_AVAILABLE:
                namespace['sp'] = sp
                namespace['scipy'] = sp
                
            # Evaluate function
            y = eval(func_text, {"__builtins__": {}}, namespace)
            
            # Plot
            self.ax.clear()
            self.ax.plot(x, y, 'b-', linewidth=2)
            self.ax.grid(True)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title(f'y = {func_text}')
            
            self.canvas.draw()
            
        except Exception as e:
            # Could show error in status bar or message box
            print(f"Plot error: {e}")
    
    def clear_plot(self):
        if MATPLOTLIB_AVAILABLE:
            self.ax.clear()
            self.ax.grid(True)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.canvas.draw()


class HelpDialog(QDialog):
    """Help dialog showing available functions and usage examples"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator Help")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        help_text = QTextBrowser()
        help_text.setHtml(self.get_help_content())
        layout.addWidget(help_text)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
    def get_help_content(self):
        return """
        <h2>Advanced Scientific Calculator Help</h2>
        
        <h3>Basic Usage</h3>
        <p>Type mathematical expressions in the document editor. Results appear in real-time on the right.</p>
        
        <h3>Variable Definition</h3>
        <p>Define variables: <code>x = 5</code>, <code>y = x * 2</code></p>
        
        <h3>Control Flow & Functions</h3>
        <ul>
            <li><b>If statements:</b> <code>if x > 0:</code></li>
            <li><b>Functions:</b> <code>def my_func(n): return n * 2</code></li>
            <li><b>For loops:</b> <code>for i in range(10):</code></li>
            <li><b>While loops:</b> <code>while count < 5:</code></li>
        </ul>
        
        <h3>Available Libraries and Functions</h3>
        
        <h4>Python Math Library</h4>
        <ul>
            <li><code>math.sin(x)</code>, <code>math.cos(x)</code>, <code>math.tan(x)</code></li>
            <li><code>math.sqrt(x)</code>, <code>math.log(x)</code>, <code>math.exp(x)</code></li>
            <li><code>math.pi</code>, <code>math.e</code></li>
        </ul>
        
        <h4>NumPy (use np.)</h4>
        <ul>
            <li>Arrays: <code>np.array([1,2,3])</code></li>
            <li>Functions: <code>np.sin(x)</code>, <code>np.cos(x)</code>, <code>np.sqrt(x)</code></li>
            <li>Linear algebra: <code>np.dot(a, b)</code>, <code>np.linalg.inv(matrix)</code></li>
            <li>Statistics: <code>np.mean(data)</code>, <code>np.std(data)</code></li>
        </ul>
        
        <h4>SciPy (use sp.)</h4>
        <ul>
            <li>Optimization: <code>sp.optimize.minimize(func, x0)</code></li>
            <li>Integration: <code>sp.integrate.quad(func, a, b)</code></li>
            <li>Statistics: <code>sp.stats.norm.pdf(x)</code></li>
            <li>Linear algebra: <code>sp.linalg.solve(A, b)</code></li>
        </ul>
        
        <h4>SymPy (use sym.)</h4>
        <ul>
            <li>Symbolic variables: <code>x = sym.Symbol('x')</code></li>
            <li>Algebra: <code>sym.expand((x+1)**2)</code>, <code>sym.factor(x**2-1)</code></li>
            <li>Calculus: <code>sym.diff(x**2, x)</code>, <code>sym.integrate(x**2, x)</code></li>
            <li>Equation solving: <code>sym.solve(x**2 - 4, x)</code></li>
        </ul>
        
        <h3>Examples</h3>
        <h4>Basic Math:</h4>
        <p><code>x = 5</code></p>
        <p><code>y = math.sin(x) + np.cos(x)</code></p>
        
        <h4>Control Flow:</h4>
        <p><code>if x > 0:<br>&nbsp;&nbsp;&nbsp;&nbsp;result = "positive"<br>else:<br>&nbsp;&nbsp;&nbsp;&nbsp;result = "negative"</code></p>
        
        <h4>Functions:</h4>
        <p><code>def factorial(n):<br>&nbsp;&nbsp;&nbsp;&nbsp;if n <= 1:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return 1<br>&nbsp;&nbsp;&nbsp;&nbsp;return n * factorial(n-1)</code></p>
        
        <h4>Loops:</h4>
        <p><code>total = 0<br>for i in range(10):<br>&nbsp;&nbsp;&nbsp;&nbsp;total += i</code></p>
        
        <h4>Arrays & Matrices:</h4>
        <p><code>matrix = np.array([[1,2],[3,4]])</code></p>
        <p><code>det = np.linalg.det(matrix)</code></p>
        
        <h4>Symbolic Math:</h4>
        <p><code>t = sym.Symbol('t')</code></p>
        <p><code>expr = sym.diff(t**3 + 2*t**2, t)</code></p>
        """


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python syntax highlighter with VS Code-like colors"""
    
    def __init__(self, document: QTextDocument):
        super().__init__(document)
        self.setup_highlighting_rules()
    
    def setup_highlighting_rules(self):
        """Setup the highlighting rules for Python syntax"""
        self.highlighting_rules = []
        
        # VS Code-like color scheme
        # Keywords (purple/magenta)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(86, 156, 214))  # Light blue
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Built-in functions (yellow)
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(220, 220, 170))  # Light yellow
        
        builtins = [
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
            'enumerate', 'eval', 'exec', 'filter', 'float', 'format',
            'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
            'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
            'iter', 'len', 'list', 'locals', 'map', 'max', 'min',
            'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
            'range', 'repr', 'reversed', 'round', 'set', 'setattr',
            'slice', 'sorted', 'str', 'sum', 'super', 'tuple', 'type',
            'vars', 'zip'
        ]
        
        for builtin in builtins:
            pattern = QRegularExpression(f'\\b{builtin}\\b')
            self.highlighting_rules.append((pattern, builtin_format))
        
        # Numbers (light green)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(181, 206, 168))  # Light green
        
        # Integer and float patterns
        number_pattern = QRegularExpression(r'\b\d+\.?\d*([eE][+-]?\d+)?\b')
        self.highlighting_rules.append((number_pattern, number_format))
        
        # Hex, oct, bin numbers
        hex_pattern = QRegularExpression(r'\b0[xX][0-9a-fA-F]+\b')
        self.highlighting_rules.append((hex_pattern, number_format))
        
        oct_pattern = QRegularExpression(r'\b0[oO][0-7]+\b')
        self.highlighting_rules.append((oct_pattern, number_format))
        
        bin_pattern = QRegularExpression(r'\b0[bB][01]+\b')
        self.highlighting_rules.append((bin_pattern, number_format))
        
        # Strings (orange/salmon)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(206, 145, 120))  # Orange/salmon
        
        # Single quoted strings
        single_quote_pattern = QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'")
        self.highlighting_rules.append((single_quote_pattern, string_format))
        
        # Double quoted strings
        double_quote_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"')
        self.highlighting_rules.append((double_quote_pattern, string_format))
        
        # Triple quoted strings (multiline)
        triple_quote_format = QTextCharFormat()
        triple_quote_format.setForeground(QColor(206, 145, 120))  # Orange/salmon
        triple_single_pattern = QRegularExpression(r"'''.*?'''", QRegularExpression.PatternOption.DotMatchesEverythingOption)
        triple_double_pattern = QRegularExpression(r'""".*?"""', QRegularExpression.PatternOption.DotMatchesEverythingOption)
        self.highlighting_rules.append((triple_single_pattern, triple_quote_format))
        self.highlighting_rules.append((triple_double_pattern, triple_quote_format))
        
        # Comments (green)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(106, 153, 85))  # Green
        comment_format.setFontItalic(True)
        
        comment_pattern = QRegularExpression(r'#.*$')
        self.highlighting_rules.append((comment_pattern, comment_format))
        
        # Function definitions (yellow)
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(220, 220, 170))  # Light yellow
        function_format.setFontWeight(QFont.Weight.Bold)
        
        function_pattern = QRegularExpression(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        self.highlighting_rules.append((function_pattern, function_format))
        
        # Class definitions (light blue)
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(78, 201, 176))  # Cyan/turquoise
        class_format.setFontWeight(QFont.Weight.Bold)
        
        class_pattern = QRegularExpression(r'\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        self.highlighting_rules.append((class_pattern, class_format))
        
        # Mathematical module names (light purple)
        module_format = QTextCharFormat()
        module_format.setForeground(QColor(156, 220, 254))  # Light blue
        module_format.setFontWeight(QFont.Weight.Bold)
        
        math_modules = ['math', 'np', 'numpy', 'sp', 'scipy', 'sym', 'sympy']
        for module in math_modules:
            pattern = QRegularExpression(f'\\b{module}\\.')
            self.highlighting_rules.append((pattern, module_format))
        
        # Operators (white/light gray)
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(212, 212, 212))  # Light gray
        
        operators = [
            '=', '==', '!=', '<', '<=', '>', '>=',
            '\\+', '-', '\\*', '/', '//', '%', '\\*\\*',
            '\\+=', '-=', '\\*=', '/=', '//=', '%=', '\\*\\*=',
            '&', '\\|', '\\^', '~', '<<', '>>', '&=', '\\|=', '\\^=',
            '<<=', '>>=', 'and', 'or', 'not', 'in', 'is'
        ]
        
        for op in operators:
            pattern = QRegularExpression(f'\\s*{op}\\s*')
            self.highlighting_rules.append((pattern, operator_format))
        
        # Parentheses, brackets, braces (light gray)
        bracket_format = QTextCharFormat()
        bracket_format.setForeground(QColor(255, 215, 0))  # Gold
        bracket_format.setFontWeight(QFont.Weight.Bold)
        
        bracket_pattern = QRegularExpression(r'[\(\)\[\]\{\}]')
        self.highlighting_rules.append((bracket_pattern, bracket_format))
        
        # Self keyword (purple)
        self_format = QTextCharFormat()
        self_format.setForeground(QColor(86, 156, 214))  # Light blue
        self_format.setFontWeight(QFont.Weight.Bold)
        
        self_pattern = QRegularExpression(r'\bself\b')
        self.highlighting_rules.append((self_pattern, self_format))
    
    def setup_light_theme(self):
        """Setup highlighting rules for light theme"""
        self.highlighting_rules = []
        
        # Light theme colors (darker colors for better visibility on light background)
        # Keywords (dark blue)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(0, 0, 255))  # Blue
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Built-in functions (dark orange)
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(128, 0, 128))  # Purple
        
        builtins = [
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
            'enumerate', 'eval', 'exec', 'filter', 'float', 'format',
            'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
            'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
            'iter', 'len', 'list', 'locals', 'map', 'max', 'min',
            'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
            'range', 'repr', 'reversed', 'round', 'set', 'setattr',
            'slice', 'sorted', 'str', 'sum', 'super', 'tuple', 'type',
            'vars', 'zip'
        ]
        
        for builtin in builtins:
            pattern = QRegularExpression(f'\\b{builtin}\\b')
            self.highlighting_rules.append((pattern, builtin_format))
        
        # Numbers (dark red)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(139, 0, 0))  # Dark red
        
        number_pattern = QRegularExpression(r'\b\d+\.?\d*([eE][+-]?\d+)?\b')
        self.highlighting_rules.append((number_pattern, number_format))
        
        hex_pattern = QRegularExpression(r'\b0[xX][0-9a-fA-F]+\b')
        self.highlighting_rules.append((hex_pattern, number_format))
        
        oct_pattern = QRegularExpression(r'\b0[oO][0-7]+\b')
        self.highlighting_rules.append((oct_pattern, number_format))
        
        bin_pattern = QRegularExpression(r'\b0[bB][01]+\b')
        self.highlighting_rules.append((bin_pattern, number_format))
        
        # Strings (dark green)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(0, 128, 0))  # Dark green
        
        single_quote_pattern = QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'")
        self.highlighting_rules.append((single_quote_pattern, string_format))
        
        double_quote_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"')
        self.highlighting_rules.append((double_quote_pattern, string_format))
        
        triple_quote_format = QTextCharFormat()
        triple_quote_format.setForeground(QColor(0, 128, 0))  # Dark green
        triple_single_pattern = QRegularExpression(r"'''.*?'''", QRegularExpression.PatternOption.DotMatchesEverythingOption)
        triple_double_pattern = QRegularExpression(r'""".*?"""', QRegularExpression.PatternOption.DotMatchesEverythingOption)
        self.highlighting_rules.append((triple_single_pattern, triple_quote_format))
        self.highlighting_rules.append((triple_double_pattern, triple_quote_format))
        
        # Comments (gray)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))  # Gray
        comment_format.setFontItalic(True)
        
        comment_pattern = QRegularExpression(r'#.*$')
        self.highlighting_rules.append((comment_pattern, comment_format))
        
        # Function definitions (dark blue)
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(0, 0, 139))  # Dark blue
        function_format.setFontWeight(QFont.Weight.Bold)
        
        function_pattern = QRegularExpression(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        self.highlighting_rules.append((function_pattern, function_format))
        
        # Class definitions (dark cyan)
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(0, 139, 139))  # Dark cyan
        class_format.setFontWeight(QFont.Weight.Bold)
        
        class_pattern = QRegularExpression(r'\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        self.highlighting_rules.append((class_pattern, class_format))
        
        # Mathematical module names (dark blue)
        module_format = QTextCharFormat()
        module_format.setForeground(QColor(0, 0, 139))  # Dark blue
        module_format.setFontWeight(QFont.Weight.Bold)
        
        math_modules = ['math', 'np', 'numpy', 'sp', 'scipy', 'sym', 'sympy']
        for module in math_modules:
            pattern = QRegularExpression(f'\\b{module}\\.')
            self.highlighting_rules.append((pattern, module_format))
        
        # Operators (black)
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(0, 0, 0))  # Black
        
        operators = [
            '=', '==', '!=', '<', '<=', '>', '>=',
            '\\+', '-', '\\*', '/', '//', '%', '\\*\\*',
            '\\+=', '-=', '\\*=', '/=', '//=', '%=', '\\*\\*=',
            '&', '\\|', '\\^', '~', '<<', '>>', '&=', '\\|=', '\\^=',
            '<<=', '>>=', 'and', 'or', 'not', 'in', 'is'
        ]
        
        for op in operators:
            pattern = QRegularExpression(f'\\s*{op}\\s*')
            self.highlighting_rules.append((pattern, operator_format))
        
        # Parentheses, brackets, braces (dark orange)
        bracket_format = QTextCharFormat()
        bracket_format.setForeground(QColor(255, 140, 0))  # Dark orange
        bracket_format.setFontWeight(QFont.Weight.Bold)
        
        bracket_pattern = QRegularExpression(r'[\(\)\[\]\{\}]')
        self.highlighting_rules.append((bracket_pattern, bracket_format))
        
        # Self keyword (blue)
        self_format = QTextCharFormat()
        self_format.setForeground(QColor(0, 0, 255))  # Blue
        self_format.setFontWeight(QFont.Weight.Bold)
        
        self_pattern = QRegularExpression(r'\bself\b')
        self.highlighting_rules.append((self_pattern, self_format))
    
    def setup_custom_theme(self, colors):
        """Setup highlighting rules with custom colors"""
        self.highlighting_rules = []
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(colors['keyword'])
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(colors['number'])
        
        number_pattern = QRegularExpression(r'\b\d+\.?\d*([eE][+-]?\d+)?\b')
        self.highlighting_rules.append((number_pattern, number_format))
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(colors['string'])
        
        single_quote_pattern = QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'")
        self.highlighting_rules.append((single_quote_pattern, string_format))
        
        double_quote_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"')
        self.highlighting_rules.append((double_quote_pattern, string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(colors['comment'])
        comment_format.setFontItalic(True)
        
        comment_pattern = QRegularExpression(r'#.*$')
        self.highlighting_rules.append((comment_pattern, comment_format))
        
        # Rehighlight the document
        self.rehighlight()
    
    def highlightBlock(self, text):
        """Apply syntax highlighting to a block of text"""
        # Apply all highlighting rules
        for pattern, format in self.highlighting_rules:
            expression = pattern
            match_iterator = expression.globalMatch(text)
            
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class LineNumberArea(QWidget):
    """Widget for displaying line numbers"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor
        
    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    """Custom text editor with line numbers and inline results"""
    
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        self.line_results = {}  # Store results for each line
        
        # Connect signals
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        
        # Set initial width
        self.update_line_number_area_width(0)
        
        # Setup fonts and margins
        font = QFont("Consolas", 12)
        self.setFont(font)
        
    def line_number_area_width(self):
        """Calculate width needed for line number area"""
        digits = 1
        max_block = max(1, self.blockCount())
        while max_block >= 10:
            max_block //= 10
            digits += 1
        
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, new_block_count):
        """Update the viewport margins for line numbers"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """Update the line number area when scrolling"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
    
    def line_number_area_paint_event(self, event):
        """Paint the line numbers"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(240, 240, 240))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        height = self.fontMetrics().height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(120, 120, 120))
                painter.drawText(0, int(top), self.line_number_area.width() - 5, height,
                               Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def paintEvent(self, event):
        """Custom paint event to draw inline results"""
        super().paintEvent(event)
        
        # Draw inline results
        painter = QPainter(self.viewport())
        painter.setPen(QColor(0, 150, 0))  # Green for results
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        height = self.fontMetrics().height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                # Draw inline result if available
                if block_number + 1 in self.line_results:
                    result = self.line_results[block_number + 1]
                    result_text = f" = {result}"
                    
                    # Calculate position at end of line text
                    text_width = self.fontMetrics().horizontalAdvance(block.text())
                    result_x = text_width + 20  # Add some padding
                    
                    # Make sure it fits in the viewport
                    if result_x < self.viewport().width() - 200:
                        painter.drawText(int(result_x), int(top + height - 3), result_text)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def set_line_result(self, line_number, result):
        """Set the result for a specific line"""
        self.line_results[line_number] = result
        self.update()  # Trigger repaint
    
    def clear_line_results(self):
        """Clear all inline results"""
        self.line_results.clear()
        self.update()


class ScientificCalculator(QMainWindow):
    """Main calculator application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Scientific Calculator - Document Mode")
        self.setGeometry(100, 100, 1400, 800)
        self.variables: Dict[str, Any] = {}
        self.calculation_history = []
        self.settings = QSettings("ScientificCalculator", "Settings")
        self.text_font = QFont("Consolas", 12)
        # Use better fallback fonts for macOS
        if not self.text_font.exactMatch():
            self.text_font = QFont("Monaco", 12)  # macOS monospace font
            if not self.text_font.exactMatch():
                self.text_font = QFont("monospace", 12)  # generic fallback
        self.text_color = QColor(0, 0, 0)
        self.bg_color = QColor(255, 255, 255)
        self.decimal_precision = 6
        self.theme = "dark"
        self.last_error = ""
        self.setup_ui()
        self.setup_calculation_namespace()  # <-- Moved before menu bar setup
        self.setup_menu_bar()
        self.setup_toolbar()
        self.load_settings()  # Load settings after UI is set up
        self.apply_styling()
        self.load_panel_configuration()  # Load panel configuration after UI setup

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
                "symbols": symbols,
                "expand": expand,
                "factor": factor,
                "simplify": simplify,
                "solve": solve,
                "diff": diff,
                "sym_integrate": sym_integrate,
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
        self.variables.clear()
        self.line_results.clear()
        self.namespace = self.base_namespace.copy()
        self.variables_widget.update_variables({})

    def setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Document management
        new_doc_action = QAction("New Document", self)
        new_doc_action.setShortcut("Ctrl+N")
        new_doc_action.triggered.connect(self.new_document)
        file_menu.addAction(new_doc_action)
        
        file_menu.addSeparator()
        
        print_action = QAction("Print", self)
        print_action.triggered.connect(self.print_document)
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        # Undo/Redo actions
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo_action)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo_action)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        edit_menu.addAction(settings_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        unit_converter_action = QAction("Unit Converter", self)
        unit_converter_action.triggered.connect(self.open_unit_converter)
        tools_menu.addAction(unit_converter_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Dock widget toggles
        graph_toggle = self.graph_dock.toggleViewAction()
        graph_toggle.setText("Graph Plotter")
        view_menu.addAction(graph_toggle)
        
        history_toggle = self.history_dock.toggleViewAction()
        history_toggle.setText("History Panel")
        view_menu.addAction(history_toggle)
        
        functions_toggle = self.functions_dock.toggleViewAction()
        functions_toggle.setText("Custom Functions")
        view_menu.addAction(functions_toggle)
        
        variables_toggle = self.variables_dock.toggleViewAction()
        variables_toggle.setText("Variable Inspector")
        view_menu.addAction(variables_toggle)
        
        view_menu.addSeparator()
        
        # Panel layout configuration
        panel_layout_action = QAction("Configure Panel Layout", self)
        panel_layout_action.triggered.connect(self.open_panel_layout_config)
        view_menu.addAction(panel_layout_action)
        
        # Theme customizer
        theme_action = QAction("Customize Theme", self)
        theme_action.triggered.connect(self.open_theme_customizer)
        view_menu.addAction(theme_action)
        
        # Math Functions menu
        self.setup_math_menu(menubar)
        self.setup_random_menu(menubar)
        self.setup_statistics_menu(menubar)
        self.setup_cmath_menu(menubar)
        self.setup_decimal_menu(menubar)
        self.setup_fractions_menu(menubar)
        
        # Constants menu
        self.setup_constants_menu(menubar)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
    def setup_toolbar(self):
        """Setup the toolbar with quick actions"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Quick function buttons
        functions = [
            ("π", "math.pi"),
            ("e", "math.e"),
            ("sin", "math.sin("),
            ("cos", "math.cos("),
            ("tan", "math.tan("),
            ("√", "math.sqrt("),
            ("log", "math.log("),
            ("ln", "math.log("),
            ("x²", "**2"),
            ("x^y", "**")
        ]
        
        for name, func in functions:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, f=func: self.insert_function(f))
            toolbar.addWidget(btn)
        
    def setup_math_menu(self, menubar):
        """Setup the Math Functions menu"""
        math_menu = menubar.addMenu("Math")
        
        # Trigonometric functions
        trig_menu = math_menu.addMenu("Trigonometric")
        trig_functions = [
            ("sin(x)", "math.sin("),
            ("cos(x)", "math.cos("),
            ("tan(x)", "math.tan("),
            ("asin(x)", "math.asin("),
            ("acos(x)", "math.acos("),
            ("atan(x)", "math.atan("),
            ("atan2(y,x)", "math.atan2("),
            ("sinh(x)", "math.sinh("),
            ("cosh(x)", "math.cosh("),
            ("tanh(x)", "math.tanh("),
            ("asinh(x)", "math.asinh("),
            ("acosh(x)", "math.acosh("),
            ("atanh(x)", "math.atanh("),
        ]
        for name, func in trig_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            trig_menu.addAction(action)
        
        # Logarithmic and exponential
        log_menu = math_menu.addMenu("Logarithmic & Exponential")
        log_functions = [
            ("exp(x)", "math.exp("),
            ("log(x)", "math.log("),
            ("log10(x)", "math.log10("),
            ("log2(x)", "math.log2("),
            ("log(x, base)", "math.log("),
            ("pow(x, y)", "math.pow("),
            ("sqrt(x)", "math.sqrt("),
        ]
        for name, func in log_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            log_menu.addAction(action)
        
        # Number theory and utilities
        util_menu = math_menu.addMenu("Number Theory & Utilities")
        util_functions = [
            ("abs(x)", "abs("),
            ("ceil(x)", "math.ceil("),
            ("floor(x)", "math.floor("),
            ("round(x)", "round("),
            ("trunc(x)", "math.trunc("),
            ("fabs(x)", "math.fabs("),
            ("gcd(a, b)", "math.gcd("),
            ("lcm(a, b)", "math.lcm("),
            ("factorial(x)", "math.factorial("),
            ("comb(n, k)", "math.comb("),
            ("perm(n, k)", "math.perm("),
        ]
        for name, func in util_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            util_menu.addAction(action)
        
        # Special functions
        special_menu = math_menu.addMenu("Special Functions")
        special_functions = [
            ("gamma(x)", "math.gamma("),
            ("lgamma(x)", "math.lgamma("),
            ("erf(x)", "math.erf("),
            ("erfc(x)", "math.erfc("),
            ("degrees(x)", "math.degrees("),
            ("radians(x)", "math.radians("),
        ]
        for name, func in special_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            special_menu.addAction(action)
    
    def setup_random_menu(self, menubar):
        """Setup the Random menu"""
        random_menu = menubar.addMenu("Random")
        random_functions = [
            ("random()", "random.random()"),
            ("randint(a, b)", "random.randint("),
            ("uniform(a, b)", "random.uniform("),
            ("choice(seq)", "random.choice("),
            ("shuffle(seq)", "random.shuffle("),
            ("sample(seq, k)", "random.sample("),
            ("seed(n)", "random.seed("),
        ]
        for name, func in random_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            random_menu.addAction(action)

    def setup_statistics_menu(self, menubar):
        """Setup the Statistics menu"""
        stats_menu = menubar.addMenu("Statistics")
        stats_functions = [
            ("mean(data)", "statistics.mean("),
            ("median(data)", "statistics.median("),
            ("mode(data)", "statistics.mode("),
            ("stdev(data)", "statistics.stdev("),
            ("variance(data)", "statistics.variance("),
            ("harmonic_mean(data)", "statistics.harmonic_mean("),
            ("multimode(data)", "statistics.multimode("),
        ]
        for name, func in stats_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            stats_menu.addAction(action)

    def setup_cmath_menu(self, menubar):
        """Setup the Complex Math menu"""
        cmath_menu = menubar.addMenu("Complex Math (cmath)")
        cmath_functions = [
            ("sqrt(z)", "cmath.sqrt("),
            ("exp(z)", "cmath.exp("),
            ("log(z)", "cmath.log("),
            ("sin(z)", "cmath.sin("),
            ("cos(z)", "cmath.cos("),
            ("tan(z)", "cmath.tan("),
            ("phase(z)", "cmath.phase("),
            ("polar(z)", "cmath.polar("),
            ("rect(r, phi)", "cmath.rect("),
        ]
        for name, func in cmath_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            cmath_menu.addAction(action)

    def setup_decimal_menu(self, menubar):
        """Setup the Decimal menu"""
        decimal_menu = menubar.addMenu("Decimal")
        decimal_functions = [
            ("Decimal('0.1')", "decimal.Decimal('"),
            ("getcontext()", "decimal.getcontext()"),
            ("setcontext(ctx)", "decimal.setcontext("),
            ("localcontext()", "decimal.localcontext()"),
        ]
        for name, func in decimal_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            decimal_menu.addAction(action)

    def setup_fractions_menu(self, menubar):
        """Setup the Fractions menu"""
        fractions_menu = menubar.addMenu("Fractions")
        fractions_functions = [
            ("Fraction(1, 3)", "fractions.Fraction("),
            ("Fraction.from_float(0.5)", "fractions.Fraction.from_float("),
            ("Fraction.from_decimal(d)", "fractions.Fraction.from_decimal("),
            ("gcd(a, b)", "fractions.gcd("),
        ]
        for name, func in fractions_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            fractions_menu.addAction(action)

    def setup_constants_menu(self, menubar):
        """Setup the Constants menu"""
        constants_menu = menubar.addMenu("Constants")
        # Mathematical constants
        math_constants = [
            ("π (pi)", "math.pi"),
            ("e (Euler's number)", "math.e"),
            ("τ (tau = 2π)", "math.tau"),
            ("∞ (infinity)", "math.inf"),
            ("NaN", "math.nan"),
        ]
        for name, const in math_constants:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, c=const: self.insert_function(c))
            constants_menu.addAction(action)
        # NumPy constants
        if 'np' in self.base_namespace:
            constants_menu.addSeparator()
            numpy_constants = [
                ("np.pi", "np.pi"),
                ("np.e", "np.e"),
                ("np.inf", "np.inf"),
                ("np.nan", "np.nan"),
            ]
            for name, const in numpy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)
        # SymPy constants
        if 'sym' in self.base_namespace:
            constants_menu.addSeparator()
            sympy_constants = [
                ("sym.pi", "sym.pi"),
                ("sym.E", "sym.E"),
                ("sym.I (imaginary unit)", "sym.I"),
                ("sym.oo (infinity)", "sym.oo"),
                ("sym.zoo (complex infinity)", "sym.zoo"),
            ]
            for name, const in sympy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)

    def setup_toolbar(self):
        """Setup the toolbar with quick actions"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Quick function buttons
        functions = [
            ("π", "math.pi"),
            ("e", "math.e"),
            ("sin", "math.sin("),
            ("cos", "math.cos("),
            ("tan", "math.tan("),
            ("√", "math.sqrt("),
            ("log", "math.log("),
            ("ln", "math.log("),
            ("x²", "**2"),
            ("x^y", "**")
        ]
        
        for name, func in functions:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, f=func: self.insert_function(f))
            toolbar.addWidget(btn)
        
    def setup_math_menu(self, menubar):
        """Setup the Math Functions menu"""
        math_menu = menubar.addMenu("Math")
        
        # Trigonometric functions
        trig_menu = math_menu.addMenu("Trigonometric")
        trig_functions = [
            ("sin(x)", "math.sin("),
            ("cos(x)", "math.cos("),
            ("tan(x)", "math.tan("),
            ("asin(x)", "math.asin("),
            ("acos(x)", "math.acos("),
            ("atan(x)", "math.atan("),
            ("atan2(y,x)", "math.atan2("),
            ("sinh(x)", "math.sinh("),
            ("cosh(x)", "math.cosh("),
            ("tanh(x)", "math.tanh("),
            ("asinh(x)", "math.asinh("),
            ("acosh(x)", "math.acosh("),
            ("atanh(x)", "math.atanh("),
        ]
        for name, func in trig_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            trig_menu.addAction(action)
        
        # Logarithmic and exponential
        log_menu = math_menu.addMenu("Logarithmic & Exponential")
        log_functions = [
            ("exp(x)", "math.exp("),
            ("log(x)", "math.log("),
            ("log10(x)", "math.log10("),
            ("log2(x)", "math.log2("),
            ("log(x, base)", "math.log("),
            ("pow(x, y)", "math.pow("),
            ("sqrt(x)", "math.sqrt("),
        ]
        for name, func in log_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            log_menu.addAction(action)
        
        # Number theory and utilities
        util_menu = math_menu.addMenu("Number Theory & Utilities")
        util_functions = [
            ("abs(x)", "abs("),
            ("ceil(x)", "math.ceil("),
            ("floor(x)", "math.floor("),
            ("round(x)", "round("),
            ("trunc(x)", "math.trunc("),
            ("fabs(x)", "math.fabs("),
            ("gcd(a, b)", "math.gcd("),
            ("lcm(a, b)", "math.lcm("),
            ("factorial(x)", "math.factorial("),
            ("comb(n, k)", "math.comb("),
            ("perm(n, k)", "math.perm("),
        ]
        for name, func in util_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            util_menu.addAction(action)
        
        # Special functions
        special_menu = math_menu.addMenu("Special Functions")
        special_functions = [
            ("gamma(x)", "math.gamma("),
            ("lgamma(x)", "math.lgamma("),
            ("erf(x)", "math.erf("),
            ("erfc(x)", "math.erfc("),
            ("degrees(x)", "math.degrees("),
            ("radians(x)", "math.radians("),
        ]
        for name, func in special_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            special_menu.addAction(action)
    
    def setup_random_menu(self, menubar):
        """Setup the Random menu"""
        random_menu = menubar.addMenu("Random")
        random_functions = [
            ("random()", "random.random()"),
            ("randint(a, b)", "random.randint("),
            ("uniform(a, b)", "random.uniform("),
            ("choice(seq)", "random.choice("),
            ("shuffle(seq)", "random.shuffle("),
            ("sample(seq, k)", "random.sample("),
            ("seed(n)", "random.seed("),
        ]
        for name, func in random_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            random_menu.addAction(action)

    def setup_statistics_menu(self, menubar):
        """Setup the Statistics menu"""
        stats_menu = menubar.addMenu("Statistics")
        stats_functions = [
            ("mean(data)", "statistics.mean("),
            ("median(data)", "statistics.median("),
            ("mode(data)", "statistics.mode("),
            ("stdev(data)", "statistics.stdev("),
            ("variance(data)", "statistics.variance("),
            ("harmonic_mean(data)", "statistics.harmonic_mean("),
            ("multimode(data)", "statistics.multimode("),
        ]
        for name, func in stats_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            stats_menu.addAction(action)

    def setup_cmath_menu(self, menubar):
        """Setup the Complex Math menu"""
        cmath_menu = menubar.addMenu("Complex Math (cmath)")
        cmath_functions = [
            ("sqrt(z)", "cmath.sqrt("),
            ("exp(z)", "cmath.exp("),
            ("log(z)", "cmath.log("),
            ("sin(z)", "cmath.sin("),
            ("cos(z)", "cmath.cos("),
            ("tan(z)", "cmath.tan("),
            ("phase(z)", "cmath.phase("),
            ("polar(z)", "cmath.polar("),
            ("rect(r, phi)", "cmath.rect("),
        ]
        for name, func in cmath_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            cmath_menu.addAction(action)

    def setup_decimal_menu(self, menubar):
        """Setup the Decimal menu"""
        decimal_menu = menubar.addMenu("Decimal")
        decimal_functions = [
            ("Decimal('0.1')", "decimal.Decimal('"),
            ("getcontext()", "decimal.getcontext()"),
            ("setcontext(ctx)", "decimal.setcontext("),
            ("localcontext()", "decimal.localcontext()"),
        ]
        for name, func in decimal_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            decimal_menu.addAction(action)

    def setup_fractions_menu(self, menubar):
        """Setup the Fractions menu"""
        fractions_menu = menubar.addMenu("Fractions")
        fractions_functions = [
            ("Fraction(1, 3)", "fractions.Fraction("),
            ("Fraction.from_float(0.5)", "fractions.Fraction.from_float("),
            ("Fraction.from_decimal(d)", "fractions.Fraction.from_decimal("),
            ("gcd(a, b)", "fractions.gcd("),
        ]
        for name, func in fractions_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            fractions_menu.addAction(action)

    def setup_constants_menu(self, menubar):
        """Setup the Constants menu"""
        constants_menu = menubar.addMenu("Constants")
        # Mathematical constants
        math_constants = [
            ("π (pi)", "math.pi"),
            ("e (Euler's number)", "math.e"),
            ("τ (tau = 2π)", "math.tau"),
            ("∞ (infinity)", "math.inf"),
            ("NaN", "math.nan"),
        ]
        for name, const in math_constants:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, c=const: self.insert_function(c))
            constants_menu.addAction(action)
        # NumPy constants
        if 'np' in self.base_namespace:
            constants_menu.addSeparator()
            numpy_constants = [
                ("np.pi", "np.pi"),
                ("np.e", "np.e"),
                ("np.inf", "np.inf"),
                ("np.nan", "np.nan"),
            ]
            for name, const in numpy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)
        # SymPy constants
        if 'sym' in self.base_namespace:
            constants_menu.addSeparator()
            sympy_constants = [
                ("sym.pi", "sym.pi"),
                ("sym.E", "sym.E"),
                ("sym.I (imaginary unit)", "sym.I"),
                ("sym.oo (infinity)", "sym.oo"),
                ("sym.zoo (complex infinity)", "sym.zoo"),
            ]
            for name, const in sympy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)

    def setup_toolbar(self):
        """Setup the toolbar with quick actions"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Quick function buttons
        functions = [
            ("π", "math.pi"),
            ("e", "math.e"),
            ("sin", "math.sin("),
            ("cos", "math.cos("),
            ("tan", "math.tan("),
            ("√", "math.sqrt("),
            ("log", "math.log("),
            ("ln", "math.log("),
            ("x²", "**2"),
            ("x^y", "**")
        ]
        
        for name, func in functions:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, f=func: self.insert_function(f))
            toolbar.addWidget(btn)
        
    def setup_math_menu(self, menubar):
        """Setup the Math Functions menu"""
        math_menu = menubar.addMenu("Math")
        
        # Trigonometric functions
        trig_menu = math_menu.addMenu("Trigonometric")
        trig_functions = [
            ("sin(x)", "math.sin("),
            ("cos(x)", "math.cos("),
            ("tan(x)", "math.tan("),
            ("asin(x)", "math.asin("),
            ("acos(x)", "math.acos("),
            ("atan(x)", "math.atan("),
            ("atan2(y,x)", "math.atan2("),
            ("sinh(x)", "math.sinh("),
            ("cosh(x)", "math.cosh("),
            ("tanh(x)", "math.tanh("),
            ("asinh(x)", "math.asinh("),
            ("acosh(x)", "math.acosh("),
            ("atanh(x)", "math.atanh("),
        ]
        for name, func in trig_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            trig_menu.addAction(action)
        
        # Logarithmic and exponential
        log_menu = math_menu.addMenu("Logarithmic & Exponential")
        log_functions = [
            ("exp(x)", "math.exp("),
            ("log(x)", "math.log("),
            ("log10(x)", "math.log10("),
            ("log2(x)", "math.log2("),
            ("log(x, base)", "math.log("),
            ("pow(x, y)", "math.pow("),
            ("sqrt(x)", "math.sqrt("),
        ]
        for name, func in log_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            log_menu.addAction(action)
        
        # Number theory and utilities
        util_menu = math_menu.addMenu("Number Theory & Utilities")
        util_functions = [
            ("abs(x)", "abs("),
            ("ceil(x)", "math.ceil("),
            ("floor(x)", "math.floor("),
            ("round(x)", "round("),
            ("trunc(x)", "math.trunc("),
            ("fabs(x)", "math.fabs("),
            ("gcd(a, b)", "math.gcd("),
            ("lcm(a, b)", "math.lcm("),
            ("factorial(x)", "math.factorial("),
            ("comb(n, k)", "math.comb("),
            ("perm(n, k)", "math.perm("),
        ]
        for name, func in util_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            util_menu.addAction(action)
        
        # Special functions
        special_menu = math_menu.addMenu("Special Functions")
        special_functions = [
            ("gamma(x)", "math.gamma("),
            ("lgamma(x)", "math.lgamma("),
            ("erf(x)", "math.erf("),
            ("erfc(x)", "math.erfc("),
            ("degrees(x)", "math.degrees("),
            ("radians(x)", "math.radians("),
        ]
        for name, func in special_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            special_menu.addAction(action)
    
    def setup_random_menu(self, menubar):
        """Setup the Random menu"""
        random_menu = menubar.addMenu("Random")
        random_functions = [
            ("random()", "random.random()"),
            ("randint(a, b)", "random.randint("),
            ("uniform(a, b)", "random.uniform("),
            ("choice(seq)", "random.choice("),
            ("shuffle(seq)", "random.shuffle("),
            ("sample(seq, k)", "random.sample("),
            ("seed(n)", "random.seed("),
        ]
        for name, func in random_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            random_menu.addAction(action)

    def setup_statistics_menu(self, menubar):
        """Setup the Statistics menu"""
        stats_menu = menubar.addMenu("Statistics")
        stats_functions = [
            ("mean(data)", "statistics.mean("),
            ("median(data)", "statistics.median("),
            ("mode(data)", "statistics.mode("),
            ("stdev(data)", "statistics.stdev("),
            ("variance(data)", "statistics.variance("),
            ("harmonic_mean(data)", "statistics.harmonic_mean("),
            ("multimode(data)", "statistics.multimode("),
        ]
        for name, func in stats_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            stats_menu.addAction(action)

    def setup_cmath_menu(self, menubar):
        """Setup the Complex Math menu"""
        cmath_menu = menubar.addMenu("Complex Math (cmath)")
        cmath_functions = [
            ("sqrt(z)", "cmath.sqrt("),
            ("exp(z)", "cmath.exp("),
            ("log(z)", "cmath.log("),
            ("sin(z)", "cmath.sin("),
            ("cos(z)", "cmath.cos("),
            ("tan(z)", "cmath.tan("),
            ("phase(z)", "cmath.phase("),
            ("polar(z)", "cmath.polar("),
            ("rect(r, phi)", "cmath.rect("),
        ]
        for name, func in cmath_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            cmath_menu.addAction(action)

    def setup_decimal_menu(self, menubar):
        """Setup the Decimal menu"""
        decimal_menu = menubar.addMenu("Decimal")
        decimal_functions = [
            ("Decimal('0.1')", "decimal.Decimal('"),
            ("getcontext()", "decimal.getcontext()"),
            ("setcontext(ctx)", "decimal.setcontext("),
            ("localcontext()", "decimal.localcontext()"),
        ]
        for name, func in decimal_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            decimal_menu.addAction(action)

    def setup_fractions_menu(self, menubar):
        """Setup the Fractions menu"""
        fractions_menu = menubar.addMenu("Fractions")
        fractions_functions = [
            ("Fraction(1, 3)", "fractions.Fraction("),
            ("Fraction.from_float(0.5)", "fractions.Fraction.from_float("),
            ("Fraction.from_decimal(d)", "fractions.Fraction.from_decimal("),
            ("gcd(a, b)", "fractions.gcd("),
        ]
        for name, func in fractions_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            fractions_menu.addAction(action)

    def setup_constants_menu(self, menubar):
        """Setup the Constants menu"""
        constants_menu = menubar.addMenu("Constants")
        # Mathematical constants
        math_constants = [
            ("π (pi)", "math.pi"),
            ("e (Euler's number)", "math.e"),
            ("τ (tau = 2π)", "math.tau"),
            ("∞ (infinity)", "math.inf"),
            ("NaN", "math.nan"),
        ]
        for name, const in math_constants:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, c=const: self.insert_function(c))
            constants_menu.addAction(action)
        # NumPy constants
        if 'np' in self.base_namespace:
            constants_menu.addSeparator()
            numpy_constants = [
                ("np.pi", "np.pi"),
                ("np.e", "np.e"),
                ("np.inf", "np.inf"),
                ("np.nan", "np.nan"),
            ]
            for name, const in numpy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)
        # SymPy constants
        if 'sym' in self.base_namespace:
            constants_menu.addSeparator()
            sympy_constants = [
                ("sym.pi", "sym.pi"),
                ("sym.E", "sym.E"),
                ("sym.I (imaginary unit)", "sym.I"),
                ("sym.oo (infinity)", "sym.oo"),
                ("sym.zoo (complex infinity)", "sym.zoo"),
            ]
            for name, const in sympy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)

    def setup_toolbar(self):
        """Setup the toolbar with quick actions"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Quick function buttons
        functions = [
            ("π", "math.pi"),
            ("e", "math.e"),
            ("sin", "math.sin("),
            ("cos", "math.cos("),
            ("tan", "math.tan("),
            ("√", "math.sqrt("),
            ("log", "math.log("),
            ("ln", "math.log("),
            ("x²", "**2"),
            ("x^y", "**")
        ]
        
        for name, func in functions:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, f=func: self.insert_function(f))
            toolbar.addWidget(btn)
        
    def setup_math_menu(self, menubar):
        """Setup the Math Functions menu"""
        math_menu = menubar.addMenu("Math")
        
        # Trigonometric functions
        trig_menu = math_menu.addMenu("Trigonometric")
        trig_functions = [
            ("sin(x)", "math.sin("),
            ("cos(x)", "math.cos("),
            ("tan(x)", "math.tan("),
            ("asin(x)", "math.asin("),
            ("acos(x)", "math.acos("),
            ("atan(x)", "math.atan("),
            ("atan2(y,x)", "math.atan2("),
            ("sinh(x)", "math.sinh("),
            ("cosh(x)", "math.cosh("),
            ("tanh(x)", "math.tanh("),
            ("asinh(x)", "math.asinh("),
            ("acosh(x)", "math.acosh("),
            ("atanh(x)", "math.atanh("),
        ]
        for name, func in trig_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            trig_menu.addAction(action)
        
        # Logarithmic and exponential
        log_menu = math_menu.addMenu("Logarithmic & Exponential")
        log_functions = [
            ("exp(x)", "math.exp("),
            ("log(x)", "math.log("),
            ("log10(x)", "math.log10("),
            ("log2(x)", "math.log2("),
            ("log(x, base)", "math.log("),
            ("pow(x, y)", "math.pow("),
            ("sqrt(x)", "math.sqrt("),
        ]
        for name, func in log_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            log_menu.addAction(action)
        
        # Number theory and utilities
        util_menu = math_menu.addMenu("Number Theory & Utilities")
        util_functions = [
            ("abs(x)", "abs("),
            ("ceil(x)", "math.ceil("),
            ("floor(x)", "math.floor("),
            ("round(x)", "round("),
            ("trunc(x)", "math.trunc("),
            ("fabs(x)", "math.fabs("),
            ("gcd(a, b)", "math.gcd("),
            ("lcm(a, b)", "math.lcm("),
            ("factorial(x)", "math.factorial("),
            ("comb(n, k)", "math.comb("),
            ("perm(n, k)", "math.perm("),
        ]
        for name, func in util_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            util_menu.addAction(action)
        
        # Special functions
        special_menu = math_menu.addMenu("Special Functions")
        special_functions = [
            ("gamma(x)", "math.gamma("),
            ("lgamma(x)", "math.lgamma("),
            ("erf(x)", "math.erf("),
            ("erfc(x)", "math.erfc("),
            ("degrees(x)", "math.degrees("),
            ("radians(x)", "math.radians("),
        ]
        for name, func in special_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            special_menu.addAction(action)
    
    def setup_random_menu(self, menubar):
        """Setup the Random menu"""
        random_menu = menubar.addMenu("Random")
        random_functions = [
            ("random()", "random.random()"),
            ("randint(a, b)", "random.randint("),
            ("uniform(a, b)", "random.uniform("),
            ("choice(seq)", "random.choice("),
            ("shuffle(seq)", "random.shuffle("),
            ("sample(seq, k)", "random.sample("),
            ("seed(n)", "random.seed("),
        ]
        for name, func in random_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            random_menu.addAction(action)

    def setup_statistics_menu(self, menubar):
        """Setup the Statistics menu"""
        stats_menu = menubar.addMenu("Statistics")
        stats_functions = [
            ("mean(data)", "statistics.mean("),
            ("median(data)", "statistics.median("),
            ("mode(data)", "statistics.mode("),
            ("stdev(data)", "statistics.stdev("),
            ("variance(data)", "statistics.variance("),
            ("harmonic_mean(data)", "statistics.harmonic_mean("),
            ("multimode(data)", "statistics.multimode("),
        ]
        for name, func in stats_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            stats_menu.addAction(action)

    def setup_cmath_menu(self, menubar):
        """Setup the Complex Math menu"""
        cmath_menu = menubar.addMenu("Complex Math (cmath)")
        cmath_functions = [
            ("sqrt(z)", "cmath.sqrt("),
            ("exp(z)", "cmath.exp("),
            ("log(z)", "cmath.log("),
            ("sin(z)", "cmath.sin("),
            ("cos(z)", "cmath.cos("),
            ("tan(z)", "cmath.tan("),
            ("phase(z)", "cmath.phase("),
            ("polar(z)", "cmath.polar("),
            ("rect(r, phi)", "cmath.rect("),
        ]
        for name, func in cmath_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            cmath_menu.addAction(action)

    def setup_decimal_menu(self, menubar):
        """Setup the Decimal menu"""
        decimal_menu = menubar.addMenu("Decimal")
        decimal_functions = [
            ("Decimal('0.1')", "decimal.Decimal('"),
            ("getcontext()", "decimal.getcontext()"),
            ("setcontext(ctx)", "decimal.setcontext("),
            ("localcontext()", "decimal.localcontext()"),
        ]
        for name, func in decimal_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            decimal_menu.addAction(action)

    def setup_fractions_menu(self, menubar):
        """Setup the Fractions menu"""
        fractions_menu = menubar.addMenu("Fractions")
        fractions_functions = [
            ("Fraction(1, 3)", "fractions.Fraction("),
            ("Fraction.from_float(0.5)", "fractions.Fraction.from_float("),
            ("Fraction.from_decimal(d)", "fractions.Fraction.from_decimal("),
            ("gcd(a, b)", "fractions.gcd("),
        ]
        for name, func in fractions_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            fractions_menu.addAction(action)

    def setup_constants_menu(self, menubar):
        """Setup the Constants menu"""
        constants_menu = menubar.addMenu("Constants")
        # Mathematical constants
        math_constants = [
            ("π (pi)", "math.pi"),
            ("e (Euler's number)", "math.e"),
            ("τ (tau = 2π)", "math.tau"),
            ("∞ (infinity)", "math.inf"),
            ("NaN", "math.nan"),
        ]
        for name, const in math_constants:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, c=const: self.insert_function(c))
            constants_menu.addAction(action)
        # NumPy constants
        if 'np' in self.base_namespace:
            constants_menu.addSeparator()
            numpy_constants = [
                ("np.pi", "np.pi"),
                ("np.e", "np.e"),
                ("np.inf", "np.inf"),
                ("np.nan", "np.nan"),
            ]
            for name, const in numpy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)
        # SymPy constants
        if 'sym' in self.base_namespace:
            constants_menu.addSeparator()
            sympy_constants = [
                ("sym.pi", "sym.pi"),
                ("sym.E", "sym.E"),
                ("sym.I (imaginary unit)", "sym.I"),
                ("sym.oo (infinity)", "sym.oo"),
                ("sym.zoo (complex infinity)", "sym.zoo"),
            ]
            for name, const in sympy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)

    def setup_toolbar(self):
        """Setup the toolbar with quick actions"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Quick function buttons
        functions = [
            ("π", "math.pi"),
            ("e", "math.e"),
            ("sin", "math.sin("),
            ("cos", "math.cos("),
            ("tan", "math.tan("),
            ("√", "math.sqrt("),
            ("log", "math.log("),
            ("ln", "math.log("),
            ("x²", "**2"),
            ("x^y", "**")
        ]
        
        for name, func in functions:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, f=func: self.insert_function(f))
            toolbar.addWidget(btn)
        
    def setup_math_menu(self, menubar):
        """Setup the Math Functions menu"""
        math_menu = menubar.addMenu("Math")
        
        # Trigonometric functions
        trig_menu = math_menu.addMenu("Trigonometric")
        trig_functions = [
            ("sin(x)", "math.sin("),
            ("cos(x)", "math.cos("),
            ("tan(x)", "math.tan("),
            ("asin(x)", "math.asin("),
            ("acos(x)", "math.acos("),
            ("atan(x)", "math.atan("),
            ("atan2(y,x)", "math.atan2("),
            ("sinh(x)", "math.sinh("),
            ("cosh(x)", "math.cosh("),
            ("tanh(x)", "math.tanh("),
            ("asinh(x)", "math.asinh("),
            ("acosh(x)", "math.acosh("),
            ("atanh(x)", "math.atanh("),
        ]
        for name, func in trig_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            trig_menu.addAction(action)
        
        # Logarithmic and exponential
        log_menu = math_menu.addMenu("Logarithmic & Exponential")
        log_functions = [
            ("exp(x)", "math.exp("),
            ("log(x)", "math.log("),
            ("log10(x)", "math.log10("),
            ("log2(x)", "math.log2("),
            ("log(x, base)", "math.log("),
            ("pow(x, y)", "math.pow("),
            ("sqrt(x)", "math.sqrt("),
        ]
        for name, func in log_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            log_menu.addAction(action)
        
        # Number theory and utilities
        util_menu = math_menu.addMenu("Number Theory & Utilities")
        util_functions = [
            ("abs(x)", "abs("),
            ("ceil(x)", "math.ceil("),
            ("floor(x)", "math.floor("),
            ("round(x)", "round("),
            ("trunc(x)", "math.trunc("),
            ("fabs(x)", "math.fabs("),
            ("gcd(a, b)", "math.gcd("),
            ("lcm(a, b)", "math.lcm("),
            ("factorial(x)", "math.factorial("),
            ("comb(n, k)", "math.comb("),
            ("perm(n, k)", "math.perm("),
        ]
        for name, func in util_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            util_menu.addAction(action)
        
        # Special functions
        special_menu = math_menu.addMenu("Special Functions")
        special_functions = [
            ("gamma(x)", "math.gamma("),
            ("lgamma(x)", "math.lgamma("),
            ("erf(x)", "math.erf("),
            ("erfc(x)", "math.erfc("),
            ("degrees(x)", "math.degrees("),
            ("radians(x)", "math.radians("),
        ]
        for name, func in special_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            special_menu.addAction(action)
    
    def setup_random_menu(self, menubar):
        """Setup the Random menu"""
        random_menu = menubar.addMenu("Random")
        random_functions = [
            ("random()", "random.random()"),
            ("randint(a, b)", "random.randint("),
            ("uniform(a, b)", "random.uniform("),
            ("choice(seq)", "random.choice("),
            ("shuffle(seq)", "random.shuffle("),
            ("sample(seq, k)", "random.sample("),
            ("seed(n)", "random.seed("),
        ]
        for name, func in random_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            random_menu.addAction(action)

    def setup_statistics_menu(self, menubar):
        """Setup the Statistics menu"""
        stats_menu = menubar.addMenu("Statistics")
        stats_functions = [
            ("mean(data)", "statistics.mean("),
            ("median(data)", "statistics.median("),
            ("mode(data)", "statistics.mode("),
            ("stdev(data)", "statistics.stdev("),
            ("variance(data)", "statistics.variance("),
            ("harmonic_mean(data)", "statistics.harmonic_mean("),
            ("multimode(data)", "statistics.multimode("),
        ]
        for name, func in stats_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            stats_menu.addAction(action)

    def setup_cmath_menu(self, menubar):
        """Setup the Complex Math menu"""
        cmath_menu = menubar.addMenu("Complex Math (cmath)")
        cmath_functions = [
            ("sqrt(z)", "cmath.sqrt("),
            ("exp(z)", "cmath.exp("),
            ("log(z)", "cmath.log("),
            ("sin(z)", "cmath.sin("),
            ("cos(z)", "cmath.cos("),
            ("tan(z)", "cmath.tan("),
            ("phase(z)", "cmath.phase("),
            ("polar(z)", "cmath.polar("),
            ("rect(r, phi)", "cmath.rect("),
        ]
        for name, func in cmath_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            cmath_menu.addAction(action)

    def setup_decimal_menu(self, menubar):
        """Setup the Decimal menu"""
        decimal_menu = menubar.addMenu("Decimal")
        decimal_functions = [
            ("Decimal('0.1')", "decimal.Decimal('"),
            ("getcontext()", "decimal.getcontext()"),
            ("setcontext(ctx)", "decimal.setcontext("),
            ("localcontext()", "decimal.localcontext()"),
        ]
        for name, func in decimal_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            decimal_menu.addAction(action)

    def setup_fractions_menu(self, menubar):
        """Setup the Fractions menu"""
        fractions_menu = menubar.addMenu("Fractions")
        fractions_functions = [
            ("Fraction(1, 3)", "fractions.Fraction("),
            ("Fraction.from_float(0.5)", "fractions.Fraction.from_float("),
            ("Fraction.from_decimal(d)", "fractions.Fraction.from_decimal("),
            ("gcd(a, b)", "fractions.gcd("),
        ]
        for name, func in fractions_functions:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, f=func: self.insert_function(f))
            fractions_menu.addAction(action)

    def setup_constants_menu(self, menubar):
        """Setup the Constants menu"""
        constants_menu = menubar.addMenu("Constants")
        # Mathematical constants
        math_constants = [
            ("π (pi)", "math.pi"),
            ("e (Euler's number)", "math.e"),
            ("τ (tau = 2π)", "math.tau"),
            ("∞ (infinity)", "math.inf"),
            ("NaN", "math.nan"),
        ]
        for name, const in math_constants:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, c=const: self.insert_function(c))
            constants_menu.addAction(action)
        # NumPy constants
        if 'np' in self.base_namespace:
            constants_menu.addSeparator()
            numpy_constants = [
                ("np.pi", "np.pi"),
                ("np.e", "np.e"),
                ("np.inf", "np.inf"),
                ("np.nan", "np.nan"),
            ]
            for name, const in numpy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)
        # SymPy constants
        if 'sym' in self.base_namespace:
            constants_menu.addSeparator()
            sympy_constants = [
                ("sym.pi", "sym.pi"),
                ("sym.E", "sym.E"),
                ("sym.I (imaginary unit)", "sym.I"),
                ("sym.oo (infinity)", "sym.oo"),
                ("sym.zoo (complex infinity)", "sym.zoo"),
            ]
            for name, const in sympy_constants:
                action = QAction(name, self)
                action.triggered.connect(lambda checked, c=const: self.insert_function(c))
                constants_menu.addAction(action)

    def setup_toolbar(self):
        """Setup the toolbar with quick actions"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Quick function buttons
        functions = [
            ("π", "math.pi"),
            ("e", "math.e"),
            ("sin", "math.sin("),
            ("cos", "math.cos("),
            ("tan", "math.tan("),
            ("√", "math.sqrt("),
            ("log", "math.log("),
            ("ln", "math.log("),
            ("x²", "**2"),
            ("x^y", "**")
        ]
        
        for name, func in functions:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, f=func: self.insert_function(f))
            toolbar.addWidget(btn)
        
    def new_document(self):
        """Create a new document tab"""
        tab_count = self.tab_widget.count()
        title = f"Document {tab_count + 1}"
        self.create_new_document(title)
    
    def undo_action(self):
        """Undo last action in current editor"""
        editor = self.get_current_editor()
        if editor:
            editor.undo()
    
    def redo_action(self):
        """Redo last action in current editor"""
        editor = self.get_current_editor()
        if editor:
            editor.redo()
    
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
        try:
            from panel_config_manager import PanelConfigManager, PanelLayoutDialog
            
            # Initialize config manager if not exists
            if not hasattr(self, 'panel_config_manager'):
                self.panel_config_manager = PanelConfigManager()
            
            # Create and show dialog
            layout_dialog = PanelLayoutDialog(self, self.panel_config_manager)
            layout_dialog.show_layout_config()
            
        except ImportError:
            QMessageBox.warning(self, "Error", 
                              "Panel configuration manager not available. "
                              "Please ensure panel_config_manager.py is in the same directory.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to open panel configuration: {e}")
    
    def reload_panel_layout(self):
        """Reload panel layout based on configuration"""
        try:
            if not hasattr(self, 'panel_config_manager'):
                from panel_config_manager import PanelConfigManager
                self.panel_config_manager = PanelConfigManager()
            
            layout = self.panel_config_manager.get_panel_layout()
            self.apply_panel_layout(layout)
            
        except Exception as e:
            print(f"Error reloading panel layout: {e}")
    
    def apply_panel_layout(self, layout):
        """Apply a panel layout configuration"""
        # This is a simplified version - you can expand this based on your needs
        for position, config in layout.items():
            panel_name = config.get("panel")
            visible = config.get("visible", False)
            
            if panel_name and visible:
                # Show/hide panels based on configuration
                if panel_name == "history" and hasattr(self, 'history_dock'):
                    self.history_dock.setVisible(True)
                elif panel_name == "functions" and hasattr(self, 'functions_dock'):
                    self.functions_dock.setVisible(True)
                elif panel_name == "graph" and hasattr(self, 'graph_dock'):
                    self.graph_dock.setVisible(True)
                elif panel_name == "variables" and hasattr(self, 'variables_dock'):
                    self.variables_dock.setVisible(True)
    
    def apply_panel_styling(self, panel_name):
        """Apply styling to a specific panel"""
        try:
            if not hasattr(self, 'panel_config_manager'):
                from panel_config_manager import PanelConfigManager
                self.panel_config_manager = PanelConfigManager()
            
            stylesheet = self.panel_config_manager.generate_qt_stylesheet(panel_name)
            
            # Apply stylesheet to appropriate dock widget
            if panel_name == "history" and hasattr(self, 'history_dock'):
                self.history_dock.setStyleSheet(stylesheet)
            elif panel_name == "functions" and hasattr(self, 'functions_dock'):
                self.functions_dock.setStyleSheet(stylesheet)
            elif panel_name == "graph" and hasattr(self, 'graph_dock'):
                self.graph_dock.setStyleSheet(stylesheet)
            elif panel_name == "variables" and hasattr(self, 'variables_dock'):
                self.variables_dock.setStyleSheet(stylesheet)
                
        except Exception as e:
            print(f"Error applying panel styling for {panel_name}: {e}")
    
    def load_panel_configuration(self):
        """Load and apply panel configuration on startup"""
        try:
            from panel_config_manager import PanelConfigManager
            self.panel_config_manager = PanelConfigManager()
            
            # Apply layout
            layout = self.panel_config_manager.get_panel_layout()
            self.apply_panel_layout(layout)
            
            # Apply styling to all panels
            for panel_name in self.panel_config_manager.get_available_panels():
                self.apply_panel_styling(panel_name)
                
        except Exception as e:
            print(f"Error loading panel configuration: {e}")
    
    def insert_custom_function(self, name, code):
        """Insert custom function into current editor"""
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.insertText(f"{name}(")
            editor.setFocus()
    
    def insert_function(self, function_text):
        """Insert function or constant into current editor"""
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.insertText(function_text)
            editor.setFocus()
    
    def insert_conversion_result(self, result):
        """Insert conversion result into current editor"""
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.insertText(result)
            editor.setFocus()
    
    def restore_from_history(self, expression):
        """Restore calculation from history"""
        editor = self.get_current_editor()
        if editor:
            cursor = editor.textCursor()
            cursor.insertText(expression + "\n")
            editor.setFocus()
    
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
    
    def clear_variables(self):
        """Clear all variables"""
        self.variables.clear()
        self.namespace = self.base_namespace.copy()
        self.variables_widget.update_variables({})
        # Clear line results and recalculate
        editor = self.get_current_editor()
        if editor:
            self.recalculate_all(editor)
    
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
    
    def apply_custom_theme(self, theme_data):
        """Apply custom theme from theme customizer"""
        try:
            colors = theme_data['colors']
            font = theme_data['font']
            font_size = theme_data['font_size']
            
            # Validate font
            if not isinstance(font, QFont):
                font = QFont("Monaco", 12)
            
            # Update current settings
            self.text_font = font
            self.text_font.setPointSize(font_size)
            self.bg_color = colors['bg']
            self.text_color = colors['text']
            
            # Apply styling
            self.apply_styling()
            
            # Update all editors
            for i in range(self.tab_widget.count()):
                widget = self.tab_widget.widget(i)
                if widget and hasattr(widget, 'editor'):
                    editor = widget.editor
                    editor.setFont(self.text_font)
                    
                    # Apply custom styling
                    editor.setStyleSheet(f"""
                        QPlainTextEdit {{
                            background-color: {colors['bg'].name()};
                            color: {colors['text'].name()};
                            border: 1px solid #3c3c3c;
                            line-height: 1.4;
                            padding: 10px;
                            selection-background-color: #264f78;
                            selection-color: white;
                        }}
                    """)
                    
                    # Update highlighter with custom colors
                    if hasattr(widget, 'highlighter'):
                        widget.highlighter.setup_custom_theme(colors)
        except Exception as e:
            print(f"Error applying custom theme: {e}")
            QMessageBox.warning(self, "Theme Error", f"Failed to apply theme: {e}")
    
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
        
        results_lines = []
        
        # Process lines to handle multi-line statements
        processed_lines = self.process_multiline_statements(lines)
        
        for item in processed_lines:
            line_num = item['line_num']
            code_block = item['code']
            is_multiline = item['is_multiline']
            
            if not code_block.strip() or code_block.strip().startswith('#'):
                results_lines.append("")
                continue
                
            try:
                # Update namespace with current variables
                self.namespace.update(self.variables)
                
                if is_multiline:
                    # Execute multi-line code block
                    result = self.execute_multiline_code(code_block)
                    if result is not None:
                        formatted_result = self.format_result(result)
                        self.line_results[line_num] = formatted_result
                        results_lines.append(f"= {formatted_result}")
                        
                        # Add to history
                        self.history_widget.add_calculation(code_block, formatted_result)
                    else:
                        self.line_results[line_num] = "executed"
                        results_lines.append("✓ executed")
                else:
                    # Handle single line as before
                    if '=' in code_block and not any(op in code_block.split('=')[0] for op in ['==', '!=', '<=', '>=']):
                        # Variable assignment
                        var_name = code_block.split('=')[0].strip()
                        var_expression = code_block.split('=', 1)[1].strip()
                        
                        # Evaluate the right side
                        result = eval(var_expression, {"__builtins__": {}}, self.namespace)
                        self.variables[var_name] = result
                        self.namespace[var_name] = result
                        
                        # Format and store result
                        formatted_result = self.format_result(result)
                        self.line_results[line_num] = f"{var_name} = {formatted_result}"
                        results_lines.append(f"= {formatted_result}")
                        
                        # Add to history
                        self.history_widget.add_calculation(code_block, formatted_result)
                        
                    else:
                        # Regular expression evaluation
                        result = eval(code_block, {"__builtins__": {}}, self.namespace)
                        formatted_result = self.format_result(result)
                        self.line_results[line_num] = formatted_result
                        results_lines.append(f"= {formatted_result}")
                        
                        # Add to history
                        self.history_widget.add_calculation(code_block, formatted_result)
                        
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.line_results[line_num] = error_msg
                results_lines.append(f"❌ {str(e)}")
        
        # Update inline results in code editor
        self.update_inline_results(editor)
        self.update_variables_display()
    
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
    
    def process_multiline_statements(self, lines):
        """Process lines to handle multi-line statements"""
        processed = []
        current_block = ""
        block_start = 0
        indent_level = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                if current_block:
                    current_block += line + "\n"
                else:
                    processed.append({
                        'line_num': i,
                        'code': line,
                        'is_multiline': False
                    })
                continue
            
            # Check for multi-line indicators
            if (stripped.endswith(':') or 
                any(stripped.startswith(kw) for kw in ['def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ', 'elif ', 'else:']) or
                indent_level > 0):
                
                if not current_block:
                    block_start = i
                current_block += line + "\n"
                
                # Update indent level
                if stripped.endswith(':'):
                    indent_level += 1
                elif line.startswith('    ') or line.startswith('\t'):
                    pass  # Keep current indent level
                else:
                    indent_level = max(0, indent_level - 1)
                
                # If we're back to base level, end the block
                if indent_level == 0 and not stripped.endswith(':'):
                    processed.append({
                        'line_num': block_start,
                        'code': current_block.strip(),
                        'is_multiline': True
                    })
                    current_block = ""
            else:
                # Single line statement
                if current_block:
                    # Finish previous block first
                    processed.append({
                        'line_num': block_start,
                        'code': current_block.strip(),
                        'is_multiline': True
                    })
                    current_block = ""
                
                # Add single line
                processed.append({
                    'line_num': i,
                    'code': line,
                    'is_multiline': False
                })
        
        # Handle any remaining block
        if current_block:
            processed.append({
                'line_num': block_start,
                'code': current_block.strip(),
                'is_multiline': True
            })
        
        return processed
    
    def execute_multiline_code(self, code_block):
        """Execute multi-line code block"""
        try:
            # Try to compile and execute the code
            compiled_code = compile(code_block, '<calculator>', 'exec')
            
            # Create a local namespace for execution
            local_ns = {}
            exec(compiled_code, self.namespace, local_ns)
            
            # Update variables with any new assignments
            self.variables.update(local_ns)
            
            # Check if the last line is an expression (return its value)
            lines = code_block.strip().split('\n')
            last_line = lines[-1].strip()
            
            # Try to evaluate the last line as an expression
            if last_line and not any(last_line.startswith(kw) for kw in 
                                   ['def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ', 'elif ', 'else:', 'return ', 'yield ', 'import ', 'from ']):
                try:
                    result = eval(last_line, self.namespace, local_ns)
                    return result
                except:
                    pass
            
            return None
            
        except Exception as e:
            raise e
    
    def format_result(self, result):
        """Format calculation result for display"""
        if result is None:
            return "None"
        
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
        elif hasattr(result, '__iter__') and not isinstance(result, str):
            # Handle arrays, lists, tuples
            try:
                if len(result) > 10:
                    # Show first few elements for large arrays
                    preview = list(result[:3])
                    return f"[{', '.join(self.format_result(x) for x in preview)}, ... ({len(result)} items)]"
                else:
                    return f"[{', '.join(self.format_result(x) for x in result)}]"
            except:
                return str(result)
        else:
            # For other types, just convert to string
            result_str = str(result)
            if len(result_str) > 200:
                return result_str[:200] + "..."
            return result_str
    
    def highlight_current_line_result(self, line_number):
        """Highlight the result for the current line"""
        # This is a placeholder for highlighting functionality
        # Could be implemented to show the current line's result more prominently
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
    
    def open_settings(self):
        """Open settings dialog"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QColorDialog, QFontDialog, QComboBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # Font selection
        font_layout = QHBoxLayout()
        font_label = QLabel("Font:")
        font_button = QPushButton(f"{self.text_font.family()} {self.text_font.pointSize()}pt")
        def choose_font():
            font, ok = QFontDialog.getFont(self.text_font, self)
            if ok:
                self.text_font = font
                font_button.setText(f"{font.family()} {font.pointSize()}pt")
        font_button.clicked.connect(choose_font)
        font_layout.addWidget(font_label)
        font_layout.addWidget(font_button)
        layout.addLayout(font_layout)
        
        # Precision setting
        precision_layout = QHBoxLayout()
        precision_label = QLabel("Decimal Precision:")
        precision_spin = QSpinBox()
        precision_spin.setRange(1, 15)
        precision_spin.setValue(self.decimal_precision)
        precision_layout.addWidget(precision_label)
        precision_layout.addWidget(precision_spin)
        layout.addLayout(precision_layout)
        
        # Theme selection
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_combo = QComboBox()
        theme_combo.addItems(["Default", "Dark", "Light"])
        theme_combo.setCurrentText(self.theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(theme_combo)
        layout.addLayout(theme_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        def accept_settings():
            self.decimal_precision = precision_spin.value()
            self.theme = theme_combo.currentText()
            self.apply_styling()
            self.save_settings()
            dialog.accept()
        
        ok_button.clicked.connect(accept_settings)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.exec()
    
    def apply_styling(self):
        """Apply current styling settings to the interface"""
        # Apply styling to all document editors
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if widget and hasattr(widget, 'editor'):
                editor = widget.editor
                editor.setFont(self.text_font)
                
                if self.theme == "dark":
                    # Dark theme with VS Code-like colors
                    editor.setStyleSheet(f"""
                        QPlainTextEdit {{
                            background-color: #1e1e1e;
                            color: #d4d4d4;
                            border: 1px solid #3c3c3c;
                            line-height: 1.4;
                            padding: 10px;
                            selection-background-color: #264f78;
                            selection-color: white;
                        }}
                    """)
                    # Reset highlighter to dark theme
                    if hasattr(widget, 'highlighter'):
                        widget.highlighter.setup_highlighting_rules()
                else:
                    # Light theme with custom colors
                    editor.setStyleSheet(f"""
                        QPlainTextEdit {{
                            background-color: {self.bg_color.name()};
                            color: {self.text_color.name()};
                            border: 1px solid #ccc;
                            line-height: 1.4;
                            padding: 10px;
                            selection-background-color: #3399ff;
                            selection-color: white;
                        }}
                    """)
                    # Update highlighter to light theme
                    if hasattr(widget, 'highlighter'):
                        widget.highlighter.setup_light_theme()
                
                # Force rehighlighting
                if hasattr(widget, 'highlighter'):
                    widget.highlighter.rehighlight()
        
        # Variables display styling in AI panel
        if hasattr(self, 'ai_panel') and self.ai_panel:
            self.ai_panel.variables_display.setFont(self.text_font)
            self.ai_panel.variables_display.setStyleSheet(f"""
                QTextEdit {{
                    background-color: #f0f0f0;
                    color: #333;
                    border: 1px solid #ccc;
                    line-height: 1.2;
                    padding: 5px;
                    font-size: 9pt;
                }}
            """)
        
    def update_highlighter_theme(self):
        """Update syntax highlighter colors based on current theme"""
        if hasattr(self, 'highlighter'):
            if self.theme == "dark":
                # Already set up for dark theme in the highlighter
                pass
            else:
                # Update highlighter for light theme
                self.highlighter.setup_light_theme()
    
    def show_help(self):
        """Show the help dialog"""
        help_dialog = HelpDialog(self)
        help_dialog.exec()
        
    def print_document(self):
        """Print the document and results"""
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            # Create a combined document for printing
            combined_text = "Mathematical Document with Inline Results\n" + "="*50 + "\n\n"
            
            doc_lines = self.document_editor.toPlainText().split('\n')
            
            for i, line in enumerate(doc_lines):
                if line.strip():
                    line_result = ""
                    if i in self.line_results:
                        line_result = f" = {self.line_results[i]}"
                    combined_text += f"Line {i+1:2d}: {line}{line_result}\n"
                else:
                    combined_text += f"Line {i+1:2d}: {line}\n"
            
            if self.variables:
                combined_text += "\nVariables:\n" + "-"*20 + "\n"
                for var, value in self.variables.items():
                    combined_text += f"{var} = {self.format_result(value)}\n"
            
            # Print the combined document
            text_document = QTextDocument()
            text_document.setPlainText(combined_text)
            text_document.print(printer)


class HistoryPanel(QWidget):
    """Widget for displaying calculation history"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_calculator = parent
        self.setup_ui()
        self.history = []
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_label = QLabel("Calculation History")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(header_label)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.restore_calculation)
        layout.addWidget(self.history_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_history)
        
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.export_history)
        
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
    
    def add_calculation(self, expression, result):
        """Add a calculation to the history"""
        timestamp = QTimer().remainingTime()  # Simple timestamp
        history_item = {
            'expression': expression,
            'result': result,
            'timestamp': timestamp
        }
        
        self.history.append(history_item)
        
        # Update list widget
        display_text = f"{expression} = {result}"
        if len(display_text) > 60:
            display_text = display_text[:57] + "..."
            
        list_item = QListWidgetItem(display_text)
        list_item.setData(Qt.ItemDataRole.UserRole, history_item)
        self.history_list.addItem(list_item)
        
        # Keep only last 100 items
        if self.history_list.count() > 100:
            self.history_list.takeItem(0)
            self.history.pop(0)
    
    def restore_calculation(self, item):
        """Restore a calculation from history to the current editor"""
        history_item = item.data(Qt.ItemDataRole.UserRole)
        if history_item and self.parent_calculator:
            self.parent_calculator.restore_from_history(history_item['expression'])
    
    def clear_history(self):
        """Clear all history"""
        self.history.clear()
        self.history_list.clear()
    
    def export_history(self):
        """Export history to a text file"""
        if not self.history:
            QMessageBox.information(self, "Export History", "No calculations to export.")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export History", "calculation_history.txt", "Text Files (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Calculator History\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for item in self.history:
                        f.write(f"{item['expression']} = {item['result']}\n")
                
                QMessageBox.information(self, "Export Complete", f"History exported to {filename}")
                
            except Exception as e:
                QMessageBox.warning(self, "Export Error", f"Failed to export history: {e}")


class CustomFunctionLibrary(QWidget):
    """Widget for managing custom functions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.functions = {}
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Custom Functions"))
        
        self.add_function_btn = QPushButton("Add Function")
        self.add_function_btn.clicked.connect(self.add_function)
        header_layout.addWidget(self.add_function_btn)
        
        layout.addLayout(header_layout)
        
        # Functions list
        self.functions_list = QListWidget()
        self.functions_list.itemDoubleClicked.connect(self.insert_function)
        layout.addWidget(self.functions_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.insert_btn = QPushButton("Insert")
        
        self.edit_btn.clicked.connect(self.edit_function)
        self.delete_btn.clicked.connect(self.delete_function)
        self.insert_btn.clicked.connect(self.insert_selected_function)
        
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.insert_btn)
        
        layout.addLayout(btn_layout)
        
    def add_function(self):
        """Add a new custom function"""
        dialog = CustomFunctionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.name_input.text().strip()
            code = dialog.code_input.toPlainText().strip()
            description = dialog.desc_input.text().strip()
            
            if name and code:
                self.functions[name] = {'code': code, 'description': description}
                self.refresh_list()
    
    def edit_function(self):
        """Edit selected function"""
        current_item = self.functions_list.currentItem()
        if current_item:
            name = current_item.text().split(' - ')[0]
            if name in self.functions:
                dialog = CustomFunctionDialog(self)
                dialog.name_input.setText(name)
                dialog.code_input.setPlainText(self.functions[name]['code'])
                dialog.desc_input.setText(self.functions[name]['description'])
                
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    new_name = dialog.name_input.text().strip()
                    code = dialog.code_input.toPlainText().strip()
                    description = dialog.desc_input.text().strip()
                    
                    if new_name and code:
                        if new_name != name:
                            del self.functions[name]
                        self.functions[new_name] = {'code': code, 'description': description}
                        self.refresh_list()
    
    def delete_function(self):
        """Delete selected function"""
        current_item = self.functions_list.currentItem()
        if current_item:
            name = current_item.text().split(' - ')[0]
            if name in self.functions:
                del self.functions[name]
                self.refresh_list()
    
    def insert_selected_function(self):
        """Insert selected function into editor"""
        current_item = self.functions_list.currentItem()
        if current_item:
            name = current_item.text().split(' - ')[0]
            self.insert_function(current_item)
    
    def insert_function(self, item):
        """Insert function into the main editor"""
        name = item.text().split(' - ')[0]
        if name in self.functions and hasattr(self.parent(), 'insert_custom_function'):
            self.parent().insert_custom_function(name, self.functions[name]['code'])
    
    def refresh_list(self):
        """Refresh the functions list"""
        self.functions_list.clear()
        for name, func_data in self.functions.items():
            desc = func_data.get('description', '')
            display_text = f"{name} - {desc}" if desc else name
            self.functions_list.addItem(display_text)


class CustomFunctionDialog(QDialog):
    """Dialog for adding/editing custom functions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Function")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Form
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Function name (e.g., my_func)")
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Description (optional)")
        
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("def my_func(x):\n    return x**2 + 1")
        
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.desc_input)
        form_layout.addRow("Code:", self.code_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class UnitConverterDialog(QDialog):
    """Dialog for unit conversions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Unit Converter")
        self.setModal(True)
        self.resize(400, 300)
        self.setup_ui()
        self.setup_conversions()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Category selection
        self.category_combo = QComboBox()
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_combo)
        
        # From/To selection
        from_layout = QHBoxLayout()
        self.from_combo = QComboBox()
        self.from_value = QLineEdit("1")
        from_layout.addWidget(QLabel("From:"))
        from_layout.addWidget(self.from_combo)
        from_layout.addWidget(self.from_value)
        layout.addLayout(from_layout)
        
        to_layout = QHBoxLayout()
        self.to_combo = QComboBox()
        self.to_value = QLineEdit()
        self.to_value.setReadOnly(True)
        to_layout.addWidget(QLabel("To:"))
        to_layout.addWidget(self.to_combo)
        to_layout.addWidget(self.to_value)
        layout.addLayout(to_layout)
        
        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert)
        layout.addWidget(self.convert_btn)
        
        # Insert button
        self.insert_btn = QPushButton("Insert Result")
        self.insert_btn.clicked.connect(self.insert_result)
        layout.addWidget(self.insert_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        # Connect signals
        self.category_combo.currentTextChanged.connect(self.update_units)
        self.from_value.textChanged.connect(self.convert)
        self.from_combo.currentTextChanged.connect(self.convert)
        self.to_combo.currentTextChanged.connect(self.convert)
        
    def setup_conversions(self):
        """Setup conversion factors"""
        self.conversions = {
           
           
            "Length": {
                "meter": 1.0,
                "kilometer": 1000.0,
                "centimeter": 0.01,
                "millimeter": 0.001,
                "inch": 0.0254,
                "foot": 0.3048,
                "yard": 0.9144,
                "mile": 1609.344,
            },
            "Mass": {
                "kilogram": 1.0,
                "gram": 0.001,
                "pound": 0.453592,
                "ounce": 0.0283495,
                "ton": 1000.0,
            },
            "Temperature": {
                "celsius": 1.0,
                "fahrenheit": 1.0,
                "kelvin": 1.0,
            },
            "Area": {
                "square_meter": 1.0,
                "square_kilometer": 1000000.0,
                "square_centimeter": 0.0001,
                "square_inch": 0.00064516,
                "square_foot": 0.092903,
                "acre": 4046.86,
            },
            "Volume": {
                "liter": 1.0,
                "milliliter": 0.001,
                "gallon": 3.78541,
                "quart": 0.946353,
                "pint": 0.473176,
                "cup": 0.236588,
                "fluid_ounce": 0.0295735,
            }
        }
        
        # Populate category combo
        self.category_combo.addItems(list(self.conversions.keys()))
        self.update_units()
        
    def update_units(self):
        """Update unit combos based on selected category"""
        category = self.category_combo.currentText()
        if category in self.conversions:
            units = list(self.conversions[category].keys())
            
            self.from_combo.clear()
            self.to_combo.clear()
            
            self.from_combo.addItems(units)
            self.to_combo.addItems(units)
            
            if len(units) > 1:
                self.to_combo.setCurrentIndex(1)
    
    def convert(self):
        """Perform the conversion"""
        try:
            value = float(self.from_value.text())
            category = self.category_combo.currentText()
            from_unit = self.from_combo.currentText()
            to_unit = self.to_combo.currentText()
            
            if category == "Temperature":
                result = self.convert_temperature(value, from_unit, to_unit)
            elif category in self.conversions:
                from_factor = self.conversions[category][from_unit]
                to_factor = self.conversions[category][to_unit]
                result = value * from_factor / to_factor
            else:
                result = value
            
            self.to_value.setText(f"{result:.6g}")
            
        except (ValueError, KeyError):
            self.to_value.setText("Error")
    
    def convert_temperature(self, value, from_unit, to_unit):
        """Convert temperature units"""
        # Convert to Celsius first
        if from_unit == "fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "kelvin":
            celsius = value - 273.15
        else:  # celsius
            celsius = value
            
        # Convert from Celsius to target
        if to_unit == "fahrenheit":
            return celsius * 9/5 + 32
        elif to_unit == "kelvin":
            return celsius + 273.15
        else:  # celsius
            return celsius
    
    def insert_result(self):
        """Insert conversion result into main editor"""
        if hasattr(self.parent(), 'insert_conversion_result'):
            result = self.to_value.text()
            if result and result != "Error":
                self.parent().insert_conversion_result(result)


class VariableInspector(QWidget):
    """Widget for inspecting and managing variables"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Variable Inspector"))
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_variables)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Variables tree
        self.variables_tree = QTreeWidget()
        self.variables_tree.setHeaderLabels(["Name", "Type", "Value"])
        self.variables_tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.variables_tree)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.delete_btn = QPushButton("Delete Selected")
        self.edit_btn = QPushButton("Edit Value")
        self.copy_btn = QPushButton("Copy Name")
        
        self.delete_btn.clicked.connect(self.delete_variable)
        self.edit_btn.clicked.connect(self.edit_variable)
        self.copy_btn.clicked.connect(self.copy_variable_name)
        
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.copy_btn)
        
        layout.addLayout(btn_layout)
    
    def update_variables(self, variables):
        """Update the variables display"""
        self.variables_tree.clear()
        
        for name, value in variables.items():
            item = QTreeWidgetItem([
                name,
                type(value).__name__,
                str(value)[:100] + ("..." if len(str(value)) > 100 else "")
            ])
            self.variables_tree.addTopLevelItem(item)
    
    def refresh_variables(self):
        """Refresh variables from parent"""
        if hasattr(self.parent(), 'get_current_variables'):
            variables = self.parent().get_current_variables()
            self.update_variables(variables)
    
    def delete_variable(self):
        """Delete selected variable"""
        current_item = self.variables_tree.currentItem()
        if current_item and hasattr(self.parent(), 'delete_variable'):
            var_name = current_item.text(0)
            self.parent().delete_variable(var_name)
            self.refresh_variables()
    
    def edit_variable(self):
        """Edit selected variable value"""
        current_item = self.variables_tree.currentItem()
        if current_item and hasattr(self.parent(), 'edit_variable'):
            var_name = current_item.text(0)
            current_value = current_item.text(2)
            
            new_value, ok = QLineEdit().text(), True  # Simplified for now
            if ok and hasattr(self.parent(), 'edit_variable'):
                self.parent().edit_variable(var_name, new_value)
                self.refresh_variables()
    
    def copy_variable_name(self):
        """Copy variable name to clipboard"""
        current_item = self.variables_tree.currentItem()
        if current_item:
            var_name = current_item.text(0)
            QApplication.clipboard().setText(var_name)


class ThemeCustomizer(QDialog):
    """Dialog for customizing themes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Theme Customizer")
        self.setModal(True)
        self.resize(500, 600)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Preset themes
        layout.addWidget(QLabel("Preset Themes:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Dark (VS Code)", "Light", "Monokai", "Solarized Dark", 
            "Solarized Light", "GitHub", "Custom"
        ])
        layout.addWidget(self.theme_combo)
        
        # Custom colors section
        colors_group = QGroupBox("Custom Colors")
        colors_layout = QFormLayout(colors_group)
        
        self.bg_color_btn = QPushButton("Background")
        self.text_color_btn = QPushButton("Text")
        self.keyword_color_btn = QPushButton("Keywords")
        self.string_color_btn = QPushButton("Strings")
        self.comment_color_btn = QPushButton("Comments")
        self.number_color_btn = QPushButton("Numbers")
        
        colors_layout.addRow("Background:", self.bg_color_btn)
        colors_layout.addRow("Text:", self.text_color_btn)
        colors_layout.addRow("Keywords:", self.keyword_color_btn)
        colors_layout.addRow("Strings:", self.string_color_btn)
        colors_layout.addRow("Comments:", self.comment_color_btn)
        colors_layout.addRow("Numbers:", self.number_color_btn)
        
        layout.addWidget(colors_group)
        
        # Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QFormLayout(font_group)
        
        self.font_btn = QPushButton("Choose Font")
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(12)
        
        font_layout.addRow("Font:", self.font_btn)
        font_layout.addRow("Size:", self.font_size_spin)
        
        layout.addWidget(font_group)
        
        # Preview
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setPlainText(
            "# Sample Python code\n"
            "import math\n"
            "x = 5\n"
            "y = math.sin(x) * 2.5\n"
            "print(f'Result: {y}')"
        )
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_theme)
        layout.addWidget(buttons)
        
        # Connect signals
        self.theme_combo.currentTextChanged.connect(self.load_preset_theme)
        self.bg_color_btn.clicked.connect(lambda: self.choose_color('bg'))
        self.text_color_btn.clicked.connect(lambda: self.choose_color('text'))
        self.keyword_color_btn.clicked.connect(lambda: self.choose_color('keyword'))
        self.string_color_btn.clicked.connect(lambda: self.choose_color('string'))
        self.comment_color_btn.clicked.connect(lambda: self.choose_color('comment'))
        self.number_color_btn.clicked.connect(lambda: self.choose_color('number'))
        self.font_btn.clicked.connect(self.choose_font)
        
        # Initialize colors
        self.colors = {
            'bg': QColor(30, 30, 30),
            'text': QColor(212, 212, 212),
            'keyword': QColor(86, 156, 214),
            'string': QColor(206, 145, 120),
            'comment': QColor(106, 153, 85),
            'number': QColor(181, 206, 168)
        }
        
        # Initialize font - use system default if Consolas is not available
        self.current_font = QFont("Consolas", 12)
        if not self.current_font.exactMatch():
            self.current_font = QFont("Monaco", 12)  # macOS monospace font
            if not self.current_font.exactMatch():
                self.current_font = QFont("monospace", 12)  # fallback
        
        # Set initial font size in spinner
        self.font_size_spin.setValue(self.current_font.pointSize())
        
        # Connect font size spinner
        self.font_size_spin.valueChanged.connect(self.update_preview)
        
        # Initial preview update
        self.update_preview()
        
    def load_preset_theme(self, theme_name):
        """Load a preset theme"""
        if theme_name == "Dark (VS Code)":
            self.colors.update({
                'bg': QColor(30, 30, 30),
                'text': QColor(212, 212, 212),
                'keyword': QColor(86, 156, 214),
                'string': QColor(206, 145, 120),
                'comment': QColor(106, 153, 85),
                'number': QColor(181, 206, 168)
            })
        elif theme_name == "Light":
            self.colors.update({
                'bg': QColor(255, 255, 255),
                'text': QColor(0, 0, 0),
                'keyword': QColor(0, 0, 255),
                'string': QColor(0, 128, 0),
                'comment': QColor(128, 128, 128),
                'number': QColor(139, 0, 0)
            })
        elif theme_name == "Monokai":
            self.colors.update({
                'bg': QColor(39, 40, 34),
                'text': QColor(248, 248, 242),
                'keyword': QColor(249, 38, 114),
                'string': QColor(230, 219, 116),
                'comment': QColor(117, 113, 94),
                'number': QColor(174, 129, 255)
            })
        # Add more presets as needed
        
        self.update_preview()
    
    def choose_color(self, color_type):
        """Choose a color for a specific element"""
        color = QColorDialog.getColor(self.colors[color_type], self)
        if color.isValid():
            self.colors[color_type] = color
            self.update_preview()
    
    def choose_font(self):
        """Choose font"""
        try:
            font, ok = QFontDialog.getFont(self.current_font, self)
            if ok and isinstance(font, QFont):
                self.current_font = font
                self.font_size_spin.setValue(font.pointSize())
                self.update_preview()
        except Exception as e:
            print(f"Error choosing font: {e}")
            # Fallback to default font
            self.current_font = QFont("Monaco", 12)
    
    def update_preview(self):
        """Update the preview text styling"""
        try:
            if isinstance(self.current_font, QFont):
                font_family = self.current_font.family()
                font_size = self.font_size_spin.value()
            else:
                # Fallback font
                self.current_font = QFont("Monaco", 12)
                font_family = self.current_font.family()
                font_size = 12
                
            self.preview_text.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {self.colors['bg'].name()};
                    color: {self.colors['text'].name()};
                    font-family: {font_family};
                    font-size: {font_size}pt;
                }}
            """)
        except Exception as e:
            print(f"Error updating preview: {e}")
    
    def apply_theme(self):
        """Apply theme to parent"""
        if hasattr(self.parent(), 'apply_custom_theme'):
            # Ensure we have a valid font
            if not isinstance(self.current_font, QFont):
                self.current_font = QFont("Monaco", 12)
                
            theme_data = {
                'colors': self.colors,
                'font': self.current_font,
                'font_size': self.font_size_spin.value()
            }
            self.parent().apply_custom_theme(theme_data)


class SettingsDialog(QDialog):
    """Dialog for customizing text appearance and calculator settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator Settings")
        self.setModal(True)
        self.resize(400, 350)
        self.setup_ui()
        
        # Initialize values
        self.current_font = QFont("Consolas", 12)
        self.text_color = QColor(0, 0, 0)
        self.bg_color = QColor(255, 255, 255)
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create form layout
        form_layout = QFormLayout()
        
        # Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QFormLayout(font_group)
        
        self.font_btn = QPushButton("Choose Font")
        self.font_btn.clicked.connect(self.choose_font)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(12)
        
        font_layout.addRow("Font:", self.font_btn)
        font_layout.addRow("Font Size:", self.font_size_spin)
        
        layout.addWidget(font_group)
        
        # Color settings
        color_group = QGroupBox("Color Settings")
        color_layout = QFormLayout(color_group)
        
        self.text_color_btn = QPushButton("Text Color")
        self.text_color_btn.clicked.connect(self.choose_text_color)
        
        self.bg_color_btn = QPushButton("Background Color")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        
        color_layout.addRow("Text:", self.text_color_btn)
        color_layout.addRow("Background:", self.bg_color_btn)
        
        layout.addWidget(color_group)
        
        # Other settings
        other_group = QGroupBox("Other Settings")
        other_layout = QFormLayout(other_group)
        
        self.precision_spin = QSpinBox()
        self.precision_spin.setRange(1, 15)
        self.precision_spin.setValue(6)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        
        other_layout.addRow("Decimal Precision:", self.precision_spin)
        other_layout.addRow("Theme:", self.theme_combo)
        
        layout.addWidget(other_group)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def choose_font(self):
        font, ok = QFontDialog.getFont(self.current_font, self)
        if ok:
            self.current_font = font
            self.font_size_spin.setValue(font.pointSize())
            
    def choose_text_color(self):
        color = QColorDialog.getColor(self.text_color, self)
        if color.isValid():
            self.text_color = color
            
    def choose_bg_color(self):
        color = QColorDialog.getColor(self.bg_color, self)
        if color.isValid():
            self.bg_color = color


def launch_app():
    """Launch the calculator GUI application."""
    try:
        print("Starting Advanced Scientific Calculator...")
        app = QApplication(sys.argv)
        app.setApplicationName("Advanced Scientific Calculator")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("Scientific Calculator")
        print("QApplication created successfully")

        print("Creating main window...")
        main_win = ScientificCalculator()
        print("Main window created successfully")
        
        main_win.show()
        print("Main window shown, starting event loop...")

        # Start the event loop
        result = app.exec()
        print(f"Event loop finished with result: {result}")
        sys.exit(result)
        
    except Exception as e:
        print(f"Error launching application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    launch_app()
