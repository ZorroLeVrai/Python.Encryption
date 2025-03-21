import pytest
import encryption.cypher as cypher

def test_encrypt_decrypt_generate_same_data():
    key = cypher.KeyGenerator().generate_key()
    input_data = b"Hello, World!"
    data_encoder = cypher.DataFernetEncoder(key)
    encrypted_data = data_encoder.encode(input_data)
    decrypted_data = data_encoder.decode(encrypted_data)
    assert input_data == decrypted_data

def test_encrypt_decrypt_with_custom_key():
    key = cypher.KeyGenerator("This is a key").generate_key()
    input_data = b"Hello, World!"
    data_encoder = cypher.DataFernetEncoder(key)
    encrypted_data = data_encoder.encode(input_data)
    decrypted_data = data_encoder.decode(encrypted_data)
    assert input_data == decrypted_data

def test_encrypt_decrypt_with_invalid_key():
    key = cypher.KeyGenerator("This is a key").generate_key()
    input_data = b"Hello, World!"
    data_encoder = cypher.DataFernetEncoder(key)
    encrypted_data = data_encoder.encode(input_data)
    invalid_key = cypher.KeyGenerator("Invalid key").generate_key()
    data_encoder = cypher.DataFernetEncoder(invalid_key)
    with pytest.raises(Exception):
        data_encoder.decode(encrypted_data)
