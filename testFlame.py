from lib.background import Flame, VillageObjects, VillageObject
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((1500, 750))
vil = VillageObjects()
o = []

pos = open('./Map/villageobject.txt', 'r')
for i, line in enumerate(pos):
    if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
    line = line.replace('\n', '')
    elements = line.split(' ')
    p = [int(ele) for ele in elements]
    o += [vil.Generate((p[0], p[1]), p[2], SCREEN)]

while True:
    SCREEN.fill((255, 255, 100))
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
        
    keystate = pygame.key.get_pressed()
    
    for i in o:
        i.Update()
    
    pygame.display.update()
    
