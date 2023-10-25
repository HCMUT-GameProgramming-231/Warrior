from lib import background, warrior, processor, camera, slime, menu
import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()


SCREEN = pygame.display.set_mode((1500, 750))
gr = background.Ground(SCREEN, './Map/map.txt')
w = warrior.WarriorAnimation(SCREEN)
cam = camera.Camera(1500/ 2, 750 / 2, 6000, 750)
menu = menu.MainMenu(SCREEN, 1500, 750, w.name)
proc = processor.Processor(SCREEN, w, gr, cam, menu)


clock = pygame.time.Clock()

#test animation
while True:
    SCREEN.fill('#152238')
    
    proc.Update(60)


    pygame.display.update()
    clock.tick(60)
    #print(clock.get_fps())
