from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.search_quota_error_response_code import SearchQuotaErrorResponseCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchQuotaErrorResponse")


@_attrs_define
class SearchQuotaErrorResponse:
    """
    Attributes:
        message (str): Error message Example: Index not found.
        code (SearchQuotaErrorResponseCode): Stable, machine-readable reason. Branch on this, not on `message`.
        limit (int): Searches permitted this calendar month at the organization's tier. Example: 10000.
        used (int): Searches the organization got this calendar month. A rejected request does not count. Example:
            10000.
        reset_at (datetime.datetime): Start of the next calendar month, when the quota resets. Example:
            2026-10-01T00:00:00.000Z.
        error (str | Unset): Detailed error information Example: No index found with the provided name.
    """

    message: str
    code: SearchQuotaErrorResponseCode
    limit: int
    used: int
    reset_at: datetime.datetime
    error: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        code = self.code.value

        limit = self.limit

        used = self.used

        reset_at = self.reset_at.isoformat()

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
                "code": code,
                "limit": limit,
                "used": used,
                "resetAt": reset_at,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        code = SearchQuotaErrorResponseCode(d.pop("code"))

        limit = d.pop("limit")

        used = d.pop("used")

        reset_at = isoparse(d.pop("resetAt"))

        error = d.pop("error", UNSET)

        search_quota_error_response = cls(
            message=message,
            code=code,
            limit=limit,
            used=used,
            reset_at=reset_at,
            error=error,
        )

        search_quota_error_response.additional_properties = d
        return search_quota_error_response

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
