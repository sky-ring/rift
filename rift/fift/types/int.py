from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.util import type_id


class Int(_FiftBaseType):
    __type_id__ = type_id("Int")

    def __init__(self, value: int | None = None, __factory__: bool = False):
        if value is not None:
            self.value = value

    def __load_data__(self, value: str, *args, **kwargs):
        self.value = int(value)

    @classmethod
    def __type__(cls) -> str:
        return "int"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Int):
            return __o.value == self.value
        return isinstance(__o, int) and __o == self.value

    def __bool__(self):
        return bool(self.value)


Factory.register(Int.__type__(), Int)
