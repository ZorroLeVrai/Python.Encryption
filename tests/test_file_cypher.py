import pytest
from encryption.cypher import generate_encryption_key
import encryption.file_cypher as file_cypher
from unittest.mock import patch

def test_file_name_encrypt_decrypt_generate_same_name():
    file_name = "Hello world.jpg"
    encoded_file_name = file_cypher.encode_file_name(file_name)
    decoded_file_name = file_cypher.decode_file_name(encoded_file_name)
    assert file_name == decoded_file_name

@pytest.mark.parametrize("encrypt_file", [True, False])
def test_file_encrypt_decrypt_generate_same_data(encrypt_file: bool):
    with patch("encryption.file_cypher.load_data") as mock_load_data, \
        patch("encryption.file_cypher.save_data") as mock_save_data:
        key = generate_encryption_key()
        file_name = "Hello world.jpg"
        input_data = b"Hello, World!"
        mock_load_data.return_value = input_data
        encrypted_file_name, encrypted_data = file_cypher.FileEncoder(encrypt_file, key).encode_file(file_name)
        mock_load_data.return_value = encrypted_data
        decrypted_file_name, decrypted_data = file_cypher.FileEncoder(encrypt_file, key).decode_file(encrypted_file_name)
        assert input_data == decrypted_data
        assert file_name == decrypted_file_name