class Field:
    CLOSED_STATE = 0
    FLAGGED_STATE = 1
    MAYBE_STATE = 2
    OPENED_STATE = 3
    
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._mines_nearby = 0
        self._is_mine = False
        self._state = Field.CLOSED_STATE
        
    def putMine(self):
        self._is_mine = True
        
    def isMine(self):
        return self._is_mine
        
    def setMinesNearby(self, no):
        self._mines_nearby = no
        
    def getMinesNearby(self):
        return self._mines_nearby
        
    def isClosed(self):
        return self._state == Field.CLOSED_STATE
        
    def isOpened(self):
        return self._state == Field.OPENED_STATE
        
    def isMarked(self):
        return self._state == Field.FLAGGED_STATE or self._state == Field.MAYBE_STATE
        
    def onRightClick(self):
        if not self.isClosed():
            return
            
        elif self._state == Field.CLOSED_STATE:
            self._state = Field.FLAGGED_STATE
            
        elif self._state == Field.FLAGGED_STATE:
            self._state = Field.MAYBE_STATE
            
        else:
            self._state = Field.CLOSED_STATE
            
    def open(self):
        self._state = Field.OPENED_STATE