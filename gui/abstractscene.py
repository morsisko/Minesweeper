import abc

class AbstractScene(metaclass=abc.ABCMeta):
    """Klasa abstrakcyjna reprezentująca scenę"""
    def __init__(self, sceneManager):
        self._sceneManager = sceneManager
        
    @abc.abstractmethod
    def draw(self, window):
        """Wirtualna metoda, rysująca scenę"""
        raise NotImplementedError()
        
    @abc.abstractmethod
    def handleEvent(self, event):
        """Wirtualna metoda obsługująca eventy przesyłane do okna gry"""
        raise NotImplementedError()