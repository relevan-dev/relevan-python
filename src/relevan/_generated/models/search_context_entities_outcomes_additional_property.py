from enum import Enum


class SearchContextEntitiesOutcomesAdditionalProperty(str, Enum):
    ERROR = "error"
    TIMEOUT = "timeout"

    def __str__(self) -> str:
        return str(self.value)
