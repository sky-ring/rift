from typing import TYPE_CHECKING

from dbuilder.core import Entity

if TYPE_CHECKING:
    from dbuilder.types.types import Slice, Cell, Builder

from dbuilder.core.invokable import typed_invokable


class _BuilderBase(Entity):
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

    @typed_invokable(name="store_uint")
    def uint(self, x: int, len_: int) -> "Builder":
        pass

    @typed_invokable(name="store_int")
    def int(self, x: int, len_: int) -> "Builder":
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
