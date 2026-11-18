from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StorageUsage")


@_attrs_define
class StorageUsage:
    """
    Attributes:
        used_bytes (int): Document content bytes the organization stores now, over all of its indexes. Example:
            524288000.
        limit_bytes (int | None): Storage bytes the organization can use. `null` means no cap. Example: 2147483648.
        remaining_bytes (int | None): Bytes the organization can add before a write gets a 402 `storage_limit_exceeded`
            response. `null` means no cap. Example: 1623195648.
    """

    used_bytes: int
    limit_bytes: int | None
    remaining_bytes: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        used_bytes = self.used_bytes

        limit_bytes: int | None
        limit_bytes = self.limit_bytes

        remaining_bytes: int | None
        remaining_bytes = self.remaining_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usedBytes": used_bytes,
                "limitBytes": limit_bytes,
                "remainingBytes": remaining_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        used_bytes = d.pop("usedBytes")

        def _parse_limit_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        limit_bytes = _parse_limit_bytes(d.pop("limitBytes"))

        def _parse_remaining_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        remaining_bytes = _parse_remaining_bytes(d.pop("remainingBytes"))

        storage_usage = cls(
            used_bytes=used_bytes,
            limit_bytes=limit_bytes,
            remaining_bytes=remaining_bytes,
        )

        storage_usage.additional_properties = d
        return storage_usage

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
