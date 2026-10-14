from pathlib import Path

import pytest

from file_manager.application import CopyItem
from file_manager.domain import File, FileType
from file_manager.infrastructure import LocalFileRepository


def test_copy_item(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "copied.txt"
    source.write_text("hello")

    use_case = CopyItem(LocalFileRepository())

    result = use_case.execute(source, destination)

    assert source.exists()
    assert destination.exists()
    assert destination.read_text() == "hello"

def test_copy_item_directory(tmp_path: Path):
    source = tmp_path / "original_folder"
    destination = tmp_path / "copied_folder"

    source.mkdir()
    (source / "notes.txt").write_text("hello")

    use_case = CopyItem(LocalFileRepository())

    result = use_case.execute(source, destination)

    assert source.is_dir()
    assert destination.is_dir()
    assert (destination / 'notes.txt').read_text() == "hello"
    assert result.name == "copied_folder"
    assert result.path == destination
    assert result.file_type == FileType.DIRECTORY

def test_copy_item_destination_exists(tmp_path: Path):
    source = tmp_path / "original.txt"
    destination = tmp_path / "copied.txt"

    source.write_text("original content")
    destination.write_text("keep this content")

    use_case = CopyItem(LocalFileRepository())

    with pytest.raises(FileExistsError):
        use_case.execute(source, destination)
    
    assert source.read_text() == "original content"
    assert destination.read_text() == "keep this content"

def test_copy_item_source_does_not_exist(tmp_path: Path):
    source = tmp_path / "missing.txt"
    destination = tmp_path / "copied.txt"

    use_case = CopyItem(LocalFileRepository())
    
    with pytest.raises(FileNotFoundError):
        use_case.execute(source, destination)

    assert not destination.exists()