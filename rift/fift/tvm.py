import base64
from random import randbytes
from time import time

from rift.fift.fift import Fift
from rift.fift.types.cell import Cell
from rift.fift.types.factory import Factory
from rift.fift.types.null import Null
from rift.fift.types.tuple import Tuple
from rift.fift.types.util import create_entry
from rift.fift.utils import calc_method_id
from rift.types.addr import MsgAddress

b64 = str


class C7Register:
    unixtime: int
    balance: int
    myself: MsgAddress
    randSeed: int
    actions: int
    messages_sent: int
    block_lt: int
    trans_lt: int
    global_config: Cell

    def __init__(self) -> None:
        self.unixtime = int(time())
        self.balance = 1000
        self.myself = MsgAddress.std(0, 1)
        self.rand_seed = int.from_bytes(randbytes(32), byteorder="big")
        self.actions = 0
        self.messages_sent = 0
        self.block_lt = self.unixtime
        self.trans_lt = self.unixtime
        self.global_config = Cell()

    def as_tuple(self) -> Tuple:
        t = Tuple()
        balance = Tuple()
        balance.append(self.balance)
        balance.append(Null())
        t.append(
            0x076EF1EA,
            self.actions,
            self.messages_sent,
            self.unixtime,
            self.block_lt,
            self.trans_lt,
            self.rand_seed,
            balance,
            self.myself,
            self.global_config,
        )
        return t


class TVMConfig:
    debug: bool = True
    code: b64 = ""
    data: b64 = ""
    selector: int = 0
    stack: list | None = None
    c7: C7Register

    def __init__(self, c7=None) -> None:
        if c7 is None:
            c7 = C7Register()
        self.c7 = c7

    def __entry__(self) -> dict:
        t = Tuple()
        t.append(self.c7.as_tuple())
        return {
            "debug": self.debug,
            "code": self.code,
            "data": self.data,
            "function_selector": self.selector,
            "init_stack": [create_entry(i) for i in self.stack],
            "c7_register": t.__stack_entry__(),
        }


class TVMResult:
    data: Cell
    actions: Cell
    logs: str
    gas: int
    stack: list


class TVMError:
    exit_code: int
    logs: str


class ExecutionError:
    error: str


class TVM:
    @classmethod
    def exec(cls, config: TVMConfig):
        result = Fift.tvm(config.__entry__())
        if result["ok"]:
            res = TVMResult()
            res.data = Factory.load("cell", result["data_cell"])
            res.actions = Factory.load("cell", result["action_list_cell"])
            res.logs = base64.b64decode(result["logs"]).decode("utf-8")
            res.gas = result["gas_consumed"]
            res.stack = [
                Factory.load(r["type"], r.get("value", None))
                for r in result["stack"]
            ]
            return res
        else:
            if "exit_code" in result:
                # This is a TVM Error
                error = TVMError()
                error.exit_code = result["exit_code"]
                error.logs = base64.b64decode(result["logs"]).decode("utf-8")
                return error
            elif "error" in result:
                # This is an execution error
                error = ExecutionError()
                error.error = result["error"]
                return error
            else:
                # Unknown error
                raise RuntimeError("Unexpected result: ", result)

    @classmethod
    def get_method(cls, code: str, data: str, method: str | int, *stack):
        config = TVMConfig()
        config.code = code
        config.data = data
        if isinstance(method, str):
            method = calc_method_id(method)
        config.selector = method
        config.stack = list(stack)
        return cls.exec(config)
