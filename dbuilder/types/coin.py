from dbuilder.core import Entity
from dbuilder.types.types import Builder, Int, Slice


class Coin(Int):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        b = to.coins(value)
        return b

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
    ):
        # TODO: HANDLE INPLACE STUFF
        v = from_.coin()
        if name is not None:
            v.__assign__(name)
        return v
