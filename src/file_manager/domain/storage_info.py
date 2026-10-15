from dataclasses import dataclass


@dataclass(frozen=True)
class StorageInfo:
    total_bytes: int
    used_bytes: int
    free_bytes: int
