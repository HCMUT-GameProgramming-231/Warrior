from .spritesheet import spritesheet
import pygame

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, SCREEN):
        self.SCREEN = SCREEN
        #ground
        self.spritesheet_ground = spritesheet('./Assets/Background/TX Tileset Ground.png')
        
        self.big_ground = self.spritesheet_ground.image_at((0, 0, 100, 100), -1)
        #self.big_ground = pygame.transform.scale(self.big_ground, (00, 100))
        self.medium_ground = self.spritesheet_ground.image_at((120, 0, 80, 80), -1)
        self.medium_y_ground = self.spritesheet_ground.image_at((220, 0, 40, 80), -1)
        self.medium_x_ground = self.spritesheet_ground.image_at((280, 0, 80, 40), -1)
        self.small_ground = self.spritesheet_ground.image_at((120, 90, 50, 50), -1)
        self.abnormal_ground = self.spritesheet_ground.image_at((380, 0, 80, 80), -1)
        self.long_y_ground = self.spritesheet_ground.image_at((0, 250, 50, 110), -1)
        self.long_x_ground = self.spritesheet_ground.image_at((0, 380, 110, 50), -1)
        self.wall_hole = self.spritesheet_ground.image_at((0, 120, 120, 120), -1)
        self.wall = self.spritesheet_ground.image_at((330, 180, 100, 100))
        
        #background object
        self.spritesheet_object = spritesheet('./Assets/Background/TX Village Props.png')
        
        self.box_1 = self.spritesheet_object.image_at((20, 0, 100, 80), -1)
        self.box_2 = self.spritesheet_object.image_at((120, 0, 60, 80), -1)
        self.box_3 = self.spritesheet_object.image_at((190, 0, 60, 80), -1)
        
        self.tile_map = []
        
        tile_map = open('./Map/map.txt','r')
        for i,line in enumerate(tile_map):
            line = line.replace('\n', '')
            elements = line.split(' ')
            self.tile_map += [[int(ele) for ele in elements]]
        tile_map.close()
        
        self.map = []
        rect = pygame.Rect(0, 0, 0, 0)
        for y in range(len(self.tile_map)):
            line = []
            for x in range(len(self.tile_map[y])):
                tile = self.tile_map[y][x]
                if tile == 0:
                    rect.x += 100
                    line += [(rect)]
                elif tile == 1:
                    gr_rect = self.big_ground.get_rect()
                    rect.h  = gr_rect.h
                    rect.w = gr_rect.w
                    line += [(self.big_ground, pygame.Rect(rect))]
                    rect.x += gr_rect.w - 8
  
            self.map += [line]
            rect.x = 0
            rect.y += 100

            
        
    def Update(self):
        
        for index_y in range(len(self.map)):
            for index_x in range(len(self.map[index_y])):
                if self.tile_map[index_y][index_x] == 1:
                    rect = self.map[index_y][index_x][1]
                    self.SCREEN.blit(self.map[index_y][index_x][0], self.map[index_y][index_x][1])

                    print(self.map[index_y][index_x][1])