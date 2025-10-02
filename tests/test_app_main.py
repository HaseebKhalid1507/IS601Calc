import builtins


def run_session(inputs):
    from app import main as app_main  # import locally to avoid state leaks

    it = iter(inputs)

    def fake_input(prompt=""):
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


def test_help_and_exit(capsys):
    run_session(["help", "exit"])
    out = capsys.readouterr().out
    assert "Supported operations:" in out
    assert "Goodbye" in out


def test_unknown_command_then_quit(capsys):
    run_session(["foo", "q"])
    out = capsys.readouterr().out
    assert "Unknown command/operation" in out
    assert "Goodbye" in out


def test_history_empty_then_add_and_show(capsys):
    run_session(["history", "+", "1", "2", "history", "exit"])
    out = capsys.readouterr().out
    assert "(no history yet)" in out
    # calculation echo
    assert "1.0 + 2.0 = 3.0" in out
    # history format uses '?' placeholder
    assert "1.0 ? 2.0 = 3.0" in out


def test_invalid_number_and_interrupt(capsys):
    # invalid first number, then valid; then user interrupts on second number (EOF)
    run_session(["*", "not-a-number", "3",])
    out = capsys.readouterr().out
    assert "Invalid number" in out
    assert "Goodbye" in out


def test_divide_by_zero(capsys):
    run_session(["/", "5", "0", "quit"])  # after showing error, quit
    out = capsys.readouterr().out
    assert "Error:" in out


def test_immediate_eof_on_command(capsys):
    # No inputs at all -> EOF at command prompt, handled by inner try around input
    run_session([])
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_first_number_interrupt(capsys):
    # User selects op then immediately EOF on first number
    run_session(["+"])  # next prompt will raise EOF
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_outer_keyboardinterrupt(capsys):
    # Simulate Ctrl-C occurring during help printing (outside the inner input try),
    # so it is caught by the outermost try/except in main().
    import app.main as app_main

    original = app_main.print_help
    try:
        # Replace print_help with a function that raises KeyboardInterrupt
        app_main.print_help = lambda: (_ for _ in ()).throw(KeyboardInterrupt())
        run_session(["help"])  # triggers print_help -> KeyboardInterrupt
    finally:
        app_main.print_help = original
    out = capsys.readouterr().out
    assert "Goodbye" in out
