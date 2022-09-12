from rift.core import Entity
from rift.core.condition import Cond
from rift.types.types import Builder, Slice
from rift.types.utils import CachingSubscriptable


class Maybe(metaclass=CachingSubscriptable):
    has: Entity
    bound: Entity

    def __getattr__(self, item):
        return getattr(self.bound, item)

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Maybe") -> "Builder":
        if value is None:
            b = to.uint(0, 1)
            return b
        if not isinstance(value, Maybe):
            return type(value).__serialize__(to, value)
            pass
        base = cls.__basex__
        to.__assign__("_b_tmp_")
        with Cond() as c:
            c.match(value.has)
            b = to.uint(1, 1)
            b = base.__serialize__(b, value.bound)
            b.__assign__("_b_tmp_")
            c.otherwise()
            b = to.uint(0, 1)
            b.__assign__("_b_tmp_")
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
        base = cls.__basex__
        if inplace:
            i = from_.uint_(1)
        else:
            i = from_.uint(1)
        m = Maybe()
        m.has = i
        m.has.__assign__(f"{name}_has")
        with Cond() as c:
            c.match(i)
            d = base.__deserialize__(from_, name=name, inplace=inplace)
            m.bound = d
        return m

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
        lazy: bool = True,
        **kwargs,
    ):
        base = cls.__basex__
        base.__predefine__(name=name)

    @classmethod
    def type_name(cls) -> str:
        base = cls.__basex__
        return base.type_name()

    @classmethod
    def __build_type__(cls, item):
        return type(
            "Maybe_%s" % item.__name__,
            (cls,),
            {
                "__basex__": item,
            },
        )
