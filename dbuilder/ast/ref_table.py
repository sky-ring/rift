import json


class ReferenceTable:
    refs: dict[str, dict[str, int]] = {}
    current_scope = ""

    @classmethod
    def init_scope(cls, scope):
        cls.refs[scope] = {}
        cls.current_scope = scope

    @classmethod
    def ref(cls, name: str):
        scope = cls.refs[cls.current_scope]
        if name not in scope:
            scope[name] = 0
        scope[name] += 1

    @classmethod
    def mark(cls, *args):
        for a in args:
            # We check if it's entity
            if hasattr(a, "__magic__") and a.__magic__ == 0x050794:
                if a.NAMED:
                    cls.ref(a.name)

    @classmethod
    def dump(cls):
        o = json.dumps(cls.refs, indent=4)
        return o
