
import base64
from .cypher import decode_from_base64, decrypt_input, encode_to_base64, encrypt_input
from .file import load_data, save_data
from typing import Tuple, Optional


def encode_file_name(file_name: str) -> str:
    """Encodes a filename-safe Base64 string by removing padding."""
    # Transform the file name into a filename-safe Base 64 string
    return encode_to_base64(file_name.encode(), True).decode()


def decode_file_name(url_safe_file_name: str) -> str:
    """Decodes a filename-safe Base64 string by adding padding if necessary."""
    return decode_from_base64(url_safe_file_name.encode(), True).decode()


class FileEncoder:
    def __init__(self, encrypt_file: bool, key: Optional[bytes]):
        self.encrypt_file = encrypt_file
        self.key = key

    def encode_file(self, file_name: str) -> Tuple[str, bytes]:
        input_data = load_data(file_name)
        if self.encrypt_file:
            encrypted_data = encrypt_input(self.key, input_data)
        else:
            encrypted_data = encode_to_base64(input_data, False)

        encrypted_file_name = encode_file_name(file_name)
        save_data(encrypted_file_name, encrypted_data)
        return encrypted_file_name, encrypted_data

    def decode_file(self, encrypted_file_name: str) -> Tuple[str, bytes]:
        encrypted_data = load_data(encrypted_file_name)
        if self.encrypt_file:
            decrypted_data = decrypt_input(self.key, encrypted_data)
        else:
            decrypted_data = decode_from_base64(encrypted_data, False)
        decrypted_file_name = decode_file_name(encrypted_file_name)
        save_data(decrypted_file_name, decrypted_data)
        return decrypted_file_name, decrypted_data
