import random
from .field import Field

class Board:
    """Klasa reprezentująca planszę"""
    DIRECTIONS = [(-1, -1,), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    def __init__(self, width, height, mines):
        self._width = width
        self._height = height
        self._mines = mines
        self._board = []
        
        self._createBoard()
        
    def getWidth(self):
        """Metoda zwracająca szerokość planszy"""
        return self._width
        
    def getHeight(self):
        """Metoda zwracająca wysokość planszy"""
        return self._height
        
    def getMineCount(self):
        """Metoda zwracająca liczbę min na planszy"""
        return self._mines
        
    def _createBoard(self):
        """Metoda tworząca planszę"""
        for y in range(self._height):
            self._board.append([])
            for x in range(self._width):
                self._board[-1].append(Field(x, y))
                
    def printBoard(self):
        """Metoda wypisująca cała planszę w sposób tekstowy, używana do debuggowania"""
        for y in range(self._height + 1):
            for x in range(self._width + 1):
                if x == 0 and y == 0:
                    print("y/x", end="")
                    
                elif y == 0:
                    print(x, end="")
                    
                elif x == 0:
                    print(y, end="")
                    
                else:
                    field = self._board[y - 1][x - 1]
                    if field.isClosed():
                        print("?", end="")
                    elif field.isMine():
                        print("X", end="")
                    else:
                        print(field.getMinesNearby(), end="")
                    
                print("\t", end="")
                
            print("")
            
                
    def initBoard(self, excludeX, excludeY):
        """Metoda inicjalizująca planszę"""
        self._putMines(excludeX, excludeY)
                
    def _putMines(self, excludeX, excludeY):
        """Metoda ustawiająca miny na planszy, z pominięciem koordynatów które wskazał użytkownik odkrywając pierwsze pole"""
        positions = []
        for y in range(self._height):
            for x in range(self._width):
                if x == excludeX and y == excludeY:
                    continue
                positions.append((x, y))
                    
        random.shuffle(positions)
        
        for i in range(self._mines):
            x, y = positions[i]
            self._board[y][x].putMine()
            
        self._countNearbyMines()
            
    def _countNearbyMines(self):
        """Metoda zliczająca ile min jest w okolicy wszystkich pól na planszy"""
        for y in range(self._height):
            for x in range(self._width):
                currentCount = 0
                for dirX, dirY in Board.DIRECTIONS:
                    newX = x + dirX
                    newY = y + dirY
                    
                    if newX < 0 or newY < 0 or newX >= self._width or newY >= self._height:
                        continue
                        
                    if self._board[newY][newX].isMine():
                        currentCount += 1
                    
                self._board[y][x].setMinesNearby(currentCount)
                
    def openField(self, x, y):
        """Metoda otwierająca pole i sąsiadów pola o zadanych koordynatach, wywoływana rekurencyjnie"""
        field = self.getField(x, y)
        
        if field.isOpened():
            return
            
        if field.isMarked():
            return
            
        if field.isMine():
            field.open()
            return
            
        if field.getMinesNearby() > 0:
            field.open()
            return
               
        field.open()
            
        for dirX, dirY in Board.DIRECTIONS:
            newX = x + dirX
            newY = y + dirY
            
            if newX < 0 or newY < 0 or newX >= self._width or newY >= self._height:
                continue
                
            self.openField(newX, newY)
            
    def getField(self, x, y):
        """Metoda zwracająca Field o zadanych koordynatach""" 
        return self._board[y][x]