from typing import TYPE_CHECKING

from rift.fift.types.slice import Slice as FiftSlice
from rift.func.types.types import Slice as FunCSlice
from rift.meta.behaviors import stub

if TYPE_CHECKING:
    from rift.func.types.types import Cont, Tuple
    from rift.types.bases.cell import Cell


class Slice(FunCSlice + FiftSlice):
    @stub
    def coin(self) -> int:
        pass

    @stub
    def uint_(self, bits: int) -> int:
        pass

    @stub
    def uint(self, bits: int) -> int:
        pass

    @stub
    def sint_(self, bits: int) -> int:
        pass

    @stub
    def sint(self, bits: int) -> int:
        pass

    @stub
    def hash(self) -> int:
        pass

    @stub
    def string_hash(self) -> int:
        pass

    @stub
    def check_signature(self, signature: "Slice", public_key: int) -> int:
        pass

    @stub
    def compute_data_size(self, max_cells: int) -> tuple[int, int, int]:
        pass

    @stub
    def bless(self) -> "Cont":
        pass

    @stub
    def end_parse(self) -> None:
        pass

    @stub
    def ref_(self) -> "Cell":
        pass

    @stub
    def ref(self) -> "Cell":
        pass

    @stub
    def bits_(self, len_: int) -> "Slice":
        pass

    @stub
    def bits(self, len_: int) -> "Slice":
        pass

    @stub
    def skip_n(self, len_: int) -> None:
        pass

    @stub
    def skip_n_(self, len_: int) -> None:
        pass

    @stub
    def first_bits(self, len_: int) -> "Slice":
        pass

    @stub
    def skip_last_n(self, len_: int) -> None:
        pass

    @stub
    def skip_last_n_(self, len_: int) -> None:
        pass

    @stub
    def slice_last(self, len_: int) -> "Slice":
        pass

    @stub
    def ldict_(self) -> "Cell":
        pass

    @stub
    def ldict(self) -> "Cell":
        pass

    @stub
    def skip_dict(self) -> None:
        pass

    @stub
    def maybe_ref_(self) -> "Cell":
        pass

    @stub
    def maybe_ref(self) -> "Cell":
        pass

    @stub
    def refs_n(self) -> int:
        pass

    @stub
    def bits_n(self) -> int:
        pass

    @stub
    def bits_refs_n(self) -> tuple[int, int]:
        pass

    @stub
    def is_empty(self) -> int:
        pass

    @stub
    def is_data_empty(self) -> int:
        pass

    @stub
    def are_refs_empty(self) -> int:
        pass

    @stub
    def depth(self) -> int:
        pass

    @stub
    def addr_(self) -> "Slice":
        pass

    @stub
    def parse_addr(self) -> "Tuple":
        pass

    @stub
    def parse_std_addr(self) -> tuple[int, int]:
        pass

    @stub
    def parse_var_addr(self) -> tuple[int, "Slice"]:
        pass

    @stub
    def is_equal(self, b: "Slice") -> int:
        pass
