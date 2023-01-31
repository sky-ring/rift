from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.func.types.types import (
        Slice,
        Cont,
        Cell,
        Tuple,
        Dict,
        IDict,
        UDict,
        PfxDict,
    )

from rift.core.invokable import typed_invokable
from rift.func.types.entity_base import _EntityBase


class _SliceBase(_EntityBase):
    @typed_invokable(name="load_coins_")
    def coin_(self) -> int:
        pass

    @typed_invokable(name="load_uint_")
    def uint_(self, bits: int) -> int:
        pass

    @typed_invokable(name="preload_uint")
    def uint(self, bits: int) -> int:
        pass

    @typed_invokable(name="load_int_")
    def sint_(self, bits: int) -> int:
        pass

    @typed_invokable(name="preload_int")
    def sint(self, bits: int) -> int:
        pass

    @typed_invokable(name="slice_hash")
    def hash(self) -> int:
        pass

    @typed_invokable(name="string_hash")
    def string_hash(self) -> int:
        pass

    @typed_invokable(name="check_data_signature")
    def check_signature(self, signature: "Slice", public_key: int) -> int:
        pass

    @typed_invokable(name="slice_compute_data_size")
    def compute_data_size(self, max_cells: int) -> tuple[int, int, int]:
        pass

    @typed_invokable(name="bless")
    def bless(self) -> "Cont":
        pass

    @typed_invokable(name="end_parse")
    def end_parse(self) -> None:
        pass

    @typed_invokable(name="load_ref_")
    def ref_(self) -> "Cell":
        pass

    @typed_invokable(name="preload_ref")
    def ref(self) -> "Cell":
        pass

    @typed_invokable(name="load_bits_")
    def bits_(self, len_: int) -> "Slice":
        pass

    @typed_invokable(name="preload_bits")
    def bits(self, len_: int) -> "Slice":
        pass

    @typed_invokable(name="skip_bits")
    def skip_n(self, len_: int) -> None:
        pass

    @typed_invokable(name="skip_bits")
    def skip_n_(self, len_: int) -> None:
        pass

    @typed_invokable(name="first_bits")
    def first_bits(self, len_: int) -> "Slice":
        pass

    @typed_invokable(name="skip_last_bits")
    def skip_last_n(self, len_: int) -> None:
        pass

    @typed_invokable(name="skip_last_bits")
    def skip_last_n_(self, len_: int) -> None:
        pass

    @typed_invokable(name="slice_last")
    def slice_last(self, len_: int) -> "Slice":
        pass

    @typed_invokable(name="load_dict_")
    def ldict_(self) -> "Dict":
        pass

    @typed_invokable(name="preload_dict")
    def ldict(self) -> "Dict":
        pass

    @typed_invokable(name="load_dict_")
    def idict_(self) -> "IDict":
        pass

    @typed_invokable(name="preload_dict")
    def idict(self) -> "IDict":
        pass

    @typed_invokable(name="load_dict_")
    def udict_(self) -> "UDict":
        pass

    @typed_invokable(name="preload_dict")
    def udict(self) -> "UDict":
        pass

    @typed_invokable(name="load_dict_")
    def pdict_(self) -> "PfxDict":
        pass

    @typed_invokable(name="preload_dict")
    def pdict(self) -> "PfxDict":
        pass

    @typed_invokable(name="skip_dict")
    def skip_dict(self) -> None:
        pass

    @typed_invokable(name="load_maybe_ref_")
    def maybe_ref_(self) -> "Cell":
        pass

    @typed_invokable(name="preload_maybe_ref")
    def maybe_ref(self) -> "Cell":
        pass

    @typed_invokable(name="slice_refs")
    def refs_n(self) -> int:
        pass

    @typed_invokable(name="slice_bits")
    def bits_n(self) -> int:
        pass

    @typed_invokable(name="slice_bits_refs")
    def bits_refs_n(self) -> tuple[int, int]:
        pass

    @typed_invokable(name="slice_empty?")
    def is_empty(self) -> int:
        pass

    @typed_invokable(name="slice_data_empty?")
    def is_data_empty(self) -> int:
        pass

    @typed_invokable(name="slice_refs_empty?")
    def are_refs_empty(self) -> int:
        pass

    @typed_invokable(name="slice_depth")
    def depth(self) -> int:
        pass

    @typed_invokable(name="load_msg_addr_")
    def addr_(self) -> "Slice":
        pass

    @typed_invokable(name="parse_addr")
    def parse_addr(self) -> "Tuple":
        pass

    @typed_invokable(name="parse_std_addr")
    def parse_std_addr(self) -> tuple[int, int]:
        pass

    @typed_invokable(name="parse_var_addr")
    def parse_var_addr(self) -> tuple[int, "Slice"]:
        pass

    @typed_invokable(name="equal_slices")
    def is_equal(self, b: "Slice") -> int:
        pass
