from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.fift.types.cell import Cell
    from rift.fift.types.tuple import Tuple

from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.util import type_id


class Slice(_FiftBaseType):
    __type_id__ = type_id("Slice")

    def __init__(self, __value__: str = None, __factory__: bool = False):
        if not __factory__ and __value__:
            self.__load_data__(__value__)

    @classmethod
    def __type__(cls) -> str:
        return "cell_slice"

    def coin_(self) -> int:
        r: int
        s: Slice
        r, s = self.cmd("Gram@+", self)
        self.value = s.value
        return r

    def coin(self) -> int:
        r: int = self.cmd("Gram@", self)[0]
        return r

    def uint_(self, bits: int) -> int:
        r: int
        s: Slice
        r, s = self.cmd("u@+", self, bits)
        self.value = s.value
        return r

    def uint(self, bits: int) -> int:
        r: int = self.cmd("u@", self, bits)[0]
        return r

    def sint_(self, bits: int) -> int:
        r: int
        s: Slice
        r, s = self.cmd("i@+", self, bits)
        self.value = s.value
        return r

    def sint(self, bits: int) -> int:
        r: int = self.cmd("i@", self, bits)[0]
        return r

    def hash(self) -> int:
        pass

    def string_hash(self) -> int:
        pass

    def check_signature(self, signature: "Slice", public_key: int) -> int:
        pass

    def compute_data_size(self, max_cells: int) -> tuple[int, int, int]:
        pass

    def end_parse(self) -> None:
        pass

    def ref_(self) -> "Cell":
        r: "Cell"
        s: Slice
        s, r = self.cmd("ref@+", self)
        self.value = s.value
        return r

    def ref(self) -> "Cell":
        r: "Cell" = self.cmd("ref@", self)[0]
        return r

    def bits_(self, len_: int) -> "Slice":
        pass

    def bits(self, len_: int) -> "Slice":
        pass

    def skip_n(self, len_: int) -> None:
        pass

    def skip_n_(self, len_: int) -> None:
        pass

    def first_bits(self, len_: int) -> "Slice":
        pass

    def skip_last_n(self, len_: int) -> None:
        pass

    def skip_last_n_(self, len_: int) -> None:
        pass

    def slice_last(self, len_: int) -> "Slice":
        pass

    def ldict_(self) -> "Cell":
        x = self.uint_(1)
        if x == 1:
            return self.ref_()
        return None

    def ldict(self) -> "Cell":
        return self.ref()

    def skip_dict(self) -> None:
        pass

    def maybe_ref_(self) -> "Cell":
        pass

    def maybe_ref(self) -> "Cell":
        pass

    def refs_n(self) -> int:
        return self.cmd("srefs", self)[0]

    def bits_n(self) -> int:
        return self.cmd("sbits", self)[0]

    def bits_refs_n(self) -> tuple[int, int]:
        pass

    def is_empty(self) -> int:
        pass

    def is_data_empty(self) -> int:
        pass

    def are_refs_empty(self) -> int:
        pass

    def depth(self) -> int:
        pass

    def addr_(self) -> "Slice":
        x = self.uint_(2)
        if x == 0:
            return None
        if x == 2:
            # TODO: return proper address object
            w = self.uint_(9)
            a = self.uint_(256)
            return None
        return None

    def parse_addr(self) -> "Tuple":
        pass

    def parse_std_addr(self) -> tuple[int, int]:
        pass

    def parse_var_addr(self) -> tuple[int, "Slice"]:
        pass

    def is_equal(self, b: "Slice") -> int:
        pass


Factory.register(Slice.__type__(), Slice)
