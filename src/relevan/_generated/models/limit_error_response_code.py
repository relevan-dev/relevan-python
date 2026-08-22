from enum import Enum


class LimitErrorResponseCode(str, Enum):
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

    def __str__(self) -> str:
        return str(self.value)
