"""
main.py - REPL Interface for IS601 Proj1 (DRY + pylint-friendly)
"""

from calculator import add, subtract, multiply, divide


def get_number(prompt: str) -> float:
    """Safely get a number from the user with validation.

    Keeps prompting until a valid float is entered. Handles EOF/KeyboardInterrupt
    by re-raising so the caller can decide how to exit the REPL cleanly.
    """
    while True:
        try:
            user_input = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            # propagate to allow clean REPL shutdown in main()
            raise
        try:
            return float(user_input)
        except ValueError:
            print("❌ Invalid number. Please enter a valid numeric value.")


def main() -> None:
    """Run the calculator REPL. Handles known errors explicitly to satisfy pylint."""
    print("🧮 Simple Calculator (type 'quit' to exit)")

    operations = {
        "+": ("+", add),
        "-": ("-", subtract),
        "*": ("*", multiply),
        "/": ("/", divide),
    }

    while True:
        try:
            op = input("Enter operation (+, -, *, /): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break

        if op in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break

        if op not in operations:
            print("❌ Unknown operation. Please choose from +, -, *, or /.")
            continue

        try:
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break

        symbol, func = operations[op]
        try:
            result = func(a, b)
            print(f"{a} {symbol} {b} = {result}")
        except ValueError as exc:
            # Known domain error from calculator functions (e.g. divide by zero)
            print(f"Error: {exc}")

        # NOTE: We intentionally avoid catching broad Exception to satisfy pylint.


if __name__ == "__main__":
    main()
