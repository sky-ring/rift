from rift.meta.behaviors import Behaved


class FiftBehavior(metaclass=Behaved):
    @classmethod
    def __is_active__(cls):
        return False
