from dbuilder import method
from dbuilder.core.invokable import InvokableFunc
from dbuilder.types import Cell, Slice


class Contract:
    def __init__(self):
        pass

    @method
    def recv_internal(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        self.internal_receive(balance, msg_value, in_msg_full, in_msg_body)

    @method
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
