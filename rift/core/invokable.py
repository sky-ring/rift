from functools import partial

from rift.ast import CallStacks
from rift.ast.types import Expr, Statement
from rift.core.factory import Factory
from rift.core.mark import mark
from rift.core.utils import init_abstract_type


class InvokableFunc:
    def __init__(self, name):
        self.name = name
        self.method_annotations = None

    def __call__(self, *args, **kwargs):
        mark(*args)
        e = Factory.build(
            "Entity",
            Expr.call_func(
                self.name,
                *args,
                annotations=self.method_annotations,
            ),
        )
        setattr(e, "__unpackable", True)
        setattr(e, "__expr", CallStacks.expression(e.data))
        e.has_expr = True
        return e


class InvokableBinder:
    def __init__(self, name, method_annotations=None):
        self.name = name
        self.method_annotations = method_annotations

    def bind(self, entity):
        self.entity = entity

    def __call__(self, *args, **kwargs):
        mark(*args)
        rt = None
        if self.method_annotations is not None:
            rt = self.method_annotations.get("return", None)
        e = init_abstract_type(
            rt,
            data=Expr.call_expr(
                self.entity,
                self.name,
                *args,
                annotations=self.method_annotations,
            ),
        )
        setattr(e, "__unpackable", True)
        setattr(e, "__expr", CallStacks.expression(e.data))
        e.has_expr = True
        return e


class Invokable(InvokableBinder):
    def __init__(self, name, entity, method_annotations=None):
        super().__init__(name, method_annotations=method_annotations)
        self.bind(entity)


class TypedInvokable(Invokable):
    def __init__(self, name, entity, return_) -> None:
        if return_ in Factory.engines:
            return_ = Factory.engines[return_]
        super().__init__(
            name,
            entity,
            method_annotations={
                "return": return_,
            },
        )


def typed_invokable(name=None, return_=None):
    return partial(typed_invokable_, name=name, return_=return_)


def typed_invokable_(func, name=None, return_=None):
    def new_f(*args, **kwargs):
        nonlocal name
        nonlocal return_
        mark(*args)
        self = args[0]
        args = args[1:]
        if return_ is None:
            annotations = func.__annotations__
            annotations = {**annotations} if annotations else {}
            return_ = annotations.get("return", None)
        if name is None:
            name = func.__name__
        return TypedInvokable(name, self, return_=return_)(*args, **kwargs)

    return new_f
