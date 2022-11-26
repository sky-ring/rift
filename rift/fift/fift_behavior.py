from rift.meta.behaviors import Behaved
from rift.runtime.config import Config, Mode


class FiftBehavior(metaclass=Behaved):
    def cmd(self, command: str, *args):
        from rift.fift.fift import Fift

        return Fift.exec(command, *args)

    def call(self, cmd: str, *args):
        return self.cmd(cmd, self, *args)

    def call_(self, cmd: str, *args):
        (res, *others) = self.call(cmd, *args)
        self.value = res.value
        return others

    @classmethod
    def __is_active__(cls):
        return Config.mode == Mode.FIFT
