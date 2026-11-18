from enum import Enum


class SearchContextEntitiesMatchesItemMode(str, Enum):
    BOOST = "boost"
    FILTER = "filter"

    def __str__(self) -> str:
        return str(self.value)
