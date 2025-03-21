import base64
from cryptography.fernet import Fernet
from typing import Optional
from .file import load_data


def generate_encryption_key() -> bytes:
    """
    Generate a new encryption key
    """
    return Fernet.generate_key()


def generate_personal_key(custom_key: str) -> bytes:
    """
    Generate a personal key
    """
    length = len(custom_key)
    if length < 32:
        custom_key = custom_key.ljust(32, "+")
    elif length > 32:
        custom_key = custom_key[:32]
    return base64.urlsafe_b64encode(custom_key.encode())


def create_key_file(file_name: str = "key.txt" , custom_key: Optional[str] = None) -> bytes:
    """
    Create a key file
    """
    key = generate_personal_key(custom_key) if custom_key else generate_encryption_key()
    with open(file_name, "wb") as file:
        file.write(key)
    return key


def load_key_file(file_name: str = "key.txt") -> bytes:
    """
    Load a key file
    """
    return load_data(file_name)


def encode_to_base64(data: bytes, use_safe_url: bool) -> bytes:
    """Encodes content to Base64 and remove paddings."""
    encoded_data = base64.urlsafe_b64encode(data) if use_safe_url else base64.b64encode(data)
    return encoded_data.rstrip(b"=")

def decode_from_base64(data: bytes, use_safe_url: bool) -> bytes:
    """Decodes content from Base64 by adding padding if necessary."""
    # Add padding if necessary
    padding_needed = len(data) % 4  # Base64 requires multiples of 4
    if padding_needed:
        data += b"=" * (4 - padding_needed)
    # Decode data from Base64
    return base64.urlsafe_b64decode(data) if use_safe_url else base64.b64decode(data)
    

def handle_encryption(key: bytes, input: bytes, encrypt: bool) -> bytes:
    """
    Encrypt or decrypt the input data using the key
    Args:
        key: the encryption key
        input: the input data
        encrypt: whether to encrypt or decrypt the data
    Returns:
        the encrypted or decrypted data
    """
    fernet = Fernet(key)

    # encrypt or decrypt the data
    output = fernet.encrypt(input) if encrypt else fernet.decrypt(input)

    return output

def encrypt_input(key: bytes, input: bytes) -> bytes:
    """
    Encrypt the input data using the key
    Args:
        key: the encryption key
        input: the input data
    Returns:
        the encrypted data
    """
    return handle_encryption(key, input, True)

def decrypt_input(key: bytes, input: bytes) -> bytes:
    """
    Decrypt the input data using the key
    Args:
        key: the encryption key
        input: the input data
    Returns:
        the decrypted data
    """
    return handle_encryption(key, input, False)
