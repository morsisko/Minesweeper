import pygame
class Counter:
    WIDTH = 13
    HEIGHT = 26
    TEXTURES = [pygame.image.load('assets/counter_{}.png'.format(i)) for i in range(10)]
    def __init__(self, x, y, digits):
        self._x = x
        self._y = y
        self._value = 0
        self._digits = digits
        
    def setValue(self, value):
        self._value = value
    
    def draw(self, window):
        valueToDraw = min(10 ** self._digits - 1, self._value)
        valueToDraw = max(0, self._value)
        
        currentDigitPower = 10 ** (self._digits - 1)
        
        for i in range(self._digits):
            toDraw = int((self._value // currentDigitPower) % 10)
            window.blit(Counter.TEXTURES[toDraw], (self._x + (Counter.WIDTH * i), self._y))
            
            currentDigitPower /= 10 