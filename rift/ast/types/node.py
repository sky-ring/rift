import uuid

from rift.ast.printer import Printer


class Node:
    N_ID = 0
    id_to_node = {}
    index_to_node = {}

    def __init__(self):
        self._id = uuid.uuid4().hex
        self._index = Node.N_ID
        Node.N_ID += 1
        Node.id_to_node[self._id] = self
        Node.index_to_node[self._index] = self

    def node_id(self):
        return self._id

    def node_index(self):
        return self._index

    @staticmethod
    def find(node_id: str) -> "Node":
        return Node.id_to_node[node_id]

    def print_func(self, printer: Printer):
        pass
