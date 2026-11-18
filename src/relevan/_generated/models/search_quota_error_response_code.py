from enum import Enum


class SearchQuotaErrorResponseCode(str, Enum):
    SEARCH_QUOTA_EXCEEDED = "search_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
