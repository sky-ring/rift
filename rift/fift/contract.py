import functools

from rift.fift.test_result import TestResult
from rift.fift.tvm import TVM
from rift.fift.types.cell import Cell


class ExecutableContract:
    def __init__(self, code: Cell, data: Cell) -> None:
        self.code = code
        self.data = data

    def _run_method(self, name: str, *args):
        known_names = {
            "recv_internal": 0,
            "main": 0,
            "recv_external": -1,
            "run_ticktock": -2,
            "split_prepare": -3,
            "split_install": -4,
        }
        if name in known_names:
            name = known_names[name]
        res = TVM.get_method(self.code.value, self.data.value, name, *args)
        res = TestResult(res)
        if res.is_ok():
            # Here we alter the data to new state
            # TODO: It's better to process actions and alter the code too
            self.data = res.result.data
        return res

    def __getattr__(self, name: str):
        f = functools.partial(ExecutableContract._run_method, self, name)
        return f

    @classmethod
    def create(
        cls,
        code: Cell,
        data: Cell,
        methods: list[str],
    ) -> "ExecutableContract":
        contract = ExecutableContract(code, data)
        for m in methods:
            f = functools.partial(ExecutableContract._run_method, contract, m)
            setattr(contract, m, f)
        return contract
