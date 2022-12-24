from rift.fift.types.int import Int as FiftInt
from rift.func.types.types import Int as FunCInt
from rift.meta.behaviors import stub


class Int(FunCInt + FiftInt):
    pass
