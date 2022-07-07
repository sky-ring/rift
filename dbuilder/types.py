class _UIntType(type):
    def __new__(cls, bits):
        return super().__new__(cls, "UInt%d" % bits, (), {
            "bits": bits
        })


def UInt(bits: int):
    return _UIntType(bits)

