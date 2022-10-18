from rift.native.c_annot import is_native


class NativeLib(type):
    def __new__(mcs, name, bases, attrs):
        for a, v in list(attrs.items()):
            if is_native(v):
                attrs[f"native_{v.native_name}"] = NativeLib._native_func(v)
                attrs[a] = NativeLib._native_caller(v.native_name)
        c = super().__new__(mcs, name, bases, attrs)
        return c

    @staticmethod
    def _native_func(def_f):
        name = def_f.native_name

        def _native_func_creator(self):
            a_n = f"cached_native_{name}"
            if hasattr(self, a_n):
                return getattr(self, a_n)
            f = getattr(self._lib, name)
            args = def_f.__code__.co_varnames
            annots = def_f.__annotations__
            types = [annots[x] for x in args]
            f.argtypes = list(types)
            f.restype = annots["return"]
            setattr(self, a_n, f)
            return f

        return _native_func_creator

    @staticmethod
    def _native_caller(name):
        def _native_call(self, *args):
            a_n = f"native_{name}"
            f = getattr(self, a_n)()
            r = f(*args)
            return r

        return _native_call
