from pathlib import Path

from file_manager.domain import FileRepository


class DeleteItem:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def execute(self, path: Path) -> None:
        self.repository.delete_item(path)