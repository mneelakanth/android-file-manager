from dataclasses import dataclass
from pathlib import Path

from .file_type import FileType

@dataclass(frozen=True)
class File:
    name: str
    path: Path
    file_type: FileType
    size: int

