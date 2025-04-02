import sys
from encryption.file_encoder import FileEncoder
from encryption.key_generator import KeyFileGenerator
from datetime import datetime

def encode_decode_directory() -> None:
    file_encoder = FileEncoder(False, KeyFileGenerator().generate())
    before = datetime.now()
    file_encoder.encode_directory(r"E:\Users\Amine\Extended Area\Old_Documents2")
    after = datetime.now()
    print("Time to encode:", after - before)

    before = datetime.now()
    file_encoder.decode_directory(r"E:\Users\Amine\Extended Area\Old_Documents2.cry")
    after = datetime.now()
    print("Time to decode:", after - before)


def print_arguments() -> None:
    print("Arguments: ", sys.argv[1:])
    

def generate_file_key() -> None:
    key_file_generator = KeyFileGenerator("key.txt", "dnss stuff")
    key_file_generator.generate()

    
print_arguments()