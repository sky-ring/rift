from dbuilder import Entity, Expr, Statement, CallStacks


class InvokableFunc:
    def __init__(self, name):
        self.name = name
        self.method_annotations = None

    def __call__(self, *args, **kwargs):
        e = Entity(
            Expr.call_func(
                self.name,
                *args,
                annotations=self.method_annotations,
            ),
        )
        setattr(e, "__unpackable", True)
        setattr(e, "__expr", CallStacks.add_statement(Statement.EXPR, e.data))
        e.has_expr = True
        return e
