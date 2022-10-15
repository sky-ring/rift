from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory


class String(_FiftBaseType):
    def __init__(self, __factory__: bool = False):
        pass

    @classmethod
    def __type__(cls) -> str:
        return "string"


Factory.register(String.__type__(), String)
