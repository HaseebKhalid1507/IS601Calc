# pylint: disable=too-few-public-methods
class PowerOperation:
    """Exponentiation operation: returns a ** b.

    Edge cases:
    - 0 ** negative is undefined (would raise ZeroDivisionError); raise ValueError for clarity.
    """

    def apply(self, a: float, b: float) -> float:  # pragma: no cover - covered via tests
        if a == 0 and b < 0:
            raise ValueError("Cannot raise 0 to a negative power")
        return a ** b
