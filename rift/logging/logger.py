import time
from enum import Enum
from functools import total_ordering

import colorful as cf


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

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Logger:
    logging_level = Level.DEBUG
    palette = {
        "red": "#F75590",
        "blue": "#3DB1F5",
        "white": "#FFFFFF",
        "green": "#9EE493",
        "yellow": "#FFF689",
        "black": "#000000",
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
    }

    @classmethod
    def log(cls, logger, level: Level, msg: str, **kwargs):
        cf.use_palette(Logger.palette)
        if Logger.logging_level >= level:
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
                    content = "{c.%s}%s{c.reset}" % (color, content)
                else:
                    content = v
                nd[k] = content
            log_msg = log_head + " " + log_body.format(**nd)
            print(log_msg.format(c=cf))


def log_info(tag, message, **kwargs):
    Logger.log(tag, Level.INFO, message, **kwargs)


def log_warn(tag, message, **kwargs):
    Logger.log(tag, Level.WARNING, message, **kwargs)


def log_panic(tag, message, **kwargs):
    Logger.log(tag, Level.PANIC, message, **kwargs)
