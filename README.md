# Advanced Scientific Calculator with AI Assistant

A powerful PyQt6-based scientific calculator that supports Python's math library, NumPy, SciPy, and SymPy for advanced mathematical computations. Now featuring an AI assistant powered by FLAN-T5 for code help, debugging, and function discovery.

## 🆕 New Features (v3.0)

- **🤖 AI Assistant**: FLAN-T5-powered chatbot for code help and debugging
- **Smart Code Explanation**: AI explains your code and suggests improvements
- **Function Discovery**: AI suggests relevant functions for your mathematical tasks
- **Error Debugging**: AI helps debug and fix code errors
- **Interactive Chat**: Real-time conversation with AI about programming questions

## Features

- **Multi-library Support**: Access to Python's math, NumPy, SciPy, and SymPy libraries
- **Control Flow Support**: If statements, loops, function definitions
- **Variable Definition**: Define and reuse variables across calculations
- **Document-style Interface**: Track all calculations with line-by-line output
- **Python Syntax Highlighting**: VS Code-style syntax highlighting with dark/light themes
- **AI Code Assistant**: Get help with debugging, explanations, and function suggestions
- **Customizable Interface**: Choose text size, color, font, and background
- **Print Support**: Print calculation history
- **Real-time Results**: Immediate calculation results after each input

## Installation

1. Install Python 3.8 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

**AI Assistant Requirements:**
- The AI assistant requires `transformers`, `torch`, `sentencepiece`, and `protobuf`
- These are included in `requirements.txt`
- First run may take several minutes to download the FLAN-T5 model (~300MB)
- AI features work offline after initial model download

## Usage

### Running the Application
```bash
python calculator.py
```

### Basic Operations
- Type mathematical expressions in the input field
- Press Enter or click "Calculate" to execute
- Results appear immediately in the history panel

### Variable Definition
```python
x = 5
y = x * 2
z = math.sin(x) + math.cos(y)
```

### Available Libraries

#### Python Math Library
```python
math.sin(x), math.cos(x), math.tan(x)
math.sqrt(x), math.log(x), math.exp(x)
math.pi, math.e
```

#### NumPy (prefix: np.)
```python
arr = np.array([1, 2, 3, 4])
np.mean(arr)
np.std(arr)
matrix = np.array([[1,2],[3,4]])
np.linalg.det(matrix)
```

#### SciPy (prefix: sp.)
```python
sp.optimize.minimize_scalar(lambda x: x**2 + 2*x + 1)
sp.integrate.quad(lambda x: x**2, 0, 1)
sp.stats.norm.pdf(0)
```

#### SymPy (prefix: sym.)
```python
x = sym.Symbol('x')
expr = x**2 + 2*x + 1
sym.expand(expr)
sym.factor(expr)
sym.diff(expr, x)
sym.integrate(expr, x)
sym.solve(expr, x)
```

## 🤖 AI Assistant

The calculator includes an intelligent AI assistant powered by FLAN-T5 to help with coding, debugging, and mathematical problem-solving.

### Accessing the AI Assistant

1. **Menu Access**: Go to `🤖 AI Assistant` → `Open AI Chat`
2. **Toolbar**: Click the `🤖 AI Chat` button in the toolbar
3. **Keyboard Shortcut**: Use quick access via menu options

### AI Features

#### 💬 Interactive Chat
- Open the AI chat dialog for general questions about Python, NumPy, SciPy, and SymPy
- Ask about function syntax, mathematical concepts, or programming help
- Get suggestions for functions and libraries for specific tasks

#### 🔍 Code Debugging
1. Select problematic code in the editor
2. Use `🤖 AI Assistant` → `Debug Selected Code`
3. AI analyzes the code and provides debugging suggestions

#### 📖 Code Explanation
1. Select any code in the editor
2. Use `🤖 AI Assistant` → `Explain Selected Code`
3. AI explains what the code does and suggests improvements

#### 🎯 Function Suggestions
1. Use `🤖 AI Assistant` → `Suggest Functions`
2. Describe what you want to accomplish
3. AI suggests relevant Python/NumPy/SciPy/SymPy functions with examples

### AI Chat Interface

The AI chat dialog includes:
- **Chat History**: View conversation history
- **Quick Actions**: Buttons for debugging, explaining, and suggestions
- **Real-time Responses**: AI responds in real-time (may take a few seconds)

### Example AI Interactions

**Function Discovery:**
```
You: "Functions for linear algebra operations"
AI: "NumPy linear algebra functions: np.dot(a,b) for matrix multiplication, 
     np.linalg.inv(A) for inverse, np.linalg.det(A) for determinant, 
     np.linalg.eig(A) for eigenvalues"
```

**Code Explanation:**
```
Selected code: matrix = np.array([[1,2],[3,4]])
AI: "This code creates a 2x2 NumPy array representing a matrix with 
     values [[1,2],[3,4]]. You can perform linear algebra operations on it."
```

**Debugging Help:**
```
Code with error: x = np.aray([1,2,3])
AI: "The error occurs because 'aray' is misspelled. It should be 'array'. 
     Correct code: x = np.array([1,2,3])"
```

### AI Performance Notes

- First run downloads the FLAN-T5 model (~300MB) - this may take a few minutes
- AI responses typically take 1-3 seconds to generate
- Works offline after initial setup
- Provides fallback responses with built-in knowledge for common questions
- Best results with specific, clear questions

## Customization

1. **Settings Dialog**: Edit → Settings
   - Choose font and font size
   - Select text and background colors
   - Set decimal precision

2. **Quick Functions**: Use toolbar buttons for common functions

3. **Printing**: File → Print to print calculation history

### Example Calculations

```python
# Basic arithmetic with variables
a = 10
b = 20
result = (a + b) * math.pi

# Matrix operations
matrix = np.array([[1, 2], [3, 4]])
inverse = np.linalg.inv(matrix)
determinant = np.linalg.det(matrix)

# Symbolic mathematics
x = sym.Symbol('x')
equation = x**3 - 6*x**2 + 11*x - 6
roots = sym.solve(equation, x)
derivative = sym.diff(equation, x)

# Scientific calculations
data = np.random.normal(0, 1, 100)
mean = np.mean(data)
std = np.std(data)
```

## Keyboard Shortcuts

- **Enter**: Calculate expression
- **Ctrl+L**: Clear history
- **Ctrl+R**: Clear variables

## Tips

1. Use descriptive variable names for better readability
2. The history panel shows input in blue, results in green, and errors in red
3. All NumPy and SciPy functions are available with their respective prefixes
4. SymPy expressions can be mixed with numerical calculations
5. Use the help dialog (Help → Help) for a comprehensive function reference

## Troubleshooting

### General Issues
- If you get import errors, ensure all packages in requirements.txt are installed
- For SymPy symbolic calculations, always define symbols first: `x = sym.Symbol('x')`
- Large matrices or complex calculations may take time to compute
- Check the error messages in red for syntax or calculation errors

### AI Assistant Issues
- **"AI Not Available"**: Install AI dependencies with `pip install transformers torch sentencepiece protobuf`
- **"AI Not Ready"**: Wait for model to load (shows progress in terminal)
- **Slow AI responses**: Normal on first run; subsequent responses are faster
- **Short AI responses**: AI includes fallback knowledge base for common questions
- **Model download fails**: Check internet connection; model downloads automatically on first use
