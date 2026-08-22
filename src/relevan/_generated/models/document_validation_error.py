from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DocumentValidationError")


@_attrs_define
class DocumentValidationError:
    """
    Attributes:
        document_index (int): Zero-based index of the failing document in the request array Example: 2.
        field (str):  Example: price.
        message (str):  Example: Field 'price' must be of kind 'number'..
    """

    document_index: int
    field: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        document_index = self.document_index

        field = self.field

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documentIndex": document_index,
                "field": field,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        document_index = d.pop("documentIndex")

        field = d.pop("field")

        message = d.pop("message")

        document_validation_error = cls(
            document_index=document_index,
            field=field,
            message=message,
        )

        document_validation_error.additional_properties = d
        return document_validation_error

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
