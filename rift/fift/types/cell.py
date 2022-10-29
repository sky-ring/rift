from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.fift.types.slice import Slice
    from rift.fift.types.builder import Builder
    from rift.fift.types.int import Int
    from rift.fift.types.bytes import Bytes

from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.util import type_id


class Cell(_FiftBaseType):
    __type_id__ = type_id("Cell")

    def __init__(self, __factory__: bool = False, __value__: str = None):
        if not __factory__:
            c: Cell = self.cmd("<b b>")[0]
            self.value = c.value
        if __value__ is not None:
            self.__load_data__(__value__)

    @classmethod
    def __type__(cls) -> str:
        return "cell"

    def parse(self) -> "Slice":
        return self.cmd("<s", self)[0]

    def hash(self) -> "Int":
        return self.cmd("hashu", self)[0]

    def hashB(self) -> "Bytes":
        return self.cmd("hashB", self)[0]

    @classmethod
    def __serialize__(
        cls,
        to: "Builder",
        value: "_FiftBaseType",
    ) -> "Builder":
        if value is None:
            return to
        s = value.parse()
        return to.slice(s)

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        inplace: bool = True,
        **kwargs,
    ):
        if inplace:
            v = from_.ref_()
        else:
            v = from_.ref()
        return v

    def __eq__(self, __o: "Cell") -> bool:
        return __o.value == self.value


Factory.register(Cell.__type__(), Cell)
