"""
Common imports and constants for the calculator application
"""

import sys
import os
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
    from sympy import (
        symbols, expand, factor, simplify, solve, diff, integrate as sym_integrate,
        # Algebraic operations
        collect, apart, together, cancel, trigsimp, expand_trig, powsimp,
        expand_log, expand_power_base, expand_power_exp, expand_complex,
        # Equation solving
        solveset, linsolve, nonlinsolve, solve_poly_system,
        # Symbolic variables and expressions
        Symbol, I as sympy_I, E, pi, oo, zoo,
        # Matrix operations
        Matrix, eye, zeros as sym_zeros, ones as sym_ones, diag,
        # Calculus
        limit, series, summation, product,
        # Simplification
        simplify, nsimplify, ratsimp, radsimp, powdenest,
        # Logic and sets
        Eq, Ne, Lt, Le, Gt, Ge,
        # Number theory
        isprime, factorint, divisors, gcd, lcm,
        # Special functions
        factorial, binomial, sqrt, cbrt, root,
        # Parsing
        sympify, parse_expr,
        # Printing
        latex, pretty, pprint
    )
    SYMPY_AVAILABLE = True
except ImportError:
    sym = None
    SYMPY_AVAILABLE = False

# NOTE: Do NOT import matplotlib Qt backend or FigureCanvas at module import time here.
# Importing backend_qtagg touches Qt and can initialize Qt before QApplication exists,
# which may cause crashes on some platforms (especially macOS). Instead only detect
# whether matplotlib is installed; specific Qt backend imports should be performed
# lazily inside widgets that create plot canvases (see src/widgets/graph_plot_widget.py).
try:
    import matplotlib
    MATPLOTLIB_AVAILABLE = True
except Exception:
    matplotlib = None
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
