import traceback
from os import makedirs, path, umask


class _DirNode:
    children: list["_DirNode"]
    name: str
    parent: "_DirNode"

    def __init__(self, name):
        self.children = []
        self.name = name
        self.parent = None

    def __lshift__(self, other: str):
        n = _DirNode(other)
        n.parent = self
        self.children.append(n)
        return n

    def __rshift__(self, other: str):
        n = _DirNode(other)
        n.parent = self
        self.children.append(n)
        return self

    def leaves(self):
        if len(self.children) == 0:
            yield self
        for child in self.children:
            for leaf in child.leaves():
                yield leaf

    def as_dir(self):
        p = []
        node = self
        while node is not None:
            p.insert(0, node.name)
            node = node.parent
        return path.join(*p)


class DirectoryStructure(_DirNode):
    def __init__(self, root: str):
        super(DirectoryStructure, self).__init__(root)

    def create_dirs(self, exists_ok=False) -> bool:
        for leaf in self.leaves():
            p = leaf.as_dir()
            try:
                makedirs(p, 0o777, exists_ok)
            except Exception:
                return False
        return True
