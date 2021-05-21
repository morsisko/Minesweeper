import pygame

class SceneManager:
    """Klasa zarządzająca scenami"""
    def __init__(self, width, height):
        self.resizeWindow(width, height) 
        
    def resizeWindow(self, width, height):
        """Metoda zmieniająca rozmiar okna"""
        self._window = pygame.display.set_mode((width, height))
    
    def setScene(self, scene):
        """Metoda ustawiająca aktualną scenę"""
        self._scene = scene
        
    def draw(self):
        """Metoda rysująca aktualną scenę"""
        self._window.fill((192, 192, 192))
        self._scene.draw(self._window)
        
    def handleEvent(self, event):
        """Metoda przekazująca aktualny event do aktualnej sceny"""
        return self._scene.handleEvent(event)