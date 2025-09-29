"""
Utility functions for data processing.
"""

import json
from typing import List, Dict

def load_config(filename: str) -> Dict:
    """Load configuration from JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def process_data(data: List[Dict]) -> List[Dict]:
    """Process a list of data dictionaries."""
    processed = []
    for item in data:
        if 'value' in item and item['value'] > 0:
            item['processed'] = True
            processed.append(item)
    return processed

def save_results(data: List[Dict], filename: str) -> bool:
    """Save processed data to JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False
