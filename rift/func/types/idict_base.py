from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.func.types.types import Slice, Cell, IDict, Builder

from rift.core.invokable import typed_invokable
from rift.func.types.dict_base import _DictBase


class _IDictBase(_DictBase):
    @typed_invokable(name="idict_set_ref")
    def set_ref(self, key_len: int, index: int, value: "Cell") -> "IDict":
        pass

    @typed_invokable(name="idict_set_ref")
    def set_ref_(self, key_len: int, index: int, value: "Cell") -> None:
        pass

    @typed_invokable(name="idict_get_ref")
    def get_ref(self, key_len: int, index: int) -> "Cell":
        pass

    @typed_invokable(name="idict_get_ref?")
    def get_ref_check(self, key_len: int, index: int) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_set_get_ref")
    def set_get_ref(
        self,
        key_len: int,
        index: int,
        value: "Cell",
    ) -> tuple["IDict", "Cell"]:
        pass

    @typed_invokable(name="idict_set_get_ref")
    def set_get_ref_(self, key_len: int, index: int, value: "Cell") -> "Cell":
        pass

    @typed_invokable(name="idict_delete?")
    def delete_check(self, key_len: int, index: int) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_delete?")
    def delete_check_(self, key_len: int, index: int) -> int:
        pass

    @typed_invokable(name="idict_get?")
    def get_check(self, key_len: int, index: int) -> tuple["Slice", int]:
        pass

    @typed_invokable(name="idict_delete_get?")
    def delete_get_check(
        self,
        key_len: int,
        index: int,
    ) -> tuple["IDict", "Slice", int]:
        pass

    @typed_invokable(name="idict_delete_get?")
    def delete_get_check_(
        self,
        key_len: int,
        index: int,
    ) -> tuple["Slice", int]:
        pass

    @typed_invokable(name="idict_set")
    def set(self, key_len: int, index: int, value: "Slice") -> "IDict":
        pass

    @typed_invokable(name="idict_set")
    def set_(self, key_len: int, index: int, value: "Slice") -> None:
        pass

    @typed_invokable(name="idict_add?")
    def add_check(
        self,
        key_len: int,
        index: int,
        value: "Slice",
    ) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_add?")
    def add_check_(self, key_len: int, index: int, value: "Slice") -> int:
        pass

    @typed_invokable(name="idict_replace?")
    def replace_check(
        self,
        key_len: int,
        index: int,
        value: "Slice",
    ) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_replace?")
    def replace_check_(self, key_len: int, index: int, value: "Slice") -> int:
        pass

    @typed_invokable(name="idict_set_builder")
    def set_builder(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> "IDict":
        pass

    @typed_invokable(name="idict_set_builder")
    def set_builder_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> None:
        pass

    @typed_invokable(name="idict_add_builder?")
    def add_builder_check(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_replace_builder?")
    def replace_builder_check(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_add_builder?")
    def add_builder_check_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> int:
        pass

    @typed_invokable(name="idict_replace_builder?")
    def replace_builder_check_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> int:
        pass

    @typed_invokable(name="idict_delete_get_min")
    def delete_get_min(
        self,
        key_len: int,
    ) -> tuple["IDict", int, "Slice", int]:
        pass

    @typed_invokable(name="idict::delete_get_min")
    def delete_get_min_(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_delete_get_max")
    def delete_get_max(
        self,
        key_len: int,
    ) -> tuple["IDict", int, "Slice", int]:
        pass

    @typed_invokable(name="idict::delete_get_max")
    def delete_get_max_(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_min?")
    def get_min_check(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_max?")
    def get_max_check(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_min_ref?")
    def get_min_ref_check(self, key_len: int) -> tuple[int, "Cell", int]:
        pass

    @typed_invokable(name="idict_get_max_ref?")
    def get_max_ref_check(self, key_len: int) -> tuple[int, "Cell", int]:
        pass

    @typed_invokable(name="idict_get_next?")
    def get_next_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_nexteq?")
    def get_nexteq_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_prev?")
    def get_prev_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_preveq?")
    def get_preveq_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
        lazy: bool = True,
        **kwargs,
    ):
        if inplace:
            v = from_.idict_()
        else:
            v = from_.idict()
        if name is not None:
            v.__assign__(name)
        return v
