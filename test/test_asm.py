from dbuilder.core.annots import asm, impure
from dbuilder.func.library import Library
from dbuilder.types import Cell, Slice

from .util import compile


class Asm(Library):
    @asm()
    def my_address(self) -> Slice:
        return "MYADDR"

    @impure
    @asm(name="compute_data_size?")
    def compute_data_size_check(
        self,
        c: Cell,
        max_cells: int,
    ) -> tuple[int, int, int, int]:
        return "CDATASIZEQ", "NULLSWAPIFNOT2", "NULLSWAPIFNOT"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="idict_get_preveq?",
    )
    def idict_get_preveq_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIGETPREVEQ", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="udict_get_min_ref?")
    def udict_get_min_ref_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Cell, int]:
        return "DICTUMINREF", "NULLSWAPIFNOT2"

    @asm(
        input_order=("value", "key", "dict_", "key_len"),
        name="pfxdict_set?",
    )
    def pfxdict_set_check(
        self,
        dict_: Cell,
        key_len: int,
        key: Slice,
        value: Slice,
    ) -> tuple[Cell, int]:
        return "PFXDICTSET"


def test_compile():
    compile(Asm)
