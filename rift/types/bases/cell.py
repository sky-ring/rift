from rift.fift.types.cell import Cell as FiftCell
from rift.func.types.types import Cell as FunCCell
from rift.meta.behaviors import stub


class Cell(FunCCell + FiftCell):
    pass
