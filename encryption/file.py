import hashlib
import os

def save_data(file_name: str, data: bytes) -> None:
    with open(file_name, 'wb') as file:
        file.write(data)

def load_data(file_name: str) -> bytes:
    with open(file_name, 'rb') as file:
        return file.read()
    
def rename(path_src: str, path_dst: str) -> None:
    os.rename(path_src, path_dst)

def mkdir(path: str) -> None:
    os.mkdir(path)
    
def generate_file_hash(file_name: str) -> str:
    hasher = hashlib.sha256()  # You can also use md5(), sha1(), etc.
    with open(file_name, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):  # Read in chunks
            hasher.update(chunk)
    return hasher.hexdigest()

def are_identical_files(file_name1: str, file_name2: str) -> bool:
    return generate_file_hash(file_name1) == generate_file_hash(file_name2)
