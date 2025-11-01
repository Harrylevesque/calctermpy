"""
Help dialog for the calculator application
"""

from ..core.imports import *


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
