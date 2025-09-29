#!/usr/bin/env python3
"""
Main application entry point.
"""

from calculator import Calculator, add
from utils import load_config, process_data, save_results

def main():
    """Main application function."""
    print("Starting Calculator Application...")
    
    # Load configuration
    config = load_config("config.json")
    
    # Create calculator instance
    calc = Calculator()
    
    # Perform some calculations
    result1 = calc.calculate("add", 10, 5)
    result2 = calc.calculate("multiply", 3, 4)
    
    print(f"Results: {result1}, {result2}")
    
    # Show history
    history = calc.get_history()
    for entry in history:
        print(f"History: {entry}")
    
    # Process some data
    sample_data = [
        {"id": 1, "value": 10},
        {"id": 2, "value": -5},
        {"id": 3, "value": 20}
    ]
    
    processed = process_data(sample_data)
    save_results(processed, "output.json")
    
    print("Application completed successfully!")

if __name__ == "__main__":
    main()
