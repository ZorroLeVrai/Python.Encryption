
import base64
from cypher import decrypt_input, encrypt_input
from file import load_data, save_data


def encode_file_name(key: bytes, file_name: str) -> str:
    """Encodes a filename-safe Base64 string by removing padding."""
    # Encrypt the file name
    encrypted_file_name = encrypt_input(key, file_name.encode())
    # Transform the encrypted file name into a filename-safe Base 64 string
    return base64.urlsafe_b64encode(encrypted_file_name).decode().rstrip("=")

def decode_file_name(key: bytes, url_safe_encrypted_file_name: str) -> str:
    """Decodes a filename-safe Base64 string by adding padding if necessary."""
    # Add padding if necessary
    padding_needed = len(url_safe_encrypted_file_name) % 4  # Base64 requires multiples of 4
    if padding_needed:
        url_safe_encrypted_file_name += "=" * (4 - padding_needed)
    # Decode the filename-safe Base 64 string
    encrypted_file_name = base64.urlsafe_b64decode(url_safe_encrypted_file_name)
    # Decrypt the file name
    return decrypt_input(key, encrypted_file_name)


def handle_file_encryption(key: bytes, fileName: str) -> None:
    input_data = load_data(fileName)
    encrypted_data = encrypt_input(input_data, key)
    encrypted_file_name = encode_file_name(fileName, key)
    save_data(encrypted_file_name, encrypted_data)