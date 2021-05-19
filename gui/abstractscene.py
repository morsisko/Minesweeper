class AbstractScene:
    def __init__(self, sceneManager):
        self._sceneManager = sceneManager
        
    def draw(self, window):
        raise NotImplementedError()
        
    def handleEvent(self, event):
        raise NotImplementedError()