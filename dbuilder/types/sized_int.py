from dbuilder.core import Entity
from dbuilder.types.types import Builder, Int, Slice


class SizedIntType(Int):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if cls.__signed__:
            b = to.sint(value, cls.__bits__)
        else:
            b = to.uint(value, cls.__bits__)
        return b

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
    ):
        if cls.__signed__:
            if inplace:
                v = from_.sint_(cls.__bits__)
            else:
                v = from_.sint(cls.__bits__)
        else:
            if inplace:
                v = from_.uint_(cls.__bits__)
            else:
                v = from_.uint(cls.__bits__)
        if name is not None:
            v.__assign__(name)
        return v


class _IntTypeBuilder(type):
    def __new__(cls, bits=32, signed=False):
        return super().__new__(
            cls,
            "%sInt%d" % ("" if signed else "U", bits),
            (SizedIntType,),
            {
                "__bits__": bits,
                "__signed__": signed,
            },
        )


def SizedInt(bits: int = 32, signed: bool = False):
    return _IntTypeBuilder.__new__(_IntTypeBuilder, bits=bits, signed=signed)
