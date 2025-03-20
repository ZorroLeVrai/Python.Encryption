from cypher import generate_encryption_key, encrypt_input, decrypt_input
from file_cypher import decode_file_name, encode_file_name

file_name = "test.txt"
key = generate_encryption_key()
encoded_file_name = encode_file_name(key, file_name)
print(f"Encoded file name: {encoded_file_name}")
decoded_file_name = decode_file_name(key, encoded_file_name)
print(f"Decoded file name: {decoded_file_name}")