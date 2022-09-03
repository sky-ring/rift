import json


class ReferenceTable:
    refs: dict[str, dict[str, int]] = {}
    eliminatables: dict[str, list[str]] = {}
    current_scope = ""

    @classmethod
    def init_scope(cls, scope):
        cls.refs[scope] = {}
        cls.eliminatables[scope] = []
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

    @classmethod
    def eliminatable(cls, name: str):
        cls.eliminatables[cls.current_scope].append(name)

    @classmethod
    def is_eliminatable(cls, scope: str, name: str) -> bool:
        eliminatable = name in cls.eliminatables[scope]
        count = cls.refs[scope].get(name, 0)
        return eliminatable and count == 0
