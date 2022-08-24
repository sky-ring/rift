from typing import TYPE_CHECKING

from dbuilder.core import Entity

if TYPE_CHECKING:
    from dbuilder.types.types import Builder, Slice


class _EntityBase(Entity):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        return to

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
    ):
        pass

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
    ):
        if name is None:
            return
        from dbuilder.library.std import std

        v = std.null()
        v.__assign__(name)
        v.data.annotations["return"] = cls
