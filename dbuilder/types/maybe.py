from typing import TYPE_CHECKING

from dbuilder.core import Entity
from dbuilder.core.condition import Cond
from dbuilder.library.std import std
from dbuilder.types.bases.entity_base import _EntityBase
from dbuilder.types.types import Builder, Cell, Slice

if TYPE_CHECKING:
    from dbuilder.types.payload import Payload


class MaybeType(_EntityBase):
    has: Entity
    bound: Entity

    def __getattr__(self, item):
        return getattr(self.bound, item)

    @classmethod
    def __serialize__(cls, to: "Builder", value: "MaybeType") -> "Builder":
        base = cls.__basex__
        to.__assign__("_b_tmp_")
        with Cond() as c:
            c.match(value.has)
            b = to.uint(1)
            b = base.__serialize__(b, value.bound)
            b.__assign__("_b_tmp_")
            c.otherwise()
            b = to.uint(0)
            b.__assign__("_b_tmp_")
        return b

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
    ):
        base = cls.__basex__
        if inplace:
            i = from_.uint_(1)
        else:
            i = from_.uint(1)
        m = MaybeType()
        m.has = i
        m.has.__assign__(f"{name}_has")
        base.__predefine__(name=name)
        with Cond() as c:
            c.match(i)
            d = base.__deserialize__(from_, name=name, inplace=inplace)
            m.bound = d
        return m

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
    ):
        return

    @classmethod
    def type_name(cls) -> str:
        base = cls.__basex__
        return base.type_name()


class _MaybeTypeBuilder(type):
    def __new__(cls, base_cls=Cell):
        return super().__new__(
            cls,
            "Maybe_%s" % (base_cls.__name__,),
            (MaybeType,),
            {
                "__basex__": base_cls,
            },
        )


def Maybe(base: type = Cell):
    return _MaybeTypeBuilder.__new__(_MaybeTypeBuilder, base_cls=base)
