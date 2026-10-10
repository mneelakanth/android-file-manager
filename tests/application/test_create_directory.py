from pathlib import Path

import pytest

from file_manager.application import CreateDirectory
from file_manager.domain import FileType
from file_manager.infrastructure import LocalFileRepository


def test_create_directory(tmp_path: Path):
    directory_path = tmp_path / "Documents"

    repository = LocalFileRepository()
    use_case = CreateDirectory(repository)

    result = use_case.execute(directory_path)

    assert directory_path.exists()
    assert directory_path.is_dir()
    assert result.name == "Documents"
    assert result.path == directory_path
    assert result.file_type == FileType.DIRECTORY
    assert result.size == directory_path.stat().st_size

def test_create_directory_already_exists(tmp_path: Path):
    directory_path = tmp_path / "Documents"
    directory_path.mkdir()

    repository = LocalFileRepository()
    use_case = CreateDirectory(repository)

    with pytest.raises(FileExistsError):
        use_case.execute(directory_path)

def test_create_directory_parent_does_not_exist(tmp_path: Path):
    directory_path = tmp_path / "Missing" / "Documents"

    repository = LocalFileRepository()
    use_case = CreateDirectory(repository)

    with pytest.raises(FileNotFoundError):
        use_case.execute(directory_path)