from rift import *
from rift.fift.tvm import TVM, TVMError, TVMResult
from rift.network.error import NetworkError
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

    KeyStore.override(
        "7a00324def8cdae8f70772914146de82f78e4dbe36bc49e4b289f9402d6e058a"
    )

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
        d,
        body=body_ref,
        amount=0,
        independent=True,
    )
    print("Contract Address:", MsgAddress.human_readable(address))
    # What we're trying to do here is to redeploy an existing wallet on the network
    # We expect it to throw error due to seq_no mismatch (33)
    # If you change the private key, this test will fail if the account doesn't have enough balance
    # Rerunning the test with charged wallet will result in successful execution
    try:
        r = msg.send(testnet=True)
        print("Deploy successful, message is accepted:")
        print(r)
    except NetworkError as ne:
        if "terminating vm with exit code 33" in ne.error:
            print("Redeploy case is covered!")
        elif "Failed to unpack account state" in ne.error:
            print(
                "No Funds case covered, account is null, try to charge the address with Test TON Giver and Retry!"
            )
        else:
            # Unexpected Case!!
            raise ne
