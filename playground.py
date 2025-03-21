from encryption.cypher import create_key_file, load_key_file
from encryption.file_cypher import FileEncoder


# key = load_key_file()
# file_encoder = FileEncoder(key)
# encoded_file_name, _ = file_encoder.encode_file("photo.jpg")
# print("Encoded file name:", encoded_file_name)

key = load_key_file()
file_encoder = FileEncoder(key)
decoded_file_name, _ = file_encoder.decode_file("cGhvdG8uanBn")
print("Decoded file name:", decoded_file_name)
