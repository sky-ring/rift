from rift.fift.types.string import String as FiftString
from rift.func.types.types import String as FunCString
from rift.meta.behaviors import stub


class String(FunCString + FiftString):
    pass
