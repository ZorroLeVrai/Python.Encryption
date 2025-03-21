import base64
from cryptography.fernet import Fernet
from abc import ABC, abstractmethod


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
