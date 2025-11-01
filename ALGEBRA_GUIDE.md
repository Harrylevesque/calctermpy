# Algebra Solving Features Guide

## Overview
This calculator now includes comprehensive symbolic algebra solving capabilities powered by SymPy. You can work with multiple symbolic variables (including imaginary/complex variables), condense and expand formulas, solve equations, and perform advanced algebraic manipulations.

## Features Added

### 1. **Symbolic Variables**
Create and work with symbolic variables for algebraic manipulation:
- Single variables: `x = symbols('x')`
- Multiple variables: `x, y, z = symbols('x y z')`
- Complex/imaginary variables: `z1, z2 = symbols('z1 z2', complex=True)`
- Real-constrained variables: `a, b = symbols('a b', real=True)`
- Built-in imaginary unit: `I` (SymPy's imaginary unit)

### 2. **Formula Condensing**
**Collecting Terms:**
- `collect(expr, x)` - Collect all terms with respect to variable x
- Example: `collect(x*y + x - 3 + 2*x**2, x)` → `2*x**2 + x*(y + 1) - 3`

**Combining Fractions:**
- `together(expr)` - Combine fractions into single fraction
- Example: `together(1/x + 1/y)` → `(x + y)/(x*y)`

**Canceling:**
- `cancel(expr)` - Cancel common factors in numerator/denominator
- Example: `cancel((x**2 - 1)/(x - 1))` → `x + 1`

### 3. **Formula Expansion**
- `expand(expr)` - Expand algebraic expressions
- `factor(expr)` - Factor expressions
- `expand_trig(expr)` - Expand trigonometric expressions
- `expand_log(expr)` - Expand logarithmic expressions
- `expand_complex(expr)` - Expand complex number expressions

Examples:
```python
expand((x + y)**2)  # → x**2 + 2*x*y + y**2
factor(x**2 - y**2)  # → (x - y)*(x + y)
expand((x + I*y)**2)  # → x**2 - y**2 + 2*I*x*y
```

### 4. **Simplification**
Multiple simplification methods:
- `simplify(expr)` - General simplification
- `trigsimp(expr)` - Trigonometric simplification
- `powsimp(expr)` - Power simplification
- `ratsimp(expr)` - Rational simplification
- `radsimp(expr)` - Radical simplification

### 5. **Equation Solving**
Solve single equations or systems:
- `solve(equation, variable)` - General equation solver
- `solveset(equation, variable)` - Modern solver returning sets
- `linsolve([eq1, eq2], [x, y])` - Linear system solver
- `nonlinsolve([eq1, eq2], [x, y])` - Nonlinear system solver

Examples:
```python
# Simple equation
solve(x**2 - 4, x)  # → [-2, 2]

# Equation with imaginary solutions
solve(x**2 + 1, x)  # → [-I, I]

# System of equations
solve([x + y - 5, x - y - 1], [x, y])  # → {x: 3, y: 2}

# Using Eq() for clarity
solve(Eq(x**2, 4), x)  # → [-2, 2]
```

### 6. **Multiple Imaginary Variables**
Work with multiple complex/imaginary variables:
```python
z1, z2, z3 = symbols('z1 z2 z3', complex=True)
expand((z1 + z2)**2)  # → z1**2 + 2*z1*z2 + z2**2
expand((z1 + z2)*(z1 - z2))  # → z1**2 - z2**2
```

## Using the Algebra Helper Dialog

Access via: **Tools → Algebra Helper**

The Algebra Helper provides an interactive interface with four tabs:

### Tab 1: Variables
- Create single or multiple symbolic variables
- Create complex/imaginary variables
- Generate code that can be copied to your document

### Tab 2: Manipulation
- Enter an expression
- Apply various operations with a single click:
  - Expand, Factor, Simplify
  - Collect Terms, Together, Apart
  - Trig Simplify, Expand Trig
  - Power Simplify, Expand Log
  - Rational Simplify, Cancel
- See results instantly
- Copy commands to clipboard

### Tab 3: Equation Solving
- Enter single equations or systems
- Specify variables to solve for
- Choose solver type (solve, solveset, linsolve)
- View solutions

### Tab 4: Reference
- Quick reference guide for all algebra functions
- Examples and usage tips

## Available Functions in the Calculator

All these functions are available directly in your calculator documents:

**Core Symbolic:**
- `symbols()`, `Symbol()`, `sympify()`, `parse_expr()`

**Constants:**
- `I` (imaginary unit), `E` (Euler's number), `pi`, `oo` (infinity)

**Algebraic Operations:**
- `expand()`, `factor()`, `simplify()`, `collect()`, `apart()`, `together()`, `cancel()`
- `trigsimp()`, `expand_trig()`, `powsimp()`, `expand_log()`
- `nsimplify()`, `ratsimp()`, `radsimp()`, `powdenest()`

**Equation Solving:**
- `solve()`, `solveset()`, `linsolve()`, `nonlinsolve()`, `solve_poly_system()`

**Relations:**
- `Eq()`, `Ne()`, `Lt()`, `Le()`, `Gt()`, `Ge()`

**Matrix Operations:**
- `Matrix()`, `eye()`, `sym_zeros()`, `sym_ones()`, `diag()`

**Calculus:**
- `diff()`, `sym_integrate()`, `limit()`, `series()`, `summation()`, `product()`

**Number Theory:**
- `isprime()`, `factorint()`, `divisors()`, `gcd()`, `lcm()`

**Special Functions:**
- `factorial()`, `binomial()`, `sqrt()`, `cbrt()`, `root()`

**Display:**
- `latex()`, `pretty()`, `pprint()`

## Example Workflows

### Example 1: Expanding and Factoring
```python
# Create variables
x, y = symbols('x y')

# Expand
expand((x + y)**3)
# Result: x**3 + 3*x**2*y + 3*x*y**2 + y**3

# Factor back
factor(x**3 + 3*x**2*y + 3*x*y**2 + y**3)
# Result: (x + y)**3
```

### Example 2: Solving Quadratic Equations
```python
x = symbols('x')
a, b, c = symbols('a b c')

# General quadratic formula
solve(a*x**2 + b*x + c, x)
# Result: [(-b - sqrt(b**2 - 4*a*c))/(2*a), (-b + sqrt(b**2 - 4*a*c))/(2*a)]

# Specific case
solve(x**2 + 5*x + 6, x)
# Result: [-3, -2]
```

### Example 3: Complex Variable Algebra
```python
# Create complex variables
z1, z2 = symbols('z1 z2', complex=True)

# Expand product
expand((z1 + z2)*(conjugate(z1) + conjugate(z2)))

# Work with imaginary unit
expr = (x + I*y)**2
expand(expr)
# Result: x**2 - y**2 + 2*I*x*y
```

### Example 4: System of Equations
```python
x, y, z = symbols('x y z')

# Solve linear system
system = [
    x + y + z - 6,
    2*x - y + z - 3,
    x + 2*y - z - 2
]
solve(system, [x, y, z])
# Result: {x: 1, y: 2, z: 3}
```

## Tips

1. **Use the Algebra Helper** for interactive exploration of functions
2. **See ALGEBRA_EXAMPLES.txt** for comprehensive examples
3. **Variables persist** across lines in your document
4. **Combine with calculus** - use `diff()`, `integrate()` with symbolic expressions
5. **Matrix algebra** works with symbolic entries
6. **Pretty printing** - use `pprint()` for nicely formatted output

## Installation Note

If SymPy is not installed, install it with:
```bash
pip install sympy
```

The calculator will detect its availability automatically.
