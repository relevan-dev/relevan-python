from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_context_decay import SearchContextDecay
    from ..models.search_context_entities import SearchContextEntities
    from ..models.search_context_fallback import SearchContextFallback
    from ..models.search_context_retrieval import SearchContextRetrieval


T = TypeVar("T", bound="SearchContext")


@_attrs_define
class SearchContext:
    """
    Attributes:
        query_used (str): The query actually executed, post-enrichment
        total_hits (int):
        matched_terms (list[str]): Union of matched terms across all returned hits
        top_contributing_fields (list[str]): Fields that contributed score, ordered by contribution descending
        title_field (None | str): Field holding each document's human-readable label, resolved from the index mapping.
            Null when the index has no text field. Example: title.
        scoring_summary (str):
        suggestions (str): Guidance for reformulating the query
        searchable_fields (list[str]): All fields configured as searchable on this index
        session_id (str): This request's session identifier — the request's sessionId echoed back, or a new one when it
            was omitted. Send it back on the next call to continue this session. Example:
            8f14e45f-ceea-467e-a1a4-8f6c1c1a1a1a.
        query_id (str): This request's unique id. Send it as queryId on a POST
            /v1-beta/{orgId}/indexes/{indexName}/feedback call to report feedback about one of these results. Example:
            3c2e6e0a-9b7a-4e8b-9e2f-1a2b3c4d5e6f.
        warnings (list[str] | Unset): Problems with the request that the search worked around, for example boost terms
            that are not in the query. Absent when there are none. Example: ['Ignored boost terms that are not in the query:
            [term]. Boost only a word that is in the query.'].
        fallback (SearchContextFallback | Unset): Present when the first query of a long query found no document, and a
            less strict query found the results. Absent otherwise.
        entities (SearchContextEntities | Unset): The places in the query that the search matched to fields of the
            index. Absent when the index does not match places.
        retrieval (SearchContextRetrieval | Unset): The retrieval mode that the hybrid gate chose for the query. Absent
            when the index has no hybrid search.
        decay (SearchContextDecay | Unset): Among hits that match equally well, a newer document of a decayed profile
            ranks higher. Absent when the index has no recency decay.
    """

    query_used: str
    total_hits: int
    matched_terms: list[str]
    top_contributing_fields: list[str]
    title_field: str | None
    scoring_summary: str
    suggestions: str
    searchable_fields: list[str]
    session_id: str
    query_id: str
    warnings: list[str] | Unset = UNSET
    fallback: SearchContextFallback | Unset = UNSET
    entities: SearchContextEntities | Unset = UNSET
    retrieval: SearchContextRetrieval | Unset = UNSET
    decay: SearchContextDecay | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query_used = self.query_used

        total_hits = self.total_hits

        matched_terms = self.matched_terms

        top_contributing_fields = self.top_contributing_fields

        title_field: str | None
        title_field = self.title_field

        scoring_summary = self.scoring_summary

        suggestions = self.suggestions

        searchable_fields = self.searchable_fields

        session_id = self.session_id

        query_id = self.query_id

        warnings: list[str] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        fallback: dict[str, Any] | Unset = UNSET
        if not isinstance(self.fallback, Unset):
            fallback = self.fallback.to_dict()

        entities: dict[str, Any] | Unset = UNSET
        if not isinstance(self.entities, Unset):
            entities = self.entities.to_dict()

        retrieval: dict[str, Any] | Unset = UNSET
        if not isinstance(self.retrieval, Unset):
            retrieval = self.retrieval.to_dict()

        decay: dict[str, Any] | Unset = UNSET
        if not isinstance(self.decay, Unset):
            decay = self.decay.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queryUsed": query_used,
                "totalHits": total_hits,
                "matchedTerms": matched_terms,
                "topContributingFields": top_contributing_fields,
                "titleField": title_field,
                "scoringSummary": scoring_summary,
                "suggestions": suggestions,
                "searchableFields": searchable_fields,
                "sessionId": session_id,
                "queryId": query_id,
            }
        )
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if fallback is not UNSET:
            field_dict["fallback"] = fallback
        if entities is not UNSET:
            field_dict["entities"] = entities
        if retrieval is not UNSET:
            field_dict["retrieval"] = retrieval
        if decay is not UNSET:
            field_dict["decay"] = decay

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_context_decay import SearchContextDecay
        from ..models.search_context_entities import SearchContextEntities
        from ..models.search_context_fallback import SearchContextFallback
        from ..models.search_context_retrieval import SearchContextRetrieval

        d = dict(src_dict)
        query_used = d.pop("queryUsed")

        total_hits = d.pop("totalHits")

        matched_terms = cast(list[str], d.pop("matchedTerms"))

        top_contributing_fields = cast(list[str], d.pop("topContributingFields"))

        def _parse_title_field(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        title_field = _parse_title_field(d.pop("titleField"))

        scoring_summary = d.pop("scoringSummary")

        suggestions = d.pop("suggestions")

        searchable_fields = cast(list[str], d.pop("searchableFields"))

        session_id = d.pop("sessionId")

        query_id = d.pop("queryId")

        warnings = cast(list[str], d.pop("warnings", UNSET))

        _fallback = d.pop("fallback", UNSET)
        fallback: SearchContextFallback | Unset
        if isinstance(_fallback, Unset):
            fallback = UNSET
        else:
            fallback = SearchContextFallback.from_dict(_fallback)

        _entities = d.pop("entities", UNSET)
        entities: SearchContextEntities | Unset
        if isinstance(_entities, Unset):
            entities = UNSET
        else:
            entities = SearchContextEntities.from_dict(_entities)

        _retrieval = d.pop("retrieval", UNSET)
        retrieval: SearchContextRetrieval | Unset
        if isinstance(_retrieval, Unset):
            retrieval = UNSET
        else:
            retrieval = SearchContextRetrieval.from_dict(_retrieval)

        _decay = d.pop("decay", UNSET)
        decay: SearchContextDecay | Unset
        if isinstance(_decay, Unset):
            decay = UNSET
        else:
            decay = SearchContextDecay.from_dict(_decay)

        search_context = cls(
            query_used=query_used,
            total_hits=total_hits,
            matched_terms=matched_terms,
            top_contributing_fields=top_contributing_fields,
            title_field=title_field,
            scoring_summary=scoring_summary,
            suggestions=suggestions,
            searchable_fields=searchable_fields,
            session_id=session_id,
            query_id=query_id,
            warnings=warnings,
            fallback=fallback,
            entities=entities,
            retrieval=retrieval,
            decay=decay,
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
