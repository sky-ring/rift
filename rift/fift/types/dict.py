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
from rift.network.network import Network
from rift.util import type_id


class Dict(Cell):
    __type_id__ = type_id("Dict")

    @classmethod
    def __type__(cls) -> str:
        return "dict"

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


Factory.register(Dict.__type__(), Dict)
