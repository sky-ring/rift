from typing import List

from dbuilder.ast.condition import IfFlow
from dbuilder.ast.contract import Contract
from dbuilder.ast.method import Method
from dbuilder.ast.node import Node
from dbuilder.ast.statement import Statement


class CallStacks(object):
    calls: List = []
    functions = set()
    __instance = None
    current_contract: Contract = None

    @staticmethod
    def get_instance() -> "CallStacks":
        if CallStacks.__instance is None:
            CallStacks()
        return CallStacks.__instance

    def __init__(self):
        if CallStacks.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CallStacks.__instance = self

    @staticmethod
    def add(call):
        CallStacks.get_instance().calls.append(call)
        return len(CallStacks.get_instance().calls) - 1

    @staticmethod
    def insert(call, pos=-1):
        if pos == -1:
            CallStacks.add(call)
            return
        CallStacks.get_instance().calls.insert(pos, call)

    @staticmethod
    def get_stack() -> str:
        x = ""
        for call in CallStacks.get_instance().calls:
            x += str(call) + "\n"
        return x

    @staticmethod
    def declare_contract(name):
        CallStacks.current_contract = Contract(name)

    @staticmethod
    def declare_method(name, args):
        m = Method(name, args)
        CallStacks.current_contract.add_method(m)
        pass

    @staticmethod
    def add_statement(type, *args):
        s = Statement(type, args)
        CallStacks.current_contract.add_statement(s)

    @staticmethod
    def return_(entity):
        CallStacks.add_statement(Statement.RETURN, entity)

    @staticmethod
    def end_method(method):
        CallStacks.current_contract.end_method(method)
        pass

    @staticmethod
    def begin_if(cond):
        nif = IfFlow()
        nif.iff(cond)
        CallStacks.current_contract.add_statement(nif)
        return nif.node_id()

    @staticmethod
    def else_if(id, cond=None):
        nif: IfFlow = Node.find(id)
        if cond:
            nif.iff(cond)
        else:
            nif.else_()
        pass

    @staticmethod
    def end_if(id):
        nif: IfFlow = Node.find(id)
        CallStacks.current_contract.current_method.end_statement(nif)
        pass


    @staticmethod
    def call_(name, *args, operand=None):
        if operand:
            CallStacks.add_statement(Statement.METHOD_CALL, name, operand, *args)
        else:
            CallStacks.add_statement(Statement.FUNC_CALL, name, *args)


    @staticmethod
    def func():
        codes = []
        indent = 0
        indents = []
        for call in CallStacks.get_instance().calls:
            if call["type"] == "DECL_METHOD":
                codes.append("_ %s(%s){" % (call["name"], ", ".join(call["args"])))
                indents.append(indent)
                indent += 1
            elif call["type"] == "DEFINE_ENTITY":
                indents.append(indent)
                e = call["entity"]
                v = call["value"]
                if v["type"] == "expr":
                    codes.append("var %s = %s %s %s;" % (e, v["op1"], v["op"], v["op2"]))
            elif call["type"] == "RETURN_ENTITY":
                indents.append(indent)
                codes.append("return %s;" % call["entity"])
            elif call["type"] == "END_METHOD":
                indent -= 1
                indents.append(indent)
                codes.append("}")
            elif call["type"] == "METHOD_CALL":
                indents.append(indent)
                n: str = call["name"]
                if n.endswith("_"):
                    n = "~" + n.removesuffix("_")
                else:
                    if "operand" in call:
                        n = "." + n
                op = call["operand"] if "operand" in call else ""

                # codes.append("var %s = %s%s(%s);" % (call["result"], op, n,
                #                                      ",".join(
                #                                          [str(x) for x in call["args"]]
                #                                      )))
                def transform(x):
                    if isinstance(x, str):
                        return "\"%s\"" % x
                    return str(x)

                codes.append("%s%s(%s);" % (op, n, ",".join(
                    [transform(x) for x in call["args"]]
                )))
            elif call["type"] == "IF_BLOCK":
                if call["index"] == 1:
                    codes.append("if(%s){" % call["cond"])
                    indents.append(indent)
                    indent += 1
                else:
                    indent -= 1
                    indents.append(indent)
                    codes.append("}")
                    indents.append(indent)
                    codes.append("else if (%s) {" % call["cond"])
                    indent += 1
            elif call["type"] == "ELSE_BLOCK":
                indent -= 1
                indents.append(indent)
                indents.append(indent)
                codes.append("}")
                codes.append("else {")
                indent += 1
            elif call["type"] == "END_IF":
                indent -= 1
                indents.append(indent)
                codes.append("}")

        return "\n".join(list([(x1 * "\t") + x2 for x1, x2 in zip(indents, codes)]))
