# Test Project

## Project Overview
This project is a simple calculator application that performs basic arithmetic operations and processes data. It serves as an entry point for users to interact with the calculator functionality.

## Features
- **Calculator Operations:** Supports addition, subtraction, multiplication, and division with a history of operations.
- **Data Processing:** Includes utility functions to load configuration, process data, and save results to a JSON file.

## Prerequisites
- Python 3.x

## Installation
1. Clone the repository:
   ```bash
   git clone https://your-repo-url.git
   cd test_project
   ```
2. Ensure you have Python installed on your system.

## Usage
To run the application, execute the following command:
```bash
python main.py
```

### Example Usage
Here is a simple example of how to use the calculator:
```python
# Import the Calculator class
from calculator import Calculator

# Create an instance of Calculator
calc = Calculator()

# Perform operations
result = calc.add(10, 5)
print("Result of addition:", result)
```

## Project Structure
```
test_project/
├── utils.py
├── calculator.py
└── main.py
```
- **main.py:** Entry point of the application that orchestrates loading configuration, performing calculations, processing data, and saving results.
- **calculator.py:** Defines basic arithmetic operations and a Calculator class that manages operation history.
- **utils.py:** Provides utility functions for loading configuration from JSON, processing data, and saving results.

## Configuration
There are currently no specific configuration files. The application can be configured through code changes in `utils.py` if needed.

## API Documentation
### Endpoints
- **main.py:** This file does not define any API endpoints; it serves as a console application.

## Contributing Guidelines
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.