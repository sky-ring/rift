from dbuilder.core import Entity
from dbuilder.types.types import Builder, Slice


class SizedSlice(Slice):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
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
        if inplace:
            v = from_.bits_(cls.__bits__)
        else:
            v = from_.bits(cls.__bits__)
        if name is not None:
            v.__assign__(name)
        return v


class _SliceTypeBuilder(type):
    def __new__(cls, bits=32):
        return super().__new__(
            cls,
            "Slice%d" % (bits,),
            (SizedSlice,),
            {
                "__bits__": bits,
            },
        )


def slice(bits: int = 32):
    return _SliceTypeBuilder.__new__(_SliceTypeBuilder, bits=bits)
