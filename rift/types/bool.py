from rift.core import Entity
from rift.logging import log_system
from rift.types.bases import Builder, Int, Slice


class Bool(Int):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        b = to.uint(value, 1)
        return b

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
        lazy: bool = True,
        **kwargs,
    ):
        log_system(
            "DE", "[{name}] loading bool [{lazy}]", name=name, lazy=lazy
        )
        if inplace:
            v = from_.uint_(1)
        else:
            v = from_.uint(1)
        if name is not None:
            v.__assign__(name)
        return v
