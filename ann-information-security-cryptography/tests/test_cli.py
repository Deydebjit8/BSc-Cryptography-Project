import pytest

from src.cli import main


def value_after(output, prefix):
    for line in output.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    raise AssertionError(f"{prefix!r} not found in output:\n{output}")


def test_encrypt_then_decrypt_with_printed_hex_key(capsys):
    text = "Can you please look into it? It's very urgent!"  # key contains CR and LF
    assert main(["encrypt", text]) == 0
    out = capsys.readouterr().out
    token = value_after(out, "Ciphertext token:")
    key_hex = value_after(out, "Generated key (hex):")

    assert main(["decrypt", token, key_hex]) == 0
    assert f"Decrypted: {text}" in capsys.readouterr().out


def test_demo_prints_the_report_style_flow(capsys):
    assert main(["demo", "Namaste India!"]) == 0
    out = capsys.readouterr().out
    assert "Generated key (hex): 2e130c0c12010f45" in out
    assert "Intermediate ciphertext: `ramaujeg}hes" in out
    assert "Final ciphertext: rmuehs}aajge`" in out
    assert "Decrypted: Namaste India!" in out


def test_errors_return_non_zero(capsys):
    assert main(["encrypt", ""]) == 1
    assert main(["decrypt", "not-a-token", "2e130c"]) == 1
    assert main(["decrypt", "not-a-token", "zz"]) == 1
    assert capsys.readouterr().out.count("Error:") == 3


@pytest.mark.parametrize(
    "answers, expected",
    [
        (["3", "May everyone stay happy."], "Decrypted: May everyone stay happy."),
        (["9"], "Invalid choice."),
    ],
)
def test_interactive_menu(monkeypatch, capsys, answers, expected):
    replies = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(replies))
    main([])
    assert expected in capsys.readouterr().out


def test_interactive_menu_handles_interrupt(monkeypatch, capsys):
    def interrupt(_prompt=""):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", interrupt)
    assert main([]) == 1
    assert "interrupted" in capsys.readouterr().out
