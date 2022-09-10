from dbuilder import *

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
        signature: slice[512]
        seq_no: uint32
        valid_until: uint32

    data: Data

    def external_receive(
        ctx,
        in_msg: Slice,
    ) -> None:
        msg = ctx.ExternalBody(in_msg)
        assert msg.valid_until > std.now(), 35
        assert msg.seq_no == ctx.data.seq_no, 33
        assert std.check_signature(
            msg.hash(after="signature"),
            msg.signature,
            ctx.data.public_key,
        ), 34
        std.accept_message()
        while msg.refs():
            mode = msg >> uint8
            std.send_raw_message(msg >> Ref[Cell], mode)
        ctx.data.seq_no += 1
        ctx.data.save()


def test_compile():
    compile(SimpleWallet)
