from dbuilder.types.msg import StateInit
from dbuilder.types.addr import MsgAddress
from dbuilder.types.utils import CachingSubscriptable


class ContractAddr(metaclass=CachingSubscriptable):
    def __init__(self, code, **kwargs):
        base = self.__basex__
        if isinstance(code, str):
            code = kwargs[code]
        dt = base.Data(**kwargs)
        self._init = StateInit(
            split_depth=None,
            special=None,
            code=code,
            data=dt.as_cell(),
            library=None,
        ).as_cell()
        self._addr = MsgAddress.std(0, self._init.hash())

    def get(self):
        return self._addr

    def __assign__(self, v):
        pass

    @classmethod
    def __build_type__(cls, item):
        return type(
            "ContractAddr_%s" % item.__name__,
            (cls,),
            {
                "__basex__": item,
            },
        )
