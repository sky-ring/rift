from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory


class Bytes(_FiftBaseType):
    def __init__(self, __factory__: bool = False):
        pass

    @classmethod
    def __type__(cls) -> str:
        return "bytes"


Factory.register(Bytes.__type__(), Bytes)
