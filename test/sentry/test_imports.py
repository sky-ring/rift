from test.util import compile

from rift import *
from rift.ast.sentry.base_types import SentryHalted
import requests
from os.path import join
from rift_tonlib.types.cell import Cell
import os, ssl


class DisallowIllegalImports(Contract):
    def external_receive(self) -> None:
        pass


def test_compile():
    try:
        compile(DisallowIllegalImports)
        raise RuntimeError("Shouldn't have compiled")
    except SentryHalted as se:
        assert len(se.warnings) == 5
