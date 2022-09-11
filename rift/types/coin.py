from rift.core import Entity
from rift.types.types import Builder, Int, Slice


class Coin(Int):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if isinstance(value, Int) and value.value == 0:
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
        # TODO: HANDLE INPLACE STUFF
        v = from_.coin()
        if name is not None:
            v.__assign__(name)
        return v
