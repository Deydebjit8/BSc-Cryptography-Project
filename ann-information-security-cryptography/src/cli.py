"""Command-line interface for the educational B.Sc. project demo.

    python -m src.cli                          interactive menu
    python -m src.cli demo "Namaste India!"    encrypt + decrypt, like the report's program
    python -m src.cli encrypt "some text"      print key (hex) and ciphertext token
    python -m src.cli decrypt TOKEN KEY_HEX    recover the plaintext

Generated keys usually contain control characters, so keys are always
printed and entered as hexadecimal text.
"""

from __future__ import annotations

import argparse
from typing import Any, Sequence

from .crypto_system import decrypt, encrypt, key_from_hex, render


def _show_encryption(result: dict[str, Any]) -> None:
    print("Generated key (hex):", result["key_hex"])
    print("Generated key (chars):", render(map(ord, result["key"])))
    print("Intermediate ciphertext:", render(result["intermediate_values"]))
    print("Final ciphertext:", render(result["cipher_values"]))
    print("Ciphertext token:", result["token"])


def _encrypt(text: str | None) -> int:
    plaintext = text if text is not None else input("Enter plaintext: ")
    try:
        result = encrypt(plaintext)
    except ValueError as exc:
        print("Error:", exc)
        return 1
    _show_encryption(result)
    print("\nShare the key separately from the token.")
    return 0


def _decrypt(token: str | None, key_hex: str | None) -> int:
    token = token if token is not None else input("Enter ciphertext token: ")
    key_hex = key_hex if key_hex is not None else input("Enter key (hex): ")
    try:
        plaintext = decrypt(token.strip(), key_from_hex(key_hex))
    except ValueError as exc:
        print("Error:", exc)
        return 1
    print("Decrypted:", plaintext)
    return 0


def _demo(text: str | None) -> int:
    plaintext = text if text is not None else input("Enter the plaintext to encrypt: ")
    try:
        result = encrypt(plaintext)
        decrypted = decrypt(result["token"], result["key"])
    except ValueError as exc:
        print("Error:", exc)
        return 1
    _show_encryption(result)
    print("Decrypted:", decrypted)
    return 0


def _menu() -> int:
    print("B.Sc. Information Security using ANN - educational CLI")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Demo (encrypt and decrypt, as in the report)")
    choice = input("Choose: ").strip()
    if choice == "1":
        return _encrypt(None)
    if choice == "2":
        return _decrypt(None, None)
    if choice == "3":
        return _demo(None)
    print("Invalid choice.")
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.cli",
        description="Educational demo of the B.Sc. project encryption heuristic. "
        "Not for protecting real secrets. Run without arguments for a menu.",
    )
    commands = parser.add_subparsers(dest="command")

    encrypt_cmd = commands.add_parser("encrypt", help="encrypt text")
    encrypt_cmd.add_argument("text", nargs="?", help="plaintext (prompted if omitted)")

    decrypt_cmd = commands.add_parser("decrypt", help="decrypt a ciphertext token")
    decrypt_cmd.add_argument("token", nargs="?", help="ciphertext token")
    decrypt_cmd.add_argument("key_hex", nargs="?", help="key as hexadecimal text")

    demo_cmd = commands.add_parser("demo", help="encrypt and decrypt, as in the report")
    demo_cmd.add_argument("text", nargs="?", help="plaintext (prompted if omitted)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "encrypt":
            return _encrypt(args.text)
        if args.command == "decrypt":
            return _decrypt(args.token, args.key_hex)
        if args.command == "demo":
            return _demo(args.text)
        return _menu()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram interrupted by the user. Exiting...")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
