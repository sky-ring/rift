from dbuilder import method


class ContractMeta(type):
    def __new__(mcs, name, bases, attrs):
        for a, v in attrs.items():
            if a.startswith("__"):
                continue
            if callable(v):
                attrs[a] = method(v)
        return super(ContractMeta, mcs).__new__(mcs, name, bases, attrs)
