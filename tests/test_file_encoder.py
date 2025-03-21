import pytest
from encryption.key_generator import KeyGenerator
import encryption.file_encoder as file_encoder
from unittest.mock import patch
import os

def test_file_name_encrypt_decrypt_generate_same_name() -> None:
    file_name = "Hello world.jpg"
    file_name_encoder = file_encoder.FileNameEncoder()
    encoded_file_name = file_name_encoder.encode(file_name)
    decoded_file_name = file_name_encoder.decode(encoded_file_name)
    assert file_name == decoded_file_name

@pytest.mark.parametrize("encrypt_file", [True, False])
def test_file_encrypt_decrypt_generate_same_data(encrypt_file: bool) -> None:
    with patch("encryption.file_encoder.load_data") as mock_load_data, \
        patch("encryption.file_encoder.save_data") as mock_save_data:
        key = KeyGenerator().generate_key()
        dst_path = os.path.join("Users", "Microsoft", "Repo")
        src_full_path = "Hello world.jpg"
        input_data = b"Hello, World!"
        mock_load_data.return_value = input_data
        encrypted_full_path, encrypted_data = file_encoder.FileEncoder(encrypt_file, key).encode_file(src_full_path, dst_path)
        mock_load_data.return_value = encrypted_data
        decrypted_file_name, decrypted_data = file_encoder.FileEncoder(encrypt_file, key).decode_file(encrypted_full_path, "")
        assert input_data == decrypted_data
        assert src_full_path == decrypted_file_name
        assert encrypted_full_path != src_full_path

def test_only_directory_encrypt_decrypt_generate_same_data() -> None:
    with patch("encryption.file_encoder.mkdir") as mock_mkdir:
        #full_path = r"Users\Teckel Plus\Pictures"
        full_path = os.path.join("Users", "Teckel Plus", "Pictures")
        dst_path = r"Temp"
        encoded_full_path = file_encoder.FileEncoder.encode_only_directory(full_path, dst_path)
        decoded_full_path = file_encoder.FileEncoder.decode_only_directory(encoded_full_path, os.path.dirname(full_path))
        assert full_path == decoded_full_path
        assert encoded_full_path != full_path
