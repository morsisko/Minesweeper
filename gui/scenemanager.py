class SceneManager:
    def __init__(self):
        pass
        
    def setScene(self, scene):
        self._scene = scene
        
    def draw(self, window):
        self._scene.draw(window)
        
    def handleEvent(self, event):
        return self._scene.handleEvent(event)