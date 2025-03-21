
from .cypher import DataBase64Encoder, DataFernetEncoder
from .file import load_data, save_data
from typing import Tuple, Optional

class FileNameEncoder:
    def __init__(self):
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

    def decode_file(self, encrypted_file_name: str) -> Tuple[str, bytes]:
        encrypted_data = load_data(encrypted_file_name)
        decrypted_data = self.encoder.decode(encrypted_data)
        decrypted_file_name = self.file_name_encoder.decode(encrypted_file_name)
        save_data(decrypted_file_name, decrypted_data)
        return decrypted_file_name, decrypted_data
