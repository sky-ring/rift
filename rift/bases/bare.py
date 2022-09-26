from rift import *


class BaseContract(Contract):
    def internal_receive(self) -> None:
        super().internal_receive()

    def external_receive(self) -> None:
        super().external_receive()
