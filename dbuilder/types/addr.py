from dbuilder.core import Entity
from dbuilder.types.int_aliases import uint2
from dbuilder.types.types import Builder, Int, Slice


class MsgAddress(Slice):
    Empty = uint2(0b00)

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if isinstance(value, Int):
            b = type(value).__serialize__(to, value)
        else:
            b = to.slice(value)
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
        v = from_.addr_()
        if name is not None:
            v.__assign__(name)
        return v
