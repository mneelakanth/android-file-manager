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


def test_copy_file(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "copied.txt"
    source.write_text("hello")

    repository = LocalFileRepository()

    result = repository.copy_item(source, destination)

    assert source.exists()
    assert destination.exists()
    assert destination.read_text() == "hello"
    assert result.name == "copied.txt"
    assert result.path == destination
    assert result.size == 5

def test_copy_directory(tmp_path: Path):
    source = tmp_path / "original_folder"
    destination = tmp_path / "copied_folder"
    
    source.mkdir()
    (source / "notes.txt").write_text("hello")

    repository = LocalFileRepository()

    result = repository.copy_item(source, destination)
    assert source.is_dir()
    assert destination.is_dir()
    assert (destination / "notes.txt").read_text() == "hello"
    assert result.name == "copied_folder"
    assert result.path == destination
    assert result.file_type == FileType.DIRECTORY

def test_copy_file_destination_exists(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "copied.txt"

    source.write_text("original content")
    destination.write_text("keep this content")

    repository = LocalFileRepository()

    with pytest.raises(FileExistsError):
        repository.copy_item(source, destination)
    
    assert source.read_text() == "original content"
    assert destination.read_text() == "keep this content"

def test_copy_file_source_does_not_exist(tmp_path: Path):
    source = tmp_path / "missing.txt"
    destination = tmp_path / "copied.txt"

    repository = LocalFileRepository()
    
    with pytest.raises(FileNotFoundError):
        repository.copy_item(source, destination)

    assert not destination.exists()

def test_copy_directory_destination_exists(tmp_path: Path):
    source = tmp_path / "original_folder"
    destination = tmp_path / "copied_folder"
    
    source.mkdir()
    (source / "notes.txt").write_text("original content")

    destination.mkdir()
    (destination / "existing.txt").write_text("keep this file")

    repository = LocalFileRepository()

    with pytest.raises(FileExistsError):
        repository.copy_item(source, destination)

    assert (source / "notes.txt").read_text() == "original content"    
    assert (destination / "existing.txt").read_text() == "keep this file"
    assert not(destination / "notes.txt").exists()