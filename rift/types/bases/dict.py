from rift.fift.types.dict import Dict as FiftDict
from rift.func.types.types import Dict as FunCDict
from rift.meta.behaviors import stub


class Dict(FunCDict + FiftDict):
    pass
