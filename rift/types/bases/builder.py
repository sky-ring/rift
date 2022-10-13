from typing import TYPE_CHECKING

from rift.fift.types.builder import Builder as FiftBuilder
from rift.func.types.types import Builder as FunCBuilder
from rift.meta.behaviors import stub

if TYPE_CHECKING:
    from rift.types.bases.cell import Cell
    from rift.types.bases.slice import Slice


class Builder(FunCBuilder + FiftBuilder):
    @stub
    def refs_n(self) -> int:
        pass

    @stub
    def bits_n(self) -> int:
        pass

    @stub
    def depth(self) -> int:
        pass

    @stub
    def end(self) -> "Cell":
        pass

    @stub
    def ref(self, c: "Cell") -> "Builder":
        pass

    @stub
    def uint(self, x: int, len_: int) -> "Builder":
        pass

    @stub
    def sint(self, x: int, len_: int) -> "Builder":
        pass

    @stub
    def slice(self, s: "Slice") -> "Builder":
        pass

    @stub
    def dict(self, c: "Cell") -> "Builder":
        pass

    @stub
    def coins(self, x: int) -> "Builder":
        pass

    @stub
    def is_null(self) -> int:
        pass

    @stub
    def builder(self, from_: "Builder") -> "Builder":
        pass
