from dbuilder.func.contract import Contract
from dbuilder.library.std import std
from dbuilder.types import Cell, Slice
from dbuilder.types.addr import MsgAddress
from dbuilder.types.bool import Bool
from dbuilder.types.coin import Coin
from dbuilder.types.constructor import Constructor
from dbuilder.types.either import Either
from dbuilder.types.maybe import Maybe
from dbuilder.types.model import Model
from dbuilder.types.payload import Payload
from dbuilder.types.ref import Ref
from dbuilder.types.sized_int import SizedInt
from dbuilder.types.types import Dict

from .util import compile


class TickTock(Payload):
    tick: Bool
    tock: Bool


class SimpleLib(Payload):
    public: Bool
    root: Ref(Cell)
    pass


class StateInit(Payload):
    split_depth: Maybe(SizedInt(5))
    special: Maybe(TickTock)
    code: Maybe(Ref(Cell))
    data: Maybe(Ref(Cell))
    library: Dict
    pass


class CurrencyCollection(Payload):
    pass


class InternalMsgInfo(Payload):
    __tag__ = "$0"
    ihr_disabled: Bool
    bounce: Bool
    bounced: Bool
    src: MsgAddress
    dest: MsgAddress
    value: CurrencyCollection
    ihr_fee: Coin
    fwd_fee: Coin
    created_lt: SizedInt(64)
    created_at: SizedInt(32)


class InboundExtMsgInfo(Payload):
    __tag__ = "$10"
    src: MsgAddress
    dest: MsgAddress
    import_fee: Coin


class OutboundExtMsgInfo(Payload):
    __tag__ = "$11"
    src: MsgAddress
    dest: MsgAddress
    created_lt: SizedInt(64)
    created_at: SizedInt(32)


CommonMsgInfo = Constructor(InternalMsgInfo, InboundExtMsgInfo)


class Message(Payload):
    info: CommonMsgInfo
    init: Maybe(Either(StateInit, Ref(StateInit)))
    # TODO: body: X


class SimpleMsg(Contract):
    """Simple Msg Sender Contract."""

    class Data(Model):
        class KeyPair(Payload):
            pub: SizedInt(32)
            priv: SizedInt(32)

        seq_no: SizedInt(32)
        public_key: SizedInt(256)
        ref: Ref(Cell)
        key: Ref(KeyPair)
        maybe_cell: Maybe(Ref(Cell))
        maybe_key: Maybe(KeyPair)
        some_either: Either(KeyPair, Ref(KeyPair))

    data: Data

    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        payload = Message(in_msg)
        payload.load()


def test_compile():
    compile(SimpleMsg)
