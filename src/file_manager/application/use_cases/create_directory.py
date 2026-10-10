from pathlib import Path

from file_manager.domain import File, FileRepository


class CreateDirectory:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def execute(self, path: Path) -> File:
        return self.repository.create_directory(path)