from pathlib import Path

import pytest

from file_manager.domain import FileType
from file_manager.application import MoveItem
from file_manager.infrastructure import LocalFileRepository


def test_move_item(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "moved.txt"
    source.write_text("hello")

    use_case = MoveItem(LocalFileRepository())

    result = use_case.execute(source, destination)

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
    (source / "notes.txt").write_text("keep this content")

    use_case = MoveItem(LocalFileRepository())
    result = use_case.execute(source, destination)

    assert not source.exists()
    assert destination.is_dir()
    assert (destination / "notes.txt").read_text() == "keep this content"
    assert result.name == "moved_folder"
    assert result.path == destination
    assert result.file_type == FileType.DIRECTORY

def test_move_item_destination_exists(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "moved.txt"
    source.write_text("hello")
    destination.write_text("keep this content")

    use_case = MoveItem(LocalFileRepository())

    with pytest.raises(FileExistsError):
        use_case.execute(source, destination)

    assert source.read_text() == "hello"
    assert destination.read_text() == "keep this content"

def test_move_item_source_does_not_exist(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "moved.txt"

    use_case = MoveItem(LocalFileRepository())

    with pytest.raises(FileNotFoundError):
        use_case.execute(source, destination)

    assert not source.exists()

def test_move_item_same_path(tmp_path: Path):
    source = tmp_path / "original.txt"
    source.write_text("hello")
    
    use_case = MoveItem(LocalFileRepository())

    result = use_case.execute(source, source)

    assert source.exists()
    assert source.read_text() == "hello"
    assert result.name == "original.txt"
    assert result.path == source
    assert result.size == 5

    
    