class MinesweeperException(Exception):
    """Klasa bazowa dla wyjątków"""
    pass
    
class BoardTooSmallException(MinesweeperException):
    """Wyjątek informujący, że podane wymiary planszy są zbyt małe"""
    pass
    
class BoardTooBigException(MinesweeperException):
    """Wyjątek informujący, że podane wymiary planszy są zbyt duże"""
    pass
    
class TooManyMinesException(MinesweeperException):
    """Wyjątek informujący, że podana liczba min jest zbyt duża dla aktualnych wymiarów planszy"""
    pass
    
class TooLittleMinesException(MinesweeperException):
    """Wyjątek informujący, że podana liczba min jest zbyt mała dla aktualnych wymiarów planszy"""
    pass