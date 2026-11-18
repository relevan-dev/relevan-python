from enum import Enum


class UsageTier(str, Enum):
    ENTERPRISE = "enterprise"
    LEARN = "learn"
    OPTIMIZE = "optimize"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)
