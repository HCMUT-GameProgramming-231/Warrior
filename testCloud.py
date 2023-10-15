import pygame
from lib.background import Cloud


pygame.init()

SCREEN = pygame.display.set_mode((1500, 750), vsync=1)
cloud = Cloud(SCREEN)

clock = pygame.time.Clock()

#test animation
while True:
    SCREEN.fill('#152238')
    
    ev = pygame.event.get()
   
    for e in ev:
        if e.type == pygame.QUIT:
            pygame.quit()

    cloud.Update()    

    pygame.display.update()
    clock.tick(60)
