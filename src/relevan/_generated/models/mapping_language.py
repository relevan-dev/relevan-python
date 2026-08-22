from enum import Enum


class MappingLanguage(str, Enum):
    ENGLISH = "english"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
