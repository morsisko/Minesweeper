import abc

class AbstractScene(metaclass=abc.ABCMeta):
    def __init__(self, sceneManager):
        self._sceneManager = sceneManager
        
    @abc.abstractmethod
    def draw(self, window):
        raise NotImplementedError()
        
    @abc.abstractmethod
    def handleEvent(self, event):
        raise NotImplementedError()