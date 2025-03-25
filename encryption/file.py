import hashlib
from pathlib import Path
import os

def save_data(file_name: str | Path, data: bytes) -> None:
    file_name_str = str(file_name) if isinstance(file_name, Path) else file_name
    with open(file_name_str, 'wb') as file:
        file.write(data)

def load_data(file_name: str | Path) -> bytes:
    file_name_str = str(file_name) if isinstance(file_name, Path) else file_name
    with open(file_name_str, 'rb') as file:
        return file.read()

def rename(path_src: str | Path, path_dst: str | Path) -> None:
    path_src_str = str(path_src) if isinstance(path_src, Path) else path_src
    path_dst_str = str(path_dst) if isinstance(path_dst, Path) else path_dst
    os.rename(path_src_str, path_dst_str)

def mkdir(path: str | Path) -> None:
    path_str = str(path) if isinstance(path, Path) else path
    os.mkdir(path_str)
    
def generate_file_hash(file_name: str) -> str:
    hasher = hashlib.sha256()  # You can also use md5(), sha1(), etc.
    with open(file_name, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):  # Read in chunks
            hasher.update(chunk)
    return hasher.hexdigest()

def are_identical_files(file_name1: str, file_name2: str) -> bool:
    return generate_file_hash(file_name1) == generate_file_hash(file_name2)
