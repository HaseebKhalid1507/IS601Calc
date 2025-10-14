# IS601Calc – Modular OOP Calculator (Patterns, pandas, CI)

An object-oriented calculator with a simple REPL, full test coverage, and CI. The functional `src/` implementation has been removed in favor of the OOP `app/` package.

## Prerequisites
- Python 3.8+
- Dependencies listed in `requirements.txt`

## Run the app
- Interactive REPL:
  - python -m app.main
- Commands inside REPL:
  - +, -, *, /, ^, root to perform a calculation
  - help to list commands and supported operations
  - history to show previous calculations
  - clear to clear history
  - undo / redo to navigate history states (Memento)
  - save [path] to persist history to CSV (pandas)
  - load [path] to load history from CSV (pandas)
  - exit | quit | q to leave

### Configuration via environment or .env
- Create a `.env` file (see `.env.example`) to configure runtime behavior:
  - `AUTO_SAVE` (1/true/yes/on) to enable automatic saving after each calculation
  - `HISTORY_CSV_PATH` default CSV file for auto-load on startup and for save/load commands

Example `.env`:

```
AUTO_SAVE=true
HISTORY_CSV_PATH=history.csv
```

## Features
- OOP + Patterns:
  - Strategy: independent operation classes for +, -, *, /, ^, root
  - Factory: `CalculationFactory` maps symbols to strategies
  - Facade: `main.py` exposes a simple REPL to underlying subsystems
  - Observer: `History` supports observer callbacks invoked on add
  - Memento: `History.Caretaker` provides undo/redo
- pandas-backed persistence:
  - `History.to_dataframe()`, `save_csv()`, and `load_csv()`
  - Optional: if pandas is missing, persistence commands report an error
- Config via env/dotenv:
  - `AUTO_SAVE` (true/false) enables auto-saving after each calculation
  - `HISTORY_CSV_PATH` sets default CSV path
- Robust error handling (LBYL/EAFP): invalid inputs, divide by zero, invalid roots

## Testing and linting
- Combined run locally:
  - pytest --pylint --cov=app --cov-report=term-missing --cov-fail-under=100
- Coverage tips:
  - Use `# pragma: no cover` to exclude intentionally unreachable lines
    (e.g., platform-dependent code or except blocks used only in CI paths)
- Coverage is measured for `app/` only; tests cover 100% of the lines

## CI
- GitHub Actions workflow runs on push/PR:
  - Installs dependencies and runs pytest with pylint
  - Enforces 100% coverage on `app/`

Tips:
- If you intentionally need to skip coverage on non-critical lines (e.g., prints/UI only or optional-dependency paths), use `# pragma: no cover`.
- Keep REPL behavior in `app/main.py` consistent; handler functions help satisfy lint rules without changing UX.

## Project structure
- app/
  - operation/: Operation classes and protocol
  - calculation/: Calculation, Factory, History (+ observers/memento/pandas)
  - config.py: environment/dotenv-based settings
  - main.py: REPL entrypoint (Facade)
- tests/: Unit tests for operations, calculations, history, and REPL
- .github/workflows/python-app.yml: CI workflow
- pytest.ini, .pylintrc, requirements.txt: Config and dependencies
