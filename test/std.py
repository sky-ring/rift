import unittest

from dbuilder import Engine
from dbuilder.core.annots import asm, impure
from dbuilder.func.library import Library
from dbuilder.types import Slice, Cell, Tuple, Builder, Cont
from dbuilder.library.std import Stdlib


class CompileTestCase(unittest.TestCase):
    def test_compile(self):
        # Library
        # TODO: Fix the imports of the class
        # and compile it without need of dependencies
        t = Engine.patched(Stdlib)
        compiled = Engine.compile(t)
        print(compiled.to_func())


if __name__ == "__main__":
    unittest.main()
