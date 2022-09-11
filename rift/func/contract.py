from rift.ast import CallStacks
from rift.core.annots import impure, method
from rift.core.condition import Cond
from rift.core.entity import mark
from rift.core.factory import Factory
from rift.core.invokable import InvokableFunc
from rift.core.loop import While
from rift.func.meta_contract import ContractMeta
from rift.types.types import Cell, Slice


class Contract(metaclass=ContractMeta):
    def __init__(self):
        pass

    @impure
    @method()
    def recv_internal(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        self.internal_receive(balance, msg_value, in_msg_full, in_msg_body)

    @impure
    @method()
    def recv_external(
        self,
        in_msg_body: Slice,
    ) -> None:
        self.external_receive(in_msg_body)

    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        pass

    def external_receive(
        self,
        in_msg_body: Slice,
    ) -> None:
        pass

    def __getattr__(self, item):
        return InvokableFunc(item)

    def ret_(self, *t):
        mark(*t)
        if len(t) == 0:
            CallStacks.return_(None)
            return
        return CallStacks.return_(*t)

    def factory_(self, type_, value):
        n_map = {"int": "Int"}
        name = n_map[type_]
        return Factory.build(name, value)

    def _cond(self):
        return Cond()

    def _while(self, cond):
        return While(cond)

    def _throw(self, what):
        return self.throw(what)

    def _m_assign(self, tmp, names, values):
        if hasattr(tmp, "__magic__") and tmp.__magic__ == 0x050794:
            tmp.__massign__(names, values)
        elif isinstance(tmp, tuple):
            for n, v in zip(names, values):
                v.__assign__(n)
