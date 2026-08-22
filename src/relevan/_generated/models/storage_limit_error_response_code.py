from enum import Enum


class StorageLimitErrorResponseCode(str, Enum):
    STORAGE_LIMIT_EXCEEDED = "storage_limit_exceeded"

    def __str__(self) -> str:
        return str(self.value)
