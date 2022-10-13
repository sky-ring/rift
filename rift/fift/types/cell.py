from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.fift.types.slice import Slice
    from rift.fift.types.builder import Builder

from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory


class Cell(_FiftBaseType):
    def __init__(self, __factory__: bool = False):
        pass

    @classmethod
    def __type__(cls) -> str:
        return "cell"

    def parse(self) -> "Slice":
        return self.cmd("<s", self)[0]

    @classmethod
    def __serialize__(
        cls, to: "Builder", value: "_FiftBaseType"
    ) -> "Builder":
        if value is None:
            return to
        return to.ref(value)

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


Factory.register(Cell.__type__(), Cell)
