from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_document_content import CreateDocumentContent


T = TypeVar("T", bound="CreateDocument")


@_attrs_define
class CreateDocument:
    """
    Attributes:
        id (str): Caller-supplied document ID, unique within the index. Alphanumeric, underscore, period, colon, and
            hyphen only. Example: sku-12345.
        content (CreateDocumentContent): Document content. All fields must be declared in the index mapping.
    """

    id: str
    content: CreateDocumentContent
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        content = self.content.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "content": content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_document_content import CreateDocumentContent

        d = dict(src_dict)
        id = d.pop("id")

        content = CreateDocumentContent.from_dict(d.pop("content"))

        create_document = cls(
            id=id,
            content=content,
        )

        create_document.additional_properties = d
        return create_document

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
