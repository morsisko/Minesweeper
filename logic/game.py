import time
from logic.exceptions import MinesweeperException, BoardTooSmallException, BoardTooBigException, TooManyMinesException, TooLittleMinesException
from .board import Board

class Game:
    WAITING = -1
    STARTED = 0
    LOST = 1
    WON = 2
    MAX_BOARD_SIZE = 15
    MIN_BOARD_SIZE = 2
    
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
        
    def _doActionBasingOnGameState(self):            
        if self._state == Game.WON:
            self._gameEndedTimestamp = int(time.time() * 1000)
            print("Zwyciestwo")
            
        elif self._state == Game.LOST:
            self._gameEndedTimestamp = int(time.time() * 1000)
            print("Porazka")
        
    def _checkGameState(self):
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
        if x < 0 or y < 0 or x >= self._board.getWidth() or y >= self._board.getHeight():
            return
            
        field = self._board.getField(x, y)
        field.onRightClick()
        
        self._checkGameState()  
        
    def leftClick(self, x, y):
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
        return self._state == Game.WON or self._state == Game.LOST
        
    def isWon(self):
        return self._state == Game.WON

    def isLost(self):
        return self._state == Game.LOST
        
    def getField(self, x, y):
        return self._board.getField(x, y)
        
    def getLastOpenedField(self):
        return self._lastOpenedField
        
    def getFlaggedFieldsCount(self):
        result = 0
        for y in range(self._board.getHeight()):
            for x in range(self._board.getWidth()):
                if self._board.getField(x, y).isFlagged():
                    result += 1
                    
        return result
        
    def getTimePlayingInSeconds(self):
        if self._gameStartedTimestamp == 0:
            return 0
            
        if self._gameEndedTimestamp == 0:
            return (int(time.time() * 1000) - self._gameStartedTimestamp) // 1000
            
        return (self._gameEndedTimestamp - self._gameStartedTimestamp) // 1000