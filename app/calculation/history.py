from typing import List, Optional
from .calculation import Calculation


class History:
    def __init__(self) -> None:
        self._items: List[Calculation] = []

    def add(self, calc: Calculation) -> None:
        self._items.append(calc)

    def all(self) -> List[Calculation]:
        return list(self._items)

    def last(self) -> Optional[Calculation]:
        return self._items[-1] if self._items else None

    def clear(self) -> None:
        self._items.clear()

    def to_strings(self) -> List[str]:
        return [f"{c.a} ? {c.b} = {c.execute()}" for c in self._items]
