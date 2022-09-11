import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rift.core import Entity
    from rift.types.types import Slice, Builder

from rift.core.invokable import typed_invokable
from rift.types.bases.entity_base import _EntityBase


class _CellBase(_EntityBase):
    @typed_invokable(name="begin_parse")
    def parse(self) -> "Slice":
        pass

    @typed_invokable(name="cell_hash")
    def hash(self) -> int:
        pass

    @typed_invokable(name="compute_data_size")
    def compute_data_size(self, max_cells: int) -> tuple[int, int, int]:
        pass

    @typed_invokable(name="compute_data_size?")
    def compute_data_size_check(
        self,
        max_cells: int,
    ) -> tuple[int, int, int, int]:
        pass

    @typed_invokable(name="set_data")
    def set_data(self) -> None:
        pass

    @typed_invokable(name="cell_depth")
    def depth(self) -> int:
        pass

    @typed_invokable(name="cell_null?")
    def is_null(self) -> int:
        pass

    @typed_invokable(name="send_raw_message")
    def send_raw_message(self, mode: int) -> None:
        pass

    @typed_invokable(name="set_code")
    def set_code(self) -> None:
        pass

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if value is None:
            return to
        return to.ref(value)

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
        lazy: bool = True,
        **kwargs,
    ):
        if inplace:
            v = from_.ref_()
        else:
            v = from_.ref()
        if name is not None:
            v.__assign__(name)
        return v
