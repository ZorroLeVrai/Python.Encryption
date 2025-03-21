
from .encoders import DataBase64Encoder, DataEncoder, DataFernetEncoder
from .file import load_data, rename, save_data
from typing import Tuple, Optional
import os

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

    @staticmethod
    def replace_last_dot(input_string: str, post_fix: str) -> str:
        # Split the string from the last occurrence of "."
        parts = input_string.rsplit(".", 1)
        # If there's no dot, return the original string
        if len(parts) == 1:
            return input_string
        # Replace the last "." with ".old."
        return f"{parts[0]}.{post_fix}.{parts[1]}"
    
    def encode_file(self, file_name: str) -> Tuple[str, bytes]:
        """
        Encodes a given file
        Args:
            file_name: The name of the file to encode
        Returns:
            The name of the encoded file and the encoded data
        """
        input_data = load_data(file_name)
        encrypted_data = self.encoder.encode(input_data)
        encrypted_file_name = self.file_name_encoder.encode(file_name)
        save_data(encrypted_file_name, encrypted_data)
        return encrypted_file_name, encrypted_data

    def decode_file(self, encrypted_file_name: str, post_fix: str = "") -> Tuple[str, bytes]:
        """
        Decodes a given file
        Args:
            encrypted_file_name: The name of the file to decode
            post_fix: The post-fix to add to the decoded file name
        Returns:
            The name of the decoded file and the decoded data
        """
        encrypted_data = load_data(encrypted_file_name)
        decrypted_data = self.encoder.decode(encrypted_data)
        decrypted_file_name = self.file_name_encoder.decode(encrypted_file_name)
        if post_fix:
            decrypted_file_name = self.replace_last_dot(decrypted_file_name, post_fix)
        save_data(decrypted_file_name, decrypted_data)
        return decrypted_file_name, decrypted_data
    
    @staticmethod
    def encode_only_directory(full_path: str, parent_directory: Optional[str] = None, directory_name: Optional[str] = None) -> str:
        """
        Encodes only the directory name
        Args:
            directory_path: The path to the directory to encode
        """
        if not parent_directory:
            parent_directory = os.path.dirname(full_path)
        if not directory_name:
            directory_name = os.path.basename(full_path)
        encoded_directory_name = FileNameEncoder().encode(directory_name)
        encoded_full_path = os.path.join(parent_directory, encoded_directory_name)
        rename(full_path, encoded_full_path)
        return encoded_full_path

    @staticmethod
    def decode_only_directory(full_path: str, parent_directory: Optional[str] = None, directory_name: Optional[str] = None, post_fix: str = "") -> str:
        """
        Decodes only the directory name
        Args:
            directory_path: The path to the directory to decode
            post_fix: The post-fix to add to the decoded directory name
        """
        if not parent_directory:
            parent_directory = os.path.dirname(full_path)
        if not directory_name:
            directory_name = os.path.basename(full_path)
        decoded_directory_name = FileNameEncoder().decode(directory_name)
        if post_fix:
            decoded_directory_name += f".{post_fix}"
        decoded_full_path = os.path.join(parent_directory, decoded_directory_name)
        rename(full_path, decoded_full_path)
        return decoded_full_path

    def encode_directory(self, directory_path: str) -> None:
        for item_name in os.listdir(directory_path):
            full_path = os.path.join(directory_path, item_name)
            if os.path.isdir(item_name):
                self.encode_directory(full_path)
                self.encode_only_directory(full_path, directory_path, item_name)
            else:
                self.encode_file(full_path)

        self.encode_only_directory(directory_path)


    def decode_directory(self, directory_path: str, post_fix: str = "") -> None:
        for item_name in os.listdir(directory_path):
            full_path = os.path.join(directory_path, item_name)
            if os.path.isdir(item_name):
                self.decode_directory(full_path)
                self.decode_only_directory(full_path, directory_path, item_name)
            else:
                self.decode_file(full_path)
            
        self.decode_only_directory(directory_path, None, None, post_fix)
