import pytest
import encryption.encoders as encoders
import encryption.key_generator as key_generator

def test_encrypt_decrypt_generate_same_data() -> None:
    key = key_generator.KeyGenerator().generate_key()
    input_data = b"Hello, World!"
    data_encoder = encoders.DataFernetEncoder(key)
    encrypted_data = data_encoder.encode(input_data)
    decrypted_data = data_encoder.decode(encrypted_data)
    assert input_data == decrypted_data

def test_encrypt_decrypt_with_custom_key() -> None:
    key = key_generator.KeyGenerator("This is a key").generate_key()
    input_data = b"Hello, World!"
    data_encoder = encoders.DataFernetEncoder(key)
    encrypted_data = data_encoder.encode(input_data)
    decrypted_data = data_encoder.decode(encrypted_data)
    assert input_data == decrypted_data

def test_encrypt_decrypt_with_invalid_key() -> None:
    key = key_generator.KeyGenerator("This is a key").generate_key()
    input_data = b"Hello, World!"
    data_encoder = encoders.DataFernetEncoder(key)
    encrypted_data = data_encoder.encode(input_data)
    invalid_key = key_generator.KeyGenerator("Invalid key").generate_key()
    data_encoder = encoders.DataFernetEncoder(invalid_key)
    with pytest.raises(Exception):
        data_encoder.decode(encrypted_data)
