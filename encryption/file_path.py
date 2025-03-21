from __future__ import annotations
from pathlib import Path
import os

class DirectoryPath:
    def __init__(self, full_path: str, parent_directory: str, directory_name: str):
        self.full_path = full_path
        self.parent_directory = parent_directory
        self.directory_name = directory_name

    def move_to_child(self, child_directory_name: str) -> DirectoryPath:
        full_path = os.path.join(self.full_path, child_directory_name)
        parent_directory = self.full_path
        return DirectoryPath(full_path, parent_directory, child_directory_name)
    
    def list_all_items(self) -> list[str]:
        return os.listdir(self.full_path)
    
    def list_directories_files(self) -> tuple[list[str], list[str]]:
        directories = []
        files = []
        for item_name in self.list_all_items():
            full_path = os.path.join(self.full_path, item_name)
            if os.path.isdir(full_path):
                directories.append(item_name)
            else:
                files.append(item_name)
        return directories, files
    
    def is_directory(self) -> bool:
        return os.path.isdir(self.full_path)


class DirectoryPathBuilder:
    @staticmethod
    def build_directory_path_from_full_path(full_path: str) -> DirectoryPath:
        parent_directory = os.path.dirname(full_path)
        directory_name = os.path.basename(full_path)
        return DirectoryPath(full_path, parent_directory, directory_name)