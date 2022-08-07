from dbuilder.types.types import Int


class SizedIntType(Int):
    pass


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
