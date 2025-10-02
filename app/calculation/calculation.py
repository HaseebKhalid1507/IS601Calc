from dataclasses import dataclass
from app.operation import Operation


@dataclass(frozen=True)
class Calculation:
    op: Operation
    a: float
    b: float

    def execute(self) -> float:
        return self.op.apply(self.a, self.b)
