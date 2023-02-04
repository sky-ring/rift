from typing import Type, TypeVar

from rift.core.annots import impure, is_method, method
from rift.core.invokable import InvokableFunc
from rift.fift.contract import ExecutableContract
from rift.fift.types.cell import Cell as FiftCell
from rift.func.meta_contract import ContractMeta
from rift.func.types.types import Cell, Slice
from rift.func.util import cls_attrs
from rift.network.network import Network
from rift.types.bases.cell import Cell as GeneralCell
from rift.types.model import Model
from rift.types.msg import (
    ExternalMessage,
    InternalMessage,
    MsgAddress,
    StateInit,
)
from rift.types.payload import Payload

T = TypeVar("T", bound="Contract")


class Contract(metaclass=ContractMeta):
    __fc_code__ = None
    __interface__ = False
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

    def connect(
        self,
        network: Network,
        addr: str,
        use_code=False,
        use_data=True,
    ):
        self._addr = addr
        acc = network.get_account(self._addr)
        if acc.state != acc.state.ACTIVE:
            return False, acc
        if use_data:
            d_slice = FiftCell(__value__=acc.data).parse()
            if hasattr(type(self), "Data"):
                Data = type(self).Data
                self.data = Data.from_slice(d_slice)
            else:
                self.data = d_slice
        if use_code:
            self.__code_cell__ = FiftCell(__value__=acc.code)
        return True, acc

    @classmethod
    def address(
        cls,
        data: GeneralCell | Model | Payload,
        code: GeneralCell = None,
        pretty=False,
        return_state=False,
    ) -> Slice | str | tuple[Slice | str, GeneralCell]:
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
        address = MsgAddress.std(0, s_hash)
        if pretty:
            address = MsgAddress.human_readable(address)
        if return_state:
            return address, s
        return address

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
        address, s = cls.address(data, code, pretty=False, return_state=True)
        if ref_state:
            s = s.as_ref()
        if body is None:
            body = GeneralCell()
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
    def code(cls) -> Cell:
        return cls.__code_cell__

    @classmethod
    def instantiate(cls: Type[T], data: Cell) -> T:
        attrs = cls_attrs(cls)
        methods = list(filter(lambda x: is_method(x[1]), attrs.items()))
        methods = [x[0] for x in methods]
        return ExecutableContract.create(cls.code(), data, methods)
