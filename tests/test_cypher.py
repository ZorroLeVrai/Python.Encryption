import pytest
import encryption.cypher as cypher

@pytest.fixture
def setup():
    key = cypher.generate_encryption_key()
    return key

def test_encrypt_decrypt(setup):
    key = setup
    input_data = b"Hello, World!"
    encrypted_data = cypher.encrypt_input(key, input_data)
    decrypted_data = cypher.decrypt_input(key, encrypted_data)
    assert input_data == decrypted_data
