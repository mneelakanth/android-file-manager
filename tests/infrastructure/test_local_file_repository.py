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


def test_move_file(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "moved.txt"
    source.write_text("hello")

    repository = LocalFileRepository()

    result = repository.move_item(source, destination)

    assert not source.exists()
    assert destination.exists()
    assert destination.read_text() == "hello"
    assert result.name == "moved.txt"
    assert result.path == destination
    assert result.size == 5

def test_move_directory(tmp_path: Path):
    source = tmp_path / "original_folder"
    destination = tmp_path / "moved_folder"
    
    source.mkdir()
    (source / "notes.txt").write_text("hello")

    repository = LocalFileRepository()

    result = repository.move_item(source, destination)
    assert not source.exists()
    assert destination.is_dir()
    assert (destination / "notes.txt").read_text() == "hello"
    assert result.name == "moved_folder"
    assert result.path == destination
    assert result.file_type == FileType.DIRECTORY

def test_move_file_destination_exists(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "moved.txt"

    source.write_text("original content")
    destination.write_text("keep this content")

    repository = LocalFileRepository()

    with pytest.raises(FileExistsError):
        repository.move_item(source, destination)
    
    assert source.read_text() == "original content"
    assert destination.read_text() == "keep this content"

def test_move_file_source_does_not_exist(tmp_path: Path):
    source = tmp_path / "missing.txt"
    destination = tmp_path / "moved.txt"

    repository = LocalFileRepository()
    
    with pytest.raises(FileNotFoundError):
        repository.move_item(source, destination)

    assert not destination.exists()

def test_move_item_to_same_path(tmp_path: Path):
    source = tmp_path / "notes.txt"
    source.write_text("hello")

    repository = LocalFileRepository()

    result = repository.move_item(source, source)

    assert source.exists()
    assert source.read_text() == "hello"
    assert result.name == "notes.txt"
    assert result.path == source
    assert result.size == 5

def test_get_storage_info(tmp_path: Path):
    repository = LocalFileRepository()

    result = repository.get_storage_info(tmp_path)

    assert result.total_bytes > 0
    assert result.used_bytes >= 0
    assert result.free_bytes >= 0
    assert result.total_bytes == result.used_bytes + result.free_bytes

def test_search_items_by_name(tmp_path: Path):
    (tmp_path / "Photo.jpg").write_text("image")
    (tmp_path / "notes.txt").write_text("notes")
    (tmp_path / "documents").mkdir()

    repository = LocalFileRepository()

    result = repository.search_items(tmp_path, "photo")

    assert len(result) == 1
    assert result[0].name == "Photo.jpg"
    assert result[0].path == tmp_path / "Photo.jpg"

def test_search_items_sorted_alphabetically(tmp_path: Path):
    (tmp_path / "Zebra.txt").write_text("z")
    (tmp_path / "Apple.txt").write_text("a")
    (tmp_path / "mango.txt").write_text("m")

    repository = LocalFileRepository()

    result = repository.search_items(tmp_path, ".txt")

    assert [item.name for item in result] == [
        "Apple.txt", "mango.txt", "Zebra.txt"
    ]

def test_search_items_no_match(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("hello")
    (tmp_path / "Photo.jpg").write_text("photos")

    repository = LocalFileRepository()

    result = repository.search_items(tmp_path, "video")

    assert result == []

def test_search_items_directory_does_not_exist(tmp_path: Path):
    missing_directory = tmp_path / "missing"

    repository = LocalFileRepository()

    with pytest.raises(FileNotFoundError):
        repository.search_items(missing_directory, "notes")

def test_search_items_path_is_a_file(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("hello")

    repository = LocalFileRepository()

    with pytest.raises(NotADirectoryError):
        repository.search_items(file_path, "notes")

