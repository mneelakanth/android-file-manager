from pathlib import Path

import pytest

from file_manager.application import GetStorageInfo
from file_manager.infrastructure import LocalFileRepository


def test_get_storage_info(tmp_path: Path):
    repository = LocalFileRepository()

    use_case = GetStorageInfo(LocalFileRepository())
    result = use_case.execute(tmp_path)

    assert result.total_bytes > 0
    assert result.used_bytes >= 0
    assert result.free_bytes >= 0
    assert result.total_bytes == result.used_bytes + result.free_bytes

def test_get_storage_info_path_does_not_exist(tmp_path: Path):
    invalid_path = tmp_path / "missing_directory"

    use_case = GetStorageInfo(LocalFileRepository())

    with pytest.raises(FileNotFoundError):
        use_case.execute(invalid_path)