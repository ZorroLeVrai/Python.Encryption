from cryptography.fernet import Fernet

def generate_encryption_key() -> bytes:
    """
    Generate a new encryption key
    """
    return Fernet.generate_key()


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
