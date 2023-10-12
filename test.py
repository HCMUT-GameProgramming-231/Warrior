from lib import spritesheet, warrior
import pygame

pygame.init()

SCREEN = pygame.display.set_mode((500, 500))
ss = spritesheet.spritesheet("./Assets/Warrior/Warrior_SheetnoEffect.png")

w = warrior.WarriorAnimation(SCREEN)

#print(ss.sheet.get_bounding_rect())
ss.sheet = pygame.transform.scale(ss.sheet, (300, 850))

clock = pygame.time.Clock()
index_x = 0
index_y = 0
#test to get all sprite in sprite sheet
frame = 0
clock.tick(60)
while True:
    SCREEN.fill((255, 255, 255))
    
    ev = pygame.event.get()
   
    w.GetEvent(ev)

    
    w.Update(clock.get_time(), 60, (250,250))
    

    pygame.display.update()
    clock.tick(60)

    