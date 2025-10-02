"""
Parameterized tests for calculator operations.
Covers multiple input scenarios efficiently.
"""

import pytest
from src.calculator import add, subtract, multiply, divide


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (1.5, 2.5, 4.0),
    ],
)
def test_add_param(a, b, expected):
    assert add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (5, 3, 2),
        (0, 5, -5),
        (-1, -1, 0),
        (2.5, 0.5, 2.0),
    ],
)
def test_subtract_param(a, b, expected):
    assert subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 6),
        (-1, 1, -1),
        (0, 100, 0),
        (1.2, 3.0, 3.6),
    ],
)
def test_multiply_param(a, b, expected):
    assert multiply(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (6, 3, 2),
        (-6, 3, -2),
        (5, 2, 2.5),
        (2.5, 0.5, 5.0),
    ],
)
def test_divide_param(a, b, expected):
    assert divide(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a,b", [(1, 0), (0.0, 0), (-5, 0)])
def test_divide_by_zero_param(a, b):
    with pytest.raises(ValueError):
        divide(a, b)
