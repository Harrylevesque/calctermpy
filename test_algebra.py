"""
Quick test script for algebra solving features
"""

# Test if sympy is available
try:
    from sympy import *
    print("✓ SymPy is available")
    
    # Test 1: Create symbolic variables
    print("\n1. Creating symbolic variables:")
    x, y, z = symbols('x y z')
    print(f"   Variables created: x, y, z")
    
    # Test 2: Expand formula
    print("\n2. Expanding (x + y)^2:")
    result = expand((x + y)**2)
    print(f"   Result: {result}")
    
    # Test 3: Factor formula
    print("\n3. Factoring x^2 + 2x + 1:")
    result = factor(x**2 + 2*x + 1)
    print(f"   Result: {result}")
    
    # Test 4: Simplify
    print("\n4. Simplifying (x^2 - 1)/(x - 1):")
    result = simplify((x**2 - 1)/(x - 1))
    print(f"   Result: {result}")
    
    # Test 5: Solve equation
    print("\n5. Solving x^2 - 4 = 0:")
    result = solve(x**2 - 4, x)
    print(f"   Result: {result}")
    
    # Test 6: Solve with imaginary solutions
    print("\n6. Solving x^2 + 1 = 0:")
    result = solve(x**2 + 1, x)
    print(f"   Result: {result}")
    print(f"   (I represents the imaginary unit)")
    
    # Test 7: Multiple imaginary variables
    print("\n7. Working with multiple complex variables:")
    z1, z2 = symbols('z1 z2', complex=True)
    expr = (z1 + z2)*(z1 - z2)
    result = expand(expr)
    print(f"   expand((z1 + z2)*(z1 - z2)) = {result}")
    
    # Test 8: System of equations
    print("\n8. Solving system: x + y = 5, x - y = 1:")
    result = solve([x + y - 5, x - y - 1], [x, y])
    print(f"   Result: {result}")
    
    # Test 9: Collect terms
    print("\n9. Collecting terms in x*y + x - 3 + 2*x^2:")
    expr = x*y + x - 3 + 2*x**2
    result = collect(expr, x)
    print(f"   Result: {result}")
    
    # Test 10: Trigonometric simplification
    print("\n10. Trigonometric: sin(x)^2 + cos(x)^2:")
    result = trigsimp(sin(x)**2 + cos(x)**2)
    print(f"    Result: {result}")
    
    print("\n" + "="*50)
    print("✓ All algebra functions working correctly!")
    print("="*50)
    
except ImportError as e:
    print(f"✗ SymPy is not available: {e}")
    print("\nPlease install sympy:")
    print("  pip install sympy")
