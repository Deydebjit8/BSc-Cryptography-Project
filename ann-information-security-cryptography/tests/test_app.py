from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

APP = Path(__file__).resolve().parents[1] / "app" / "streamlit_app.py"


def run_app():
    return AppTest.from_file(str(APP), default_timeout=30).run()


def test_app_loads_without_errors():
    at = run_app()
    assert not at.exception
    assert [tab.label for tab in at.tabs] == ["Encrypt", "Decrypt", "How it works", "About"]


def test_encrypt_then_decrypt_with_hex_key():
    text = "Can you please look into it? It's very urgent!"  # key contains CR and LF
    at = run_app()

    at.text_area(key="plaintext_input").set_value(text).run()
    at.button(key="encrypt_btn").click().run()
    assert not at.exception
    result = at.session_state["last_result"]

    at.text_area(key="token_input").set_value(result["token"]).run()
    at.text_input(key="key_hex_input").set_value(result["key_hex"]).run()
    at.button(key="decrypt_btn").click().run()

    assert not at.exception
    recovered = [box.value for box in at.text_area if box.label == "Recovered plaintext"]
    assert recovered == [text]


def test_decrypt_shows_an_error_for_a_bad_key():
    at = run_app()
    at.text_area(key="token_input").set_value("abc").run()
    at.text_input(key="key_hex_input").set_value("zz").run()
    at.button(key="decrypt_btn").click().run()
    assert not at.exception
    assert len(at.error) == 1
