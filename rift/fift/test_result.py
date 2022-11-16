from enum import Enum

from rift.fift.tvm import ExecutionError, TVMError, TVMResult


class TestError(Exception):
    def __init__(self, *args) -> None:
        self.args = args
        super().__init__(*args)


class State(Enum):
    Ok = 1
    VMError = 2
    ExError = 3


class TestResult:
    state: State
    result: TVMResult
    vm_error: TVMError
    exec_error: ExecutionError

    def __init__(self, res: TVMError | TVMResult | ExecutionError) -> None:
        if isinstance(res, TVMResult):
            # Here we alter the data to new state
            # TODO: It's better to process actions and alter the code too
            self.state = State.Ok
            self.result = res
        elif isinstance(res, TVMError):
            self.state = State.VMError
            self.vm_error = res
        elif isinstance(res, ExecutionError):
            self.state = State.ExError
            self.exec_error = res

    def expect_ok(self) -> TVMResult:
        if self.state != State.Ok:
            raise TestError("Expected successful exit but got error!")
        return self.result

    def is_ok(self) -> bool:
        return self.state == State.Ok

    def is_error(self) -> bool:
        return self.state != State.Ok

    def expect_exit(self, exit_code: int):
        if (
            self.state == State.VMError
            and self.vm_error.exit_code == exit_code
        ):
            return
        if self.state == State.VMError:
            raise TestError(
                f"Expected {exit_code} exit code but got {self.vm_error.exit_code} instead!"
            )
        else:
            raise TestError(
                f"Expected {exit_code} exit code but got unexpected error instead!"
            )

    def expect_error(self):
        if self.state == State.Ok:
            raise TestError(
                "Expected error but got successfull exit instead!"
            )
