
from .encoders import DataBase64Encoder, DataEncoder, DataFernetEncoder
from .file import load_data, save_data
from typing import Tuple, Optional

class FileNameEncoder:
    def __init__(self) -> None:
        self.encoder = DataBase64Encoder(True)

    def encode(self, file_name: str) -> str:
        """Encodes a filename"""
        return self.encoder.encode(file_name.encode()).decode()
        
    def decode(self, url_safe_file_name: str) -> str:
        """Decodes a filename"""
        return self.encoder.decode(url_safe_file_name.encode()).decode()


class FileEncoder:
    def __init__(self, encrypt_file: bool, key: Optional[bytes]):
        self.file_name_encoder = FileNameEncoder()
        self.encoder : DataEncoder
        if encrypt_file:
            if not key:
                raise ValueError("Key must be provided when encrypting a file")
            self.encoder = DataFernetEncoder(key)
        else:
            self.encoder = DataBase64Encoder(False)

    def encode_file(self, file_name: str) -> Tuple[str, bytes]:
        input_data = load_data(file_name)
        encrypted_data = self.encoder.encode(input_data)
        encrypted_file_name = self.file_name_encoder.encode(file_name)
        save_data(encrypted_file_name, encrypted_data)
        return encrypted_file_name, encrypted_data
    
    @staticmethod
    def replace_last_dot(input_string: str, post_fix: str) -> str:
        # Split the string from the last occurrence of "."
        parts = input_string.rsplit(".", 1)
        # If there's no dot, return the original string
        if len(parts) == 1:
            return input_string
        # Replace the last "." with ".old."
        return f"{parts[0]}.{post_fix}.{parts[1]}"

    def decode_file(self, encrypted_file_name: str, post_fix: str = "") -> Tuple[str, bytes]:
        encrypted_data = load_data(encrypted_file_name)
        decrypted_data = self.encoder.decode(encrypted_data)
        decrypted_file_name = self.file_name_encoder.decode(encrypted_file_name)
        if post_fix:
            decrypted_file_name = self.replace_last_dot(decrypted_file_name, post_fix)
        save_data(decrypted_file_name, decrypted_data)
        return decrypted_file_name, decrypted_data
