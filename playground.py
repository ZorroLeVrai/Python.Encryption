from encryption import file_encoder
from encryption.file_encoder import FileEncoder
from encryption.key_generator import KeyFileGenerator
from datetime import datetime

# encode_file = True

# key = KeyFileGenerator().generate()
# file_encoder = FileEncoder(encode_file, key)
# encoded_file_name, _ = file_encoder.encode_file("Teckel_Plus.png")
# print("Encoded file name:", encoded_file_name)

# key = KeyFileGenerator().load()
# file_encoder = FileEncoder(encode_file, key)
# decoded_file_name, _ = file_encoder.decode_file("VGVja2VsX1BsdXMucG5n", "new")
# print("Decoded file name:", decoded_file_name)


file_encoder = FileEncoder(True, KeyFileGenerator().generate())
print("Start encoding at:", datetime.now())
file_encoder.encode_directory(r"E:\Users\Amine\Extended Area\Old_Documents2")
print("End encoding at:", datetime.now())

print("Start decoding at:", datetime.now())
file_encoder.decode_directory(r"E:\Users\Amine\Extended Area\Old_Documents2.cry")
print("End decoding at:", datetime.now())
