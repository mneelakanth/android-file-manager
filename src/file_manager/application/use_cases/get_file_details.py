from pathlib import Path

from file_manager.domain import File, FileRepository


class GetFileDetails:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def execute(self, path: Path) -> File:
        return self.repository.get_file_info(path)