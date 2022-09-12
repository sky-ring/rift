from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.types.types import Slice, Cell, UDict, Builder

from rift.core.invokable import typed_invokable
from rift.types.bases.dict_base import _DictBase


class _UDictBase(_DictBase):
    @typed_invokable(name="udict_set_ref")
    def set_ref(self, key_len: int, index: int, value: "Cell") -> "UDict":
        pass

    @typed_invokable(name="udict_set_ref")
    def set_ref_(self, key_len: int, index: int, value: "Cell") -> None:
        pass

    @typed_invokable(name="udict_get_ref")
    def get_ref(self, key_len: int, index: int) -> "Cell":
        pass

    @typed_invokable(name="udict_get_ref?")
    def get_ref_check(self, key_len: int, index: int) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_set_get_ref")
    def set_get_ref(
        self,
        key_len: int,
        index: int,
        value: "Cell",
    ) -> tuple["UDict", "Cell"]:
        pass

    @typed_invokable(name="udict_set_get_ref")
    def set_get_ref_(self, key_len: int, index: int, value: "Cell") -> "Cell":
        pass

    @typed_invokable(name="udict_delete?")
    def delete_check(self, key_len: int, index: int) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_delete?")
    def delete_check_(self, key_len: int, index: int) -> int:
        pass

    @typed_invokable(name="udict_get?")
    def get_check(self, key_len: int, index: int) -> tuple["Slice", int]:
        pass

    @typed_invokable(name="udict_delete_get?")
    def delete_get_check(
        self,
        key_len: int,
        index: int,
    ) -> tuple["UDict", "Slice", int]:
        pass

    @typed_invokable(name="udict_delete_get?")
    def delete_get_check_(
        self,
        key_len: int,
        index: int,
    ) -> tuple["Slice", int]:
        pass

    @typed_invokable(name="udict_set")
    def set(self, key_len: int, index: int, value: "Slice") -> "UDict":
        pass

    @typed_invokable(name="udict_set")
    def set_(self, key_len: int, index: int, value: "Slice") -> None:
        pass

    @typed_invokable(name="udict_add?")
    def add_check(
        self,
        key_len: int,
        index: int,
        value: "Slice",
    ) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_add?")
    def add_check_(self, key_len: int, index: int, value: "Slice") -> int:
        pass

    @typed_invokable(name="udict_replace?")
    def replace_check(
        self,
        key_len: int,
        index: int,
        value: "Slice",
    ) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_replace?")
    def replace_check_(self, key_len: int, index: int, value: "Slice") -> int:
        pass

    @typed_invokable(name="udict_set_builder")
    def set_builder(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> "UDict":
        pass

    @typed_invokable(name="udict_set_builder")
    def set_builder_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> None:
        pass

    @typed_invokable(name="udict_add_builder?")
    def add_builder_check(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_replace_builder?")
    def replace_builder_check(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_add_builder?")
    def add_builder_check_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> int:
        pass

    @typed_invokable(name="udict_replace_builder?")
    def replace_builder_check_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> int:
        pass

    @typed_invokable(name="udict_delete_get_min")
    def delete_get_min(
        self,
        key_len: int,
    ) -> tuple["UDict", int, "Slice", int]:
        pass

    @typed_invokable(name="udict::delete_get_min")
    def delete_get_min_(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_delete_get_max")
    def delete_get_max(
        self,
        key_len: int,
    ) -> tuple["UDict", int, "Slice", int]:
        pass

    @typed_invokable(name="udict::delete_get_max")
    def delete_get_max_(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_min?")
    def get_min_check(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_max?")
    def get_max_check(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_min_ref?")
    def get_min_ref_check(self, key_len: int) -> tuple[int, "Cell", int]:
        pass

    @typed_invokable(name="udict_get_max_ref?")
    def get_max_ref_check(self, key_len: int) -> tuple[int, "Cell", int]:
        pass

    @typed_invokable(name="udict_get_next?")
    def get_next_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_nexteq?")
    def get_nexteq_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_prev?")
    def get_prev_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_preveq?")
    def get_preveq_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass
