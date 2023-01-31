from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.fift.types.slice import Slice
    from rift.fift.types.cell import Cell

from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.util import type_id


class Builder(_FiftBaseType):
    __type_id__ = type_id("Builder")

    def __init__(self, __factory__: bool = False):
        if not __factory__:
            b: Builder = self.cmd("<b")[0]
            self.value = b.value

    @classmethod
    def __type__(cls) -> str:
        return "builder"

    def refs_n(self) -> int:
        return self.cmd("brefs", self)[0]

    def bits_n(self) -> int:
        return self.cmd("bbits", self)[0]

    def depth(self) -> int:
        pass

    def end(self) -> "Cell":
        return self.cmd("b>", self)[0]

    def ref(self, c: "Cell") -> "Builder":
        b: Builder = self.cmd("ref,", self, c)[0]
        # self.value = b.value
        # return self
        return b

    def uint(self, x: int, len_: int) -> "Builder":
        b: Builder = self.cmd("u,", self, x, len_)[0]
        # self.value = b.value
        # return self
        return b

    def sint(self, x: int, len_: int) -> "Builder":
        b: Builder = self.cmd("i,", self, x, len_)[0]
        # self.value = b.value
        # return self
        return b

    def slice(self, s: "Slice") -> "Builder":
        b: Builder = self.cmd("s,", self, s)[0]
        # self.value = b.value
        # return self
        return b

    def dict(self, c: "Cell") -> "Builder":
        b = self.uint(1 if c is not None else 0, 1)
        if c is not None:
            return b.ref(c)
        return b

    def coins(self, x: int) -> "Builder":
        b: Builder = self.cmd("Gram,", self, x)[0]
        # self.value = b.value
        # return self
        return b

    def is_null(self) -> int:
        return self.bits_n() == 0 and self.refs_n() == 0

    def builder(self, from_: "Builder") -> "Builder":
        b: Builder = self.cmd("b+", self, from_)[0]
        # self.value = b.value
        # return self
        return b


Factory.register(Builder.__type__(), Builder)
