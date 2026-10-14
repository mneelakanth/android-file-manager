from pathlib import Path

import pytest

from file_manager.domain import FileType
from file_manager.infrastructure import LocalFileRepository


def test_get_file_info(tmp_path: Path):
    file_path = tmp_path / "apple.txt"
    file_path.write_text("hello")

    repository = LocalFileRepository()

    result = repository.get_file_info(file_path)

    assert result.name == "apple.txt"
    assert result.path == file_path
    assert result.file_type == FileType.FILE
    assert result.size == 5

def test_delete_file(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("hello")

    repository = LocalFileRepository()

    result = repository.delete_item(file_path)

    assert result is None
    assert not file_path.exists()

def test_delete_empty_directory(tmp_path: Path):
    directory_path = tmp_path / "documents"
    directory_path.mkdir()  

    repository = LocalFileRepository()
    
    result = repository.delete_item(directory_path)

    assert result is None
    assert not directory_path.exists()

def test_delete_non_empty_directory_raises_error(tmp_path: Path):
    directory_path = tmp_path / "documents"
    directory_path.mkdir()  

    file_path = directory_path / "notes.txt"
    file_path.write_text("hello")

    repository = LocalFileRepository()

    with pytest.raises(OSError):
        repository.delete_item(directory_path)

    assert directory_path.is_dir()
    assert file_path.read_text() == "hello"