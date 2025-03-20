
import base64
from .cypher import decrypt_input, encrypt_input
from .file import load_data, save_data


def encode_file_name(file_name: str) -> str:
    """Encodes a filename-safe Base64 string by removing padding."""
    # Transform the file name into a filename-safe Base 64 string
    return base64.urlsafe_b64encode(file_name.encode()).decode().rstrip("=")

def decode_file_name(url_safe_file_name: str) -> str:
    """Decodes a filename-safe Base64 string by adding padding if necessary."""
    # Add padding if necessary
    padding_needed = len(url_safe_file_name) % 4  # Base64 requires multiples of 4
    if padding_needed:
        url_safe_file_name += "=" * (4 - padding_needed)
    # Decode the filename-safe Base 64 string
    return base64.urlsafe_b64decode(url_safe_file_name).decode()


def encode_file(key: bytes, file_name: str) -> None:
    input_data = load_data(file_name)
    encrypted_data = encrypt_input(key, input_data)
    encrypted_file_name = encode_file_name(file_name)
    save_data(encrypted_file_name, encrypted_data)

def decode_file(key: bytes, encrypted_file_name: str) -> None:
    encrypted_data = load_data(encrypted_file_name)
    decrypted_data = decrypt_input(key, encrypted_data)
    decrypted_file_name = decode_file_name(encrypted_file_name)
    save_data(decrypted_file_name, decrypted_data)
