from rift.fift.fift import Fift
from rift.meta.behaviors import Behaved
from rift.runtime.config import Config, Mode


class FiftBehavior(metaclass=Behaved):
    def cmd(self, command: str, *args):
        return Fift.exec(command, *args)

    @classmethod
    def __is_active__(cls):
        return Config.mode == Mode.FIFT
