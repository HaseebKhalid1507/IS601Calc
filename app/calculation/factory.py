from typing import Dict, Type
from app.operation import (
    Operation,
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
)
from .calculation import Calculation


class CalculationFactory:
    _ops: Dict[str, Type[Operation]] = {
        "+": AddOperation,
        "-": SubtractOperation,
        "*": MultiplyOperation,
        "/": DivideOperation,
        "^": PowerOperation,
        "root": RootOperation,
    }

    @classmethod
    def supported(cls):
        return list(cls._ops.keys())

    @classmethod
    def from_symbol(cls, symbol: str, a: float, b: float) -> Calculation:
        op_cls = cls._ops.get(symbol)
        if op_cls is None:
            raise ValueError(f"Unknown operation: {symbol}")
        op_instance: Operation = op_cls()  # type: ignore[call-arg]
        return Calculation(op=op_instance, a=a, b=b)

    @classmethod
    def symbol_for(cls, op: Operation) -> str:
        """Return the symbol for a given Operation instance, or '?' if unknown."""
        for symbol, op_cls in cls._ops.items():
            if isinstance(op, op_cls):
                return symbol
        return "?"
