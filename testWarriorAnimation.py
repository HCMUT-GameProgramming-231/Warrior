from lib import  warrior
import pygame

pygame.init()

SCREEN = pygame.display.set_mode((500, 500))
w = warrior.WarriorAnimation(SCREEN)

clock = pygame.time.Clock()

#test animation
while True:
    SCREEN.fill((255, 255, 255))
    
    ev = pygame.event.get()
   
    w.GetEvent(ev)

    
    w.Update(clock.get_time(), 60, (250,250))
    

    pygame.display.update()
    clock.tick(60)

    