from pathlib import Path

import pytest

from file_manager.domain.file_type import FileType
from file_manager.application import RenameItem
from file_manager.infrastructure import LocalFileRepository 

def test_rename_item(tmp_path: Path):
    source = tmp_path / "old.txt"
    destination = tmp_path / "new.txt"
    source.write_text("hello")

    use_case = RenameItem(LocalFileRepository())

    result = use_case.execute(source, destination)

    assert not source.exists()
    assert destination.exists()
    assert result.name == "new.txt"
    assert result.path == destination
    assert result.size == 5

def test_rename_item_destination_exists(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "new.txt"
    
    source.write_text("original")
    destination.write_text("Keep this file")

    use_case = RenameItem(LocalFileRepository())

    with pytest.raises(FileExistsError):
        use_case.execute(source, destination)

    assert source.read_text() == "original"
    assert destination.read_text() == "Keep this file"


def test_rename_directory(tmp_path: Path):
    source = tmp_path / "old_folder"
    destination = tmp_path / "new_folder"

    source.mkdir()
    (source / "notes.txt").write_text("hello")

    use_case = RenameItem(LocalFileRepository())

    result = use_case.execute(source, destination)

    assert not source.exists()
    assert destination.is_dir()
    assert (destination / "notes.txt").read_text() == "hello"
    assert result.name == "new_folder"
    assert result.file_type == FileType.DIRECTORY

def test_rename_item_to_same_path(tmp_path: Path):
    source = tmp_path / "notes.txt"
    source.write_text("hello")

    use_case = RenameItem(LocalFileRepository())

    result = use_case.execute(source, source)

    assert source.exists()
    assert source.read_text() == "hello"
    assert result.name == "notes.txt"
    assert result.path == source

def test_rename_item_source_does_not_exist(tmp_path: Path):
    source = tmp_path / "missing.txt"
    destination = tmp_path / "renamed.txt"

    use_case = RenameItem(LocalFileRepository())

    with pytest.raises(FileNotFoundError):
        use_case.execute(source, destination)

    assert not destination.exists()

def test_rename_item_destination_parent_does_not_exist(tmp_path: Path):
    source = tmp_path / "notes.txt"
    destination = tmp_path / "missing_folder" / "renamed.txt"

    source.write_text("hello")

    use_case = RenameItem(LocalFileRepository())

    with pytest.raises(FileNotFoundError):
        use_case.execute(source, destination)

    assert source.exists()
    assert source.read_text() == "hello"
    assert not destination.exists()