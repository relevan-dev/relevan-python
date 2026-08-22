from __future__ import annotations

import warnings


class RelevanBetaWarning(UserWarning):
    """Raised on every call to a `client.beta` method.

    Endpoints under the API's `/v1-beta` path have a different stability
    guarantee than `/v1`: their contract may change without warning. This
    warning makes that visible at the call site, not only in documentation.
    """


def warn_beta(endpoint: str) -> None:
    warnings.warn(
        f"{endpoint} is a beta endpoint (/v1-beta). Its contract may change without warning.",
        category=RelevanBetaWarning,
        stacklevel=3,
    )
