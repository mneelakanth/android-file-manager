import shutil
from pathlib import Path

from file_manager.domain import File, FileType, FileRepository


class LocalFileRepository(FileRepository):

    def _create_file(self, path) -> File:
        file_type = (
            FileType.DIRECTORY
            if path.is_dir()
            else FileType.FILE
        )

        file = File(
            name=path.name, 
            path=path, 
            file_type=file_type,
            size=path.stat().st_size,
        )
        return file

    def list_directory(self, path:Path) -> list[File]:
        files = []
        
        for item in sorted(path.iterdir(), key=lambda item: item.name.lower()):
            file = self._create_file(item)
            files.append(file)
            
        return files

    def get_file_info(self, path: Path) -> File:
        return self._create_file(path)

    def create_directory(self, path: Path) -> File:
        path.mkdir()
        return self._create_file(path)

    def rename_item(self, source: Path, destination: Path) -> File:
        if source == destination:
            return self._create_file(source)
        
        if destination.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )    
                
        source.rename(destination)
        return self._create_file(destination)

    def delete_item(self, path: Path) -> None:
        if path.is_dir():
            path.rmdir()
        else:
            path.unlink()

    def copy_item(self, source: Path, destination:Path) -> File:
        if destination.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

        return self._create_file(destination)
    
        
        
        

