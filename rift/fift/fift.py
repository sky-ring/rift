import base64
import json
import re
import zlib
from ctypes import CDLL, c_char_p, c_int, c_void_p

from rift.fift.bundled_libs import FIFT_LIBS
from rift.fift.types.factory import Factory
from rift.fift.types.util import create_entry
from rift.fift.utils import calc_method_id
from rift.native import NativeLib, native_call
from rift.runtime.riftlib import RiftLibSetup


class FiftError(RuntimeError):
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)


class Fift(metaclass=NativeLib):
    _global_instance: "Fift" = None

    def __init__(
        self,
        lib_path: str | None = None,
        fift_libs: str | None = None,
        load_fift=True,
        load_utils=False,
    ):
        if not lib_path:
            lib_path = RiftLibSetup.acquire_lib(ensure=True)
        if not fift_libs:
            fift_libs = "<none>"
        self._lib = CDLL(lib_path, winmode=0x8)
        self._fift_pointer = self._fift_init(fift_libs.encode("utf-8"))
        if fift_libs == "<none>":
            self._load_internal_libs(load_fift, load_utils)

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

    @native_call("func_compile")
    def _func_compile(config_: c_char_p, len_: c_int) -> c_char_p:
        pass

    @native_call("vm_exec")
    def _tvm_exec(len_: c_int, data_: c_char_p) -> c_char_p:
        pass

    def _load_internal_libs(self, load_fift, load_utils):
        if not (load_fift or load_utils):
            return
        libs = {}
        utils = {**FIFT_LIBS}
        utils.pop("Fift")
        utils.pop("GetOpt")
        utils.pop("Lisp")
        if load_fift:
            libs = {"Fift": FIFT_LIBS["Fift"], **libs}
        if load_utils:
            libs = {**libs, "Lists": FIFT_LIBS["Lists"], **utils}
        for _lib, code in libs.items():
            zc = base64.b64decode(code)
            c = zlib.decompress(zc).decode("utf-8")
            self.eval(c, [])

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
        fift_o = json.loads(out.decode("utf-8"), strict=False)
        status = fift_o["status"]
        if status != "ok":
            raise FiftError(fift_o["message"])
        stack_o = fift_o["stack"]
        return [Factory.load(t["type"], t["value"]) for t in stack_o]

    @classmethod
    def _init(cls):
        if not cls._global_instance:
            cls._global_instance = Fift(load_utils=True)

    @classmethod
    def exec(cls, code: str, *args):
        cls._init()
        return cls._global_instance.eval(code, list(args))

    @classmethod
    def assemble(cls, program: str, fix_main=True, patch_methods=False):
        if fix_main and "DECLPROC recv_internal" not in program:
            idx = program.find("}END>c")
            main_method = (
                "DECLPROC recv_internal\nrecv_internal PROC:<{\n}>\n"
            )
            program = program[:idx] + main_method + program[idx:]
        if patch_methods:
            # NOTE: What we do here is to make the procedures
            # Use custom id - crc16 version
            # So we can call them by known id
            defined_names = [
                "recv_internal",
                "main",
                "recv_external",
                "run_ticktock",
                "split_prepare",
                "split_install",
            ]
            pattern = r"DECLPROC (.*?)\n"
            r = re.findall(pattern, program)
            r = [proc.strip() for proc in r]
            r = list(filter(lambda x: x not in defined_names, r))
            for proc in r:
                id_ = calc_method_id(proc)
                program = program.replace(
                    f"DECLPROC {proc}\n",
                    f"{id_} DECLMETHOD {proc}\n",
                )
        c = Fift.exec(program.strip())
        return c[0]

    @classmethod
    def tvm(cls, exec_config):
        cls._init()
        c = json.dumps(exec_config).encode("utf-8")
        out = cls._global_instance._tvm_exec(len(c), c)
        obj = json.loads(out.decode("utf-8"), strict=False)
        return obj

    @classmethod
    def func_compile(cls, exec_config):
        cls._init()
        c = json.dumps(exec_config).encode("utf-8")
        out = cls._global_instance._func_compile(c, len(c))
        obj = json.loads(out.decode("utf-8"), strict=False)
        return obj
