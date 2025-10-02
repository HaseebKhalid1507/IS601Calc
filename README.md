# IS601Calc – Module 4 OOP Calculator

An object-oriented calculator with a simple REPL, full test coverage, and CI. The functional `src/` implementation has been removed in favor of the OOP `app/` package.

## Prerequisites
- Python 3.8+
- Dependencies listed in `requirements.txt`

## Run the app
- Interactive REPL:
  - python -m app.main
- Commands inside REPL:
  - +, -, *, / to perform a calculation
  - help to list commands and supported operations
  - history to show previous calculations
  - exit | quit | q to leave

## Features
- OOP design:
  - Operation classes for add/subtract/multiply/divide
  - Calculation to execute operations
  - CalculationFactory to build calculations from symbols
  - History to track and display results
- Division by zero is handled with a clear error message

## Testing and linting
- Combined run locally:
  - pytest --pylint --cov=app --cov-report=term-missing --cov-fail-under=100
- Coverage is measured for `app/` only; tests cover 100% of the lines

## CI
- GitHub Actions workflow runs on push/PR:
  - Installs dependencies and runs pytest with pylint
  - Enforces 100% coverage on `app/`

## Project structure
- app/
  - operation/: Operation classes and protocol
  - calculation/: Calculation, Factory, History
  - main.py: REPL entrypoint
- tests/: Unit tests for operations, calculations, history, and REPL
- .github/workflows/python-app.yml: CI workflow
- pytest.ini, .pylintrc, requirements.txt: Config and dependencies
