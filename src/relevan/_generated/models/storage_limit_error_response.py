from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.storage_limit_error_response_code import StorageLimitErrorResponseCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="StorageLimitErrorResponse")


@_attrs_define
class StorageLimitErrorResponse:
    """
    Attributes:
        message (str): Error message Example: Index not found.
        code (StorageLimitErrorResponseCode): Stable, machine-readable reason. Branch on this, not on `message`.
        limit_bytes (int): Storage bytes permitted at the organization's tier. Example: 2147483648.
        used_bytes (int): Bytes already stored before this write. Example: 2100000000.
        incoming_bytes (int): Net bytes this write would add. Example: 50000000.
        remaining_bytes (int): Bytes free before this write. Example: 47483648.
        error (str | Unset): Detailed error information Example: No index found with the provided name.
    """

    message: str
    code: StorageLimitErrorResponseCode
    limit_bytes: int
    used_bytes: int
    incoming_bytes: int
    remaining_bytes: int
    error: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        code = self.code.value

        limit_bytes = self.limit_bytes

        used_bytes = self.used_bytes

        incoming_bytes = self.incoming_bytes

        remaining_bytes = self.remaining_bytes

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
                "code": code,
                "limitBytes": limit_bytes,
                "usedBytes": used_bytes,
                "incomingBytes": incoming_bytes,
                "remainingBytes": remaining_bytes,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        code = StorageLimitErrorResponseCode(d.pop("code"))

        limit_bytes = d.pop("limitBytes")

        used_bytes = d.pop("usedBytes")

        incoming_bytes = d.pop("incomingBytes")

        remaining_bytes = d.pop("remainingBytes")

        error = d.pop("error", UNSET)

        storage_limit_error_response = cls(
            message=message,
            code=code,
            limit_bytes=limit_bytes,
            used_bytes=used_bytes,
            incoming_bytes=incoming_bytes,
            remaining_bytes=remaining_bytes,
            error=error,
        )

        storage_limit_error_response.additional_properties = d
        return storage_limit_error_response

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
