from rift.fift.types.cell import Cell
from rift.func.contract import Contract
from rift.network.network import Network
from rift.runtime.keystore import KeyStore
from rift.types.msg import ExternalMessage, MessageFlag, MessageMode


class WalletBase(Contract):
    __interface__ = True
    __code_cell__: Cell = None

    def __init__(self, network: Network, **kwargs) -> None:
        self.network = network

    def pub_key(self) -> int:
        pass

    def seq_no(self) -> int:
        pass

    def create_body(
        self,
        message: Cell,
        valid_until: int,
        mode: int = MessageFlag.FLAG_IGNORE_ACTION_ERR
        + MessageMode.CARRY_REM_VALUE,
        forced_seq_no: int = None,
    ) -> Cell:
        pass

    def calculate_address(self):
        initial = self.initial_data()
        addr = self.address(initial, pretty=True, return_state=False)
        return addr

    def connect(self):
        addr = self.calculate_address()
        return super().connect(
            self.network,
            addr,
            use_code=False,
            use_data=True,
        )

    def send_message(
        self,
        message: Cell,
        valid_until: int,
        mode: int = MessageFlag.FLAG_IGNORE_ACTION_ERR
        + MessageMode.CARRY_REM_VALUE,
    ):
        bd = self.create_body(message, valid_until, mode)
        packed = KeyStore.sign_pack(bd)
        addr = self.calculate_address()
        msg = ExternalMessage.build(
            addr,
            body=packed,
        ).as_cell()
        return self.network.send_boc(bytes(msg))

    def initial_data(cls, **kwargs) -> Cell:
        pass

    def deploy_wallet(self):
        initial = self.initial_data()
        bd = self.create_body(None, -1, 64, forced_seq_no=0)
        bd = KeyStore.sign_pack(bd)
        msg, addr = self.deploy(
            initial,
            body=bd,
            amount=0,
            independent=True,
        )
        return self.network.send_boc(bytes(msg))
