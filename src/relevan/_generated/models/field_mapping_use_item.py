from enum import Enum


class FieldMappingUseItem(str, Enum):
    AGGREGATABLE = "aggregatable"
    AUTOCOMPLETABLE = "autocompletable"
    FILTERABLE = "filterable"
    HIGHLIGHTABLE = "highlightable"
    SEARCHABLE = "searchable"
    SORTABLE = "sortable"

    def __str__(self) -> str:
        return str(self.value)
