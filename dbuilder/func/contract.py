from dbuilder.ast import CallStacks
from dbuilder.core.annots import impure, method
from dbuilder.core.entity import mark
from dbuilder.core.factory import Factory
from dbuilder.core.invokable import InvokableFunc
from dbuilder.func.meta_contract import ContractMeta
from dbuilder.types import Cell, Slice


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
