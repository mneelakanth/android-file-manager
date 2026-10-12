from pathlib import Path

from file_manager.domain import File, FileRepository


class RenameItem:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def execute(self, source: Path, destination: Path) -> File:
        return self.repository.rename_item(source, destination)