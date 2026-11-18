from enum import Enum


class FeedbackRequestActionName(str, Enum):
    CLICK = "click"
    CONVERSION = "conversion"
    LLM_JUDGMENT = "llm_judgment"
    SEARCH_JUDGMENT = "search_judgment"

    def __str__(self) -> str:
        return str(self.value)
