class Stack:
    """Klasa do obsługi stosu o zadanym rozmiarze, wykorzystywana do przechowywania ostatnio wciśniętch klawiszy w celu zdecydowania, kiedy uruchomić podświetlanie pól z minami w wyniku wpisania specjalnego kodu"""
    def __init__(self, size):
        self._size = size
        self._data = []
        
    def push(self, item):
        """Dodawanie elementu na koniec stosu, usuwanie elementu z początku jeżeli rozmiar stosu został przekroczony"""
        self._data.append(item)
        
        if len(self._data) > self._size:
            self._data.pop(0)
            
    def compare(self, other):
        """Metoda zwracająca True jeżeli lista `other` jest równa aktualnej zawartości stosu"""
        if len(self._data) != len(other):
            return False
            
        for i in range(len(other)):
            if self._data[i] != other[i]:
                return False
                
        return True