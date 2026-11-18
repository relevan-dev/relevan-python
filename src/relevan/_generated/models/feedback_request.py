from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.feedback_request_action_name import FeedbackRequestActionName
from ..models.feedback_request_grade_type_0 import FeedbackRequestGradeType0
from ..models.feedback_request_grade_type_1 import FeedbackRequestGradeType1
from ..models.feedback_request_grade_type_2 import FeedbackRequestGradeType2
from ..models.feedback_request_source import FeedbackRequestSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_judgment_result import SearchJudgmentResult


T = TypeVar("T", bound="FeedbackRequest")


@_attrs_define
class FeedbackRequest:
    """
    Attributes:
        action_name (FeedbackRequestActionName): click: a real end user picked this result. llm_judgment: an agent
            judged this result relevant, without a human confirming it. conversion: a closing event confirmed this result
            was right — a purchase, a hire, or another outcome you define. search_judgment: an agent judged the whole
            search, once per queryId. A second search_judgment for the same queryId gets 409.
        source (FeedbackRequestSource | Unset): production: this feedback comes from real caller traffic. eval: this
            feedback comes from a test suite or benchmark run, not a real user or agent session. Defaults to production.
            Default: FeedbackRequestSource.PRODUCTION.
        query_id (str | Unset): The queryId from a prior search response's searchContext. Send it when this feedback
            concerns one specific search. Example: 3c2e6e0a-9b7a-4e8b-9e2f-1a2b3c4d5e6f.
        object_id (str | Unset): The id of the result this feedback is about. Required for type click and llm_judgment.
            Example: sku-12345.
        position (int | Unset): The rank position the result held in the response, when known.
        label (str | Unset): A short name for a conversion event, for example hire or purchase. Example: hire.
        session_id (str | Unset): The same sessionId used on the search request this feedback concerns. Example:
            8f14e45f-ceea-467e-a1a4-8f6c1c1a1a1a.
        customer_id (str | Unset): The same customerId used on the search request this feedback concerns. Example:
            user_48291.
        grade (FeedbackRequestGradeType0 | FeedbackRequestGradeType1 | FeedbackRequestGradeType2 | Unset): How useful
            the result was: 0 not useful, 1 a little useful, 2 very useful. Optional with each actionName. Requires
            objectId, except with search_judgment, where it grades the whole search. Example: 2.
        results (list[SearchJudgmentResult] | Unset): Per-result grades for a search_judgment, at most 100. Only with
            search_judgment.
        description (str | Unset): Free text, at most 2000 characters: what the user wanted, and why the results did or
            did not match. Do not include personal data that the user did not need to share. Relevan stores this text with
            the same retention as query text. Example: The user wanted waterproof hiking boots for winter. The top results
            were summer sandals..
    """

    action_name: FeedbackRequestActionName
    source: FeedbackRequestSource | Unset = FeedbackRequestSource.PRODUCTION
    query_id: str | Unset = UNSET
    object_id: str | Unset = UNSET
    position: int | Unset = UNSET
    label: str | Unset = UNSET
    session_id: str | Unset = UNSET
    customer_id: str | Unset = UNSET
    grade: (
        FeedbackRequestGradeType0 | FeedbackRequestGradeType1 | FeedbackRequestGradeType2 | Unset
    ) = UNSET
    results: list[SearchJudgmentResult] | Unset = UNSET
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_name = self.action_name.value

        source: str | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        query_id = self.query_id

        object_id = self.object_id

        position = self.position

        label = self.label

        session_id = self.session_id

        customer_id = self.customer_id

        grade: int | Unset
        if isinstance(self.grade, Unset):
            grade = UNSET
        elif isinstance(self.grade, FeedbackRequestGradeType0) or isinstance(
            self.grade, FeedbackRequestGradeType1
        ):
            grade = self.grade.value
        else:
            grade = self.grade.value

        results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actionName": action_name,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if query_id is not UNSET:
            field_dict["queryId"] = query_id
        if object_id is not UNSET:
            field_dict["objectId"] = object_id
        if position is not UNSET:
            field_dict["position"] = position
        if label is not UNSET:
            field_dict["label"] = label
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id
        if customer_id is not UNSET:
            field_dict["customerId"] = customer_id
        if grade is not UNSET:
            field_dict["grade"] = grade
        if results is not UNSET:
            field_dict["results"] = results
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_judgment_result import SearchJudgmentResult

        d = dict(src_dict)
        action_name = FeedbackRequestActionName(d.pop("actionName"))

        _source = d.pop("source", UNSET)
        source: FeedbackRequestSource | Unset
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = FeedbackRequestSource(_source)

        query_id = d.pop("queryId", UNSET)

        object_id = d.pop("objectId", UNSET)

        position = d.pop("position", UNSET)

        label = d.pop("label", UNSET)

        session_id = d.pop("sessionId", UNSET)

        customer_id = d.pop("customerId", UNSET)

        def _parse_grade(
            data: object,
        ) -> (
            FeedbackRequestGradeType0
            | FeedbackRequestGradeType1
            | FeedbackRequestGradeType2
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                grade_type_0 = FeedbackRequestGradeType0(data)

                return grade_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, int):
                    raise TypeError()
                grade_type_1 = FeedbackRequestGradeType1(data)

                return grade_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, int):
                raise TypeError()
            grade_type_2 = FeedbackRequestGradeType2(data)

            return grade_type_2

        grade = _parse_grade(d.pop("grade", UNSET))

        _results = d.pop("results", UNSET)
        results: list[SearchJudgmentResult] | Unset = UNSET
        if _results is not UNSET:
            results = []
            for results_item_data in _results:
                results_item = SearchJudgmentResult.from_dict(results_item_data)

                results.append(results_item)

        description = d.pop("description", UNSET)

        feedback_request = cls(
            action_name=action_name,
            source=source,
            query_id=query_id,
            object_id=object_id,
            position=position,
            label=label,
            session_id=session_id,
            customer_id=customer_id,
            grade=grade,
            results=results,
            description=description,
        )

        feedback_request.additional_properties = d
        return feedback_request

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
