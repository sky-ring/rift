from dbuilder.func.contract import Contract
from dbuilder.library.std import std
from dbuilder.types import Slice
from dbuilder.types.int_aliases import uint32, uint256
from dbuilder.types.model import Model
from dbuilder.types.payload import Payload
from dbuilder.types.slice import slice

from .util import compile


class SimpleWallet(Contract):
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

    class ExternalBody(Payload):
        signature: slice(512)
        seq_no: uint32
        valid_until: uint32

    data: Data

    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        self.data.load()
        msg = self.ExternalBody(in_msg)
        msg.load()
        assert msg.valid_until > std.now(), 35
        assert msg.seq_no == self.data.seq_no, 33
        assert std.check_signature(
            msg.hash(after="signature"),
            msg.signature,
            self.data.public_key,
        ), 34
        std.accept_message()
        with msg.iter_refs():
            mode = msg.uint_(8)
            std.send_raw_message(msg.ref(), mode)
        self.data.seq_no = self.data.seq_no + 1
        self.data.save()


def test_compile():
    compile(SimpleWallet)
