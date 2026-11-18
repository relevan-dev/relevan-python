from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_context_fallback_kind import SearchContextFallbackKind

T = TypeVar("T", bound="SearchContextFallback")


@_attrs_define
class SearchContextFallback:
    """Present when the first query of a long query found no document, and a less strict query found the results. Absent
    otherwise.

        Attributes:
            kind (SearchContextFallbackKind):
            original_minimum_should_match (str): The share of query terms that the first query required. Example: 60%.
            minimum_should_match (str): The share of query terms that the fallback query required. Example: 1.
    """

    kind: SearchContextFallbackKind
    original_minimum_should_match: str
    minimum_should_match: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        original_minimum_should_match = self.original_minimum_should_match

        minimum_should_match = self.minimum_should_match

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "originalMinimumShouldMatch": original_minimum_should_match,
                "minimumShouldMatch": minimum_should_match,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = SearchContextFallbackKind(d.pop("kind"))

        original_minimum_should_match = d.pop("originalMinimumShouldMatch")

        minimum_should_match = d.pop("minimumShouldMatch")

        search_context_fallback = cls(
            kind=kind,
            original_minimum_should_match=original_minimum_should_match,
            minimum_should_match=minimum_should_match,
        )

        search_context_fallback.additional_properties = d
        return search_context_fallback

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
