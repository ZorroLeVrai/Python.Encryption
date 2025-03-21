import base64
from cryptography.fernet import Fernet
from typing import Optional
from .file import load_data
from abc import ABC, abstractmethod

class KeyGenerator:
    def __init__(self, custom_key: Optional[str] = None):
        self.custom_key = custom_key

    @staticmethod
    def __generate_encryption_key() -> bytes:
        """
        Generate a new encryption key
        """
        return Fernet.generate_key()

    @staticmethod
    def __generate_personal_key(custom_key: str) -> bytes:
        """
        Generate a personal key
        """
        length = len(custom_key)
        if length < 32:
            custom_key = custom_key.ljust(32, "+")
        elif length > 32:
            custom_key = custom_key[:32]
        return base64.urlsafe_b64encode(custom_key.encode())
    
    def generate_key(self) -> bytes:
        """
        Generate a key
        """
        if self.custom_key:
            return self.__generate_personal_key(self.custom_key)
        return self.__generate_encryption_key()


class KeyFileGenerator:
    def __init__(self, file_name: str = "key.txt", custom_key: Optional[str] = None):
        self.file_name = file_name
        self.key_generator = KeyGenerator(custom_key)


    def create_key_file(self) -> bytes:
        """
        Create a key file
        """
        key = self.key_generator.generate_key()
        with open(self.file_name, "wb") as file:
            file.write(key)
        return key

    def load_key_file(self) -> bytes:
        """
        Load a key file
        """
        return load_data(self.file_name)


class DataEncoder(ABC):
    @abstractmethod
    def encode(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> bytes:
        pass

class DataBase64Encoder(DataEncoder):
    def __init__(self, use_safe_url: bool):
        self.use_safe_url = use_safe_url

    def encode(self, data: bytes) -> bytes:
        """
        Encode content to Base64 and remove paddings
        """
        encoded_data = base64.urlsafe_b64encode(data) if self.use_safe_url else base64.b64encode(data)
        return encoded_data.rstrip(b"=")

    def decode(self, data: bytes) -> bytes:
        """
        Decode content from Base64 by adding padding if necessary
        """
        # Add padding if necessary
        padding_needed = len(data) % 4  # Base64 requires multiples of 4
        if padding_needed:
            data += b"=" * (4 - padding_needed)
        # Decode data from Base64
        return base64.urlsafe_b64decode(data) if self.use_safe_url else base64.b64decode(data)


class DataFernetEncoder(DataEncoder):
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encode(self, data: bytes) -> bytes:
        """
        Encrypt the data
        """
        return self.fernet.encrypt(data)

    def decode(self, data: bytes) -> bytes:
        """
        Decrypt the data
        """
        return self.fernet.decrypt(data)
    

