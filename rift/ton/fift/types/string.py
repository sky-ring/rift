from rift.ton.fift.types._fift_base import _FiftBaseType
from rift.ton.fift.types.factory import Factory


class String(_FiftBaseType):
    def __init__(self):
        pass

    @classmethod
    def __type__(cls) -> str:
        return "string"


Factory.register(String.__type__(), String)
