import pytest
from app.operation import AddOperation, SubtractOperation, MultiplyOperation, DivideOperation

@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        (AddOperation(), 2, 3, 5),
        (SubtractOperation(), 5, 2, 3),
        (MultiplyOperation(), 2, 4, 8),
        (DivideOperation(), 6, 3, 2),
        (DivideOperation(), -6, 3, -2),
    ],
)
def test_operation_classes(op, a, b, expected):
    assert op.apply(a, b) == pytest.approx(expected)


def test_divide_by_zero():
    with pytest.raises(ValueError):
        DivideOperation().apply(1, 0)
