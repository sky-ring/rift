from typing import TYPE_CHECKING

from rift.fift.types.cell import Cell as FiftCell
from rift.func.types.types import Cell as FunCCell

if TYPE_CHECKING:
    from rift.types.ref import Ref
    from rift.types.bases.int import Int

from rift.meta.behaviors import stub


class Cell(FunCCell + FiftCell):
    @stub
    def as_ref(self) -> "Ref[Cell]":
        pass

    @stub
    def send(self, testnet=True, flags=0):
        pass

    @stub
    def hash(self) -> "Int":
        pass
