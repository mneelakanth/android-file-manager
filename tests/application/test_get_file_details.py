from pathlib import Path

from file_manager.application import GetFileDetails
from file_manager.infrastructure import LocalFileRepository 



def test_get_file_details(tmp_path: Path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")

    repository = LocalFileRepository()
    use_case = GetFileDetails(repository)

    result = use_case.execute(file_path)
   
    assert result.name == "test.txt"
    assert result.path == file_path
    assert result.size == 5
