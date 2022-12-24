from functools import partial


def native_call(name=None):
    return partial(native_call_, name=name)


def native_call_(func, name=None):
    func.native_name = name
    func.is_native = True
    return func


def is_native(func):
    return hasattr(func, "is_native") and func.is_native
