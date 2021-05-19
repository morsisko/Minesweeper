class Counter:
    def __init__(self, x, y, digits):
        self._x = x
        self._y = y
        self._value = 0
        self._digits = digits
        
    def setValue(self, value):
        self._value = value
    
    def draw(self, window):
        valueToDraw = min(10 ** digits - 1, self._value)
        valueToDraw = max(0, self._value)
        
        