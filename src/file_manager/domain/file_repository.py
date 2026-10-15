from abc import ABC, abstractmethod
from pathlib import Path

from .file import File
from .storage_info import StorageInfo

class FileRepository(ABC):

    @abstractmethod
    def list_directory(self, path: Path) -> list[File]:
        pass

    @abstractmethod
    def get_file_info(self, path: Path) -> File:
        pass

    @abstractmethod
    def create_directory(self, path: Path) -> File:
        pass

    @abstractmethod
    def rename_item(self, source: Path, destination: Path) -> File:
        pass

    @abstractmethod
    def delete_item(self, path: Path) -> None:
        pass

    @abstractmethod
    def copy_item(self, source: Path, destination: Path) -> File:
        pass

    @abstractmethod
    def move_item(self, source: Path, destination: Path) -> File:
        pass

    @abstractmethod
    def get_storage_info(self, path: Path) -> StorageInfo:
        pass

    @abstractmethod
    def search_items(self, directory: Path, query: str) -> list[File]:
        pass