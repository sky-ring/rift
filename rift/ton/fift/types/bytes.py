from rift.ton.fift.types._fift_base import _FiftBaseType
from rift.ton.fift.types.factory import Factory


class Bytes(_FiftBaseType):
    def __init__(self):
        pass

    @classmethod
    def __type__(cls) -> str:
        return "bytes"


Factory.register(Bytes.__type__(), Bytes)
