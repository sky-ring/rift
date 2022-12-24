import base64

from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.util import type_id


class Bytes(_FiftBaseType):
    __type_id__ = type_id("Bytes")

    def __init__(
        self,
        __factory__: bool = False,
        __value__: str | bytes = None,
        encoding="base64",
    ):
        if not __factory__ and __value__:
            if isinstance(__value__, str):
                if encoding == "hex":
                    v = bytes.fromhex(__value__)
                elif encoding == "base64":
                    v = __value__
                else:
                    raise RuntimeError("Invalid Encoding")
            elif isinstance(__value__, bytes):
                v = __value__
            else:
                raise RuntimeError("Invalid value")
            if isinstance(v, bytes):
                v = base64.b64encode(v).decode("utf-8")
            self.__load_data__(v)

    def __len__(self) -> int:
        return self.cmd("Blen", self)[0].value

    def hashB(self) -> "Bytes":
        return self.cmd("BhashB", self)[0]

    def __bytes__(self) -> bytes:
        return base64.b64decode(self.value)

    @classmethod
    def __type__(cls) -> str:
        return "bytes"


Factory.register(Bytes.__type__(), Bytes)
