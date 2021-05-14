class Stack:
    def __init__(self, size):
        self._size = size
        self._data = []
        
    def push(self, item):
        self._data.append(item)
        
        if len(self._data) > self._size:
            self._data.pop(0)
            
    def compare(self, other):
        if len(self._data) != len(other):
            return False
            
        for i in range(len(other)):
            if self._data[i] != other[i]:
                return False
                
        return True