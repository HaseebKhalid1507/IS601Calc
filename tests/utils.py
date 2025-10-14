import builtins
import importlib

from app import main as app_main


def run_session(inputs):
    """Feed a sequence of inputs into the app's REPL and run a session."""
    it = iter(inputs)

    def fake_input(prompt=""):  # pylint: disable=unused-argument
        try:
            return next(it)
        except StopIteration as exc:  # emulate EOF when inputs run out
            raise EOFError() from exc

    orig = builtins.input
    try:
        builtins.input = fake_input
        app_main.main()
    finally:
        builtins.input = orig


def has_pandas():
    """Return True if pandas is importable, False otherwise."""
    try:
        importlib.import_module("pandas")
        return True
    except ModuleNotFoundError:  # pragma: no cover - env dependent
        return False
