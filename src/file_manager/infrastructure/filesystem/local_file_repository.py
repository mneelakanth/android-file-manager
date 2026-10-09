from pathlib import Path

from file_manager.domain import File, FileType, FileRepository


class LocalFileRepository(FileRepository):

    def list_directory(self, path:Path) -> list[File]:
        files = []
        
        for item in sorted(path.iterdir(), key=lambda item: item.name.lower()):
            file_type = (
                FileType.DIRECTORY
                if item.is_dir()
                else FileType.FILE
            )

            files.append(
                File(
                    name=item.name, 
                    path=item, 
                    file_type=file_type,
                    size=item.stat().st_size,
                )
            )
        return files

