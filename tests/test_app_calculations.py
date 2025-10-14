import pytest
from app.calculation import Calculation, CalculationFactory, History
from app.operation import (
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
)

@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        (AddOperation(), 1, 2, 3),
        (SubtractOperation(), 5, 3, 2),
        (MultiplyOperation(), 3, 3, 9),
        (DivideOperation(), 8, 2, 4),
    ],
)
def test_calculation_execute(op, a, b, expected):
    calc = Calculation(op=op, a=a, b=b)
    assert calc.execute() == pytest.approx(expected)


def test_factory_supported():
    sup = CalculationFactory.supported()
    assert set(sup) == set(["+", "-", "*", "/", "^", "root"])  # order not enforced


@pytest.mark.parametrize(
    "symbol,a,b,expected",
    [
        ("+", 2, 2, 4),
        ("-", 5, 3, 2),
        ("*", 4, 2, 8),
        ("/", 9, 3, 3),
        ("^", 2, 3, 8),
        ("root", 2, 9, 3),
    ],
)
def test_factory_from_symbol(symbol, a, b, expected):
    calc = CalculationFactory.from_symbol(symbol, a, b)
    assert calc.execute() == pytest.approx(expected)


def test_factory_unknown_symbol():
    with pytest.raises(ValueError):
        CalculationFactory.from_symbol("%", 2, 2)


def test_history_add_and_last_and_clear():
    hist = History()
    assert hist.last() is None
    c1 = Calculation(AddOperation(), 1, 1)
    c2 = Calculation(MultiplyOperation(), 2, 3)
    hist.add(c1)
    hist.add(c2)
    assert hist.last() == c2
    all_items = hist.all()
    assert len(all_items) == 2
    hist.clear()
    assert hist.last() is None


def test_history_to_strings():
    hist = History()
    c1 = Calculation(AddOperation(), 1, 1)
    c2 = Calculation(MultiplyOperation(), 2, 3)
    hist.add(c1)
    hist.add(c2)
    strings = hist.to_strings()
    assert len(strings) == 2
    assert strings[0].startswith("1 + 1 = ")
    assert strings[1].startswith("2 * 3 = ")


def test_symbol_for_operations():
    assert CalculationFactory.symbol_for(AddOperation()) == "+"
    assert CalculationFactory.symbol_for(SubtractOperation()) == "-"
    assert CalculationFactory.symbol_for(MultiplyOperation()) == "*"
    assert CalculationFactory.symbol_for(DivideOperation()) == "/"
    assert CalculationFactory.symbol_for(PowerOperation()) == "^"
    assert CalculationFactory.symbol_for(RootOperation()) == "root"


def test_symbol_for_unknown_operation():
    class UnknownOp:  # minimal shape-compatible object
        # pylint: disable=too-few-public-methods
        def apply(self, a, b):  # pylint: disable=unused-argument
            return a  # pragma: no cover (value unused)

    assert CalculationFactory.symbol_for(UnknownOp()) == "?"
