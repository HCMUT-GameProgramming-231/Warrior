from lib.slime import Slimes
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((1500, 750))
slimes = Slimes(SCREEN)
slimes.Generate((750, 300))

while True:
    SCREEN.fill((255, 255, 255))
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
        
    keystate = pygame.key.get_pressed()
    
    if keystate[pygame.K_LEFT]:
        slimes.slimes[0].direction = 'left'
        slimes.slimes[0].current_status = 'move'
        slimes.slimes[0].moving = True
    
    if keystate[pygame.K_UP]:
        slimes.slimes[0].jumping = True
        slimes.slimes[0].current_status = 'jump'
        

    
    slimes.Update()
    
    pygame.display.update()
    
