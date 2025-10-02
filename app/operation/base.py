from typing import Protocol


class Operation(Protocol):
    """Protocol for arithmetic operations."""

    def apply(self, a: float, b: float) -> float:
        """Apply the operation to two numbers and return the result."""
        ...
