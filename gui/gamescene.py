import pygame
from logic.game import Game
from gui.button import Button
from gui.abstractscene import AbstractScene
from gui.counter import Counter


class GameScene(AbstractScene):
    """Klasa reprezentująca scenę gry"""
    TILE_SIZE = 16
    SMILE_BUTTON_SIZE = 26
    START_BOARD_Y = 35
    MINIMUM_WINDOW_WIDTH = 176
    SMILE_BUTTON_X = 5
    MINE_COUNTER_X = 5
    TIME_COUNTER_X = 5
    COUNTER_DIGITS = 3
    
    openedTextures = [pygame.image.load('assets/{}.png'.format(i)) for i in range(9)]
    closedTexture = pygame.image.load('assets/closed.png')
    flaggedTexture = pygame.image.load('assets/flagged.png')
    maybeTexture = pygame.image.load('assets/maybe.png')
    mineTexture = pygame.image.load('assets/mine.png')
    redMineTexture = pygame.image.load('assets/redmine.png')
    wrongMineTexture = pygame.image.load('assets/wrong.png')

    playingButtonTexture = pygame.image.load('assets/playing.png')
    lostButtonTexture = pygame.image.load('assets/lost.png')
    wonButtonTexture = pygame.image.load('assets/won.png')
    
    def startNewGame(self):
        """Metoda startująca nową grę"""
        from gui.menuscene import MenuScene
        self._sceneManager.setScene(MenuScene(self._sceneManager, self._x, self._y, self._mines))
    
    def __init__(self, sceneManager, x, y, mines):
        super().__init__(sceneManager)
        
        self._x = x
        self._y = y
        self._mines = mines
        self._board_y = GameScene.START_BOARD_Y
        self.g = Game(x, y, mines)
        
        windowHeight = self._board_y + self._y * GameScene.TILE_SIZE
        windowWidth = max(self._y * GameScene.TILE_SIZE, GameScene.MINIMUM_WINDOW_WIDTH)
        self._board_x = windowWidth // 2 - (self._x * GameScene.TILE_SIZE) // 2
        
        smileButtonY = GameScene.SMILE_BUTTON_X
        smileButtonX = windowWidth // 2 - GameScene.SMILE_BUTTON_SIZE // 2
        self.newGameButton = Button(smileButtonX, smileButtonY, GameScene.SMILE_BUTTON_SIZE, GameScene.SMILE_BUTTON_SIZE, GameScene.playingButtonTexture, self.startNewGame)
        
        mineCounterY = GameScene.MINE_COUNTER_X
        mineCounterX = (windowWidth // 4) - (Counter.WIDTH * GameScene.COUNTER_DIGITS) // 2
        self.mineCounter = Counter(mineCounterX, mineCounterY, GameScene.COUNTER_DIGITS)
        self.mineCounter.setValue(self._mines)
        
        timeCounterY = GameScene.TIME_COUNTER_X
        timeCounterX = ((windowWidth // 2) + (windowWidth // 4)) - (Counter.WIDTH * GameScene.COUNTER_DIGITS) // 2
        self.timeCounter = Counter(timeCounterX, timeCounterY, GameScene.COUNTER_DIGITS)
        self.timeCounter.setValue(0)
        
        sceneManager.resizeWindow(windowWidth, windowHeight)
        
    def draw(self, window):
        """Metoda rysująca scenę"""
        self.timeCounter.setValue(self.g.getTimePlayingInSeconds())
        
        for y in range(self._y):
            for x in range(self._x):
                field = self.g.getField(x, y)
                texture = GameScene.closedTexture
                
                if self.g.isLost() and field.isMine() and self.g.getLastOpenedField() == field:
                    texture = GameScene.redMineTexture
                elif self.g.isLost() and field.isMine() and not field.isFlagged():
                    texture = GameScene.mineTexture
                elif self.g.isLost() and field.isFlagged() and not field.isMine():
                    texture = GameScene.wrongMineTexture
                elif field.isClosed() and field.isFlagged():
                    texture = GameScene.flaggedTexture
                elif field.isClosed() and field.isMaybeMine():
                    texture = GameScene.maybeTexture
                elif field.isOpened():
                    texture = GameScene.openedTextures[field.getMinesNearby()]
                    
                window.blit(texture, (self._board_x + GameScene.TILE_SIZE * x, self._board_y + GameScene.TILE_SIZE * y))
                if self.g.isSecretCodeActivated() and field.isMine():
                    dark = pygame.Surface((GameScene.TILE_SIZE, GameScene.TILE_SIZE), flags=pygame.SRCALPHA)
                    dark.fill((50, 50, 50, 0))
                    window.blit(dark, (self._board_x + GameScene.TILE_SIZE * x, self._board_y + GameScene.TILE_SIZE * y), special_flags=pygame.BLEND_RGBA_SUB)
                
        self.newGameButton.draw(window)
        self.mineCounter.draw(window)
        self.timeCounter.draw(window)
        
    def handleEvent(self, event):
        """Metoda obsługująca eventy sceny"""
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.KEYUP:
            self.g.addKeypress(event.key)
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = event.pos
            
            self.newGameButton.checkClicked(x, y)
            
            if not self.g.isEnd():
                logicX = (x - self._board_x) // GameScene.TILE_SIZE
                logicY = (y - self._board_y) // GameScene.TILE_SIZE
                
                self.g.leftClick(logicX, logicY)
                
                if self.g.isLost():
                    self.newGameButton.setTexture(GameScene.lostButtonTexture)
                    
                elif self.g.isWon():
                    self.newGameButton.setTexture(GameScene.wonButtonTexture)
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and not self.g.isEnd():
            x, y = event.pos
            
            logicX = (x - self._board_x) // GameScene.TILE_SIZE
            logicY = (y - self._board_y) // GameScene.TILE_SIZE
            
            self.g.rightClick(logicX, logicY)
            self.mineCounter.setValue(self._mines - self.g.getFlaggedFieldsCount())
            
            if self.g.isLost():
                self.newGameButton.setTexture(GameScene.lostButtonTexture)
                
            elif self.g.isWon():
                self.newGameButton.setTexture(GameScene.wonButtonTexture)
                
        return True