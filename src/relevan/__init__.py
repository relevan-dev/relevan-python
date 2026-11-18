from importlib.metadata import version

from ._beta import RelevanBetaWarning
from ._errors import RelevanAPIError, RelevanAuthError, RelevanError, RelevanRateLimitError
from ._rate_limit import RateLimit
from .async_client import AsyncClient
from .client import Client
from .resources.beta import JudgedResult

__version__ = version("relevan")

__all__ = [
    "AsyncClient",
    "Client",
    "JudgedResult",
    "RateLimit",
    "RelevanAPIError",
    "RelevanAuthError",
    "RelevanBetaWarning",
    "RelevanError",
    "RelevanRateLimitError",
    "__version__",
]
