"""
A simple calculator module with basic mathematical operations.
"""

def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def subtract(a, b):
    """Subtract second number from first and return the result."""
    return a - b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide(a, b):
    """Divide first number by second and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class Calculator:
    """A calculator class for more complex operations."""
    
    def __init__(self):
        self.history = []
    
    def calculate(self, operation, a, b):
        """Perform calculation and store in history."""
        result = None
        if operation == "add":
            result = add(a, b)
        elif operation == "subtract":
            result = subtract(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        elif operation == "divide":
            result = divide(a, b)
        else:
            raise ValueError("Unknown operation")
        
        self.history.append(f"{operation}({a}, {b}) = {result}")
        return result
    
    def get_history(self):
        """Return calculation history."""
        return self.history.copy()
