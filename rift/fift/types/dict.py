import base64
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.fift.types.slice import Slice
    from rift.fift.types.builder import Builder
    from rift.fift.types.int import Int
    from rift.fift.types.bytes import Bytes

from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.cell import Cell
from rift.fift.types.factory import Factory
from rift.util import type_id


class Dict(Cell):
    __type_id__ = type_id("Dict")

    def __init__(self, __factory__: bool = False, __value__: str = None):
        if not __factory__:
            c: Dict = self.cmd("dictnew")[0]
            self.value = c.value
        if __value__ is not None:
            self.__load_data__(__value__)

    @classmethod
    def __type__(cls) -> str:
        return "dict"

    def idict_set(self, n_bits: "Int", x: "Int", value: "Slice"):
        new_d, ok = self.cmd("idict!", value, x, self, n_bits)
        new_d = Dict(__value__=new_d.value)
        return new_d, ok

    def idict_get(self, n_bits: "Int", x: "Int"):
        stack_out = self.cmd("idict@", x, self, n_bits)
        if len(stack_out) == 1:
            return None
        else:
            return stack_out[0]

    @classmethod
    def __serialize__(
        cls,
        to: "Builder",
        value: "_FiftBaseType",
    ) -> "Builder":
        b = to.dict(value)
        return b

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        inplace: bool = True,
        **kwargs,
    ):
        d = from_.ldict_()
        return d

    def __stack_entry__(self):
        return {
            "type": "cell",
            "value": self.value,
        }


Factory.register(Dict.__type__(), Dict)
