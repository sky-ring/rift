from typing import TYPE_CHECKING

from rift.core import Entity

if TYPE_CHECKING:
    from rift.types.types import Builder, Slice


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
        lazy: bool = True,
        **kwargs,
    ):
        pass

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
        lazy: bool = True,
        **kwargs,
    ):
        if name is None:
            return
        from rift.library.std import std

        v = std.null()
        v.__assign__(name)
        v.data.annotations["return"] = cls
