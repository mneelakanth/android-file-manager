from pathlib import Path

from file_manager.domain import File, FileRepository


class SearchItems:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def execute(self, directory: Path, query: str) -> list[File]:
        return self.repository.search_items(directory, query)