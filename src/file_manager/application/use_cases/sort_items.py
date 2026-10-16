from pathlib import Path

from file_manager.domain import File, FileRepository

class SortItems:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def execute(
        self, 
        directory: Path,
        sort_by: str,
        descending: bool=False,
    ) -> list[File]:
        return self.repository.sort_items(
            directory,
            sort_by,
            descending,
        )