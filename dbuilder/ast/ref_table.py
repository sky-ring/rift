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
