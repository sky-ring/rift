from typing import TYPE_CHECKING

from dbuilder.core import Entity
from dbuilder.types.bases.entity_base import _EntityBase
from dbuilder.types.types import Builder, Cell, Slice

if TYPE_CHECKING:
    from dbuilder.types.payload import Payload


    bound: "Entity"

    def __init__(self, bound) -> None:
        self.bound = bound

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if isinstance(value, Ref):
            value = value.bound
            if isinstance(value, Entity):
                b = to.ref(value)
            elif hasattr(value, "__magic__") and value.__magic__ == 0xA935E5:
                p: "Payload" = value
                c = p.as_cell()
                b = to.ref(c)
            return b
        base = cls.__basex__
        if base == Cell:
            b = to.ref(value)
        elif hasattr(base, "__magic__") and base.__magic__ == 0xA935E5:
            p: "Payload" = value
            c = p.as_cell()
            b = to.ref(c)
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
            v = from_.ref_()
        else:
            v = from_.ref()
        if base == Cell:
            if name is not None:
                v.__assign__(name)
        if hasattr(base, "__magic__") and base.__magic__ == 0xA935E5:
            v = v.parse()
            p: "Payload" = base(v, name=name)
            p.load()
            v = p
        return v

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
        lazy: bool = True,
        **kwargs,
    ):
        if name is None:
            return
        base = cls.__basex__
        if base == Cell:
            Cell.__predefine__(name)
        elif hasattr(base, "__magic__") and base.__magic__ == 0xA935E5:
            base.__predefine__(name)

    @classmethod
    def type_name(cls) -> str:
        base = cls.__basex__
        return base.type_name()


class _RefTypeBuilder(type):
    def __new__(cls, base_cls=Cell):
        return super().__new__(
            cls,
            "Ref_%s" % (base_cls.__name__,),
            (RefType,),
            {
                "__basex__": base_cls,
            },
        )


def Ref(base: type = Cell):
    return _RefTypeBuilder.__new__(_RefTypeBuilder, base_cls=base)
