from rift.func.contract import Contract
from rift.types import Cell, Slice


class BaseContract(Contract):
    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        super().internal_receive(balance, msg_value, in_msg_full, in_msg_body)

    def external_receive(self, in_msg_body: Slice) -> None:
        super().external_receive(in_msg_body)
