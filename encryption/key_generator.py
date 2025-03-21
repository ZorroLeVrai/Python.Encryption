import base64
from cryptography.fernet import Fernet
from typing import Optional
from encryption.file import load_data

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


    def generate(self) -> bytes:
        """
        Create a key file
        """
        key = self.key_generator.generate_key()
        with open(self.file_name, "wb") as file:
            file.write(key)
        return key

    def load(self) -> bytes:
        """
        Load a key file
        """
        return load_data(self.file_name)