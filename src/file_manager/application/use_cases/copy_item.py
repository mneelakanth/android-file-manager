from pathlib import Path

from file_manager.domain import File, FileRepository


class CopyItem:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def execute(self, source: Path, destination: Path):
        return self.repository.copy_item(source, destination)