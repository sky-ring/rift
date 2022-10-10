from rift.meta.behaviors import Behaved


class FunCBehavior(metaclass=Behaved):
    @classmethod
    def __is_active__(cls):
        return False
