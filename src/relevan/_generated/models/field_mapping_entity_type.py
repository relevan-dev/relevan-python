from enum import Enum


class FieldMappingEntityType(str, Enum):
    CITY = "city"
    COUNTRY = "country"
    POSTAL_CODE = "postal_code"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
