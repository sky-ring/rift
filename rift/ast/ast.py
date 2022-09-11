from rift.ast.types import Node


class AST:
    def __init__(self):
        self.nodes = {}
        self.root = Node()

    def add_node(self, node):
        self.nodes[node.node_id()] = node

    def find_node(self, node_id: str) -> Node:
        return self.nodes[node_id]
