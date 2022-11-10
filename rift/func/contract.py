from rift.core.annots import impure, method
from rift.core.invokable import InvokableFunc
from rift.func.meta_contract import ContractMeta
from rift.func.types.types import Cell, Slice
from rift.types.bases.cell import Cell as GeneralCell
from rift.types.model import Model
from rift.types.msg import (
    ExternalMessage,
    InternalMessage,
    MsgAddress,
    StateInit,
)
from rift.types.payload import Payload


class Contract(metaclass=ContractMeta):
    NOT_IMPLEMENTED = 0x91AC43

    def __init__(self):
        pass

    @impure
    @method()
    def recv_internal(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        self.balance = balance
        self.in_value = msg_value
        self.message = InternalMessage(in_msg_full.parse())
        self.body = in_msg_body
        return self.internal_receive()

    @impure
    @method()
    def recv_external(
        self,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        self.body = in_msg_body
        self.message = ExternalMessage(in_msg_full.parse())
        return self.external_receive()

    def internal_receive(
        self,
    ) -> None:
        return self.NOT_IMPLEMENTED

    def external_receive(
        self,
    ) -> None:
        return self.NOT_IMPLEMENTED

    def __getattr__(self, item):
        return InvokableFunc(item)

    @classmethod
    def deploy(
        cls,
        data: GeneralCell | Model | Payload,
        code: GeneralCell | str = None,
        body: GeneralCell = None,
        amount=10**7,
        independent: bool = False,
        ref_state=True,
    ) -> GeneralCell:
        if isinstance(data, Model) or isinstance(data, Payload):
            data = data.as_cell()
        if code is None:
            code = cls.__code_cell__
        s = StateInit(
            split_depth=None,
            special=None,
            code=code,
            data=data,
            library=None,
        )
        s = s.as_cell()
        s_hash = s.hash()
        if ref_state:
            s = s.as_ref()
        if body is None:
            body = GeneralCell()
        address = MsgAddress.std(0, s_hash)
        if not independent:
            msg = InternalMessage.build(
                address,
                state_init=s,
                body=body,
                amount=amount,
            )
        else:
            msg = ExternalMessage.build(
                address,
                state_init=s,
                body=body,
            )
        return msg.as_cell(), address

    @classmethod
    def compile(cls):

        pass
