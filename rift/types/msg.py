from copy import deepcopy

from rift.types.addr import MsgAddress
from rift.types.bool import Bool
from rift.types.coin import Coin
from rift.types.either import Either
from rift.types.int_aliases import uint5, uint32, uint64
from rift.types.maybe import Maybe
from rift.types.payload import Payload
from rift.types.ref import Ref
from rift.types.types import Cell, Dict


class TickTock(Payload):
    tick: Bool
    tock: Bool


class SimpleLib(Payload):
    public: Bool
    root: Ref[Cell]
    pass


class StateInit(Payload):
    split_depth: Maybe[uint5]
    special: Maybe[TickTock]
    code: Maybe[Ref[Cell]]
    data: Maybe[Ref[Cell]]
    library: Dict
    pass


class CurrencyCollection(Payload):
    amount: Coin
    other: Dict


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
    created_lt: uint64
    created_at: uint32

    @classmethod
    def build(
        cls,
        dest: MsgAddress,
        ihr_disabled: Bool = True,
        bounce: Bool = True,
        bounced: Bool = False,
        src: MsgAddress = MsgAddress.Empty,
        amount: Coin = 0,
        extra_currency: Dict = None,
        ihr_fee: Coin = 0,
        fwd_fee: Coin = 0,
        created_lt: uint64 = 0,
        created_at: uint32 = 0,
    ) -> "InternalMsgInfo":
        info = InternalMsgInfo()
        info.dest = dest
        info.ihr_disabled = ihr_disabled
        info.bounce = bounce
        info.bounced = bounced
        info.src = src
        info.value = CurrencyCollection()
        info.value.amount = amount
        info.value.other = extra_currency
        info.ihr_fee = ihr_fee
        info.fwd_fee = fwd_fee
        info.created_lt = created_lt
        info.created_at = created_at
        return info


class InboundExtMsgInfo(Payload):
    __tag__ = "$10"
    src: MsgAddress
    dest: MsgAddress
    import_fee: Coin


class InternalMessage(Payload):
    info: InternalMsgInfo
    init: Maybe[Either[StateInit, Ref[StateInit]]]
    body: Either[Cell, Ref[Cell]]

    @classmethod
    def __build_type__(cls, item):
        n_cls = deepcopy(cls)
        n_cls.__annotations__["body"] = Either[item, Ref[item]]
        return n_cls

    @classmethod
    def build(
        cls,
        dest: MsgAddress,
        state_init: Maybe[Either[StateInit, Ref[StateInit]]] = None,
        body: Either[Cell, Ref[Cell]] = None,
        ihr_disabled: Bool = 1,
        bounce: Bool = 1,
        bounced: Bool = 0,
        src: MsgAddress = MsgAddress.Empty,
        amount: Coin = 0,
        extra_currency: Dict = None,
        ihr_fee: Coin = 0,
        fwd_fee: Coin = 0,
        created_lt: uint64 = 0,
        created_at: uint32 = 0,
    ) -> "InternalMessage":
        msg = InternalMessage()
        msg.info = InternalMsgInfo.build(
            dest=dest,
            ihr_disabled=ihr_disabled,
            bounce=bounce,
            bounced=bounced,
            src=src,
            amount=amount,
            extra_currency=extra_currency,
            ihr_fee=ihr_fee,
            fwd_fee=fwd_fee,
            created_lt=created_lt,
            created_at=created_at,
        )
        msg.init = state_init
        msg.body = body
        return msg

    def send(self, mode: int = 0, flags: int = 0):
        c = self.as_cell()
        c.send_raw_message(mode + flags)
        pass


class MessageMode:
    ORDINARY = 0
    CARRY_REM_VALUE = 64
    CARRY_ALL_BALANCE = 128


class MessageFlag:
    FLAG_SEPERATE_FEE = 1
    FLAG_IGNORE_ACTION_ERR = 2
    FLAG_DESTROY_CONTRACT_ON_ZERO = 32
