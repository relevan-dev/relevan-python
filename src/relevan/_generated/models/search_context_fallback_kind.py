from enum import Enum


class SearchContextFallbackKind(str, Enum):
    RELAXEDMINIMUMSHOULDMATCH = "relaxedMinimumShouldMatch"

    def __str__(self) -> str:
        return str(self.value)
