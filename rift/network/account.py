from enum import Enum


class AccountState(Enum):
    EMPTY = 0
    UNINIT = 1
    ACTIVE = 2


class Account:
    state: AccountState
    balance: int
    code: str
    data: str
    addr: str

    def __init__(self, raw_data=None, addr="") -> None:
        if raw_data is not None:
            self._init_from_raw(raw_data)
        if addr != "":
            self.addr = addr

    def _init_from_raw(self, data):
        balance = int(data["balance"])
        code = data["code"]
        c_data = data["data"]
        if balance == -1:
            state = AccountState.EMPTY
        elif code == "" and c_data == "":
            state = AccountState.UNINIT
        else:
            state = AccountState.ACTIVE
        self.balance = balance
        self.code = code
        self.data = c_data
        self.state = state

    def __repr__(self) -> str:
        return (
            f"Account{{state = {self.state.name}, balance = {self.balance}}}"
        )
