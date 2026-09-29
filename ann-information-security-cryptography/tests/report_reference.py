"""Source code of the B.Sc. report, kept only as a reference for tests.

Reproduced from the "Source Code" section of the project report
(docs/project-report.pdf, pp. 33-38). Indentation and line wrapping were
restored; the logic is unchanged.

Do not reuse this module. Its ``decrypt()`` ignores the ``ciphertext``
argument and rebuilds the plaintext from side data (``combined_chars`` and
``skipped_chars``, which holds original plaintext characters). The tests use
it to check that ``src.crypto_system`` produces the same key, intermediate
ciphertext and final ciphertext as the report's program.
"""


def generate_key(plaintext):
    """Generates a key based on the plaintext."""
    key_length = 8
    key_part = (plaintext * (key_length // len(plaintext) + 1))[:key_length]
    ascii_values = [ord(char) for char in key_part]
    key = ''.join(chr(abs(ascii_values[i] - ascii_values[i-1])) for i in range(key_length))
    return key


def encode_null_chars(plaintext):
    """Encode null characters in the plaintext."""
    encoded_text = plaintext.replace('\x00', '<NULL>')  # Example encoding for null characters
    return encoded_text


def decode_null_chars(encoded_text):
    """Decode the encoded null characters back to null characters."""
    plaintext = encoded_text.replace('<NULL>', '\x00')  # Example decoding for null characters
    return plaintext


def encrypt(plaintext, key):
    plaintext = encode_null_chars(plaintext)
    """Encrypts plaintext, handling non-printable characters and additional steps."""
    skipped_indices = []
    skipped_chars = []
    encrypted_chars = []
    combined_chars = []
    intermediate_encrypted_text = ""

    for i, char in enumerate(plaintext):
        key_char = key[i % len(key)]  # Cycle through key
        encrypted_char = chr(ord(char) ^ ord(key_char))
        intermediate_encrypted_text += encrypted_char
        if not encrypted_char.isprintable():
            skipped_indices.append(i)
            skipped_chars.append(char)
            encrypted_char = '\x00'  # Use the null character as a placeholder for non-printable characters

        encrypted_chars.append(encrypted_char)
        combined_chars.append((encrypted_char, i))

    # Sort combined characters and indices
    combined_chars.sort(key=lambda x: x[1])

    # Split and concatenate
    alpha_chars = ''.join(c for c in encrypted_chars if c.isalpha())
    non_alpha_chars = ''.join(c for c in encrypted_chars if not c.isalpha())

    alpha_even = alpha_chars[::2]
    alpha_odd = alpha_chars[1::2]
    non_alpha_even = non_alpha_chars[::2]
    non_alpha_odd = non_alpha_chars[1::2]

    encrypted_text = ''.join([alpha_even, non_alpha_odd, alpha_odd, non_alpha_even])
    return encrypted_text, skipped_indices, skipped_chars, combined_chars, intermediate_encrypted_text


def decrypt(ciphertext, key, skipped_indices, skipped_chars, combined_chars, intermediate_encrypted_text):
    """Decrypts the encrypted text using the provided key and combined characters."""
    print("Intermediate ciphertext:", intermediate_encrypted_text)
    sorted_combined_chars = sorted(combined_chars, key=lambda x: x[1])
    plaintext_chars = []
    for char, index in sorted_combined_chars:
        if index in skipped_indices:
            plaintext_chars.append(skipped_chars[skipped_indices.index(index)])  # Replace the null character with the original character
        else:
            plaintext_char = chr(ord(char) ^ ord(key[index % len(key)]))
            plaintext_chars.append(plaintext_char)
    plaintext = ''.join(plaintext_chars)
    plaintext = decode_null_chars(plaintext)
    return plaintext
