from lib import background, warrior, processor, camera
import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1500, 750))
bg = background.Ground(SCREEN)
w = warrior.WarriorAnimation(SCREEN)
cam = camera.Camera(1500/ 2, 750 / 2, 5000, 750)
proc = processor.Processor(w, bg, cam)

clock = pygame.time.Clock()

#test animation
while True:
    SCREEN.fill((180, 105, 150))
    
    ev = pygame.event.get()
    
    w.GetEvent(ev)
    
    proc.Update(60, SCREEN)


    pygame.display.update()
    clock.tick(60)
