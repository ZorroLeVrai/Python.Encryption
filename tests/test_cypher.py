import pytest
import encryption.cypher as cypher

def test_encrypt_decrypt_generate_same_data():
    key = cypher.generate_encryption_key()
    input_data = b"Hello, World!"
    encrypted_data = cypher.encrypt_input(key, input_data)
    decrypted_data = cypher.decrypt_input(key, encrypted_data)
    assert input_data == decrypted_data

def test_encrypt_decrypt_with_custom_key():
    key = cypher.generate_personal_key("This is a key")
    input_data = b"Hello, World!"
    encrypted_data = cypher.encrypt_input(key, input_data)
    decrypted_data = cypher.decrypt_input(key, encrypted_data)
    assert input_data == decrypted_data

def test_encrypt_decrypt_with_invalid_key():
    key = cypher.generate_personal_key("This is a key")
    input_data = b"Hello, World!"
    encrypted_data = cypher.encrypt_input(key, input_data)
    invalid_key = key = cypher.generate_personal_key("Invalid key")
    with pytest.raises(Exception):
        cypher.decrypt_input(invalid_key, encrypted_data)
