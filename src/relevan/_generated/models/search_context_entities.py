from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_context_entities_matches_item import SearchContextEntitiesMatchesItem
    from ..models.search_context_entities_outcomes import SearchContextEntitiesOutcomes


T = TypeVar("T", bound="SearchContextEntities")


@_attrs_define
class SearchContextEntities:
    """The places in the query that the search matched to fields of the index. Absent when the index does not match places.

    Attributes:
        matches (list[SearchContextEntitiesMatchesItem]): Each value of a place field that the search used
        outcomes (SearchContextEntitiesOutcomes | Unset): How a step that finds the places ended, when it did not
            finish. The search then used plain text. Absent when each step finished. Example: {'enrich:entity-detection':
            'timeout'}.
    """

    matches: list[SearchContextEntitiesMatchesItem]
    outcomes: SearchContextEntitiesOutcomes | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        matches = []
        for matches_item_data in self.matches:
            matches_item = matches_item_data.to_dict()
            matches.append(matches_item)

        outcomes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.outcomes, Unset):
            outcomes = self.outcomes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "matches": matches,
            }
        )
        if outcomes is not UNSET:
            field_dict["outcomes"] = outcomes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_context_entities_matches_item import SearchContextEntitiesMatchesItem
        from ..models.search_context_entities_outcomes import SearchContextEntitiesOutcomes

        d = dict(src_dict)
        matches = []
        _matches = d.pop("matches")
        for matches_item_data in _matches:
            matches_item = SearchContextEntitiesMatchesItem.from_dict(matches_item_data)

            matches.append(matches_item)

        _outcomes = d.pop("outcomes", UNSET)
        outcomes: SearchContextEntitiesOutcomes | Unset
        if isinstance(_outcomes, Unset):
            outcomes = UNSET
        else:
            outcomes = SearchContextEntitiesOutcomes.from_dict(_outcomes)

        search_context_entities = cls(
            matches=matches,
            outcomes=outcomes,
        )

        search_context_entities.additional_properties = d
        return search_context_entities

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
