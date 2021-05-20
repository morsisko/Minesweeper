import pygame

class SceneManager:
    def __init__(self, width, height):
        self.resizeWindow(width, height) 
        
    def resizeWindow(self, width, height):
        self._window = pygame.display.set_mode((width, height))
    
    def setScene(self, scene):
        self._scene = scene
        
    def draw(self):
        self._window.fill((192, 192, 192))
        self._scene.draw(self._window)
        
    def handleEvent(self, event):
        return self._scene.handleEvent(event)