import base64
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.fift.types.slice import Slice
    from rift.fift.types.builder import Builder
    from rift.fift.types.int import Int
    from rift.fift.types.bytes import Bytes

from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.network.network import Network
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
        return from_

    def __eq__(self, __o: "Cell") -> bool:
        return __o.value == self.value

    def __bytes__(self) -> bytes:
        return base64.b64decode(self.value)

    def as_ref(self):
        from rift.types.ref import Ref

        return Ref[Cell](self)

    def send(self, testnet=True):
        n = Network(testnet=testnet)
        data = bytes(self)
        return n.send_boc(data)

    @classmethod
    def load_from(cls, file: str) -> "Cell":
        with open(file, "rb") as f:
            buf = f.read()
        data = base64.b64encode(buf).decode("utf-8")
        return Cell(__factory__=False, __value__=data)


Factory.register(Cell.__type__(), Cell)
