import pytest
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
        (AddOperation(), 2, 3, 5),
        (SubtractOperation(), 5, 2, 3),
        (MultiplyOperation(), 2, 4, 8),
        (DivideOperation(), 6, 3, 2),
        (DivideOperation(), -6, 3, -2),
        (PowerOperation(), 2, 3, 8),
        (RootOperation(), 2, 9, 3),
        (RootOperation(), 3, 27, 3),
    ],
)
def test_operation_classes(op, a, b, expected):
    assert op.apply(a, b) == pytest.approx(expected)


def test_divide_by_zero():
    with pytest.raises(ValueError):
        DivideOperation().apply(1, 0)


def test_power_zero_negative():
    with pytest.raises(ValueError):
        PowerOperation().apply(0, -1)


@pytest.mark.parametrize("degree,radicand", [(0, 9), (2, -9), (2.5, -8)])
def test_root_invalid_cases(degree, radicand):
    with pytest.raises(ValueError):
        RootOperation().apply(degree, radicand)
