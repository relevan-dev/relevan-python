from enum import Enum


class FieldMappingLanguage(str, Enum):
    ENGLISH = "english"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
