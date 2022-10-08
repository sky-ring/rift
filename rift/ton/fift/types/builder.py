from rift.ton.fift.types._fift_base import _FiftBaseType
from rift.ton.fift.types.factory import Factory


class Builder(_FiftBaseType):
    def __init__(self):
        pass

    @classmethod
    def __type__(cls) -> str:
        return "builder"


Factory.register(Builder.__type__(), Builder)
