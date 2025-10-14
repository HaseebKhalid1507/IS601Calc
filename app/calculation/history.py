from dataclasses import dataclass
from typing import Callable, List, Optional
from .calculation import Calculation
from .factory import CalculationFactory


class History:
    """Stores calculations and supports observers, persistence, and mementos."""

    def __init__(self) -> None:
        self._items: List[Calculation] = []
        self._observers: List[Callable[[Calculation, float], None]] = []

    def add(self, calc: Calculation) -> None:
        self._items.append(calc)
        # Notify observers after successful append
        try:
            result = calc.execute()
        except (ValueError, ZeroDivisionError):  # pragma: no cover - notify only on success
            # In case of execution error, still notify with exception info if observers expect it
            # but keep it simple: don't notify on failed execute
            return
        for obs in list(self._observers):
            obs(calc, result)

    def all(self) -> List[Calculation]:
        return list(self._items)

    def last(self) -> Optional[Calculation]:
        return self._items[-1] if self._items else None

    def clear(self) -> None:
        self._items.clear()

    def to_strings(self) -> List[str]:
        return [
            f"{c.a} {CalculationFactory.symbol_for(c.op)} {c.b} = {c.execute()}"
            for c in self._items
        ]

    # --- Observer management ---
    def register_observer(self, callback: Callable[[Calculation, float], None]) -> None:
        """Register an observer callback receiving (calculation, result)."""
        self._observers.append(callback)

    def unregister_observer(self, callback: Callable[[Calculation, float], None]) -> None:
        """Remove a previously registered observer callback."""
        try:
            self._observers.remove(callback)
        except ValueError:  # pragma: no cover - defensive
            pass

    # --- pandas persistence helpers ---
    def to_dataframe(self):  # type: ignore[override]
        """Return a pandas DataFrame of the history.

        Columns: a, op, b, result
        Lazy-imports pandas to avoid mandatory dependency at import-time.
        """
        import importlib  # pylint: disable=import-outside-toplevel

        pd = importlib.import_module("pandas")  # raises ImportError if missing
        data = [
            {
                "a": c.a,
                "op": CalculationFactory.symbol_for(c.op),
                "b": c.b,
                "result": c.execute(),
            }
            for c in self._items
        ]
        return pd.DataFrame(data, columns=["a", "op", "b", "result"])  # type: ignore[no-any-return]

    def save_csv(self, path: str) -> None:
        """Save history to CSV using pandas."""
        df = self.to_dataframe()
        df.to_csv(path, index=False)

    @classmethod
    def load_csv(cls, path: str) -> "History":
        """Load history from CSV using pandas and rebuild Calculation objects."""
        import importlib  # pylint: disable=import-outside-toplevel
        from .factory import CalculationFactory as _Factory  # pylint: disable=import-outside-toplevel

        pd = importlib.import_module("pandas")  # raises ImportError if missing
        df = pd.read_csv(path)
        hist = cls()
        for _, row in df.iterrows():
            calc = _Factory.from_symbol(str(row["op"]), float(row["a"]), float(row["b"]))
            hist.add(calc)
        return hist

    # --- Memento pattern ---
    @dataclass(frozen=True)
    class Memento:
        items: List[Calculation]

    def create_memento(self) -> "History.Memento":
        """Create a snapshot of current history state."""
        return History.Memento(list(self._items))

    def restore_memento(self, memento: "History.Memento") -> None:
        """Restore state from a memento snapshot."""
        self._items = list(memento.items)

    class Caretaker:  # pylint: disable=too-few-public-methods
        """Caretaker to manage undo/redo stacks for a History instance."""

        def __init__(self) -> None:
            self._undo: List[History.Memento] = []
            self._redo: List[History.Memento] = []

        def record(self, hist: "History") -> None:
            self._undo.append(hist.create_memento())
            self._redo.clear()

        def undo(self, hist: "History") -> bool:
            # Need at least two states: current and a previous one
            if len(self._undo) < 2:
                return False
            current = self._undo.pop()  # remove current snapshot
            self._redo.append(current)
            prev = self._undo[-1]
            hist.restore_memento(prev)
            return True

        def redo(self, hist: "History") -> bool:
            if not self._redo:
                return False
            m = self._redo.pop()
            self._undo.append(m)
            hist.restore_memento(m)
            return True
