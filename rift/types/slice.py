from rift.core import Entity
from rift.types.types import Builder, Slice
from rift.types.utils import CachingSubscriptable


class slice(Slice, metaclass=CachingSubscriptable):
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

    @classmethod
    def __build_type__(cls, size):
        return type(
            "Slice%d" % (size,),
            (cls,),
            {
                "__bits__": size,
            },
        )
