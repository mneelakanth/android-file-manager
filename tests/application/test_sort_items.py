from pathlib import Path

import pytest

from file_manager.domain import FileType
from file_manager.application import SortItems
from file_manager.infrastructure import LocalFileRepository


def test_sort_items_by_name(tmp_path:Path):
    (tmp_path / "zebra.txt").write_text("z")
    (tmp_path / "Apple.txt").write_text("a")
    (tmp_path / "mango.txt").write_text("m")

    use_case = SortItems(LocalFileRepository())

    result = use_case.execute(tmp_path, sort_by="name")

    assert [item.name for item in result] == [
        "Apple.txt",
        "mango.txt",
        "zebra.txt",
    ]

def test_sort_items_by_size(tmp_path:Path):
    (tmp_path / "large.txt").write_text("123456789")
    (tmp_path / "medium.txt").write_text("12345")
    (tmp_path / "small.txt").write_text("123")

    use_case = SortItems(LocalFileRepository())

    result = use_case.execute(tmp_path, sort_by="size")

    assert [item.name for item in result] == [
        "small.txt",
        "medium.txt",
        "large.txt",
    ]

def test_sort_items_by_size_descending(tmp_path:Path):
    (tmp_path / "small.txt").write_text("12")
    (tmp_path / "large.txt").write_text("123456789")
    (tmp_path / "medium.txt").write_text("12345")

    use_case = SortItems(LocalFileRepository())

    result = use_case.execute(
        tmp_path, 
        sort_by="size",
        descending=True,
    )

    assert [item.name for item in result] == [
        "large.txt",
        "medium.txt",
        "small.txt",
    ]

def test_sort_items_by_type(tmp_path:Path):
    (tmp_path / "notes.txt").write_text("hello")
    (tmp_path / "documents").mkdir()
    (tmp_path / "photo.jpg").write_text("image")

    use_case = SortItems(LocalFileRepository())

    result = use_case.execute(
        tmp_path, 
        sort_by="type",
    )

    assert [item.file_type for item in result] == [
        FileType.DIRECTORY,
        FileType.FILE,
        FileType.FILE,
    ]

def test_sort_items_unsupported_criterion(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("hello")

    use_case = SortItems(LocalFileRepository())

    with pytest.raises(ValueError, match="Unsupported sort criterion"):
        use_case.execute(tmp_path, sort_by="date")

def test_sort_items_does_not_exist(tmp_path: Path):
    missing_directory = tmp_path / "missing"

    use_case = SortItems(LocalFileRepository())

    with pytest.raises(FileNotFoundError):
        use_case.execute(missing_directory, sort_by="name")

def test_sort_items_path_is_a_file(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("hello")

    use_case = SortItems(LocalFileRepository())

    with pytest.raises(NotADirectoryError):
        use_case.execute(file_path, sort_by="name")


