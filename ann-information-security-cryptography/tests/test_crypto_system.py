"""Unit and integration tests for src.crypto_system.

The expected values in REPORT_SAMPLES were read from the "Output" pages of the
project report (pp. 27-28). Non-printable characters are shown as boxes in the
report's console screenshots, so only the visible characters are compared.
"""

import base64
import json
import random
import string
from pathlib import Path

import pytest

from src.crypto_system import (
    KEY_LENGTH,
    MAX_CODE_POINT,
    build_nodes,
    decrypt,
    encrypt,
    generate_key,
    inspect_ciphertext,
    key_from_hex,
    key_to_hex,
    render,
    xor_with_key,
)
from tests import report_reference

ROOT = Path(__file__).resolve().parents[1]

REPORT_SAMPLES = [
    (
        "Hello Everyone! Welcome to our project.",
        "2e1d0700034f2531",
        r'''fxkllo`GKo~om*yxkcl"@Zr'ov=A\rme`;''',
        r'''fklGomxcZoAm~"=\;xloKoyklrvre`*@'`''',
    ),
    (
        "May everyone stay happy.",
        "251418594511110d",
        r"huay gt\{v<ebel\4p85ah#",
        r"hagvbla{\8#uyteeph \<45",
    ),
    (
        "Can you please look into it? It's very urgent!",
        "231e0d4e590a0655",
        r"""`cn esuSrh/*o&9Lqfn0dr:wyqyCrrP>{++s& Qyh -+""",
        r"""ceuroqnryyrPQh/&0{+ -nsShLfdwqCrsy` *9:>+& +""",
    ),
]


def make_token(payload):
    raw = json.dumps(payload).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii")


def chars(pairs):
    """[(value, index), ...] -> [(char, index), ...] as printed in the report."""
    return [(chr(value), index) for value, index in pairs]


# --------------------------------------------------------------------------
# Key generation
# --------------------------------------------------------------------------
def test_key_generation_is_deterministic():
    assert generate_key("Namaste India!") == generate_key("Namaste India!")


def test_key_has_fixed_length():
    for text in ["a", "ab", "Namaste", "Namaste India!", "x" * 500]:
        assert len(generate_key(text)) == KEY_LENGTH


def test_key_generation_matches_report_source_code():
    # Consecutive absolute differences; key[0] wraps to the last character.
    assert key_to_hex(generate_key("Namaste India!")) == "2e130c0c12010f45"
    assert generate_key("Namaste India!") == ".\x13\x0c\x0c\x12\x01\x0fE"


def test_short_or_repeating_input_can_give_an_all_zero_key():
    # Documented limitation: XOR with this key changes nothing.
    assert generate_key("aaaa") == "\x00" * KEY_LENGTH
    assert render(xor_with_key("aaaa", generate_key("aaaa"))) == "aaaa"


def test_generate_key_rejects_empty_plaintext():
    with pytest.raises(ValueError):
        generate_key("")


# --------------------------------------------------------------------------
# Printable key format
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "text",
    ["Namaste India!", "aaaa", "বাংলা ভাষা", "\x00\x01\x02\x03", "😀 smile!", "a\ue000"],
)
def test_key_hex_round_trip(text):
    key = generate_key(text)
    assert key_from_hex(key_to_hex(key)) == key


def test_key_can_contain_a_lone_surrogate_and_still_round_trip():
    key = generate_key("a\ue000")
    assert any(0xD800 <= ord(char) <= 0xDFFF for char in key)
    result = encrypt("a\ue000")
    assert decrypt(result["token"], key_from_hex(result["key_hex"])) == "a\ue000"


def test_key_from_hex_accepts_common_spellings():
    expected = "\x2e\x13\x0c"
    assert key_from_hex("2e130c") == expected
    assert key_from_hex("2E 13 0C") == expected
    assert key_from_hex("0x2e130c") == expected
    assert key_from_hex("2e:13:0c") == expected


@pytest.mark.parametrize("bad", ["", "   ", "zz", "abc", "0x", "2e13 0"])
def test_key_from_hex_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        key_from_hex(bad)


# --------------------------------------------------------------------------
# Encryption structure (report: Flow Diagram of Encryption Heuristic)
# --------------------------------------------------------------------------
def test_worked_example_namaste_india():
    result = encrypt("Namaste India!")
    nodes = {name: chars(pairs) for name, pairs in result["nodes"].items()}

    assert result["key_hex"] == "2e130c0c12010f45"
    assert render(result["intermediate_values"]) == "`ramaujeg}hes "
    assert nodes["node1"] == [
        ("r", 1), ("a", 2), ("m", 3), ("a", 4), ("u", 5), ("j", 6),
        ("e", 7), ("g", 8), ("h", 10), ("e", 11), ("s", 12),
    ]
    assert nodes["node2"] == [("`", 0), ("}", 9), (" ", 13)]
    assert nodes["node3"] == [("r", 1), ("m", 3), ("u", 5), ("e", 7), ("h", 10), ("s", 12)]
    assert nodes["node4"] == [("a", 2), ("a", 4), ("j", 6), ("g", 8), ("e", 11)]
    assert nodes["node5"] == [("`", 0), (" ", 13)]
    assert nodes["node6"] == [("}", 9)]
    assert nodes["node7"] == nodes["node3"] + nodes["node6"]
    assert nodes["node8"] == nodes["node4"] + nodes["node5"]
    assert render(result["cipher_values"]) == "rmuehs}aajge` "
    assert result["indices"] == [1, 3, 5, 7, 10, 12, 9, 2, 4, 6, 8, 11, 0, 13]


def test_node_structure_holds_for_random_input():
    rng = random.Random(2024)
    pool = string.printable + "বাংলাéüñ"
    for _ in range(200):
        text = "".join(rng.choice(pool) for _ in range(rng.randint(1, 80)))
        values = xor_with_key(text, generate_key(text))
        nodes = build_nodes(values)

        assert sorted(nodes["node1"] + nodes["node2"], key=lambda p: p[1]) == list(
            zip(values, range(len(values)))
        )
        assert nodes["node3"] + nodes["node4"] == nodes["node1"][::2] + nodes["node1"][1::2]
        assert nodes["node7"] == nodes["node3"] + nodes["node6"]
        assert nodes["node8"] == nodes["node4"] + nodes["node5"]

        result = encrypt(text)
        assert result["cipher_values"] == [v for v, _ in nodes["node7"] + nodes["node8"]]
        assert sorted(result["indices"]) == list(range(len(text)))


def test_encryption_is_deterministic():
    assert encrypt("Namaste India!") == encrypt("Namaste India!")


# --------------------------------------------------------------------------
# Report sample outputs and differential test against the report's program
# --------------------------------------------------------------------------
@pytest.mark.parametrize("plaintext, key_hex, intermediate, final", REPORT_SAMPLES)
def test_report_sample_outputs(plaintext, key_hex, intermediate, final):
    result = encrypt(plaintext)
    assert result["key_hex"] == key_hex
    assert render(result["intermediate_values"], placeholder="") == intermediate
    assert render(result["cipher_values"], placeholder="") == final
    assert decrypt(result["token"], result["key"]) == plaintext


def test_matches_report_program_on_random_input():
    """Same key, intermediate text and final ciphertext as the report's code."""
    rng = random.Random(7)
    pool = string.printable.replace("\x00", "") + "বাংলাéüñ£"
    texts = [sample[0] for sample in REPORT_SAMPLES]
    texts += [
        "".join(rng.choice(pool) for _ in range(rng.randint(1, 60))) for _ in range(300)
    ]
    for text in texts:
        key = generate_key(text)
        assert key == report_reference.generate_key(text)

        expected_final, _, _, _, expected_intermediate = report_reference.encrypt(text, key)
        result = encrypt(text)
        assert "".join(map(chr, result["intermediate_values"])) == expected_intermediate
        assert render(result["cipher_values"], placeholder="\x00") == expected_final


# --------------------------------------------------------------------------
# Round trips
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "message",
    [
        "Namaste India!",
        "Hello World",
        "12345",
        "a",
        "aaaa",
        "Symbols: @#$%",
        "Line one\nLine two\ttabbed\r\n",
        "Bengali: বাংলা",
        "Emoji 😀 and accents éüñ",
        "NUL \x00 inside",
        "\U0010ffff\U00010000",  # XOR result above U+10FFFF
        "x" * 5000,
    ],
)
def test_encrypt_decrypt_round_trip(message):
    result = encrypt(message)
    assert decrypt(result["token"], result["key"]) == message
    assert decrypt(result["token"], key_from_hex(result["key_hex"])) == message


def test_round_trip_with_custom_key():
    result = encrypt("Meet at noon", key="secret!!")
    assert result["key"] == "secret!!"
    assert decrypt(result["token"], "secret!!") == "Meet at noon"


def test_wrong_key_does_not_recover_plaintext():
    result = encrypt("Namaste India!")
    assert decrypt(result["token"], "\x01" * KEY_LENGTH) != "Namaste India!"


def test_xor_edge_above_unicode_range_is_handled():
    result = encrypt("\U0010ffff\U00010000")
    assert max(result["intermediate_values"]) > MAX_CODE_POINT
    assert render(result["intermediate_values"]).startswith("\\U001f0000")


# --------------------------------------------------------------------------
# Token format
# --------------------------------------------------------------------------
def test_token_is_printable_ascii():
    result = encrypt("Deploy this project")
    assert result["token"].isascii()
    assert result["token"].isprintable()
    assert result["token"].strip() == result["token"]


def test_token_does_not_contain_the_key():
    result = encrypt("Namaste India!")
    payload = inspect_ciphertext(result["token"])
    assert set(payload) == {"version", "algorithm", "ciphertext", "indices"}
    assert payload["ciphertext"] == result["cipher_values"]
    assert payload["indices"] == result["indices"]


def test_token_padding_and_whitespace_are_tolerated():
    result = encrypt("Namaste India!")
    damaged = " " + result["token"].rstrip("=") + " \n"
    assert decrypt(damaged, result["key"]) == "Namaste India!"


BAD_PAYLOADS = [
    {"version": 2, "ciphertext": [1], "indices": [0]},  # unsupported version
    {"version": 1, "ciphertext": [1, 2], "indices": [0]},  # length mismatch
    {"version": 1, "ciphertext": [1, 2], "indices": [0, 0]},  # duplicate index
    {"version": 1, "ciphertext": [1, 2], "indices": [0, 5]},  # index out of range
    {"version": 1, "ciphertext": [1, 2], "indices": [0, -1]},  # negative index
    {"version": 1, "ciphertext": ["a", 2], "indices": [0, 1]},  # non-integer value
    {"version": 1, "ciphertext": [True, 2], "indices": [0, 1]},  # boolean value
    {"version": 1, "ciphertext": [1, 2], "indices": ["0", 1]},  # non-integer index
    {"version": 1, "ciphertext": [-1], "indices": [0]},  # negative value
    {"version": 1, "ciphertext": [], "indices": []},  # empty
    {"version": 1},  # missing fields
    [1, 2, 3],  # not an object
]


@pytest.mark.parametrize("payload", BAD_PAYLOADS)
def test_decrypt_rejects_malformed_payloads(payload):
    with pytest.raises(ValueError):
        decrypt(make_token(payload), "key12345")


@pytest.mark.parametrize("token", ["", "   ", "not base64 !!!", "Zm9v", "é"])
def test_decrypt_rejects_invalid_tokens(token):
    with pytest.raises(ValueError):
        decrypt(token, "key12345")


@pytest.mark.parametrize("value", [MAX_CODE_POINT + 1, 10**30])
def test_decrypt_reports_undecodable_values_as_value_error(value):
    token = make_token({"version": 1, "ciphertext": [value], "indices": [0]})
    with pytest.raises(ValueError):
        decrypt(token, "\x00")


def test_empty_inputs_are_rejected():
    with pytest.raises(ValueError):
        encrypt("")
    with pytest.raises(ValueError):
        encrypt("text", key="")
    with pytest.raises(ValueError):
        decrypt(encrypt("text")["token"], "")
    with pytest.raises(ValueError):
        xor_with_key("text", "")


# --------------------------------------------------------------------------
# Display helper
# --------------------------------------------------------------------------
def test_render_escapes_or_masks_non_printable_characters():
    values = [ord("a"), 0x0E, 0xAD, 0x200B, 0x1F0000]
    assert render(values) == "a\\x0e\\xad\\u200b\\U001f0000"
    assert render(values, placeholder="?") == "a????"
    assert render(values, placeholder="") == "a"


# --------------------------------------------------------------------------
# Documentation stays in sync with the code
# --------------------------------------------------------------------------
def test_docs_show_the_current_worked_example():
    result = encrypt("Namaste India!")
    docs = (ROOT / "docs" / "algorithm.md").read_text(encoding="utf-8")
    assert result["key_hex"] in docs
    assert result["token"] in docs
    assert render(result["cipher_values"]).strip() in docs
