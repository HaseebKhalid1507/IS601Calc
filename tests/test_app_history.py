import importlib
import os

import pytest

from app.calculation import Calculation, CalculationFactory, History
from app.operation import AddOperation


def test_history_observer_called():
    hist = History()
    calls = []

    def obs(calc, result):  # pylint: disable=unused-argument
        calls.append(result)

    hist.register_observer(obs)
    c = Calculation(AddOperation(), 1, 2)
    hist.add(c)
    assert calls == [3]
    hist.unregister_observer(obs)


def test_history_memento_undo_redo():
    hist = History()
    ct = History.Caretaker()

    # start empty
    ct.record(hist)

    hist.add(Calculation(AddOperation(), 1, 1))
    ct.record(hist)
    hist.add(Calculation(AddOperation(), 2, 2))
    ct.record(hist)

    assert len(hist.all()) == 2
    assert ct.undo(hist) is True
    assert len(hist.all()) == 1
    assert ct.undo(hist) is True
    assert len(hist.all()) == 0
    assert ct.undo(hist) is False  # nothing else to undo

    # redo twice
    assert ct.redo(hist) is True
    assert len(hist.all()) == 1
    assert ct.redo(hist) is True
    assert len(hist.all()) == 2
    assert ct.redo(hist) is False


# pylint: disable=duplicate-code
def _has_pandas():
    try:
        importlib.import_module("pandas")
        return True
    except ModuleNotFoundError:  # pragma: no cover - environment dependent
        return False


@pytest.mark.skipif(not _has_pandas(), reason="pandas not installed")
def test_history_pandas_save_load_roundtrip(tmp_path):
    hist = History()
    hist.add(CalculationFactory.from_symbol("+", 1, 2))
    hist.add(CalculationFactory.from_symbol("*", 3, 4))

    csv_path = os.path.join(tmp_path, "hist.csv")
    hist.save_csv(csv_path)
    assert os.path.exists(csv_path)

    loaded = History.load_csv(csv_path)
    strings = loaded.to_strings()
    assert len(strings) == 2
    assert strings[0].startswith("1.0 + 2.0 = 3.0")
