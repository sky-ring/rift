from rift.core.annots import asm, impure
from rift.core.entity import Entity
from rift.func.library import Library
from rift.func.types.types import Builder, Cell, Cont, Slice, Tuple


# noinspection PyTypeChecker,SpellCheckingInspection,PyUnusedLocal
class RiftLib(Library):
    __ignore__ = True

    @impure
    @asm()
    def dump(self, a: int) -> None:
        return "DUMP"


rift_lib = RiftLib()
