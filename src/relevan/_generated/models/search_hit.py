from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_hit_document import SearchHitDocument
    from ..models.search_hit_highlights import SearchHitHighlights


T = TypeVar("T", bound="SearchHit")


@_attrs_define
class SearchHit:
    """
    Attributes:
        id (str):  Example: sku-12345.
        score (float | None):  Example: 12.4.
        document (SearchHitDocument): The matched document's content
        explanation (str): Human-readable description of why this document matched Example: "neon tetra" in description
            (4.20). Total score: 12.400.
        matched_fields (list[str]): Base field names that contributed to this hit's score
        matched_terms (list[str]): Indexed terms that contributed to this hit's score
        highlights (SearchHitHighlights | Unset): Highlighted text snippets by field
    """

    id: str
    score: float | None
    document: SearchHitDocument
    explanation: str
    matched_fields: list[str]
    matched_terms: list[str]
    highlights: SearchHitHighlights | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        score: float | None
        score = self.score

        document = self.document.to_dict()

        explanation = self.explanation

        matched_fields = self.matched_fields

        matched_terms = self.matched_terms

        highlights: dict[str, Any] | Unset = UNSET
        if not isinstance(self.highlights, Unset):
            highlights = self.highlights.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "score": score,
                "document": document,
                "explanation": explanation,
                "matchedFields": matched_fields,
                "matchedTerms": matched_terms,
            }
        )
        if highlights is not UNSET:
            field_dict["highlights"] = highlights

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_hit_document import SearchHitDocument
        from ..models.search_hit_highlights import SearchHitHighlights

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        score = _parse_score(d.pop("score"))

        document = SearchHitDocument.from_dict(d.pop("document"))

        explanation = d.pop("explanation")

        matched_fields = cast(list[str], d.pop("matchedFields"))

        matched_terms = cast(list[str], d.pop("matchedTerms"))

        _highlights = d.pop("highlights", UNSET)
        highlights: SearchHitHighlights | Unset
        if isinstance(_highlights, Unset):
            highlights = UNSET
        else:
            highlights = SearchHitHighlights.from_dict(_highlights)

        search_hit = cls(
            id=id,
            score=score,
            document=document,
            explanation=explanation,
            matched_fields=matched_fields,
            matched_terms=matched_terms,
            highlights=highlights,
        )

        search_hit.additional_properties = d
        return search_hit

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
