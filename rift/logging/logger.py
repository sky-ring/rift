import time
from enum import Enum
from functools import total_ordering
from os import path

import colorful as cf

from rift.logging.error import RiftError
from rift.runtime.config import Config


@total_ordering
class Level(Enum):
    PANIC = 0
    ALERT = 1
    CRTIICAL = 2
    ERROR = 3
    WARNING = 4
    NOTE = 5
    INFO = 6
    DEBUG = 7
    SYSTEM = 100

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class StyleMocker:
    def __getattr__(self, k):
        return ""


class Logger:
    initialized = False
    logging_level = Level.INFO
    palette = {
        "red": "#F75590",
        "blue": "#3DB1F5",
        "white": "#FFFFFF",
        "green": "#9EE493",
        "yellow": "#FFF689",
        "black": "#000000",
        "mint": "#4BA3C3",
    }
    colors = {
        Level.PANIC: "red",
        Level.ALERT: "red",
        Level.CRTIICAL: "red",
        Level.ERROR: "red",
        Level.WARNING: "yellow",
        Level.NOTE: "green",
        Level.INFO: "blue",
        Level.DEBUG: "white",
        Level.SYSTEM: "mint",
    }
    log_file = None
    mocker = StyleMocker()

    @classmethod
    def init(cls):
        if not cls.initialized:
            cls.initialized = True
            cf.use_palette(Logger.palette)
            log_file_path = path.join(Config.dirs.user_data_dir, "rift.log")
            cls.log_file = open(log_file_path, "a")

    @classmethod
    def log(cls, logger, level: Level, msg: str, **kwargs):
        cls.init()
        log_head = "{c.bold}{c.%s}[%s - %s]{c.reset}" % (
            Logger.colors[level],
            logger,
            time.strftime("%Y-%m-%d %H:%M:%S"),
        )
        log_body = msg
        nd = {}
        for k, v in kwargs.items():
            if isinstance(v, tuple):
                content = v[0]
                color = v[1]
                content = "{c.%s}%s{c.reset}{c.white}" % (color, content)
            else:
                content = v
            nd[k] = content
        log_msg = log_head + " {c.reset}{c.white}" + log_body.format(**nd)
        if Logger.logging_level >= level:
            print(log_msg.format(c=cf))
        cls.log_file.write(log_msg.format(c=cls.mocker) + "\n")


def log_info(tag, message, **kwargs):
    Logger.log(tag, Level.INFO, message, **kwargs)


def log_warn(tag, message, **kwargs):
    Logger.log(tag, Level.WARNING, message, **kwargs)


def log_debug(tag, message, **kwargs):
    Logger.log(tag, Level.DEBUG, message, **kwargs)


def log_system(tag, message, **kwargs):
    Logger.log(tag, Level.SYSTEM, message, **kwargs)


def log_error(tag, message, **kwargs):
    Logger.log(tag, Level.ERROR, message, **kwargs)


def log_panic(tag, error=None, message=None, **kwargs):
    error = error or ""
    if message is None:
        message = error
    Logger.log(tag, Level.PANIC, message, **kwargs)
    raise RiftError(error)
