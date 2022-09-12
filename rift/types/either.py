from rift.core import Entity
from rift.core.condition import Cond
from rift.types.ref import Ref
from rift.types.types import Builder, Cell, Slice
from rift.types.utils import CachingSubscriptable


class Either(metaclass=CachingSubscriptable):
    which: Entity
    bound: Entity

    def __getattr__(self, item):
        return getattr(self.bound, item)

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Either") -> "Builder":
        base1 = cls.__base1__
        base2 = cls.__base2__
        if value is None:
            b = to.uint(0, 1)
            return b
        if isinstance(value, Slice):
            b = to.slice(value)
            return b
        if isinstance(value, Cell):
            b = to.ref(value)
            return b
        if not isinstance(value, Either):
            if type(value) == base1:
                v = 0
            elif type(value) == base2:
                v = 1
            else:
                msg = "got {current} expected {e1} or {e2}"
                msg = msg.format(current=type(value), e1=base1, e2=base2)
                raise RuntimeError("Couldn't match either types; " + msg)
            to = to.uint(v, 1)
            return type(value).__serialize__(to, value)
        to.__assign__("_b_tmp_")
        with Cond() as c:
            c.match(value.which)
            b = to.uint(1, 1)
            b = base2.__serialize__(b, value.bound)
            b.__assign__("_b_tmp_")
            c.otherwise()
            b = to.uint(0, 1)
            b = base1.__serialize__(b, value.bound)
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
        base1 = cls.__base1__
        base2 = cls.__base2__
        if inplace:
            i = from_.uint_(1)
        else:
            i = from_.uint(1)
        m = Either()
        m.which = i
        m.which.__assign__(f"{name}_which")
        with Cond() as c:
            c.match(i)
            d = base2.__deserialize__(from_, name=name, inplace=inplace)
            m.bound = d
            c.otherwise()
            d = base1.__deserialize__(from_, name=name, inplace=inplace)
            m.bound = d
        return m

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
        lazy: bool = True,
        **kwargs,
    ):
        base1 = cls.__base1__
        base2 = cls.__base2__
        base1.__predefine__(name=name)
        base2.__predefine__(name=name)

    @classmethod
    def __build_type__(cls, items):
        base1, base2 = items
        return type(
            "Either_%s_%s" % (base1.__name__, base2.__name__),
            (cls,),
            {
                "__base1__": base1,
                "__base2__": base2,
            },
        )
