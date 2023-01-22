from enum import Enum

from appdirs import AppDirs


class Mode(Enum):
    FUNC = 0
    FIFT = 1

    def is_func(self):
        return self.value == self.FUNC.value

    def is_fift(self):
        return self.value == self.FIFT.value


class Config:
    TEST: bool = False
    mode: Mode = Mode.FIFT
    dirs = AppDirs(appname="Rift", appauthor="Skyring")


class Scope:
    def __init__(self, mode: Mode) -> None:
        self.mode = mode

    def __enter__(self, *args, **kwargs):
        self._p_mode = Config.mode
        Config.mode = self.mode
        return self

    def __exit__(self, *args, **kwargs):
        Config.mode = self._p_mode

    def activate(self):
        Config.mode = self.mode


FunCMode = Scope(Mode.FUNC)
FiftMode = Scope(Mode.FIFT)
