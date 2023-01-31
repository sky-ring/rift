from rift.core import Entity
from rift.logging import log_system
from rift.types.bases import Builder, Int, Slice
from rift.types.utils import CachingSubscriptable


class integer(Int, metaclass=CachingSubscriptable):
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
        lazy: bool = True,
        **kwargs,
    ):
        log_system(
            "DE",
            "[{name}] loading sized int sign=>{sgn} size=>{size} [{lazy}]",
            name=name,
            lazy=lazy,
            sgn=cls.__signed__,
            size=cls.__bits__,
        )
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

    @classmethod
    def __build_type__(cls, items):
        if not isinstance(items, tuple):
            items = (items, False)
        bits, signed = items
        return type(
            "%sInt%d" % ("" if signed else "U", bits),
            (cls,),
            {
                "__bits__": bits,
                "__signed__": signed,
            },
        )
