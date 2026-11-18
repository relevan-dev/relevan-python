from enum import Enum


class FieldMappingKind(str, Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    DATE = "date"
    GEO_POINT = "geo_point"
    ID = "id"
    NUMBER = "number"
    OBJECT = "object"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
