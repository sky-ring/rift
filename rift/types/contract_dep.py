from rift.types.addr import MsgAddress
from rift.types.msg import StateInit
from rift.types.utils import CachingSubscriptable


class ContractDeployer(metaclass=CachingSubscriptable):
    def __init__(self, code, **kwargs):
        base = self.__basex__
        if isinstance(code, str):
            code = kwargs[code]
        dt = base.Data(**kwargs)
        self.state_init = StateInit(
            split_depth=None,
            special=None,
            code=code,
            data=dt.as_cell(),
            library=None,
        ).as_cell()
        self.address = MsgAddress.std(0, self.state_init.hash())

    def __assign__(self, v):
        self.state_init.__assign__(f"{v}_state_init")
        self.address.__assign__(f"{v}_address")
        return self

    @classmethod
    def __build_type__(cls, item):
        return type(
            "ContractAddr_%s" % item.__name__,
            (cls,),
            {
                "__basex__": item,
            },
        )
