from rift import *
from rift.fift.tvm import TVM, TVMError, TVMResult
from rift.network.network import Network
from rift.runtime.config import Config, Mode
from rift.runtime.keystore import KeyStore

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

    def external_receive(self) -> None:
        msg = self.body % self.ExternalBody
        assert msg.valid_until > std.now(), 35
        assert msg.seq_no == self.data.seq_no, 33
        assert std.check_signature(
            msg.hash(after="signature"),
            msg.signature,
            self.data.public_key,
        ), 34
        std.accept_message()
        while msg.refs():
            mode = msg >> uint8
            std.send_raw_message(msg >> Ref[Cell], mode)
        self.data.seq_no += 1
        self.data.save()


def test_compile():
    compile(SimpleWallet)


def test_get_methods():
    cell = compile(SimpleWallet)
    Config.mode = Mode.FIFT
    d = SimpleWallet.Data()
    d.seq_no = 1
    d.public_key = 0
    d = d.as_cell()
    r = TVM.get_method(cell.value, d.value, "get_seq_no")
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
    (seq_no,) = r.stack
    assert seq_no == 1


def test_deploy():
    compile(SimpleWallet)

    d = SimpleWallet.Data()
    d.seq_no = 0
    d.public_key = KeyStore.public_key()

    body = Builder()
    body = body.uint(0, 32)
    body = body.sint(-1, 32)
    body = body.end()
    body_signed = KeyStore.sign_pack(body)
    body_ref = body_signed.as_ref()

    msg, address = SimpleWallet.deploy(
        d, body=body_ref, amount=0, independent=True,
    )
    print("Contract Address:", MsgAddress.human_readable(address))
    r = msg.send(testnet=True)
    print(r)
