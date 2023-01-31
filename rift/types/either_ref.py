from rift.core import Entity
from rift.core.condition import Cond
from rift.library import std
from rift.logging import log_system
from rift.runtime.config import Config
from rift.types.bases import Builder, Cell, Slice
from rift.types.ref import Ref
from rift.types.utils import CachingSubscriptable
from rift.util.type_id import type_id


class EitherRef(metaclass=CachingSubscriptable):
    which: Entity
    bound: Entity

    def __getattr__(self, item):
        return getattr(self.bound, item)

    def __assign__(self, name):
        return self

    def is_ref(self):
        return self.which == 1

    @classmethod
    def __serialize__(cls, to: "Builder", value: "EitherRef") -> "Builder":
        base1 = cls.__base1__
        if value is None:
            b = to.uint(0, 1)
            return b
        if not isinstance(value, EitherRef):
            if type(value).__type_id__() == base1.__type_id__():
                v = 0
            elif type(value).__type_id__() == Ref[base1].__type_id__():
                v = 1
            elif type(value).__type_id__() == Cell.__type_id__():
                # NOTE: Is this a good approach?
                v = 0
            elif type(value).__type_id__() == Slice.__type_id__():
                # NOTE: Is this a good approach?
                v = 0
            elif type(value).__type_id__() == Ref[Cell].__type_id__():
                v = 1
            else:
                msg = "got {current} expected {e1} or {e2}"
                msg = msg.format(current=type(value), e1=base1, e2=Ref[base1])
                raise RuntimeError("Couldn't match either types; " + msg)
            to = to.uint(v, 1)
            return type(value).__serialize__(to, value)
        to.__assign__("_b_tmp_")
        with Cond() as c:
            c.match(value.which)
            b = to.uint(1, 1)
            nb = std.begin_cell()
            nb = base1.__serialize__(nb, value.bound)
            nc = nb.end()
            b = b.ref(nc)
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
        if inplace:
            i = from_.uint_(1)
        else:
            i = from_.uint(1)
        m = EitherRef()
        m.which = i
        if Config.mode.is_func():
            m.which.__assign__(f"{name}_which")
            Slice.__predefine__(f"{name}_slice")
            first_name = from_.name
            with Cond() as c:
                c.match(i)
                v = Ref[Cell].__deserialize__(from_)
                x = v.parse().__assign__(f"{name}_slice")
                c.otherwise()
                x = from_.__assign__(f"{name}_slice")
            d = base1.__deserialize__(
                x,
                name=name,
                inplace=inplace,
                lazy=lazy,
            )
            with Cond() as c:
                c.match(i == 0)
                x.__assign__(first_name)
            m.bound = d
        elif Config.mode.is_fift():
            log_system(
                "DE",
                "[{name}] loading either ref={ref} base={base} [{lazy}] from={frm}",
                name=name,
                lazy=lazy,
                ref=m.which != 0,
                base=base1.__name__,
                frm=from_._init_hash(),
            )
            if m.which == 0:
                n = from_
            else:
                n = from_.ref_().parse()
            d = base1.__deserialize__(
                n, name=name, inplace=inplace, lazy=lazy
            )
            return d
        return m

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
        lazy: bool = True,
        **kwargs,
    ):
        base1 = cls.__base1__
        base1.__predefine__(name=name)

    @classmethod
    def __build_type__(cls, item):
        base1 = item
        t = type(
            "EitherRef_%s" % (base1.__name__),
            (cls,),
            {
                "__base1__": base1,
            },
        )
        t.__type_id__ = type_id(t.__name__)
        return t
