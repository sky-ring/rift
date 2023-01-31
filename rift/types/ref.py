from typing import TYPE_CHECKING

from rift.core import Entity
from rift.fift.types._fift_base import _FiftBaseType
from rift.logging import log_system
from rift.runtime.config import Config
from rift.types.bases import Builder, Cell, Slice
from rift.types.utils import CachingSubscriptable
from rift.util.type_id import type_id

if TYPE_CHECKING:
    from rift.types.payload import Payload


class Ref(metaclass=CachingSubscriptable):
    bound: "Entity"

    def __init__(self, bound) -> None:
        self.bound = bound

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if isinstance(value, Ref):
            value = value.bound
            if isinstance(value, Entity) or isinstance(value, _FiftBaseType):
                b = to.ref(value)
            elif hasattr(value, "__magic__") and value.__magic__ == 0xA935E5:
                p: "Payload" = value
                c = p.as_cell()
                b = to.ref(c)
            return b
        base = cls.__basex__
        if value is None:
            # NOTE: Is this ideal behavior for a None ref ?! I think so
            return to
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
        if Config.mode.is_fift():
            log_system(
                "DE",
                "[{name}] loading ref=>{base} [{lazy}] from=>{frm}",
                name=name,
                lazy=lazy,
                base=base.__name__,
                frm=from_._init_hash(),
            )
        if inplace:
            v = from_.ref_()
        else:
            v = from_.ref()
        if base == Cell:
            if name is not None:
                v.__assign__(name)
        if hasattr(base, "__magic__") and base.__magic__ == 0xA935E5:
            v = v.parse()
            v = base.__deserialize__(v, name=name, lazy=lazy)
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

    @classmethod
    def __build_type__(cls, item):
        t = type(
            "Ref_%s" % item.__name__,
            (cls,),
            {
                "__basex__": item,
            },
        )
        t.__type_id__ = type_id(t.__name__)
        return t
