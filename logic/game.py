import time
from logic.exceptions import MinesweeperException, BoardTooSmallException, BoardTooBigException, TooManyMinesException, TooLittleMinesException
from logic.board import Board
from logic.stack import Stack

class Game:
    """Klasa reprezentująca stan aktualnej gry"""
    WAITING = -1
    STARTED = 0
    LOST = 1
    WON = 2
    MAX_BOARD_SIZE = 15
    MIN_BOARD_SIZE = 2
    SECRET_CODE = [120, 121, 122, 122, 121] #xyzzy
    
    def __init__(self, width, height, mines):
        if width < Game.MIN_BOARD_SIZE or height < Game.MIN_BOARD_SIZE:
            raise BoardTooSmallException
            
        if width > Game.MAX_BOARD_SIZE or height > Game.MAX_BOARD_SIZE:
            raise BoardTooBigException
            
        if mines < 0:
            raise TooLittleMinesException
            
        if mines >= (width * height):
            raise TooManyMinesException
    
        self._board = Board(width, height, mines)
        self._state = Game.WAITING
        self._lastOpenedField = None
        self._gameStartedTimestamp = 0
        self._gameEndedTimestamp = 0
        self._stack = Stack(len(Game.SECRET_CODE))
        self._cheats = False
        
    def _doActionBasingOnGameState(self):
        """Metoda wykonująca akcję bazując na aktualnym stanie gry"""
        if self._state == Game.WON:
            self._gameEndedTimestamp = int(time.time() * 1000)
            print("Zwyciestwo")
            
        elif self._state == Game.LOST:
            self._gameEndedTimestamp = int(time.time() * 1000)
            print("Porazka")
        
    def _checkGameState(self):
        """Metoda sprawdzająca czy gra została przegrana, wygrana, czy nadal może być kontynuowana"""
        if self._state != Game.STARTED:
            return
            
        closedFields = 0
        minesMarkedCorrectly = 0
        for y in range(self._board.getHeight()):
            for x in range(self._board.getWidth()):
                field = self._board.getField(x, y)
                if field.isMine() and field.isFlagged():
                    minesMarkedCorrectly += 1
                    
                if field.isClosed():
                    closedFields += 1
                    
                if field.isOpened() and field.isMine():
                    self._state = Game.LOST
                    self._doActionBasingOnGameState()
                    return
                    
        if closedFields == self._board.getMineCount() or minesMarkedCorrectly == self._board.getMineCount():
            self._state = Game.WON
            
        self._doActionBasingOnGameState()
            
    def rightClick(self, x, y):
        """Metoda obsługująca kliknięcie prawym przyciskiem myszy na planszę"""
        if x < 0 or y < 0 or x >= self._board.getWidth() or y >= self._board.getHeight():
            return
            
        field = self._board.getField(x, y)
        field.onRightClick()
        
        self._checkGameState()  
        
    def leftClick(self, x, y):
        """Metoda obsługująca kliknięcie lewym przyciskiem myszy na planszę"""
        if x < 0 or y < 0 or x >= self._board.getWidth() or y >= self._board.getHeight():
            return
    
        if self._state == Game.WAITING:
            self._state = Game.STARTED
            self._board.initBoard(x, y)
            self._gameStartedTimestamp = int(time.time() * 1000)
            
        elif self._state == Game.WON or self._state == Game.LOST:
            return
            
        self._board.openField(x, y)
        self._lastOpenedField = self._board.getField(x, y)
        
        self._checkGameState()
            
    def isEnd(self):
        """Metoda zwracająca True jeżeli gra została już zakończona (wygrana lub przegrana)"""
        return self._state == Game.WON or self._state == Game.LOST
        
    def isWon(self):
        """Metoda zwracająca True jeżeli gra została wygrana"""
        return self._state == Game.WON

    def isLost(self):
        """Metoda zwracająca True jeżeli gra została przegrana"""
        return self._state == Game.LOST
        
    def getField(self, x, y):
        """Metoda zwracająca obiekt Field o współrzędnych x i y na planszy"""
        return self._board.getField(x, y)
        
    def getLastOpenedField(self):
        """Metoda zwracająca koordynaty ostatnio otwartego pola"""
        return self._lastOpenedField
        
    def getFlaggedFieldsCount(self):
        """Metoda zwracająca liczbę pól oznaczonych flagami"""
        result = 0
        for y in range(self._board.getHeight()):
            for x in range(self._board.getWidth()):
                if self._board.getField(x, y).isFlagged():
                    result += 1
                    
        return result
        
    def getTimePlayingInSeconds(self):
        """Metoda zwracająca (w sekundach) czas od momentu rozpoczęcia gry do jej zakończenia (lub w przypadku gdy gra nie jest jeszcze zakończona, to aktualny czas jej trwania)"""
        if self._gameStartedTimestamp == 0:
            return 0
            
        if self._gameEndedTimestamp == 0:
            return (int(time.time() * 1000) - self._gameStartedTimestamp) // 1000
            
        return (self._gameEndedTimestamp - self._gameStartedTimestamp) // 1000
        
    def addKeypress(self, keycode):
        """Metoda dodająca wciśnięty klawisz do stosu wciśniętych klawiszy, oraz sprawdzająca, czy została wciśnięta sekretna kombinacja klawiszy."""
        self._stack.push(keycode)
        
        if self._stack.compare(Game.SECRET_CODE):
            self._cheats = True
            
    def isSecretCodeActivated(self):
        """Metoda sprawdzająca, czy został aktywowany tajny kod"""
        return self._cheats