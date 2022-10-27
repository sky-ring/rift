from rift.meta.meta_inheritance import mix_metas


def stub(fn):
    fn.__stub__ = True
    return fn


def is_stub(fn):
    return hasattr(fn, "__stub__") and fn.__stub__


class Behavioral_(type):
    @classmethod
    def create_new(mcs, type1, type2):
        name = f"Behavioral_{type1.__name__}_{type2.__name__}"
        bases = ()
        attrs = {
            "__meta__": {
                "types": [type1, type2],
            },
            "__is_active__": classmethod(Behavioral_.__is_active__),
            "__active_one__": classmethod(Behavioral_.__active_one__),
            "__init__": Behavioral_.__init_f__,
            "__getattr__": Behavioral_.__obj_get_attr__,
            "__getattribute__": Behavioral_.__obj_get_attribute__,
            "__repr__": Behavioral_.create_named_proxy("__repr__"),
            "__str__": Behavioral_.create_named_proxy("__str__"),
            "__bytes__": Behavioral_.create_named_proxy("__bytes__"),
            "__format__": Behavioral_.create_named_proxy("__format__"),
            "__lt__": Behavioral_.create_named_proxy("__lt__"),
            "__le__": Behavioral_.create_named_proxy("__le__"),
            "__eq__": Behavioral_.create_named_proxy("__eq__"),
            "__ne__": Behavioral_.create_named_proxy("__ne__"),
            "__gt__": Behavioral_.create_named_proxy("__gt__"),
            "__ge__": Behavioral_.create_named_proxy("__ge__"),
            "__hash__": Behavioral_.create_named_proxy("__hash__"),
            "__bool__": Behavioral_.create_named_proxy("__bool__"),
            # "__setattr__": Behavioral_.create_named_proxy("__setattr__"),
            # "__delattr__": Behavioral_.create_named_proxy("__delattr__"),
            "__add__": Behavioral_.create_named_proxy("__add__"),
            "__sub__": Behavioral_.create_named_proxy("__sub__"),
            "__mul__": Behavioral_.create_named_proxy("__mul__"),
            "__matmul__": Behavioral_.create_named_proxy("__matmul__"),
            "__truediv__": Behavioral_.create_named_proxy("__truediv__"),
            "__floordiv__": Behavioral_.create_named_proxy("__floordiv__"),
            "__mod__": Behavioral_.create_named_proxy("__mod__"),
            "__divmod__": Behavioral_.create_named_proxy("__divmod__"),
            "__pow__": Behavioral_.create_named_proxy("__pow__"),
            "__lshift__": Behavioral_.create_named_proxy("__lshift__"),
            "__rshift__": Behavioral_.create_named_proxy("__rshift__"),
            "__and__": Behavioral_.create_named_proxy("__and__"),
            "__xor__": Behavioral_.create_named_proxy("__xor__"),
            "__or__": Behavioral_.create_named_proxy("__or__"),
            "__radd__": Behavioral_.create_named_proxy("__radd__"),
            "__rsub__": Behavioral_.create_named_proxy("__rsub__"),
            "__rmul__": Behavioral_.create_named_proxy("__rmul__"),
            "__rmatmul__": Behavioral_.create_named_proxy("__rmatmul__"),
            "__rtruediv__": Behavioral_.create_named_proxy("__rtruediv__"),
            "__rfloordiv__": Behavioral_.create_named_proxy("__rfloordiv__"),
            "__rmod__": Behavioral_.create_named_proxy("__rmod__"),
            "__rdivmod__": Behavioral_.create_named_proxy("__rdivmod__"),
            "__rpow__": Behavioral_.create_named_proxy("__rpow__"),
            "__rlshift__": Behavioral_.create_named_proxy("__rlshift__"),
            "__rrshift__": Behavioral_.create_named_proxy("__rrshift__"),
            "__rand__": Behavioral_.create_named_proxy("__rand__"),
            "__rxor__": Behavioral_.create_named_proxy("__rxor__"),
            "__ror__": Behavioral_.create_named_proxy("__ror__"),
            "__iadd__": Behavioral_.create_named_proxy("__iadd__"),
            "__isub__": Behavioral_.create_named_proxy("__isub__"),
            "__imul__": Behavioral_.create_named_proxy("__imul__"),
            "__imatmul__": Behavioral_.create_named_proxy("__imatmul__"),
            "__itruediv__": Behavioral_.create_named_proxy("__itruediv__"),
            "__ifloordiv__": Behavioral_.create_named_proxy("__ifloordiv__"),
            "__imod__": Behavioral_.create_named_proxy("__imod__"),
            "__ipow__": Behavioral_.create_named_proxy("__ipow__"),
            "__ilshift__": Behavioral_.create_named_proxy("__ilshift__"),
            "__irshift__": Behavioral_.create_named_proxy("__irshift__"),
            "__iand__": Behavioral_.create_named_proxy("__iand__"),
            "__ixor__": Behavioral_.create_named_proxy("__ixor__"),
            "__ior__": Behavioral_.create_named_proxy("__ior__"),
            "__neg__": Behavioral_.create_named_proxy("__neg__"),
            "__pos__": Behavioral_.create_named_proxy("__pos__"),
            "__abs__": Behavioral_.create_named_proxy("__abs__"),
            "__invert__": Behavioral_.create_named_proxy("__invert__"),
        }
        c = Behavioral(name, bases, attrs)
        return c

    @staticmethod
    def __init_f__(self, *args, **kwargs) -> None:
        active_cls = type(self).__active_one__()
        self.__instance__ = active_cls(*args, **kwargs)

    @staticmethod
    def __obj_get_attr__(self, __name: str):
        # TODO: we gotta do these cleaner, like a rule, names...
        instance = object.__getattribute__(self, "__instance__")
        return getattr(instance, __name)

    @staticmethod
    def __obj_get_attribute__(self, __name: str):
        # IDEA: Why not diverge all to instance
        instance = object.__getattribute__(self, "__instance__")
        if __name == "__instance__":
            return instance
        attr = object.__getattribute__(instance, __name)
        return attr

    @staticmethod
    def __is_active__(cls):
        try:
            cls.__active_one__()
            return True
        except Exception:
            return False

    def __instancecheck__(cls, instance):
        # TODO: Explain
        if issubclass(type(instance), cls):
            return True
        return isinstance(instance, cls.__active_one__())

    @staticmethod
    def __active_one__(cls):
        t1, t2 = tuple(cls.__meta__["types"])
        a1 = t1.__is_active__()
        a2 = t2.__is_active__()
        if a1 and a2:
            raise RuntimeError(
                "Both types are active?! What kind of black magic is this?",
            )
        if not (a1 or a2):
            raise RuntimeError(
                "Both types are deactive?! What kind of black magic is this?",
            )
        if a1:
            return t1
        if a2:
            return t2

    def __getattr__(self, __name: str):
        return getattr(self.__active_one__(), __name)

    @staticmethod
    def create_named_proxy(name):
        def __proxy__(self, *args, **kwargs):
            i = object.__getattribute__(self, "__instance__")
            f = getattr(i, name)
            return f(*args, **kwargs)

        return __proxy__

    def __add__(self, other):
        x = Behavioral_.create_new(self, other)
        return x


class Behaved_(type):
    def __new__(mcs, name, bases, attrs):
        c = super().__new__(mcs, name, bases, attrs)
        if not hasattr(c, "__is_active__"):
            raise RuntimeError()
        return c

    def __add__(self, other):
        x = Behavioral_.create_new(self, other)
        return x


Behaved = mix_metas((Behaved_,))
Behavioral = mix_metas((Behavioral_,))
