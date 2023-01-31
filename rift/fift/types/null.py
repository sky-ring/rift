from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.util import type_id


class Null(_FiftBaseType):
    __type_id__ = type_id("Null")

    def __init__(self, __factory__: bool = False):
        pass

    def __load_data__(self, value: str, *args, **kwargs):
        self.value = value
        pass

    @classmethod
    def __type__(cls) -> str:
        return "null"

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Null)

    def __stack_entry__(self):
        return {"type": "null"}


Factory.register(Null.__type__(), Null)
