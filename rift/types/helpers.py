from rift.ast import CallStacks
from rift.core.condition import Cond
from rift.core.entity import mark
from rift.core.factory import Factory
from rift.core.loop import While
from rift.library.std import std


def hex_int(val):
    return Factory.build("HexInt", int(val, base=16))


def simple_int(val):
    return Factory.build("Int", int(val))


def ret_(*t):
    mark(*t)
    if len(t) == 0:
        CallStacks.return_(None)
        return
    return CallStacks.return_(*t)


def factory_(type_, value):
    n_map = {"int": "Int"}
    name = n_map[type_]
    return Factory.build(name, value)


def _cond():
    return Cond()


def _while(cond):
    return While(cond)


def _throw(what):
    return std.throw(what)


def _m_assign(tmp, names, values):
    if hasattr(tmp, "__magic__") and tmp.__magic__ == 0x050794:
        tmp.__massign__(names, values)
    elif isinstance(tmp, tuple):
        for n, v in zip(names, values):
            v.__assign__(n)


def throw_unless(e, c):
    return std.throw_unless(e, c)
