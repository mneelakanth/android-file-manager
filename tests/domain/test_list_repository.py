from pathlib import Path

import pytest

from file_manager.application import ListDirectory
from file_manager.infrastructure import LocalFileRepository 
from file_manager.domain import FileType

def test_list_directory(tmp_path:Path):
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "zebra.jpeg").touch()
    (tmp_path / "apple.txt").touch()
    (tmp_path / "Documents").touch()

    repository = LocalFileRepository()
    use_case = ListDirectory(repository)

    result = use_case.execute(tmp_path)

    names = [item.name for item in result]

    assert names == ["apple.txt", "Documents", "photo.jpg", "zebra.jpeg"]

def test_list_directory_path_does_not_exist(tmp_path:Path):
    repository = LocalFileRepository()

    invalid_path = tmp_path / "does-not-exist"

    with pytest.raises(FileNotFoundError):
        repository.list_directory(invalid_path)

def test_list_directory_path_is_a_file(tmp_path:Path):
    repository = LocalFileRepository()

    file_path = tmp_path / "photo.jpg"
    file_path.touch()

    with pytest.raises(NotADirectoryError):
        repository.list_directory(file_path)

def test_list_directory(tmp_path: Path):
    apple = tmp_path / "apple.txt"
    apple.write_text("hello")

    (tmp_path / "zebra.jpeg").touch()
    (tmp_path / "apple.txt").touch()
    (tmp_path / "Documents").touch()

    repository = LocalFileRepository()
    use_case = ListDirectory(repository)

    result = use_case.execute(tmp_path)

    files = {item.name: item for item in result}

    assert files["apple.txt"].size == 5

def test_list_directory_identifies_file_type(tmp_path: Path):
    file_path = tmp_path / "photo.jpg"
    file_path.touch()

    directory_path = tmp_path / "Documents"
    directory_path.mkdir()

    repository = LocalFileRepository()

    result = repository.list_directory(tmp_path)

    items = {item.name: item for item in result}
   
    assert items["photo.jpg"].file_type == FileType.FILE
    assert items["Documents"].file_type == FileType.DIRECTORY
