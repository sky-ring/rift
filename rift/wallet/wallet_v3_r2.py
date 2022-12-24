from rift.fift.types.builder import Builder
from rift.fift.types.cell import Cell
from rift.network.network import Network
from rift.runtime.keystore import KeyStore
from rift.types.int_aliases import uint32, uint256
from rift.types.model import Model
from rift.wallet.wallet_base import WalletBase


class WalletV3R2(WalletBase):
    __code_cell__: Cell = Cell(
        __value__="te6cckEBAQEAcQAA3v8AIN0gggFMl7ohggEznLqxn3Gw7UTQ0x/THzHXC//jBOCk8mCDCNcYINMf0x/TH/gjE7vyY+1E0NMf0x/T/9FRMrryoVFEuvKiBPkBVBBV+RDyo/gAkyDXSpbTB9QC+wDo0QGkyMsfyx/L/8ntVBC9ba0=",
    )

    class Data(Model):
        seq_no: uint32
        subwallet: uint32
        pub_key: uint256

    def __init__(self, network: Network, subwallet=0, **kwargs) -> None:
        super().__init__(network, **kwargs)
        self.subwallet = subwallet

    def pub_key(self) -> int:
        return self.data.pub_key

    def seq_no(self) -> int:
        return self.data.seq_no

    def initial_data(self, **kwargs) -> Cell:
        return self.Data(
            seq_no=0,
            subwallet=self.subwallet,
            pub_key=KeyStore.public_key(),
        ).as_cell()

    def create_body(
        self,
        message: Cell,
        valid_until: int = -1,
        mode: int = 64,
        forced_seq_no: int = None,
    ) -> Cell:
        b = Builder()
        b = b.uint(self.subwallet, 32)
        if valid_until == -1:
            b = b.sint(-1, 32)
        else:
            b = b.uint(valid_until, 32)
        seq = forced_seq_no if forced_seq_no is not None else self.seq_no()
        b = b.uint(seq, 32)
        b = b.uint(mode, 8)
        if message:
            b = b.ref(message)
        return b.end()
