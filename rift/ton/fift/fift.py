import json
from ctypes import CDLL, c_char_p, c_int, c_void_p

import rift.ton.fift.types
from rift.native import NativeLib, native_call
from rift.ton.fift.types.factory import Factory
from rift.ton.fift.types.util import create_entry


class Fift(metaclass=NativeLib):
    def __init__(self, lib_path: str, fift_libs: str):
        self._lib = CDLL(lib_path, winmode=0x8)
        self._fift_pointer = self._fift_init(fift_libs.encode("utf-8"))

    @native_call("fift_init")
    def _fift_init(lib_path: c_char_p) -> c_void_p:
        pass

    @native_call("fift_eval")
    def _fift_eval(
        fift_p: c_void_p,
        script: c_char_p,
        current_dir: c_char_p,
        initial_stack: c_char_p,
        initial_len: c_int,
    ) -> c_char_p:
        pass

    def eval(self, code: str, stack: list | None = None):
        if stack is None:
            stack = []
        stack_j = list(map(create_entry, stack))
        fift_config = {
            "data": stack_j,
        }
        stack_s = json.dumps(fift_config).encode("utf-8")
        c_dir = ".".encode("utf-8")
        code = code.encode("utf-8")
        out = self._fift_eval(
            self._fift_pointer,
            code,
            c_dir,
            stack_s,
            len(stack_s),
        )
        stack_o = json.loads(out.decode("utf-8"))
        return [Factory.load(t["type"], t["value"]) for t in stack_o]
