from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchContext")


@_attrs_define
class SearchContext:
    """
    Attributes:
        query_used (str): The query actually executed, post-enrichment
        total_hits (int):
        matched_terms (list[str]): Union of matched terms across all returned hits
        top_contributing_fields (list[str]): Fields that contributed score, ordered by contribution descending
        scoring_summary (str):
        suggestions (str): Guidance for reformulating the query
        searchable_fields (list[str]): All fields configured as searchable on this index
        session_id (str): This request's session identifier — the request's sessionId echoed back, or a new one when it
            was omitted. Send it back on the next call to continue this session. Example:
            8f14e45f-ceea-467e-a1a4-8f6c1c1a1a1a.
        query_id (str): This request's unique id. Send it as queryId on a POST
            /v1-beta/{orgId}/indexes/{indexName}/feedback call to report feedback about one of these results. Example:
            3c2e6e0a-9b7a-4e8b-9e2f-1a2b3c4d5e6f.
    """

    query_used: str
    total_hits: int
    matched_terms: list[str]
    top_contributing_fields: list[str]
    scoring_summary: str
    suggestions: str
    searchable_fields: list[str]
    session_id: str
    query_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query_used = self.query_used

        total_hits = self.total_hits

        matched_terms = self.matched_terms

        top_contributing_fields = self.top_contributing_fields

        scoring_summary = self.scoring_summary

        suggestions = self.suggestions

        searchable_fields = self.searchable_fields

        session_id = self.session_id

        query_id = self.query_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queryUsed": query_used,
                "totalHits": total_hits,
                "matchedTerms": matched_terms,
                "topContributingFields": top_contributing_fields,
                "scoringSummary": scoring_summary,
                "suggestions": suggestions,
                "searchableFields": searchable_fields,
                "sessionId": session_id,
                "queryId": query_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query_used = d.pop("queryUsed")

        total_hits = d.pop("totalHits")

        matched_terms = cast(list[str], d.pop("matchedTerms"))

        top_contributing_fields = cast(list[str], d.pop("topContributingFields"))

        scoring_summary = d.pop("scoringSummary")

        suggestions = d.pop("suggestions")

        searchable_fields = cast(list[str], d.pop("searchableFields"))

        session_id = d.pop("sessionId")

        query_id = d.pop("queryId")

        search_context = cls(
            query_used=query_used,
            total_hits=total_hits,
            matched_terms=matched_terms,
            top_contributing_fields=top_contributing_fields,
            scoring_summary=scoring_summary,
            suggestions=suggestions,
            searchable_fields=searchable_fields,
            session_id=session_id,
            query_id=query_id,
        )

        search_context.additional_properties = d
        return search_context

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
