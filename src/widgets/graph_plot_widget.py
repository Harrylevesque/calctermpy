"""
Graph plotting widget for mathematical functions
"""

from ..core.imports import *


class GraphPlotWidget(QWidget):
    """Widget for plotting mathematical functions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Defer matplotlib backend import until widget initialization to avoid
        # initializing Qt before QApplication exists (prevents segfaults on macOS).
        self.MATPLOTLIB_AVAILABLE = False
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.figure import Figure
            # Store references on the instance to avoid polluting globals
            self._mpl = {
                'plt': plt,
                'FigureCanvas': FigureCanvas,
                'Figure': Figure
            }
            self.MATPLOTLIB_AVAILABLE = True
        except Exception:
            self._mpl = None
            self.MATPLOTLIB_AVAILABLE = False

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
        if self.MATPLOTLIB_AVAILABLE and MATPLOTLIB_AVAILABLE:
            Figure = self._mpl['Figure']
            FigureCanvas = self._mpl['FigureCanvas']

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
        if not (self.MATPLOTLIB_AVAILABLE and MATPLOTLIB_AVAILABLE):
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
        if self.MATPLOTLIB_AVAILABLE and MATPLOTLIB_AVAILABLE:
            self.ax.clear()
            self.ax.grid(True)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.canvas.draw()
