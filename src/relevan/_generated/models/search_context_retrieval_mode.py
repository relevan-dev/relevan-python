from enum import Enum


class SearchContextRetrievalMode(str, Enum):
    HYBRID = "hybrid"
    LEXICAL = "lexical"

    def __str__(self) -> str:
        return str(self.value)
