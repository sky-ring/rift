from rift import CallStacks
from rift.core.entity import mark
from rift.core.invokable import InvokableFunc
from rift.func.meta_contract import ContractMeta


class Library(metaclass=ContractMeta):
    def __init__(self):
        pass

    def __getattr__(self, item):
        return InvokableFunc(item)

    def ret_(self, *t):
        mark(*t)
        if len(t) == 0:
            CallStacks.return_(None)
        return CallStacks.return_(*t)
