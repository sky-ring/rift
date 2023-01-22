from rift import *

from .util import compile


class SimpleWalletL2(Contract):
    """
    Simple Wallet Contract.

    # config
    get-methods:
        - seq_no
        - public_key
    """

    class Data(Model):
        seq_no: uint32
        public_key: uint256

    class ExternalBody(SignedPayload):
        seq_no: uint32
        valid_until: uint32

    data: Data

    def external_receive(self) -> None:
        msg = self.body % self.ExternalBody
        assert msg.valid_until > std.now(), 35
        assert msg.seq_no == self.data.seq_no, 33
        assert msg.verify_signature(self.data.public_key), 34
        std.accept_message()
        while msg.refs():
            mode = msg >> uint8
            std.send_raw_message(msg >> Ref[Cell], mode)
        self.data.seq_no += 1
        self.data.save()


def test_compile():
    compile(SimpleWalletL2)
