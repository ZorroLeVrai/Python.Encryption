import pytest
import encryption.file_cypher as file_cypher

def test_file_name_encrypt_decrypt_generate_same_name():
    file_name = "Hello world.jpg"
    encoded_file_name = file_cypher.encode_file_name(file_name)
    decoded_file_name = file_cypher.decode_file_name(encoded_file_name)
    assert file_name == decoded_file_name
