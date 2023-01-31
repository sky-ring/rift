from rift.core import Entity
from rift.logging import log_system
from rift.types.bases import Builder, Int, Slice


class Coin(Int):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if isinstance(value, Int) and value.value == 0:
            if hasattr(value, "NAMED") and not value.NAMED:
                b = to.uint(0, 4)
                return b
        b = to.coins(value)
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
            "DE", "[{name}] loading coin [{lazy}]", name=name, lazy=lazy
        )
        # TODO: HANDLE INPLACE STUFF
        v = from_.coin_()
        if name is not None:
            v.__assign__(name)
        return v
