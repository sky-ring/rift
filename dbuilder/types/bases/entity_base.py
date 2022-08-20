from typing import TYPE_CHECKING

from dbuilder.core import Entity

if TYPE_CHECKING:
    from dbuilder.types.types import Builder, Slice


class _EntityBase(Entity):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        pass

    @classmethod
    def __deserialize__(
        cls, from_: "Slice", name: str = None, inplace: bool = True,
    ):
        pass
