
from .encoders import DataBase64Encoder, DataEncoder, DataFernetEncoder
from .file import load_data, mkdir, save_data
from typing import Tuple, Optional
from pathlib import Path
import os

from encryption import file

class FileNameEncoder:
    def __init__(self) -> None:
        self.encoder = DataBase64Encoder(True)

    def encode(self, file_name: str) -> str:
        """Encodes a filename"""
        return self.encoder.encode(file_name.encode()).decode()
        
    def decode(self, url_safe_file_name: str) -> str:
        """Decodes a filename"""
        return self.encoder.decode(url_safe_file_name.encode()).decode()


class FileEncoder:
    def __init__(self, encrypt_file: bool, key: Optional[bytes] = None) -> None:
        self.file_name_encoder = FileNameEncoder()
        self.encoder : DataEncoder
        if encrypt_file:
            if not key:
                raise ValueError("Key must be provided when encrypting a file")
            self.encoder = DataFernetEncoder(key)
        else:
            self.encoder = DataBase64Encoder(False)

    @staticmethod
    def replace_last_dot(input_string: str, post_fix: str) -> str:
        # Split the string from the last occurrence of "."
        parts = input_string.rsplit(".", 1)
        # If there's no dot, return the original string
        if len(parts) == 1:
            return input_string
        # Replace the last "." with ".old."
        return f"{parts[0]}.{post_fix}.{parts[1]}"
    
    def encode_file(self, src_path: Path, dst_path: Path) -> Tuple[Path, bytes]:
        """
        Encodes a given file
        Args:
            src_path: The path to the file to encode
            dst_path: The path to the directory to save the encoded file
        Returns:
            The name of the encoded file and the encoded data
        """
        src_path_basename = src_path.name
        src_data = load_data(src_path)
        dst_data = self.encoder.encode(src_data)
        dst_file_name = self.file_name_encoder.encode(src_path_basename)
        dst_full_path = dst_path.joinpath(dst_file_name)
        save_data(dst_full_path, dst_data)
        return dst_full_path, dst_data

    def decode_file(self, src_path: Path, dst_path: Path, post_fix: str = "") -> Tuple[Path, bytes]:
        """
        Decodes a given file
        Args:
            encrypted_file_name: The name of the file to decode
            post_fix: The post-fix to add to the decoded file name
        Returns:
            The name of the decoded file and the decoded data
        """
        src_data = load_data(src_path)
        dst_data = self.encoder.decode(src_data)
        dst_file_name = self.file_name_encoder.decode(src_path.name)
        dst_full_path = os.path.join(str(dst_path), dst_file_name)
        if post_fix:
            dst_full_path = self.replace_last_dot(dst_file_name, post_fix)
        save_data(dst_full_path, dst_data)
        return Path(dst_full_path), dst_data
    
    @staticmethod
    def encode_only_directory(src_path: Path, dst_path: Path) -> Path:
        """
        Encodes only the directory name
        Args:
            src_path: The name of the directory to encode
            dst_path: The path to the directory to save the encoded directory
        """
        src_directory_name = src_path.name
        dst_directory_name = FileNameEncoder().encode(src_directory_name)

        dst_full_path = dst_path.joinpath(dst_directory_name)
        mkdir(dst_full_path)
        return dst_full_path

    @staticmethod
    def decode_only_directory(src_path: Path, dst_path: Path, post_fix: str = "") -> Path:
        """
        Decodes only the directory name
        Args:
            directory_path: The path to the directory to decode
            post_fix: The post-fix to add to the decoded directory name
        """
        src_directory_name = src_path.name
        dst_directory_name = FileNameEncoder().decode(src_directory_name)
        if post_fix:
            dst_directory_name += f".{post_fix}"
        dst_full_path = dst_path.joinpath(dst_directory_name)
        mkdir(dst_full_path)
        return dst_full_path
    
    def encode_directory(self, src_path_str: str) -> Path:
        """
        Encodes a directory and its contents recursively
        Args:
            src_path_str: The path to the directory to encode
        """
        src_full_path = Path(src_path_str)
        if not src_full_path.exists():
            raise FileNotFoundError(f"Source path does not exist: {src_path_str}")
        
        dst_directory_name = f"{src_full_path.name}.cry"
        dst_directory_path = src_full_path.parent.joinpath(dst_directory_name)
        os.mkdir(dst_directory_path)

        for item in src_full_path.iterdir():
            if item.is_dir():
                self.encode_directory_internal(item, dst_directory_path)
            else:
                self.encode_file(item, dst_directory_path)
        
        return dst_directory_path

    def encode_directory_internal(self, src_directory_path: Path, dst_directory_path: Path) -> None:
        """
        Encodes a directory and its contents recursively
        Args:
            src_directory_path: The path to the directory to encode
            dst_directory_path: The path to the directory to save the encoded files
        """
        dst_path = self.encode_only_directory(src_directory_path, dst_directory_path)

        directories = [path for path in src_directory_path.iterdir() if path.is_dir()]
        files = [path for path in src_directory_path.iterdir() if path.is_file()]

        for directory in directories:
            self.encode_directory_internal(directory, dst_path)

        for file in files:
            self.encode_file(file, dst_path)


    def decode_directory(self, src_path_str: str) -> Path:
        """
        Decodes a directory and its contents recursively
        Args:
            src_path_str: The path to the directory to decode
        """
        src_full_path = Path(src_path_str)
        if not src_full_path.exists():
            raise FileNotFoundError(f"Source path does not exist: {src_path_str}")
        
        scr_dir_name = src_full_path.name
        if scr_dir_name.endswith(".cry") and not os.path.isdir(src_path_str[:-4]):
            dst_directory_name = scr_dir_name[:-4]
        else:
            dst_directory_name = f"{src_full_path.name}.dec"
        dst_directory_path = src_full_path.parent.joinpath(dst_directory_name)
        os.mkdir(dst_directory_path)

        for item in src_full_path.iterdir():
            if item.is_dir():
                self.decode_directory_internal(item, dst_directory_path)
            else:
                self.decode_file(item, dst_directory_path)

        return dst_directory_path

    def decode_directory_internal(self, src_directory_path: Path, dst_directory_path: Path) -> None:
        """
        Decodes a directory and its contents recursively
        Args:
            src_directory_path: The path to the directory to decode
            dst_directory_path: The path to the directory to save the decoded files
        """
        dst_path = Path(self.decode_only_directory(src_directory_path, dst_directory_path))

        directories = [path for path in src_directory_path.iterdir() if path.is_dir()]
        files = [path for path in src_directory_path.iterdir() if path.is_file()]

        for directory in directories:
            self.decode_directory_internal(directory, dst_path)

        for file in files:
            self.decode_file(file, dst_path)
