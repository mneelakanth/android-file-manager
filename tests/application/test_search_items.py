from pathlib import Path

import pytest

from file_manager.domain.file_type import FileType
from file_manager.application import SearchItems
from file_manager.infrastructure import LocalFileRepository 



def test_search_items_by_name(tmp_path: Path):
    (tmp_path / "Photo.jpg").write_text("image")
    (tmp_path / "notes.txt").write_text("notes")
    (tmp_path / "documents").mkdir()

    use_case = SearchItems(LocalFileRepository())

    result = use_case.execute(tmp_path, "photo")

    assert len(result) == 1
    assert result[0].name == "Photo.jpg"
    assert result[0].path == tmp_path / "Photo.jpg"

def test_search_items_sorted_alphabetically(tmp_path: Path):
    (tmp_path / "Zebra.txt").write_text("z")
    (tmp_path / "Apple.txt").write_text("a")
    (tmp_path / "mango.txt").write_text("m")

    use_case = SearchItems(LocalFileRepository())

    result = use_case.execute(tmp_path, ".txt")

    assert [item.name for item in result] == [
        "Apple.txt", "mango.txt", "Zebra.txt"
    ]

def test_search_items_no_match(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("hello")
    (tmp_path / "Photo.jpg").write_text("photos")

    use_case = SearchItems(LocalFileRepository())

    result = use_case.execute(tmp_path, "video")

    assert result == []

def test_search_items_directory_does_not_exist(tmp_path: Path):
    missing_directory = tmp_path / "missing"

    use_case = SearchItems(LocalFileRepository())

    with pytest.raises(FileNotFoundError):
        use_case.execute(missing_directory, "notes")

def test_search_items_path_is_a_file(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("hello")

    use_case = SearchItems(LocalFileRepository())

    with pytest.raises(NotADirectoryError):
        use_case.execute(file_path, "notes")
