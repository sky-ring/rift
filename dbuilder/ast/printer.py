class Printer:
    def __init__(self):
        self.lines = []
        self.current_indent = 0

    def print(self, data: str, indent: int = None, **params):
        if indent is None:
            indent = self.current_indent
        self.lines.append(("\t" * indent) + data.format(**params))

    def incr_indent(self):
        self.current_indent += 1

    def decr_indent(self):
        self.current_indent -= 1
        if self.current_indent < 0:
            self.current_indent = 0

    def out(self):
        return "\n".join(self.lines)
