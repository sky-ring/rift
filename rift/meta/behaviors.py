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
        }
        c = Behavioral(name, bases, attrs)
        return c

    @staticmethod
    def __init_f__(self, *args, **kwargs) -> None:
        active_cls = type(self).__active_one__()
        self.instance = active_cls(*args, **kwargs)

    @staticmethod
    def __obj_get_attr__(self, __name: str):
        return getattr(self.instance, __name)

    @staticmethod
    def __obj_get_attribute__(self, __name: str):
        attr = object.__getattribute__(self, __name)
        if is_stub(attr):
            return getattr(self.instance, __name)
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
