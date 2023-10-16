from .spritesheet import spritesheet
import pygame

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, SCREEN):
        self.SCREEN = SCREEN
        #ground
        self.spritesheet_ground = spritesheet('./Assets/Background/TX Tileset Ground.png')
        
        self.big_ground = self.spritesheet_ground.image_at((0, 0, 95, 100), -1) #1
        #self.big_ground = pygame.transform.scale(self.big_ground, (00, 100)) 
        self.medium_ground = self.spritesheet_ground.image_at((127, 0, 65, 70), -1) #2
        self.medium_y_ground = self.spritesheet_ground.image_at((225, 0, 35, 70), -1) #3
        self.medium_x_ground = self.spritesheet_ground.image_at((289, 0, 60, 40), -1) #4
        self.small_ground = self.spritesheet_ground.image_at((125, 95, 35, 35), -1) #5
        self.abnormal_ground = self.spritesheet_ground.image_at((390, 0, 55, 70), -1) #6
        self.long_y_ground = self.spritesheet_ground.image_at((0, 255, 35, 100), -1) #7
        self.long_x_ground = self.spritesheet_ground.image_at((0, 385, 95, 35), -1) #8
        self.wall_hole = self.spritesheet_ground.image_at((0, 125, 95, 100), -1) #9
        self.wall = self.spritesheet_ground.image_at((330, 180, 95, 100)) #10
        
        self.ground_list = [self.big_ground, self.medium_ground, self.medium_y_ground, self.medium_x_ground,\
            self.small_ground, self.abnormal_ground, self.long_y_ground, self.long_x_ground, self.wall_hole, self.wall]
        
        
        self.tile_map = []
        
        tile_map = open('./Map/map.txt','r')
        for i,line in enumerate(tile_map):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            self.tile_map += [[ele for ele in elements if ele != '']]
        tile_map.close()
        
        self.map = []
        rect = pygame.Rect(0, 0, 0, 0)
        i = 0
        for y in range(len(self.tile_map)):
            for x in range(len(self.tile_map[y])):
                tile = int(self.tile_map[y][x][0])
                if tile == 0:
                    num = int(self.tile_map[y][x][2:])
                    rect.x += 20 * num
                else:
                    tile = int(self.tile_map[y][x])
                    gr_rect = self.ground_list[tile - 1].get_rect()
                    rect.h  = gr_rect.h
                    rect.w = gr_rect.w
                    self.map += [(self.ground_list[tile-1], pygame.Rect(rect), i, tile)]
                    rect.x += gr_rect.w
                i += 1

            rect.x = 0
            rect.y += 50


            
        
    def Update(self):
        for gr in self.map:
            #if self.map[i][-2] == 98: print(self.map[i][-2], self.map[i][1])
            self.SCREEN.blit(gr[0], gr[1])
                #pygame.draw.rect(self.SCREEN, (255, 0, 0), self.map[i][1])
                
    def Move(self, x, y):
        for i in range(len(self.map)):
            self.map[i][1].move_ip(x, y)
                