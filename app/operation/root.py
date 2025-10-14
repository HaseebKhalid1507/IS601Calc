# pylint: disable=too-few-public-methods
import math


class RootOperation:
    """Nth-root operation: returns a-th root of b (i.e., b ** (1/a)).

    Interprets inputs as:
    - a: degree (root index)
    - b: radicand (value to extract root from)

    Rules:
    - a == 0 is invalid.
    - Negative radicand with non-integer degree is invalid.
    - Negative radicand with even integer degree is invalid (no real root).
    - Negative radicand with odd integer degree is allowed (real negative root).
    """

    def apply(self, a: float, b: float) -> float:  # pragma: no cover - covered via tests
        if a == 0:
            raise ValueError("Root degree cannot be zero")

        # If b is negative, degree must be an integer and odd to have a real root
        if b < 0:
            # Check if a is an integer within tolerance
            if not math.isclose(a, round(a)):
                raise ValueError("Fractional root of a negative number is not real")
            a_int = int(round(a))
            if a_int % 2 == 0:
                raise ValueError("Even root of a negative number is not real")
            # For odd integer roots of negative, compute using sign handling
            return -((-b) ** (1.0 / a_int))

        return b ** (1.0 / a)
