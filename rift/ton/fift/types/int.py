from rift.ton.fift.types._fift_base import _FiftBaseType
from rift.ton.fift.types.factory import Factory


class Int(_FiftBaseType):
    def __init__(self, value: int | None = None):
        pass

    def __load_data__(self, value: str, *args, **kwargs):
        self.value = int(value)

    @classmethod
    def __type__(cls) -> str:
        return "int"


Factory.register(Int.__type__(), Int)
