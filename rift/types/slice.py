from rift.core import Entity
from rift.logging import log_system
from rift.types.bases import Builder, Slice
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
        log_system(
            "DE",
            "[{name}] loading slice size=>{size} [{lazy}]",
            name=name,
            lazy=lazy,
            size=cls.__bits__,
        )
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
