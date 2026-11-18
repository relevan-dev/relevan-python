from enum import Enum


class SearchContextRetrievalClassification(str, Enum):
    EMBEDDING_UNAVAILABLE = "embedding_unavailable"
    GATE_OFF = "gate_off"
    IDENTIFIER = "identifier"
    NATURAL_LANGUAGE = "natural_language"
    QUOTED_PHRASE = "quoted_phrase"
    SHORT_QUERY = "short_query"

    def __str__(self) -> str:
        return str(self.value)
