from gui.scenemanager import SceneManager
from gui.gamescene import GameScene
import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
sceneManager = SceneManager()
sceneManager.setScene(GameScene(sceneManager))

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        run = sceneManager.handleEvent(event)

    window.fill((127, 127, 127))
    sceneManager.draw(window)
    pygame.display.flip()

pygame.quit()
exit()