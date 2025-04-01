import pytest
from encryption.key_generator import KeyFileGenerator, KeyGenerator
import encryption.file_encoder as file_encoder
from unittest.mock import patch
from pyfakefs.fake_filesystem_unittest import Patcher
from pathlib import Path
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
        src_full_path = Path("Hello world.jpg")
        input_data = b"Hello, World!"
        mock_load_data.return_value = input_data
        encrypted_full_path, encrypted_data = file_encoder.FileEncoder(encrypt_file, key).encode_file(Path(src_full_path), Path(dst_path))
        mock_load_data.return_value = encrypted_data
        decrypted_file_name, decrypted_data = file_encoder.FileEncoder(encrypt_file, key).decode_file(Path(encrypted_full_path), Path(""))
        assert input_data == decrypted_data
        assert src_full_path == decrypted_file_name
        assert encrypted_full_path != src_full_path

def test_only_directory_encrypt_decrypt_generate_same_data() -> None:
    with patch("encryption.file_encoder.mkdir") as mock_mkdir:
        #full_path = r"Users\Teckel Plus\Pictures"
        full_path = Path(os.path.join("Users", "Teckel Plus", "Pictures"))
        dst_path = Path("Temp")
        encoded_full_path = file_encoder.FileEncoder.encode_only_directory(full_path, dst_path)
        decoded_full_path = file_encoder.FileEncoder.decode_only_directory(encoded_full_path, full_path.parent)
        assert full_path == decoded_full_path
        assert encoded_full_path != full_path

def test_directory_encrypt_decrypt_generate_same_data() -> None:
    def check_file_contains(file_path: str, expected_contents: bytes) -> bool:
        path = Path(file_path)
        if not path.exists():
            return False
        return path.is_file() and path.read_bytes() == expected_contents
    

    with Patcher() as patcher:
        fs = patcher.fs
        # Mock the file system
        fs.create_dir("/Test")
        fs.create_dir("/Test/Files")
        fs.create_dir("/Test/Teckel Plus")
        
        # Create test files
        fs.create_file("/Test/Files/file1.txt", contents=b"Content of file 1")
        fs.create_file("/Test/Files/file2.txt", contents=b"Content of file 2")
        fs.create_file("/Test/Files/file3.txt", contents=b"Content of file 3")
        fs.create_file("/Test/file4.txt", contents=b"Content of file 4")
        fs.create_file("/Test/file5.txt", contents=b"Content of file 5")
        fs.create_file("/Test/Teckel Plus/file6.txt", contents=b"My Content of file 6")

        encoder = file_encoder.FileEncoder(False, KeyFileGenerator().generate())
        encoder.encode_directory("Test")
        # Check that the encoded directory structure is correct
        assert fs.exists("Test.cry")
        # Sub directory names should be encoded
        assert not fs.exists("Test.cry/Files")
        assert not fs.exists("Test.cry/Teckel Plus")

        encoder.decode_directory("Test.cry")
        #Check that the decoded directory structure is correct
        assert fs.exists("Test.cry.dec")
        assert fs.exists("Test.cry.dec/Files")
        assert fs.exists("Test.cry.dec/Teckel Plus")

        # Check that the files are correctly decrypted
        assert check_file_contains("Test.cry.dec/Files/file1.txt", b"Content of file 1")
        assert check_file_contains("Test.cry.dec/Files/file2.txt", b"Content of file 2")
        assert check_file_contains("Test.cry.dec/Files/file3.txt", b"Content of file 3")
        assert check_file_contains("Test.cry.dec/file4.txt", b"Content of file 4")
        assert check_file_contains("Test.cry.dec/file5.txt", b"Content of file 5")
        assert check_file_contains("Test.cry.dec/Teckel Plus/file6.txt", b"My Content of file 6")
