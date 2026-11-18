from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.usage_tier import UsageTier

if TYPE_CHECKING:
    from ..models.storage_usage import StorageUsage


T = TypeVar("T", bound="Usage")


@_attrs_define
class Usage:
    """
    Attributes:
        tier (UsageTier): The plan that sets the caps in this response. Example: starter.
        storage (StorageUsage):
    """

    tier: UsageTier
    storage: StorageUsage
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tier = self.tier.value

        storage = self.storage.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tier": tier,
                "storage": storage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storage_usage import StorageUsage

        d = dict(src_dict)
        tier = UsageTier(d.pop("tier"))

        storage = StorageUsage.from_dict(d.pop("storage"))

        usage = cls(
            tier=tier,
            storage=storage,
        )

        usage.additional_properties = d
        return usage

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
