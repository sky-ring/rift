from hashlib import sha256


def type_id(cls: type | str):
    if not isinstance(cls, str):
        cls = cls.__name__
    f = sha256(cls.encode("utf-8")).digest()[:8]
    x = int.from_bytes(f, byteorder="big", signed=False)

    def f():
        return x

    return f
