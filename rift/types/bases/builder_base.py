from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.types.types import Slice, Cell, Builder

from rift.core.factory import Factory
from rift.core.invokable import typed_invokable
from rift.types.bases.entity_base import _EntityBase


class _BuilderBase(_EntityBase):
    EXPERIMENTAL_PACKING = False
    pending_uint = False
    pending_val = "0b"
    pending_len = 0

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if not _BuilderBase.EXPERIMENTAL_PACKING:
            return attr
        if name == "reset_uint" or name == "uint_base":
            return attr
        if type(attr).__name__ == "method":
            # it's method let's wrap it
            def b(*args, **kwargs):
                if name != "uint" and self.pending_uint:
                    # break summing - write pending uint
                    x = _BuilderBase.reset_uint(self)
                    args = (x, args[1:])
                result = attr(*args, **kwargs)
                return result

            return b
        return attr

    @typed_invokable(name="store_maybe_ref")
    def write_maybe(self, c: "Cell") -> "Builder":
        pass

    @typed_invokable(name="builder_refs")
    def refs_n(self) -> int:
        pass

    @typed_invokable(name="builder_bits")
    def bits_n(self) -> int:
        pass

    @typed_invokable(name="builder_depth")
    def depth(self) -> int:
        pass

    @typed_invokable(name="end_cell")
    def end(self) -> "Cell":
        pass

    @typed_invokable(name="store_ref")
    def ref(self, c: "Cell") -> "Builder":
        pass

    def reset_uint(self) -> "Builder":
        n = Factory.build("HexInt", int(self.pending_val, base=2))
        b = _BuilderBase.uint_base(self, n, self.pending_len)
        print("reseting", self.pending_val, self.pending_len)
        self.pending_uint = False
        self.pending_val = "0b"
        self.pending_len = 0
        return b

    def uint(self, x: int, len_: int) -> "Builder":
        if not _BuilderBase.EXPERIMENTAL_PACKING:
            return self.uint_base(x, len_)
        b = self
        print(type(x))
        print(x)
        if not isinstance(x, int):
            if self.pending_uint:
                b = self.reset_uint()
            b = b.uint_base(x, len_)
            return b
        if (128 - self.pending_len) < len_:
            b = self.reset_uint()
            b = b.uint(x, len_)
            return b
        self.pending_uint = True
        self.pending_len += len_
        vl_ = bin(x)[2:]
        if len(vl_) < len_:
            vl_ = ("0" * (len_ - len(vl_))) + vl_
        self.pending_val += vl_
        return self

    @typed_invokable(name="store_uint")
    def uint_base(self, x: int, len_: int) -> "Builder":
        pass

    @typed_invokable(name="store_int")
    def sint(self, x: int, len_: int) -> "Builder":
        pass

    @typed_invokable(name="store_slice")
    def slice(self, s: "Slice") -> "Builder":
        pass

    @typed_invokable(name="store_dict")
    def dict(self, c: "Cell") -> "Builder":
        pass

    @typed_invokable(name="store_coins")
    def coins(self, x: int) -> "Builder":
        pass

    @typed_invokable(name="builder_null?")
    def is_null(self) -> int:
        pass

    @typed_invokable(name="store_builder")
    def builder(self, from_: "Builder") -> "Builder":
        pass
