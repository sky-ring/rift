## FROM: https://gist.github.com/RyanKung/4830d6c8474e6bcefa4edd13f122b4df

import sys
import ast

origin_import = __import__
AST = {}


def custom_import(name, *args, **kwargs):
    # print("importing..", name)
    module = origin_import(name, *args, **kwargs)
    if not hasattr(module, '__file__'):
        return module
    try:
        f = open(
                    sys.modules[name].__file__.replace('pyc', 'py'),
                    'r'
                )
        mod_ast = ast.parse(
            ''.join(
                f.readlines()
            )
        )
        f.close()
        patched_ast = patch(mod_ast)
        exec(compile(patched_ast, name, "exec"), module.__dict__)
        AST[name] = mod_ast
        AST['%s_patched' % name] = patched_ast
        return module
    except Exception as e:
        print(e)
        return module


def gen_assign_checker_ast(targets, obj_name):
    return ast.If(
        test=ast.Call(
            func=ast.Name(id='hasattr', ctx=ast.Load()),
            args=[
                ast.Name(id=obj_name, ctx=ast.Load()),
                ast.Str(s='__assign__'),
            ],
            keywords=[],
            starargs=None,
            kwargs=None
        ),
        body=[
            ast.Assign(
                targets=[ast.Name(id=target, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id=obj_name, ctx=ast.Load()),
                        attr='__assign__',
                        ctx=ast.Load()
                    ),
                    args=[ast.Str(s=target)],
                    keywords=[],
                    starargs=None,
                    kwargs=None
                )
            )
            for target in targets],
        orelse=[]
    )


class Transformer(ast.NodeTransformer):
    def generic_visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Assign(self, node):
        # if not isinstance(node.value, ast.Name):
        #     return node
        # targets = [t.id for t in node.targets]
        # obj_name = node.value.id
        # new_node = gen_assign_checker_ast(targets, obj_name)
        # ast.copy_location(new_node, node)
        # ast.fix_missing_locations(new_node)
        # vx = ast.Expr(
        #     value=ast.Call(
        #         func=ast.Name(id='print', ctx=ast.Load()),
        #         args=[ast.Constant(value='x', kind=None)],
        #         keywords=[],
        #     ),
        # )
        targets = [t.id for t in node.targets]
        nodes = [node]
        for t in targets:
            vx = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id=t, ctx=ast.Load()),
                        attr='assignment',
                        ctx=ast.Load(),
                    ),
                    args=[ast.Constant(value=str(t), kind=None)],

                    keywords=[],
                ),
            )
            nodes.append(vx)
        for vx in nodes:
            ast.fix_missing_locations(vx)
        return nodes


def patch(node):
    trans = Transformer()
    new_node = trans.visit(node)
    ast.fix_missing_locations(new_node)
    return new_node


def change():
    __builtins__.update(**dict(
        __import__=custom_import,
        __ast__=AST
    ))