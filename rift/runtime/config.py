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
    mode: Mode = Mode.FIFT
    dirs = AppDirs(appname="Rift", appauthor="Skyring")
