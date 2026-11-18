from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_judgment_result_grade_type_0 import SearchJudgmentResultGradeType0
from ..models.search_judgment_result_grade_type_1 import SearchJudgmentResultGradeType1
from ..models.search_judgment_result_grade_type_2 import SearchJudgmentResultGradeType2
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchJudgmentResult")


@_attrs_define
class SearchJudgmentResult:
    """
    Attributes:
        object_id (str): The id of a result from the search that this judgment is about. Example: sku-12345.
        grade (SearchJudgmentResultGradeType0 | SearchJudgmentResultGradeType1 | SearchJudgmentResultGradeType2): How
            useful this result was: 0 not useful, 1 a little useful, 2 very useful.
        position (int | Unset): The rank position the result held in the response, when known.
    """

    object_id: str
    grade: (
        SearchJudgmentResultGradeType0
        | SearchJudgmentResultGradeType1
        | SearchJudgmentResultGradeType2
    )
    position: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_id = self.object_id

        grade: int
        if isinstance(self.grade, SearchJudgmentResultGradeType0) or isinstance(
            self.grade, SearchJudgmentResultGradeType1
        ):
            grade = self.grade.value
        else:
            grade = self.grade.value

        position = self.position

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "objectId": object_id,
                "grade": grade,
            }
        )
        if position is not UNSET:
            field_dict["position"] = position

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_id = d.pop("objectId")

        def _parse_grade(
            data: object,
        ) -> (
            SearchJudgmentResultGradeType0
            | SearchJudgmentResultGradeType1
            | SearchJudgmentResultGradeType2
        ):
            try:
                if not isinstance(data, int):
                    raise TypeError()
                grade_type_0 = SearchJudgmentResultGradeType0(data)

                return grade_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, int):
                    raise TypeError()
                grade_type_1 = SearchJudgmentResultGradeType1(data)

                return grade_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, int):
                raise TypeError()
            grade_type_2 = SearchJudgmentResultGradeType2(data)

            return grade_type_2

        grade = _parse_grade(d.pop("grade"))

        position = d.pop("position", UNSET)

        search_judgment_result = cls(
            object_id=object_id,
            grade=grade,
            position=position,
        )

        search_judgment_result.additional_properties = d
        return search_judgment_result

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
