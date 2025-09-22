# Project: IS601 Proj1
# Description: Initial README for Python project

## Setup
- Python 3.8+
- See requirements.txt for dependencies

## Usage
- Run `python main.py` to start the project.

## Features
- Modular calculator supporting addition, subtraction, multiplication, and division
- Division by zero is safely handled
- All logic is in `calculator.py`, used by `main.py`

## Testing & Linting
- Run unit tests and check code quality with:
  ```
  pytest --pylint --cov
  ```
- Tests are in `test_calculator.py` and cover all calculator functions

## Project Structure
- `main.py`: Entry point, interactive calculator
- `calculator.py`: Calculator logic (modular functions)
- `test_calculator.py`: Unit tests for calculator
- `.gitignore`, `requirements.txt`, `pytest.ini`, `.pylintrc`: Project config files
