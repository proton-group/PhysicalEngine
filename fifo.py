class Node:
    def __init__(self):
        self.memory = None
        self.data = None
class fifo:
    def __init__(self):
        self.base = Node()
        self.len = 0

    def add(self, data):
        self._add(data, self.base)

    def _add(self, data, node):
        if self.base.data == None:
            self.base.data = data
        else:
            if node.memory != None:
                self._add(data, node.memory)
            else:
                node.memory = Node()
                self.len += 1
                node.memory.data = data
    def read(self):
        data = self.base.data
        if self.base.memory != None:
            self.base = self.base.memory
        else:
            self.base = Node()
        return data
