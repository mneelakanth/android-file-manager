from abc import ABC, abstractmethod
from pathlib import Path

from .file import File


class FileRepository(ABC):

    @abstractmethod
    def list_directory(self, path: Path) -> list[File]:
        pass

