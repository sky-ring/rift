from dbuilder.calls import CallStacks


class Cond:
    C_ID = 0

    def __init__(self):
        Cond.C_ID += 1
        self.id = Cond.C_ID
        self.index = 0
        self.conds = []
        pass

    def match(self, cond):
        self.index += 1
        self.conds.append(cond)
        CallStacks.add({
            "type": "IF_BLOCK",
            "id": self.id,
            "index": self.index,
            "cond": cond
        })

    def otherwise(self):
        CallStacks.add({
            "type": "ELSE_BLOCK",
            "id": self.id,
            "index": self.index,
        })

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        CallStacks.add({
            "type": "END_IF",
            "id": self.id
        })

