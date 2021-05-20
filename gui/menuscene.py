import pygame
from gui.button import Button
from gui.abstractscene import AbstractScene
from gui.gamescene import GameScene
from gui.counter import Counter

class MenuScene(AbstractScene):
    WIDTH = 176
    HEIGHT = 200
    COUNTER_DIGITS = 3
    BLACK = (0, 0, 0)
    ARROW_WIDTH = 60
    ARROW_HEIGHT = 24
    
    leftTexture = pygame.image.load('assets/left.png')
    rightTexture = pygame.image.load('assets/right.png')
    
    def __init__(self, sceneManager, x=8, y=8, mines=10):
        super().__init__(sceneManager)
        self._x = x
        self._y = y
        self._mines = mines
        self._font = pygame.font.SysFont(None, 24)
        
        self._xText = self._font.render('Szerokość:', True, MenuScene.BLACK)
        _, __, textX, textY = self._xText.get_rect()
        self._xTextX = (MenuScene.WIDTH // 2) - textX // 2
        self._xTextY = 10
        
        self._yText = self._font.render('Wysokość:', True, MenuScene.BLACK)
        _, __, textX, textY = self._yText.get_rect()
        self._yTextX = (MenuScene.WIDTH // 2) - textX // 2
        self._yTextY = 66
        
        self._mineText = self._font.render('Liczba min:', True, MenuScene.BLACK)
        _, __, textX, textY = self._mineText.get_rect()
        self._mineTextX = (MenuScene.WIDTH // 2) - textX // 2
        self._mineTextY = 116
        
        self._playText = self._font.render('Kliknij aby zagrać!', True, MenuScene.BLACK)
        _, __, textX, textY = self._playText.get_rect()
        self._playTextX = (MenuScene.WIDTH // 2) - textX // 2
        self._playTextY = 166
        self.playButton = Button(self._playTextX, self._playTextY, textX, textY, self._playText, self._startGame)
        
        xCounter_y = 30
        xCounter_x = (MenuScene.WIDTH // 2) - (Counter.WIDTH * MenuScene.COUNTER_DIGITS) // 2
        self.xCounter = Counter(xCounter_x, xCounter_y, MenuScene.COUNTER_DIGITS)
        self.xCounter.setValue(self._x)
        
        decXArrow_y = 30
        decXArrow_x = (MenuScene.WIDTH // 4) - (MenuScene.ARROW_WIDTH) // 2
        self.decXArrow = Button(decXArrow_x, decXArrow_y, MenuScene.ARROW_WIDTH, MenuScene.ARROW_HEIGHT, MenuScene.leftTexture, lambda: self._setX(self._x - 1))
        
        incXArrow_y = 30
        incXArrow_x = (MenuScene.WIDTH // 2) + (MenuScene.ARROW_WIDTH) // 2
        self.incXArrow = Button(incXArrow_x, incXArrow_y, MenuScene.ARROW_WIDTH, MenuScene.ARROW_HEIGHT, MenuScene.rightTexture, lambda: self._setX(self._x + 1))
        
        yCounter_y = 86
        yCounter_x = (MenuScene.WIDTH // 2) - (Counter.WIDTH * MenuScene.COUNTER_DIGITS) // 2
        self.yCounter = Counter(yCounter_x, yCounter_y, MenuScene.COUNTER_DIGITS)
        self.yCounter.setValue(self._y)
        
        decYArrow_y = 86
        decYArrow_x = (MenuScene.WIDTH // 4) - (MenuScene.ARROW_WIDTH) // 2
        self.decYArrow = Button(decYArrow_x, decYArrow_y, MenuScene.ARROW_WIDTH, MenuScene.ARROW_HEIGHT, MenuScene.leftTexture, lambda: self._setY(self._y - 1))
        
        incYArrow_y = 86
        incYArrow_x = (MenuScene.WIDTH // 2) + (MenuScene.ARROW_WIDTH) // 2
        self.incYArrow = Button(incYArrow_x, incYArrow_y, MenuScene.ARROW_WIDTH, MenuScene.ARROW_HEIGHT, MenuScene.rightTexture, lambda: self._setY(self._y + 1))
        
        mineCounter_y = 136
        mineCounter_x = (MenuScene.WIDTH // 2) - (Counter.WIDTH * MenuScene.COUNTER_DIGITS) // 2
        self.mineCounter = Counter(mineCounter_x, mineCounter_y, MenuScene.COUNTER_DIGITS)
        self.mineCounter.setValue(self._mines)
        
        mineDecArrow_y = 136
        mineDecArrow_x = (MenuScene.WIDTH // 4) - (MenuScene.ARROW_WIDTH) // 2
        self.mineDecArrow = Button(mineDecArrow_x,mineDecArrow_y, MenuScene.ARROW_WIDTH, MenuScene.ARROW_HEIGHT, MenuScene.leftTexture, lambda: self._setMines(self._mines - 1))
        
        mineIncArrow_y = 136
        mineIncArrow_x = (MenuScene.WIDTH // 2) + (MenuScene.ARROW_WIDTH) // 2
        self.mineIncArrow = Button(mineIncArrow_x, mineIncArrow_y, MenuScene.ARROW_WIDTH, MenuScene.ARROW_HEIGHT, MenuScene.rightTexture, lambda: self._setMines(self._mines + 1))
        
        sceneManager.resizeWindow(MenuScene.WIDTH, MenuScene.HEIGHT)
        self._buttons = [self.decXArrow, self.incXArrow, self.decYArrow, self.incYArrow, self.mineDecArrow, self.mineIncArrow, self.playButton]
        
    def _setX(self, x):
        self._x = max(0, x)
        
    def _setY(self, y):
        self._y = max(0, y)
        
    def _setMines(self, mines):
        self._mines = max(0, mines)
        
    def _startGame(self):
        self._sceneManager.setScene(GameScene(self._sceneManager, self._x, self._y, self._mines))
        
    def draw(self, window):
        self.xCounter.setValue(self._x)
        self.xCounter.draw(window)
        
        self.yCounter.setValue(self._y)
        self.yCounter.draw(window)
        
        self.mineCounter.setValue(self._mines)
        self.mineCounter.draw(window)
        
        for button in self._buttons:
            button.draw(window)
            
        window.blit(self._xText, (self._xTextX, self._xTextY))
        window.blit(self._yText, (self._yTextX, self._yTextY))
        window.blit(self._mineText, (self._mineTextX, self._mineTextY))
        
    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = event.pos
            
            for button in self._buttons:
                button.checkClicked(x, y)
        
        return True