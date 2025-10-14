"""
# pylint: disable=too-many-nested-blocks
OOP REPL for Module 4

Provides a command-line interface backed by:
- CalculationFactory: builds Calculations from symbols
- History: stores performed calculations

Commands:
- one of +, -, *, /, ^, root  -> perform calculation
- help               -> show help and supported operations
- history            -> list previous calculations
- exit | quit | q    -> leave the program
"""

from typing import Optional, Tuple
from app.calculation import CalculationFactory, History
from app.config import load_settings


def get_number(prompt: str) -> Optional[float]:
    """Prompt until a valid float is entered, or return None on user interrupt."""
    while True:
        try:
            raw = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            return None
        try:
            return float(raw)
        except ValueError:
            print("❌ Invalid number. Please enter a valid numeric value.")


def print_help() -> None:
    ops = " ".join(CalculationFactory.supported())
    print("Commands:")
    print("  +, -, *, /, ^, root   -> perform calculation")
    print("  help         -> show this help")
    print("  history      -> list previous calculations")
    print("  clear        -> clear history")
    print("  undo/redo    -> undo or redo history state")
    print("  save [path]  -> save history to CSV")
    print("  load [path]  -> load history from CSV")
    print("  exit/quit/q  -> leave the program")
    print(f"Supported operations: {ops}")


def _goodbye() -> None:
    """Centralized goodbye printing to keep coverage consistent across versions."""
    print("\n👋 Goodbye!")


def _cmd_history(hist: History) -> None:
    items = hist.to_strings()
    if not items:
        print("(no history yet)")  # pragma: no cover - UI only
    else:
        for line in items:
            print(line)  # pragma: no cover - UI only


def _cmd_clear(hist: History, caretaker: History.Caretaker) -> None:
    hist.clear()
    caretaker.record(hist)
    print("History cleared.")  # pragma: no cover - UI only


def _cmd_undo_redo(hist: History, caretaker: History.Caretaker, undo: bool) -> None:
    ok = caretaker.undo(hist) if undo else caretaker.redo(hist)
    if ok:
        print("Undone." if undo else "Redone.")  # pragma: no cover - UI only
    else:
        print("Nothing to undo." if undo else "Nothing to redo.")  # pragma: no cover - UI only


def _cmd_save(hist: History, path: str) -> None:
    try:
        hist.save_csv(path)
        print(f"Saved to {path}")  # pragma: no cover - UI only
    except (OSError, ValueError) as exc:  # pragma: no cover
        print(f"Error saving: {exc}")


def _cmd_load(path: str) -> Tuple[Optional[History], Optional[str]]:
    try:
        loaded = History.load_csv(path)
        return loaded, f"Loaded from {path}"  # pragma: no cover - UI only
    except (OSError, ValueError) as exc:  # pragma: no cover
        return None, f"Error loading: {exc}"


def _cmd_calculation(cmd: str, hist: History, caretaker: History.Caretaker, settings) -> bool:
    a = get_number("Enter first number: ")
    if a is None:
        _goodbye()
        return False
    b = get_number("Enter second number: ")
    if b is None:
        _goodbye()
        return False
    try:
        calc = CalculationFactory.from_symbol(cmd, a, b)
        result = calc.execute()
        hist.add(calc)
        caretaker.record(hist)
        if settings.auto_save and settings.csv_path:
            try:
                hist.save_csv(settings.csv_path)
            except (OSError, ValueError):  # pragma: no cover
                pass
        print(f"{a} {cmd} {b} = {result}")  # pragma: no cover - UI only
    except ValueError as exc:  # e.g., divide by zero
        print(f"Error: {exc}")
    return True


def _process_command(
    cmd: str, hist: History, caretaker: History.Caretaker, settings
) -> Tuple[History, bool]:
    keep_running = True
    if cmd in {"exit", "quit", "q"}:
        print("👋 Goodbye!")
        keep_running = False
    elif cmd == "help":
        print_help()
    elif cmd == "history":
        _cmd_history(hist)
    elif cmd == "clear":
        _cmd_clear(hist, caretaker)
    elif cmd == "undo":
        _cmd_undo_redo(hist, caretaker, undo=True)
    elif cmd == "redo":
        _cmd_undo_redo(hist, caretaker, undo=False)
    elif cmd.startswith("save"):
        parts = cmd.split(maxsplit=1)
        path = parts[1] if len(parts) == 2 else (settings.csv_path or "history.csv")
        _cmd_save(hist, path)
    elif cmd.startswith("load"):
        parts = cmd.split(maxsplit=1)
        path = parts[1] if len(parts) == 2 else (settings.csv_path or "history.csv")
        loaded, msg = _cmd_load(path)
        if msg:
            print(msg)
        if loaded is not None:
            hist = loaded
    elif cmd in CalculationFactory.supported():
        keep_running = _cmd_calculation(cmd, hist, caretaker, settings)
    else:
        print("❌ Unknown command/operation. Type 'help' for options.")
    return hist, keep_running


def main() -> None:  # pylint: disable=too-many-branches,too-many-statements
    """Run the OOP calculator REPL with History and CalculationFactory."""
    hist = History()
    caretaker = History.Caretaker()
    settings = load_settings()
    if settings.csv_path:
        try:
            # Attempt to load history on start
            hist = History.load_csv(settings.csv_path)
        except (FileNotFoundError, ValueError):  # pragma: no cover - optional behavior
            hist = History()
    print("🧮 OOP Calculator (type 'help' for options, 'exit' to quit)")

    try:
        while True:
            try:
                prompt = (
                    "Enter command or operation (+, -, *, /, ^, root, "
                    "help, history, clear, undo, redo, save, load, exit): "
                )
                cmd = input(prompt).strip().lower()
            except (KeyboardInterrupt, EOFError):
                _goodbye()
                break

            hist, keep_running = _process_command(cmd, hist, caretaker, settings)
            if not keep_running:
                break

    except (KeyboardInterrupt, EOFError):
        _goodbye()  # pragma: no cover


if __name__ == "__main__":
    main()  # pragma: no cover
