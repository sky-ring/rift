from rift.meta.behaviors import Behaved
from rift.runtime.config import Config, Mode


class FunCBehavior(metaclass=Behaved):
    @classmethod
    def __is_active__(cls):
        return Config.mode == Mode.FUNC
