from lib import background, warrior, processor, camera, slime
import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1500, 750))
gr = background.Ground(SCREEN)
w = warrior.WarriorAnimation(SCREEN)
cam = camera.Camera(1500/ 2, 750 / 2, 5000, 750)
slime = slime.Slimes(SCREEN)
proc = processor.Processor(w, gr, cam, slime)


clock = pygame.time.Clock()

#test animation
while True:
    SCREEN.fill('#152238')
    
    ev = pygame.event.get()
    
    w.GetEvent(ev)
    
    proc.Update(60, SCREEN)


    pygame.display.update()
    clock.tick(60)
