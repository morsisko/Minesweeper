class MinesweeperException(Exception):
    """Base class for other exceptions"""
    pass
    
class BoardTooSmallException(MinesweeperException):
    pass
    
class BoardTooBigException(MinesweeperException):
    pass
    
class TooManyMinesException(MinesweeperException):
    pass
    
class TooLittleMinesException(MinesweeperException):
    pass