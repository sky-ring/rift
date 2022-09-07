from dbuilder.core import Entity
from dbuilder.core.condition import Cond
from dbuilder.types.bases.entity_base import _EntityBase
from dbuilder.types.ref import Ref
from dbuilder.types.types import Builder, Cell, Slice


class EitherType(_EntityBase):
    which: Entity
    bound: Entity

    def __getattr__(self, item):
        return getattr(self.bound, item)

    @classmethod
    def __serialize__(cls, to: "Builder", value: "EitherType") -> "Builder":
        base1 = cls.__base1__
        base2 = cls.__base2__
        if value is None:
            b = to.uint(0, 1)
            return b
        if not isinstance(value, EitherType):
            if type(value) == base1:
                v = 0
            elif type(value) == base2:
                v = 1
            else:
                raise RuntimeError("Couldn't match either types")
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
        m = EitherType()
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


class _EitherTypeBuilder(type):
    def __new__(cls, base1: type = Cell, base2: type = None):
        if base2 is None:
            base2 = Ref[Cell]
        return super().__new__(
            cls,
            "Either_%s_%s" % (base1.__name__, base2.__name__),
            (EitherType,),
            {
                "__base1__": base1,
                "__base2__": base2,
            },
        )


def Either(base1: type = Cell, base2: type = None):
    return _EitherTypeBuilder.__new__(
        _EitherTypeBuilder,
        base1=base1,
        base2=base2,
    )
