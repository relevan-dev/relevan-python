from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_context_retrieval_classification import SearchContextRetrievalClassification
from ..models.search_context_retrieval_mode import SearchContextRetrievalMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchContextRetrieval")


@_attrs_define
class SearchContextRetrieval:
    """The retrieval mode that the hybrid gate chose for the query. Absent when the index has no hybrid search.

    Attributes:
        mode (SearchContextRetrievalMode): hybrid: the text query and a vector query found the results. lexical: the
            text query alone found them.
        classification (SearchContextRetrievalClassification): The retrieval classification of the query: a natural-
            language query, the gate is off, an identifier pattern of the index, a quoted phrase, too few words, or a query
            embedding that failed or was too slow. Example: identifier.
        identifier (str | Unset): The name of the identifier pattern of the index that matched. Relevan chooses the
            name. Present only when classification is identifier.
    """

    mode: SearchContextRetrievalMode
    classification: SearchContextRetrievalClassification
    identifier: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        classification = self.classification.value

        identifier = self.identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mode": mode,
                "classification": classification,
            }
        )
        if identifier is not UNSET:
            field_dict["identifier"] = identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = SearchContextRetrievalMode(d.pop("mode"))

        classification = SearchContextRetrievalClassification(d.pop("classification"))

        identifier = d.pop("identifier", UNSET)

        search_context_retrieval = cls(
            mode=mode,
            classification=classification,
            identifier=identifier,
        )

        search_context_retrieval.additional_properties = d
        return search_context_retrieval

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
