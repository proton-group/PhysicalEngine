class Node:
    def __init__(self):
        self.memory = None
        self.data = None
        
class fifo:
    def __init__(self):
        self.base = Node()
        self.len = 0
        self.fifoblock = False

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
        if not self.fifoblock:
            self.add(data)
        if self.base.memory != None:
            self.base = self.base.memory
            self.len -= 1
        else:
            self.base = Node()
        return data

    def control(self, instruction):
        if instruction == "break":
            self.fifoblock = True
        if instruction == "lock":
            self.fifoblock = False
            
    def clear(self):
        self.base = Node()

