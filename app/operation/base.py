from typing import Protocol


class Operation(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for arithmetic operations."""

    def apply(self, a: float, b: float) -> float:
        """Apply the operation to two numbers and return the result."""
        ...  # pragma: no cover  # pylint: disable=unnecessary-ellipsis
