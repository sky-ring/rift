from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory


class Slice(_FiftBaseType):
    def __init__(self):
        pass

    @classmethod
    def __type__(cls) -> str:
        return "cell_slice"


Factory.register(Slice.__type__(), Slice)
