from logic.game import Game
from logic.stack import Stack
from gui.button import Button

import pygame

GAME_X = 8
GAME_Y = 8
GAME_MINES = 10
CHEATS = False

g = Game(GAME_X, GAME_Y, GAME_MINES)
stack = Stack(5)
secret_code = [120, 121, 122, 122, 121] #xyzzy

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

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

def startNewGame():
    global g
    global newGameButton
    g = Game(GAME_X, GAME_Y, GAME_MINES)
    newGameButton.setTexture(playingButtonTexture)

newGameButton = Button(300, 300, 26, 26, playingButtonTexture, startNewGame)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYUP:
            stack.push(event.key)
            
            if stack.compare(secret_code):
                CHEATS = True
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = event.pos
            
            newGameButton.checkClicked(x, y)
            
            if not g.isEnd():
                logicX = x // 16
                logicY = y // 16
                
                g.leftClick(logicX, logicY)
                
                if g.isLost():
                    newGameButton.setTexture(lostButtonTexture)
                    
                elif g.isWon():
                    newGameButton.setTexture(wonButtonTexture)
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and not g.isEnd():
            x, y = event.pos
            
            logicX = x // 16
            logicY = y // 16
            
            g.rightClick(logicX, logicY)

    window.fill((127, 127, 127))
    for y in range(GAME_Y):
        for x in range(GAME_X):
            field = g.getField(x, y)
            texture = closedTexture
            
            if g.isLost() and field.isMine() and g.getLastOpenedField() == field:
                texture = redMineTexture
            elif g.isLost() and field.isMine() and not field.isFlagged():
                texture = mineTexture
            elif g.isLost() and field.isFlagged() and not field.isMine():
                texture = wrongMineTexture
            elif field.isClosed() and field.isFlagged():
                texture = flaggedTexture
            elif field.isClosed() and field.isMaybeMine():
                texture = maybeTexture
            elif field.isOpened():
                texture = openedTextures[field.getMinesNearby()]
                
            window.blit(texture, (16 * x, 16 * y))
            if CHEATS and field.isMine():
                dark = pygame.Surface((16, 16), flags=pygame.SRCALPHA)
                dark.fill((50, 50, 50, 0))
                window.blit(dark, (16 * x, 16 * y), special_flags=pygame.BLEND_RGBA_SUB)
            
    newGameButton.draw(window)
    
    pygame.display.flip()

pygame.quit()
exit()