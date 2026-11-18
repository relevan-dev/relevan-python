from enum import Enum


class FeedbackRequestSource(str, Enum):
    EVAL = "eval"
    PRODUCTION = "production"

    def __str__(self) -> str:
        return str(self.value)
