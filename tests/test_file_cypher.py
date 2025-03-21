import pytest
from encryption.key_generator import KeyGenerator
import encryption.file_encoder as file_encoder
from unittest.mock import patch

def test_file_name_encrypt_decrypt_generate_same_name():
    file_name = "Hello world.jpg"
    file_name_encoder = file_encoder.FileNameEncoder()
    encoded_file_name = file_name_encoder.encode(file_name)
    decoded_file_name = file_name_encoder.decode(encoded_file_name)
    assert file_name == decoded_file_name

@pytest.mark.parametrize("encrypt_file", [True, False])
def test_file_encrypt_decrypt_generate_same_data(encrypt_file: bool):
    with patch("encryption.file_encoder.load_data") as mock_load_data, \
        patch("encryption.file_encoder.save_data") as mock_save_data:
        key = KeyGenerator().generate_key()
        file_name = "Hello world.jpg"
        input_data = b"Hello, World!"
        mock_load_data.return_value = input_data
        encrypted_file_name, encrypted_data = file_encoder.FileEncoder(encrypt_file, key).encode_file(file_name)
        mock_load_data.return_value = encrypted_data
        decrypted_file_name, decrypted_data = file_encoder.FileEncoder(encrypt_file, key).decode_file(encrypted_file_name)
        assert input_data == decrypted_data
        assert file_name == decrypted_file_name
        assert encrypted_file_name != file_name
