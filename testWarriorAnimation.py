from lib import  warrior
import pygame

pygame.init()

SCREEN = pygame.display.set_mode((1500, 750))
w = warrior.WarriorAnimation(SCREEN)

clock = pygame.time.Clock()

#test animation
while True:
    SCREEN.fill((180, 105, 150))
    
    ev = pygame.event.get()
   
    w.GetEvent(ev)

    
    w.Update(clock.get_time(), 60)
    

    pygame.display.update()
    clock.tick(60)

    