from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dbuilder.types.types import Slice

from dbuilder.core.invokable import typed_invokable
from dbuilder.types.bases.entity_base import _EntityBase


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
