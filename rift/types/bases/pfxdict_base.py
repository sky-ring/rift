from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.types.types import Slice, PfxDict

from rift.core.invokable import typed_invokable
from rift.types.bases.cell_base import _CellBase


class _PfxDictBase(_CellBase):
    @typed_invokable(name="pfxdict_get?")
    def pfxdict_get_check(
        self,
        key_len: int,
        key: "Slice",
    ) -> tuple["Slice", "Slice", "Slice", int]:
        pass

    @typed_invokable(name="pfxdict_set?")
    def pfxdict_set_check(
        self,
        key_len: int,
        key: "Slice",
        value: "Slice",
    ) -> tuple["PfxDict", int]:
        pass

    @typed_invokable(name="pfxdict_delete?")
    def pfxdict_delete_check(
        self,
        key_len: int,
        key: "Slice",
    ) -> tuple["PfxDict", int]:
        pass

    @typed_invokable(name="pfxdict_set?")
    def pfxdict_set_check_(
        self,
        key_len: int,
        key: "Slice",
        value: "Slice",
    ) -> int:
        pass

    @typed_invokable(name="pfxdict_delete?")
    def pfxdict_delete_check_(self, key_len: int, key: "Slice") -> int:
        pass
