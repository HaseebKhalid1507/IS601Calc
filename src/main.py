"""
main.py - REPL Interface for IS601 Proj1 (DRY + pylint-friendly)
"""

from src.calculator import add, subtract, multiply, divide


def get_number(prompt: str) -> float | None:
    """Safely get a number from the user with validation.

    Keeps prompting until a valid float is entered.
    Returns None if the user interrupts input.
    """
    while True:
        try:
            user_input = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            return None
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

    try:
        while True:
            op = input("Enter operation (+, -, *, /): ").strip().lower()

            if op in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if op not in operations:
                print("❌ Unknown operation. Please choose from +, -, *, or /.")
                continue

            a = get_number("Enter first number: ")
            if a is None:
                print("\n👋 Goodbye!")
                break

            b = get_number("Enter second number: ")
            if b is None:
                print("\n👋 Goodbye!")
                break

            symbol, func = operations[op]
            try:
                result = func(a, b)
                print(f"{a} {symbol} {b} = {result}")
            except ValueError as exc:
                print(f"Error: {exc}")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
