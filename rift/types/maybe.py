from rift.core import Entity
from rift.core.condition import Cond
from rift.func.types.types import Int
from rift.logging import log_system
from rift.runtime.config import Config
from rift.types.bases import Builder, Slice
from rift.types.utils import CachingSubscriptable


class Maybe(metaclass=CachingSubscriptable):
    has: Entity
    bound: Entity
    name: str

    def __init__(self) -> None:
        pass

    def __getattr__(self, item):
        return getattr(self.bound, item)

    def __assign__(self, name):
        return self

    def is_present(self):
        return self.has == 1

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Maybe") -> "Builder":
        if value is None:
            b = to.uint(0, 1)
            return b
        base = cls.__basex__
        if not isinstance(value, Maybe):
            b = to.uint(1, 1)
            return base.__serialize__(b, value)
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
        m = cls()
        m.has = i
        if Config.mode.is_func():
            m.has.__assign__(f"{name}_has")
            base.__predefine__(name)
            with Cond() as c:
                c.match(i)
                d = base.__deserialize__(
                    from_,
                    name=name,
                    inplace=inplace,
                    lazy=lazy,
                )
                m.bound = d
        elif Config.mode.is_fift():
            if m.has == 1:
                log_system(
                    "DE",
                    "[{name}] loaded present maybe=>{base} [{lazy}]",
                    name=name,
                    lazy=lazy,
                    base=base.__name__,
                )
                d = base.__deserialize__(
                    from_,
                    name=name,
                    inplace=inplace,
                    lazy=lazy,
                )
                return d
            else:
                log_system(
                    "DE",
                    "[{name}] loaded empty maybe=>{base} [{lazy}]",
                    name=name,
                    lazy=lazy,
                    base=base.__name__,
                )
                return None
        return m

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
        lazy: bool = True,
        **kwargs,
    ):
        base = cls.__basex__
        Int.__predefine__(name=f"{name}_has")
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
