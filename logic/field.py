class Field:
    """Klasa reprezentująca jedno pole na planszy"""
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
        
    def __eq__(self, other):
        return self._x == other._x and self._y == other._y
        
    def putMine(self):
        """Metoda kładąca mine na pole"""
        self._is_mine = True
        
    def isMine(self):
        """Metoda zwracająca True jeżeli pole jest miną, w przeciwnym wypadku False"""
        return self._is_mine
        
    def setMinesNearby(self, no):
        """Metoda ustawiająca ilość min w pobliżu pola"""
        self._mines_nearby = no
        
    def getMinesNearby(self):
        """Metoda zwracająca ilość min w pobliżu pola"""
        return self._mines_nearby
        
    def isClosed(self):
        """Metoda zwracająca True jeżeli pole nie zostało jeszcze odkryte, w przeciwnym wypadku False"""
        return self._state == Field.CLOSED_STATE or self._state == Field.FLAGGED_STATE or self._state == Field.MAYBE_STATE
        
    def isOpened(self):
        """Metoda zwracająca True jeżeli pole nie zostało jeszcze odkryte, w przeciwnym wypadku False"""
        return self._state == Field.OPENED_STATE
        
    def isMarked(self):
        """Metoda zwracająca True jeżeli pole zostało oznaczone (flagą lub znakiem zapytania), w przeciwnym wypadku False"""
        return self._state == Field.FLAGGED_STATE or self._state == Field.MAYBE_STATE
        
    def isFlagged(self):
        """Metoda zwracająca True jeżeli pole zostało oznaczone flagą, w przeciwnym wypadku False"""
        return self._state == Field.FLAGGED_STATE
        
    def isMaybeMine(self):
        """Metoda zwracająca True jeżeli pole zostało oznaczone znakiem zapytania, w przeciwnym wypadku False"""
        return self._state == Field.MAYBE_STATE
        
    def onRightClick(self):
        """Metoda dokonująca akcji po kliknięciu prawym przyciskiem na pole"""
        if self.isOpened():
            return
            
        elif self._state == Field.CLOSED_STATE:
            self._state = Field.FLAGGED_STATE
            
        elif self._state == Field.FLAGGED_STATE:
            self._state = Field.MAYBE_STATE
            
        else:
            self._state = Field.CLOSED_STATE
            
    def open(self):
        """Metoda ustawiająca pole w stan otwarty"""
        self._state = Field.OPENED_STATE