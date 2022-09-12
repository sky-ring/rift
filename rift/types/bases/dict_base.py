from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.core import Entity
    from rift.types.types import Slice, Dict, Builder

from rift.core.invokable import typed_invokable
from rift.types.bases.cell_base import _CellBase


class _DictBase(_CellBase):
    @typed_invokable(name="dict_set")
    def dict_set(
        self,
        key_len: int,
        index: "Slice",
        value: "Slice",
    ) -> "Dict":
        pass

    @typed_invokable(name="dict_set")
    def dict_set_(self, key_len: int, index: "Slice", value: "Slice") -> None:
        pass

    @typed_invokable(name="dict_set_builder")
    def dict_set_builder(
        self,
        key_len: int,
        index: "Slice",
        value: "Builder",
    ) -> "Dict":
        pass

    @typed_invokable(name="~dict_set_builder")
    def dict_set_builder_(
        self,
        key_len: int,
        index: "Slice",
        value: "Builder",
    ) -> None:
        pass

    @typed_invokable(name="dict_delete_get_min")
    def dict_delete_get_min(
        self,
        key_len: int,
    ) -> tuple["Dict", "Slice", "Slice", int]:
        pass

    @typed_invokable(name="dict::delete_get_min")
    def dict_delete_get_min_(
        self,
        key_len: int,
    ) -> tuple["Slice", "Slice", int]:
        pass

    @typed_invokable(name="dict_delete_get_max")
    def dict_delete_get_max(
        self,
        key_len: int,
    ) -> tuple["Dict", "Slice", "Slice", int]:
        pass

    @typed_invokable(name="dict::delete_get_max")
    def dict_delete_get_max_(
        self,
        key_len: int,
    ) -> tuple["Slice", "Slice", int]:
        pass

    @typed_invokable(name="dict_empty?")
    def dict_empty_check(self) -> int:
        pass

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if value is None:
            return to.uint(0, 1)
        return to.dict(value)
