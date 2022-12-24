from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.util import type_id


class String(_FiftBaseType):
    __type_id__ = type_id("String")

    def __init__(self, __factory__: bool = False, __value__: str = None):
        if __value__:
            self.value = __value__
        pass

    @classmethod
    def __type__(cls) -> str:
        return "string"


Factory.register(String.__type__(), String)
