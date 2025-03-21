from encryption.file_encoder import FileEncoder
from encryption.key_generator import KeyFileGenerator

encode_file = True

key = KeyFileGenerator().generate()
file_encoder = FileEncoder(encode_file, key)
encoded_file_name, _ = file_encoder.encode_file("Teckel_Plus.png")
print("Encoded file name:", encoded_file_name)

key = KeyFileGenerator().load()
file_encoder = FileEncoder(encode_file, key)
decoded_file_name, _ = file_encoder.decode_file("VGVja2VsX1BsdXMucG5n", "new")
print("Decoded file name:", decoded_file_name)
