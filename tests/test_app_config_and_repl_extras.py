import pytest
from app.config import load_settings
from .utils import run_session, has_pandas


def test_load_settings_env(monkeypatch):
    monkeypatch.setenv("AUTO_SAVE", "true")
    monkeypatch.setenv("HISTORY_CSV_PATH", "test_hist.csv")
    s = load_settings()
    assert s.auto_save is True
    assert s.csv_path == "test_hist.csv"




def test_repl_new_commands(capsys, tmp_path, monkeypatch):
    # Ensure autosave is off to avoid filesystem writes
    monkeypatch.delenv("AUTO_SAVE", raising=False)
    csv_path = tmp_path / "h.csv"
    # exercise power, root, clear, undo/redo, save/load, exit
    run_session([
        "^", "2", "3",  # 8
        "root", "2", "9",  # 3
        "history",
        f"save {csv_path}",
        "clear",
        "undo",
        "redo",
        f"load {csv_path}",
        "exit",
    ])
    out = capsys.readouterr().out
    assert "2.0 ^ 3.0 = 8.0" in out
    assert "2.0 root 9.0 = 3.0" in out
    if has_pandas():
        assert "Saved to" in out
        assert "Loaded from" in out
    else:
        assert "Error saving:" in out
        assert "Error loading:" in out

@pytest.mark.skipif(not has_pandas(), reason="pandas not installed")
def test_repl_auto_save_on_calculation(tmp_path, monkeypatch, capsys):
    # Enable auto-save and set path
    csv_path = tmp_path / "auto.csv"
    monkeypatch.setenv("AUTO_SAVE", "1")
    monkeypatch.setenv("HISTORY_CSV_PATH", str(csv_path))

    run_session(["+", "1", "2", "exit"])  # triggers auto-save after calc
    capsys.readouterr()
    # No explicit message on auto-save path, but file should exist
    assert csv_path.exists()
