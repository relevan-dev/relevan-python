from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.feedback_request_action_name import FeedbackRequestActionName
from ..types import UNSET, Unset

T = TypeVar("T", bound="FeedbackRequest")


@_attrs_define
class FeedbackRequest:
    """
    Attributes:
        action_name (FeedbackRequestActionName): click: a real end user picked this result. llm_judgment: an agent
            judged this result relevant, without a human confirming it. conversion: a closing event confirmed this result
            was right — a purchase, a hire, or another outcome you define.
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
    """

    action_name: FeedbackRequestActionName
    query_id: str | Unset = UNSET
    object_id: str | Unset = UNSET
    position: int | Unset = UNSET
    label: str | Unset = UNSET
    session_id: str | Unset = UNSET
    customer_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_name = self.action_name.value

        query_id = self.query_id

        object_id = self.object_id

        position = self.position

        label = self.label

        session_id = self.session_id

        customer_id = self.customer_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actionName": action_name,
            }
        )
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action_name = FeedbackRequestActionName(d.pop("actionName"))

        query_id = d.pop("queryId", UNSET)

        object_id = d.pop("objectId", UNSET)

        position = d.pop("position", UNSET)

        label = d.pop("label", UNSET)

        session_id = d.pop("sessionId", UNSET)

        customer_id = d.pop("customerId", UNSET)

        feedback_request = cls(
            action_name=action_name,
            query_id=query_id,
            object_id=object_id,
            position=position,
            label=label,
            session_id=session_id,
            customer_id=customer_id,
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
