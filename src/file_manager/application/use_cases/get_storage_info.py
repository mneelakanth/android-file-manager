from pathlib import Path

from file_manager.domain import FileRepository, StorageInfo

class GetStorageInfo:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def execute(self, path: Path) -> StorageInfo:
        return self.repository.get_storage_info(path)