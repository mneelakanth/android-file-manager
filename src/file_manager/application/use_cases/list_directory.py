from pathlib import Path

from file_manager.domain import File, FileType, FileRepository


class ListDirectory:
    def __init__(self, repository: FileRepository):
        self.repository = repository
    
    def execute(self, path: Path):
        return self.repository.list_directory(path)
