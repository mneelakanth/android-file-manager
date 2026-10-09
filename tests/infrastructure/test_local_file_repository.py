from pathlib import Path

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
