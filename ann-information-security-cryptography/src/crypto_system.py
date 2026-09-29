"""Educational implementation of the B.Sc. project's symmetric-key heuristic.

Project report: "A Survey on Information Security Using Artificial Neural
Network" (B.Sc. (Hons) Computer Science, Ramakrishna Mission Vivekananda
Centenary College, Rahara, April 2024).

Important: this is an academic demonstration, not a modern cryptographic
primitive. Do not use it to protect real secrets (see docs/algorithm.md).

Encryption follows the report's "Flow Diagram of Encryption Heuristic":

    input layer    plaintext XOR key            -> intermediate ciphertext
    hidden layer   Node 1  alphabetic values
                   Node 2  non-alphabetic values
                   Node 3  even positions of Node 1
                   Node 4  odd positions of Node 1
                   Node 5  even positions of Node 2
                   Node 6  odd positions of Node 2
                   Node 7  Node 3 + Node 6
                   Node 8  Node 4 + Node 5
    output layer   Node 7 + Node 8              -> final ciphertext

Every value keeps its original index, so decryption sorts by index and then
reverses the XOR (report: "Decryption Heuristic").
"""

from __future__ import annotations

import base64
import json
from typing import Any, Iterable

__all__ = [
    "KEY_LENGTH",
    "build_nodes",
    "decrypt",
    "encrypt",
    "generate_key",
    "inspect_ciphertext",
    "key_from_hex",
    "key_to_hex",
    "render",
    "xor_with_key",
]

KEY_LENGTH = 8
TOKEN_VERSION = 1
ALGORITHM_ID = "BSc-ANN-information-security-heuristic"
MAX_CODE_POINT = 0x10FFFF

# A cipher value together with its index in the original message.
Pair = tuple[int, int]


# --------------------------------------------------------------------------
# Key generation
# --------------------------------------------------------------------------
def generate_key(plaintext: str) -> str:
    """Generate the 8-character key described in the report.

    The plaintext is repeated until it covers KEY_LENGTH characters, the first
    KEY_LENGTH characters are taken, and key[i] is the absolute difference
    between character i and character i - 1 (index -1 wraps to the last
    character, exactly as in the report's source code).
    """
    if not plaintext:
        raise ValueError("Plaintext must not be empty.")

    key_part = (plaintext * (KEY_LENGTH // len(plaintext) + 1))[:KEY_LENGTH]
    codes = [ord(char) for char in key_part]
    return "".join(chr(abs(codes[i] - codes[i - 1])) for i in range(KEY_LENGTH))


def key_to_hex(key: str) -> str:
    """Return a printable, copy-paste-safe form of a key (UTF-8 bytes as hex).

    Generated keys usually contain control characters (for example NUL or
    newline), so the raw key cannot be typed or pasted reliably.
    """
    return key.encode("utf-8", "surrogatepass").hex()


def key_from_hex(text: str) -> str:
    """Parse a key printed by key_to_hex(). Spaces, colons and 0x are ignored."""
    cleaned = "".join(text.split()).replace(":", "")
    if cleaned[:2].lower() == "0x":
        cleaned = cleaned[2:]
    if not cleaned:
        raise ValueError("Key must not be empty.")
    try:
        return bytes.fromhex(cleaned).decode("utf-8", "surrogatepass")
    except ValueError as exc:
        raise ValueError(
            "Key must be a hexadecimal string, as printed by the encrypt step."
        ) from exc


# --------------------------------------------------------------------------
# Encryption
# --------------------------------------------------------------------------
def xor_with_key(text: str, key: str) -> list[int]:
    """XOR every character code with the cyclically repeated key."""
    if not key:
        raise ValueError("Key must not be empty.")
    return [ord(char) ^ ord(key[i % len(key)]) for i, char in enumerate(text)]


def _is_alpha(value: int) -> bool:
    return value <= MAX_CODE_POINT and chr(value).isalpha()


def build_nodes(values: list[int]) -> dict[str, list[Pair]]:
    """Build the report's hidden layer (Node 1 ... Node 8) from XOR values.

    Even/odd refers to the position inside Node 1 or Node 2 (as in the report's
    source code), not to the index in the original message.
    """
    node1 = [(v, i) for i, v in enumerate(values) if _is_alpha(v)]
    node2 = [(v, i) for i, v in enumerate(values) if not _is_alpha(v)]
    node3, node4 = node1[::2], node1[1::2]
    node5, node6 = node2[::2], node2[1::2]
    node7 = node3 + node6
    node8 = node4 + node5
    return {
        "node1": node1,
        "node2": node2,
        "node3": node3,
        "node4": node4,
        "node5": node5,
        "node6": node6,
        "node7": node7,
        "node8": node8,
    }


def _encode_token(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii")


def encrypt(plaintext: str, key: str | None = None) -> dict[str, Any]:
    """Encrypt plaintext and return a serializable result.

    If no key is given, the report's key-generation heuristic is used.
    The returned token contains only the cipher values and their indices;
    the key is never part of it and must be shared separately.
    """
    if not plaintext:
        raise ValueError("Plaintext must not be empty.")

    key = key if key is not None else generate_key(plaintext)
    if not key:
        raise ValueError("Key must not be empty.")

    intermediate = xor_with_key(plaintext, key)
    nodes = build_nodes(intermediate)
    final = nodes["node7"] + nodes["node8"]
    cipher_values = [value for value, _ in final]
    indices = [index for _, index in final]

    token = _encode_token(
        {
            "version": TOKEN_VERSION,
            "algorithm": ALGORITHM_ID,
            "ciphertext": cipher_values,
            "indices": indices,
        }
    )

    return {
        "key": key,
        "key_hex": key_to_hex(key),
        "intermediate_values": intermediate,
        "nodes": nodes,
        "cipher_values": cipher_values,
        "indices": indices,
        "token": token,
    }


# --------------------------------------------------------------------------
# Decryption
# --------------------------------------------------------------------------
def _decode_token(token: str) -> dict[str, Any]:
    try:
        text = token.strip()
        text += "=" * (-len(text) % 4)  # tolerate stripped base64 padding
        payload = json.loads(
            base64.urlsafe_b64decode(text.encode("ascii")).decode("utf-8")
        )
    except Exception as exc:
        raise ValueError("Invalid ciphertext token.") from exc
    if not isinstance(payload, dict):
        raise ValueError("Malformed ciphertext token.")
    return payload


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _restore_order(payload: dict[str, Any]) -> list[int]:
    """Sort the cipher values back into message order using their indices."""
    if payload.get("version") != TOKEN_VERSION:
        raise ValueError("Unsupported ciphertext version.")

    values = payload.get("ciphertext")
    indices = payload.get("indices")
    if not isinstance(values, list) or not isinstance(indices, list) or not values:
        raise ValueError("Malformed ciphertext token.")
    if len(values) != len(indices):
        raise ValueError("Ciphertext/index length mismatch.")
    if not all(_is_int(v) and v >= 0 for v in values):
        raise ValueError("Malformed ciphertext values.")

    restored: list[int | None] = [None] * len(values)
    for value, index in zip(values, indices):
        if not _is_int(index) or not 0 <= index < len(restored):
            raise ValueError("Malformed ciphertext index.")
        restored[index] = value

    if any(v is None for v in restored):
        raise ValueError("Ciphertext contains incomplete indices.")
    return restored  # type: ignore[return-value]


def decrypt(token: str, key: str) -> str:
    """Decrypt a token produced by encrypt().

    There is no authentication: a wrong key returns unreadable text instead
    of an error.
    """
    if not token or not token.strip():
        raise ValueError("Ciphertext token must not be empty.")
    if not key:
        raise ValueError("Key must not be empty.")

    restored = _restore_order(_decode_token(token))
    try:
        return "".join(
            chr(value ^ ord(key[i % len(key)])) for i, value in enumerate(restored)
        )
    except (ValueError, OverflowError) as exc:
        raise ValueError("Decryption failed: wrong key or corrupted token.") from exc


def inspect_ciphertext(token: str) -> dict[str, Any]:
    """Return decoded token details for demonstration/debugging."""
    return _decode_token(token)


# --------------------------------------------------------------------------
# Display helper
# --------------------------------------------------------------------------
def render(values: Iterable[int], placeholder: str | None = None) -> str:
    """Return a printable string for a sequence of character codes.

    Non-printable characters are shown as escapes such as ``\\x0e``. If
    ``placeholder`` is given they are replaced by it instead (the report's
    console output shows them as NUL/boxes).
    """
    parts: list[str] = []
    for value in values:
        char = chr(value) if 0 <= value <= MAX_CODE_POINT else ""
        if char and char.isprintable():
            parts.append(char)
        elif placeholder is not None:
            parts.append(placeholder)
        elif value <= 0xFF:
            parts.append(f"\\x{value:02x}")
        elif value <= 0xFFFF:
            parts.append(f"\\u{value:04x}")
        else:
            parts.append(f"\\U{value:08x}")
    return "".join(parts)
