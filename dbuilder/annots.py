from dbuilder.ast.expr import Expr
from dbuilder.ast.statement import Statement
from dbuilder.calls import CallStacks
from dbuilder.entity import Entity


def init_func(func):
    if not hasattr(func, "__pyfunc__"):
        setattr(func, "__pyfunc__", {})
    return func


def method(func):
    def nf(*args, **kwargs):
        slf = args[0]
        if "NO_INTERCEPT" in kwargs:
            kwargs.pop("NO_INTERCEPT")
            return func(*args, **kwargs)
        elif hasattr(slf, "__intercepted__") and getattr(slf, "__intercepted__") == 1:
            e = Entity(
                Expr.call_func(func.__name__, *args[1:])
            )
            setattr(e, "__expr", CallStacks.add_statement(
                Statement.EXPR, e.data))
            e.has_expr = True
            return e
        else:
            return func(*args, **kwargs)

    nf = init_func(nf)
    nf.__pyfunc__["type"] = ["method"]
    setattr(nf, "__args__", func.__code__.co_argcount)
    setattr(nf, "__names__",
            func.__code__.co_varnames[:func.__code__.co_argcount])
    return nf


def is_method(func):
    if not hasattr(func, "__pyfunc__"):
        return False
    type_ = func.__pyfunc__.get("type", [])
    return "method" in type_
