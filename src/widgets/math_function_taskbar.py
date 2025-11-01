"""
Math Function Taskbar: Categorized list of all math functions with tooltips and documentation links
"""

from ..core.imports import *
from PySide6.QtCore import QEvent
import webbrowser

# Function categories and functions (from MATH_LIB_FUNCTIONS.txt)
MATH_FUNCTIONS = {
    "math": [
        "acos", "acosh", "asin", "asinh", "atan", "atan2", "atanh", "ceil", "comb", "copysign", "cos", "cosh", "degrees", "dist", "erf", "erfc", "exp", "expm1", "fabs", "factorial", "floor", "fmod", "frexp", "fsum", "gamma", "gcd", "hypot", "isclose", "isfinite", "isinf", "isnan", "isqrt", "lcm", "ldexp", "lgamma", "log", "log10", "log1p", "log2", "modf", "nextafter", "perm", "pow", "prod", "radians", "remainder", "sin", "sinh", "sqrt", "tan", "tanh", "trunc"
    ],
    "random": [
        "betavariate", "choice", "choices", "expovariate", "gammavariate", "gauss", "getrandbits", "getstate", "lognormvariate", "normalvariate", "paretovariate", "randbytes", "randint", "random", "randrange", "sample", "seed", "setstate", "shuffle", "triangular", "uniform", "vonmisesvariate", "weibullvariate"
    ],
    "statistics": [
        "fmean", "geometric_mean", "harmonic_mean", "mean", "median", "median_grouped", "median_high", "median_low", "mode", "multimode", "pstdev", "pvariance", "quantiles", "stdev", "variance"
    ],
    "cmath": [
        "acos", "acosh", "asin", "asinh", "atan", "atanh", "cos", "cosh", "exp", "isclose", "isfinite", "isinf", "isnan", "log", "log10", "phase", "polar", "rect", "sin", "sinh", "sqrt", "tan", "tanh"
    ],
    "decimal": ["Context", "Decimal", "getcontext", "setcontext", "localcontext"],
    "fractions": ["Fraction", "gcd"],
    "numpy": [
        "abs", "add", "all", "allclose", "alltrue", "angle", "any", "append", "apply_along_axis", "arange", "argmax", "argmin", "argsort", "array", "asarray", "average", "bincount", "bitwise_and", "bitwise_or", "bitwise_xor", "bool_", "broadcast", "cumsum", "delete", "diag", "dot", "empty", "exp", "eye", "fill_diagonal", "flatnonzero", "flip", "floor", "hstack", "identity", "insert", "isclose", "isfinite", "isnan", "linspace", "log", "log10", "log2", "matmul", "max", "mean", "median", "min", "mod", "multiply", "nan", "nan_to_num", "nanmean", "nanmedian", "nanstd", "nansum", "ones", "prod", "ptp", "ravel", "repeat", "reshape", "round", "searchsorted", "shape", "sign", "sin", "sinh", "size", "sort", "split", "sqrt", "stack", "std", "subtract", "sum", "swapaxes", "take", "tan", "tanh", "tile", "trace", "transpose", "unique", "vstack", "where", "zeros"
    ],
    "scipy.stats": ["describe", "entropy", "kurtosis", "mode", "moment", "normaltest", "skew", "ttest_ind", "ttest_rel", "ttest_1samp", "variation"],
    "scipy.optimize": ["curve_fit", "fmin", "fmin_bfgs", "fmin_cg", "fmin_powell", "least_squares", "linprog", "minimize", "root"],
    "scipy.linalg": ["det", "eig", "inv", "norm", "solve", "svd"],
    "sympy": [
        "Abs", "Add", "And", "Apart", "binomial", "cancel", "collect", "combsimp", "cos", "cosh", "count_ops", "diff", "div", "Eq", "expand", "factor", "fraction", "gcd", "groebner", "im", "integrate", "lcm", "limit", "log", "Matrix", "Mul", "N", "nsimplify", "Or", "Poly", "Pow", "Rational", "real_root", "roots", "simplify", "sin", "sinh", "solve", "sqrt", "subs", "symbols", "tan", "tanh", "together", "trigsimp", "zeros"
    ],
    "matplotlib.pyplot": [
        "axis", "bar", "clf", "close", "errorbar", "figure", "fill", "grid", "hist", "imshow", "legend", "plot", "savefig", "scatter", "show", "subplots", "title", "xlabel", "xlim", "ylabel", "ylim"
    ]
}

# Documentation base URLs for each library
DOC_URLS = {
    "math": "https://docs.python.org/3/library/math.html#math.{func}",
    "random": "https://docs.python.org/3/library/random.html#random.{func}",
    "statistics": "https://docs.python.org/3/library/statistics.html#statistics.{func}",
    "cmath": "https://docs.python.org/3/library/cmath.html#cmath.{func}",
    "decimal": "https://docs.python.org/3/library/decimal.html#decimal.{func}",
    "fractions": "https://docs.python.org/3/library/fractions.html#fractions.{func}",
    "numpy": "https://numpy.org/doc/stable/reference/generated/numpy.{func}.html",
    "scipy.stats": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.{func}.html",
    "scipy.optimize": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.{func}.html",
    "scipy.linalg": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.{func}.html",
    "sympy": "https://docs.sympy.org/latest/modules/{func}.html",
    "matplotlib.pyplot": "https://matplotlib.org/stable/api/pyplot_summary.html#{func}"
}

# Placeholder: Function explanations (should be replaced with real docstrings or scraped info)
EXPLANATIONS = {
    "acos": "Return the arc cosine of x, in radians. Usage: math.acos(x). x must be in [-1, 1].",
    "sin": "Return the sine of x (x in radians). Usage: math.sin(x).",
    # ... Add more detailed explanations for each function ...
}

class MathFunctionTaskbar(QWidget):
    """Taskbar listing all math functions by category, with tooltips, doc links, and search"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by category, function, or description...")
        self.search_bar.textChanged.connect(self.update_display)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.search_bar)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        self.displayed_groups = []
        self.update_display()

    def update_display(self):
        # Clear previous widgets
        for group in self.displayed_groups:
            self.scroll_layout.removeWidget(group)
            group.deleteLater()
        self.displayed_groups = []
        query = self.search_bar.text().strip().lower()
        for category, functions in MATH_FUNCTIONS.items():
            # Check if category matches search
            cat_match = query in category.lower()
            group_box = QGroupBox(category)
            vbox = QVBoxLayout(group_box)
            any_visible = False
            for func in functions:
                explanation = EXPLANATIONS.get(func, f"{category}.{func}: See documentation for usage and details.")
                # Check if function or explanation matches search
                if (not query or cat_match or query in func.lower() or query in explanation.lower()):
                    btn = QPushButton(func)
                    btn.setToolTip(self.get_tooltip(category, func))
                    btn.clicked.connect(lambda checked, c=category, f=func: self.insert_function(c, f))
                    btn.installEventFilter(self)
                    vbox.addWidget(btn)
                    any_visible = True
            if any_visible:
                self.scroll_layout.addWidget(group_box)
                self.displayed_groups.append(group_box)
        self.scroll_layout.addStretch()

    def get_tooltip(self, category, func):
        explanation = EXPLANATIONS.get(func, f"{category}.{func}: See documentation for usage and details.")
        doc_url = DOC_URLS.get(category, "").replace("{func}", func)
        return f"<b>{category}.{func}</b><br>{explanation}<br><br><i>Cmd+Click/Ctrl+Click to open documentation.</i>"

    def insert_function(self, category, func):
        if hasattr(self.parent(), 'insert_function'):
            self.parent().insert_function(f"{category}.{func}(")

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                modifiers = QApplication.keyboardModifiers()
                if modifiers & Qt.KeyboardModifier.ControlModifier or modifiers & Qt.KeyboardModifier.MetaModifier:
                    func = obj.text()
                    for cat, funcs in MATH_FUNCTIONS.items():
                        if func in funcs:
                            url = DOC_URLS.get(cat, "").replace("{func}", func)
                            if url:
                                webbrowser.open(url)
                                return True
        return super().eventFilter(obj, event)
