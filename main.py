from gui.scenemanager import SceneManager
from gui.gamescene import GameScene
import pygame

pygame.init()
clock = pygame.time.Clock()
sceneManager = SceneManager(800, 600)
sceneManager.setScene(GameScene(sceneManager, 2, 2, 2))

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        run = sceneManager.handleEvent(event)

    sceneManager.draw()
    pygame.display.flip()

pygame.quit()
exit()