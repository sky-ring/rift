from typing import TYPE_CHECKING

from dbuilder.core import Entity
from dbuilder.core.condition import Cond
from dbuilder.library.std import std
from dbuilder.types.bases.entity_base import _EntityBase
from dbuilder.types.ref import Ref
from dbuilder.types.types import Builder, Cell, Slice

if TYPE_CHECKING:
    from dbuilder.types.payload import Payload


class EitherType(_EntityBase):
    which: Entity
    bound: Entity

    def __getattr__(self, item):
        return getattr(self.bound, item)

    @classmethod
    def __serialize__(cls, to: "Builder", value: "EitherType") -> "Builder":
        base1 = cls.__base1__
        base2 = cls.__base2__
        to.__assign__("_b_tmp_")
        with Cond() as c:
            c.match(value.which)
            b = to.uint(1)
            b = base2.__serialize__(b, value.bound)
            b.__assign__("_b_tmp_")
            c.otherwise()
            b = to.uint(0)
            b = base1.__serialize__(b, value.bound)
            b.__assign__("_b_tmp_")
        return b

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
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
        base1.__predefine__(name=name)
        base2.__predefine__(name=name)
        with Cond() as c:
            c.match(i)
            d = base2.__deserialize__(from_, name=name, inplace=inplace)
            m.bound = d
            c.otherwise()
            d = base1.__deserialize__(from_, name=name, inplace=inplace)
            m.bound = d
        return m


class _EitherTypeBuilder(type):
    def __new__(cls, base1: type = Cell, base2: type = None):
        if base2 is None:
            base2 = Ref(Cell)
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
