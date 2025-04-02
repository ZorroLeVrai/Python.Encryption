import os
import sys
import shutil
from encryption.file import load_data
from encryption.file_encoder import FileEncoder

arguments = sys.argv[1:]

if len(arguments) < 3:
    exit(1)

command = arguments[0]
src_path = arguments[1]
key_path = arguments[2]

if not os.path.exists(src_path):
    print(f"Source path does not exist: {src_path}")
    exit(1)
if not os.path.exists(key_path):
    print(f"Key path does not exist: {key_path}")
    exit(1)

key = load_data(key_path)
file_decoder = FileEncoder(True, key)

if command in ["encode", "crypt"]:
    print(f"Encoding directory: {src_path}")
    file_decoder.encode_directory(src_path)
    # remove the original directory
    shutil.rmtree(src_path)   
    print("Done")

elif command in ["decode", "decrypt"]:
    print(f"Decoding directory: {src_path}")
    file_decoder.decode_directory(src_path)
    shutil.rmtree(src_path)
    print("Done")
