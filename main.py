from logic.game import Game

import pygame

GAME_X = 8
GAME_Y = 8
GAME_MINES = 10

g = Game(GAME_X, GAME_Y, GAME_MINES)

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

openedTextures = [pygame.image.load('assets/{}.png'.format(i)) for i in range(9)]
closedTexture = pygame.image.load('assets/closed.png')
flaggedTexture = pygame.image.load('assets/flagged.png')
maybeTexture = pygame.image.load('assets/maybe.png')
mineTexture = pygame.image.load('assets/mine.png')

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not g.isEnd():
            x, y = event.pos
            
            logicX = x // 16
            logicY = y // 16
            
            g.leftClick(logicX, logicY)
            
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
            
            if g.isLost() and field.isMine():
                texture = mineTexture
            elif field.isClosed() and field.isFlagged():
                texture = flaggedTexture
            elif field.isClosed() and field.isMaybeMine():
                texture = maybeTexture
            elif field.isOpened():
                texture = openedTextures[field.getMinesNearby()]
                
            window.blit(texture, (16 * x, 16 * y))
    
    pygame.display.flip()

pygame.quit()
exit()