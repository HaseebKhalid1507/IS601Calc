"""
OOP REPL for Module 4

Provides a command-line interface backed by:
- CalculationFactory: builds Calculations from symbols
- History: stores performed calculations

Commands:
- one of +, -, *, /  -> perform calculation
- help               -> show help and supported operations
- history            -> list previous calculations
- exit | quit | q    -> leave the program
"""

from typing import Optional
from app.calculation import CalculationFactory, History


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
    print("  +, -, *, /   -> perform calculation")
    print("  help         -> show this help")
    print("  history      -> list previous calculations")
    print("  exit/quit/q  -> leave the program")
    print(f"Supported operations: {ops}")


def main() -> None:
    """Run the OOP calculator REPL with History and CalculationFactory."""
    hist = History()
    print("🧮 OOP Calculator (type 'help' for options, 'exit' to quit)")

    try:
        while True:
            try:
                cmd = input("Enter command or operation (+, -, *, /, help, history, exit): ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Goodbye!")
                break

            if cmd in {"exit", "quit", "q"}:
                print("👋 Goodbye!")
                break

            if cmd == "help":
                print_help()
                continue

            if cmd == "history":
                items = hist.to_strings()
                if not items:
                    print("(no history yet)")
                else:
                    for line in items:
                        print(line)
                continue

            # If it's an operation symbol, perform a calculation
            if cmd in CalculationFactory.supported():
                a = get_number("Enter first number: ")
                if a is None:
                    print("\n👋 Goodbye!")
                    break
                b = get_number("Enter second number: ")
                if b is None:
                    print("\n👋 Goodbye!")
                    break
                try:
                    calc = CalculationFactory.from_symbol(cmd, a, b)
                    result = calc.execute()
                    hist.add(calc)
                    print(f"{a} {cmd} {b} = {result}")
                except ValueError as exc:  # e.g., divide by zero
                    print(f"Error: {exc}")
                continue

            # Unknown input
            print("❌ Unknown command/operation. Type 'help' for options.")

    except (KeyboardInterrupt, EOFError):
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()  # pragma: no cover
