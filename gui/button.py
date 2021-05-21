class Button:
    """Klasa reprezentująca przycisk, po kliknięciu którego wywoływana jest określona funkcja"""
    def __init__(self, x, y, width, height, texture, on_click):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._texture = texture
        self._on_click = on_click
        
    def setTexture(self, texture):
        """Metoda ustawiająca teksturę przycisku"""
        self._texture = texture
        
    def draw(self, window):
        """Metoda rysująca przycisk"""
        window.blit(self._texture, (self._x, self._y))
        
    def checkClicked(self, mouseX, mouseY):
        """Metoda sprawdzająca czy przycisk został kliknięty, jeżeli tak, to wywoływana jest wcześniej określona funkcja"""
        if (self._x < mouseX and mouseX < self._x + self._width):
            if (self._y < mouseY and mouseY < self._y + self._height):
                self._on_click()