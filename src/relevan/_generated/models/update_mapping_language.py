from enum import Enum


class UpdateMappingLanguage(str, Enum):
    ENGLISH = "english"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
