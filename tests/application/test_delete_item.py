from pathlib import Path

import pytest

from file_manager.application import DeleteItem
from file_manager.infrastructure import LocalFileRepository

def test_delete_item(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("hello")

    use_case = DeleteItem(LocalFileRepository())

    result = use_case.execute(file_path)

    assert result is None
    assert not file_path.exists()

def test_delete_item_source_does_not_exist(tmp_path: Path):
    file_path = tmp_path / "missing.txt"

    use_case = DeleteItem(LocalFileRepository())

    with pytest.raises(FileNotFoundError):
        use_case.execute(file_path)

def test_delete_item_directory(tmp_path:Path):
    directory_path = tmp_path / "documents"
    directory_path.mkdir()

    use_cse = DeleteItem(LocalFileRepository())

    result = use_cse.execute(directory_path)

    assert result is None
    assert not directory_path.exists()

def test_delete_non_empty_raises_error(tmp_path: Path): 
    directory_path = tmp_path / "documents"
    directory_path.mkdir()

    file_path = directory_path / "notes.txt"
    file_path.write_text("hello")

    use_cse = DeleteItem(LocalFileRepository())

    with pytest.raises(OSError):
        use_cse.execute(directory_path)
    assert directory_path.is_dir()

    assert file_path.read_text() == "hello"

