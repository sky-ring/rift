from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory


class Cell(_FiftBaseType):
    def __init__(self):
        pass

    @classmethod
    def __type__(cls) -> str:
        return "cell"


Factory.register(Cell.__type__(), Cell)
