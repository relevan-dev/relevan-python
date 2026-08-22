from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.limit_error_response_code import LimitErrorResponseCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="LimitErrorResponse")


@_attrs_define
class LimitErrorResponse:
    """
    Attributes:
        message (str): Error message Example: Index not found.
        code (LimitErrorResponseCode): Stable, machine-readable reason. Branch on this, not on `message`.
        limit (int): Requests permitted in the window at the organization's tier. Example: 60.
        remaining (int): Requests left in the current window.
        reset_at (datetime.datetime): When the current window rolls over. Example: 2026-01-01T00:01:00.000Z.
        retry_after_seconds (int): Whole seconds to wait before retrying. Mirrors the `Retry-After` header. Example: 42.
        error (str | Unset): Detailed error information Example: No index found with the provided name.
    """

    message: str
    code: LimitErrorResponseCode
    limit: int
    remaining: int
    reset_at: datetime.datetime
    retry_after_seconds: int
    error: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        code = self.code.value

        limit = self.limit

        remaining = self.remaining

        reset_at = self.reset_at.isoformat()

        retry_after_seconds = self.retry_after_seconds

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
                "code": code,
                "limit": limit,
                "remaining": remaining,
                "resetAt": reset_at,
                "retryAfterSeconds": retry_after_seconds,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        code = LimitErrorResponseCode(d.pop("code"))

        limit = d.pop("limit")

        remaining = d.pop("remaining")

        reset_at = isoparse(d.pop("resetAt"))

        retry_after_seconds = d.pop("retryAfterSeconds")

        error = d.pop("error", UNSET)

        limit_error_response = cls(
            message=message,
            code=code,
            limit=limit,
            remaining=remaining,
            reset_at=reset_at,
            retry_after_seconds=retry_after_seconds,
            error=error,
        )

        limit_error_response.additional_properties = d
        return limit_error_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
