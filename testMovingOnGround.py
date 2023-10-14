from lib import background, warrior, processor
import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1500, 750))
bg = background.Ground(SCREEN)
w = warrior.WarriorAnimation(SCREEN)
proc = processor.Processor(w, bg)

clock = pygame.time.Clock()

#test animation
while True:
    SCREEN.fill((180, 105, 150))
    
    ev = pygame.event.get()
    
    w.GetEvent(ev)
    
    proc.Update(60)


    pygame.display.update()
    clock.tick(60)
