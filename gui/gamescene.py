import pygame
from logic.stack import Stack
from logic.game import Game
from gui.button import Button
from gui.abstractscene import AbstractScene
from gui.counter import Counter


class GameScene(AbstractScene):
    TILE_SIZE = 16
    SMILE_BUTTON_SIZE = 26
    GAME_X = 8
    GAME_Y = 8
    GAME_MINES = 10
    CHEATS = False
    SECRET_CODE = [120, 121, 122, 122, 121] #xyzzy
    
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
        self._sceneManager.setScene(GameScene(self._sceneManager))
    
    def __init__(self, sceneManager):
        super().__init__(sceneManager)
        
        
        self._board_y = 35
        
        windowHeight = self._board_y + GameScene.GAME_Y * GameScene.TILE_SIZE
        windowWidth = max(GameScene.GAME_Y * GameScene.TILE_SIZE, 176)
        self._board_x = windowWidth // 2 - (GameScene.GAME_X * GameScene.TILE_SIZE) // 2
        
        smileButtonY = 5
        smileButtonX = windowWidth // 2 - GameScene.SMILE_BUTTON_SIZE // 2
        self.newGameButton = Button(smileButtonX, smileButtonY, GameScene.SMILE_BUTTON_SIZE, GameScene.SMILE_BUTTON_SIZE, GameScene.playingButtonTexture, self.startNewGame)
        
        mineCounterY = 5
        mineCounterX = (windowWidth // 4) - (Counter.WIDTH * 3) // 2
        self.mineCounter = Counter(mineCounterX, mineCounterY, 3)
        self.mineCounter.setValue(GameScene.GAME_MINES)
        
        timeCounterY = 5
        timeCounterX = ((windowWidth // 2) + (windowWidth // 4)) - (Counter.WIDTH * 3) // 2
        self.timeCounter = Counter(timeCounterX, timeCounterY, 3)
        self.timeCounter.setValue(0)
        
        sceneManager.resizeWindow(windowWidth, windowHeight)
        
        self.stack = Stack(len(GameScene.SECRET_CODE))
        
        self.g = Game(GameScene.GAME_X, GameScene.GAME_Y,GameScene.GAME_MINES)
        
    def draw(self, window):
        self.timeCounter.setValue(self.g.getTimePlayingInSeconds())
        
        for y in range(GameScene.GAME_Y):
            for x in range(GameScene.GAME_X):
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
                if GameScene.CHEATS and field.isMine():
                    dark = pygame.Surface((GameScene.TILE_SIZE, GameScene.TILE_SIZE), flags=pygame.SRCALPHA)
                    dark.fill((50, 50, 50, 0))
                    window.blit(dark, (self._board_x + GameScene.TILE_SIZE * x, self._board_y + GameScene.TILE_SIZE * y), special_flags=pygame.BLEND_RGBA_SUB)
                
        self.newGameButton.draw(window)
        self.mineCounter.draw(window)
        self.timeCounter.draw(window)
        
    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.KEYUP:
            self.stack.push(event.key)
            
            if self.stack.compare(GameScene.SECRET_CODE):
                GameScene.CHEATS = True
            
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
            self.mineCounter.setValue(GameScene.GAME_MINES - self.g.getFlaggedFieldsCount())
            print(self.g.getFlaggedFieldsCount() - GameScene.GAME_MINES)
            
            if self.g.isLost():
                self.newGameButton.setTexture(GameScene.lostButtonTexture)
                
            elif self.g.isWon():
                self.newGameButton.setTexture(GameScene.wonButtonTexture)
                
        return True