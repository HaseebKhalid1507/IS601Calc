class DivideOperation:
    """Division operation."""

    def apply(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
