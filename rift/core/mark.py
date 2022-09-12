from rift.ast.types import Expr


def mark(*args):
    for o in args:
        if hasattr(o, "__magic__") and o.__magic__ == 0x050794:
            if isinstance(o.data, Expr):
                o.data.__hide__ = True
