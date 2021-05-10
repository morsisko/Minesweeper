from .board import Board

class Game:
    WAITING = -1
    STARTED = 0
    LOST = 1
    WON = 2
    
    def __init__(self, width, height, mines):
        self._board = Board(width, height, mines)
        self._state = Game.WAITING
        
    def leftClick(self, x, y):
        if self.state == Game.WAITING:
            self.state = Game.STARTED
            self._board.initBoard(x, y)
            
        self._board.open(x, y)