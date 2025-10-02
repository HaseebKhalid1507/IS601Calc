"""
Unit tests for main.py REPL interface.
These tests exercise branches by patching input() and, where useful,
calculator functions.

Run with: `pytest -q`
"""

import builtins

from src import main


def make_input_side_effect(responses):
    """Create a side-effect for input() that yields values or raises.

    `responses` is an iterable; each item is a string to return or an
    exception instance to raise.
    """
    iterator = iter(responses)

    def _input(_prompt=""):
        try:
            value = next(iterator)
        except StopIteration as exc:
            # If tests forget inputs, raise EOFError to emulate end-of-input
            raise EOFError from exc
        if isinstance(value, BaseException):
            raise value
        return value

    return _input


def test_get_number_valid(monkeypatch):
    monkeypatch.setattr(builtins, 'input', lambda _prompt='': '3.14')
    result = main.get_number('> ')
    assert isinstance(result, float)
    assert abs(result - 3.14) < 1e-9


def test_get_number_invalid_then_valid(monkeypatch, capsys):
    inputs = ['not-a-number', '  4  ']
    monkeypatch.setattr(builtins, 'input', make_input_side_effect(inputs))
    result = main.get_number('> ')
    captured = capsys.readouterr()
    assert result == 4.0
    assert 'Invalid number' in captured.out


def test_get_number_eof_returns_none(monkeypatch):
    # input() raises EOFError -> get_number should return None
    monkeypatch.setattr(builtins, 'input', lambda _prompt='': (_ for _ in ()).throw(EOFError()))
    assert main.get_number('> ') is None


def test_main_addition_session(monkeypatch, capsys):
    # simulate: + 2 3 quit
    inputs = ['+', '2', '3', 'quit']
    monkeypatch.setattr(builtins, 'input', make_input_side_effect(inputs))
    main.main()
    captured = capsys.readouterr()
    assert '2.0 + 3.0 = 5.0' in captured.out


def test_main_unknown_operation(monkeypatch, capsys):
    inputs = ['x', 'quit']
    monkeypatch.setattr(builtins, 'input', make_input_side_effect(inputs))
    main.main()
    captured = capsys.readouterr()
    assert 'Unknown operation' in captured.out


def test_main_divide_by_zero(monkeypatch, capsys):
    # Patch divide to raise ValueError for division by zero
    def fake_div(a, b):
        if b == 0:
            raise ValueError('Cannot divide by zero')
        return a / b

    monkeypatch.setattr(main, 'divide', fake_div)
    inputs = ['/', '10', '0', 'quit']
    monkeypatch.setattr(builtins, 'input', make_input_side_effect(inputs))
    main.main()
    captured = capsys.readouterr()
    assert 'Error: Cannot divide by zero' in captured.out


def test_main_quit_short(monkeypatch, capsys):
    # User types 'q' to quit immediately
    monkeypatch.setattr(builtins, 'input', make_input_side_effect(['q']))
    main.main()
    captured = capsys.readouterr()
    assert 'Goodbye' in captured.out


def test_main_get_number_none_on_first(monkeypatch, capsys):
    # Simulate entering an operation then EOF when asking for first number
    monkeypatch.setattr(builtins, 'input', make_input_side_effect(['+', EOFError()]))
    main.main()
    captured = capsys.readouterr()
    assert 'Goodbye' in captured.out


def test_main_keyboardinterrupt_on_op(monkeypatch, capsys):
    # Simulate KeyboardInterrupt at operation prompt
    monkeypatch.setattr(builtins, 'input', make_input_side_effect([KeyboardInterrupt()]))
    main.main()
    captured = capsys.readouterr()
    assert 'Goodbye' in captured.out


def test_main_second_number_eof(monkeypatch, capsys):
    # Simulate op, valid first number, then EOF for second number
    monkeypatch.setattr(builtins, 'input', make_input_side_effect(['+', '2', EOFError()]))
    main.main()
    captured = capsys.readouterr()
    assert 'Goodbye' in captured.out


def test_main_eof_on_op(monkeypatch, capsys):
    # Simulate EOFError at operation prompt to hit outer exception handler
    monkeypatch.setattr(builtins, 'input', make_input_side_effect([EOFError()]))
    main.main()
    captured = capsys.readouterr()
    assert 'Goodbye' in captured.out
