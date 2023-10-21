from .spritesheet import spritesheet
import pygame

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, SCREEN, map):
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
        
        tile_map = open(map,'r')
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
            if gr[1].right < 0 or gr[1].left > 1500: continue
            #if self.map[i][-2] == 98: print(self.map[i][-2], self.map[i][1])
            self.SCREEN.blit(gr[0], gr[1])
                #pygame.draw.rect(self.SCREEN, (255, 0, 0), self.map[i][1])
                
    def Move(self, x, y):
        for i in range(len(self.map)):
            self.map[i][1].move_ip(x, y)

class Flame(pygame.sprite.Sprite):
    
    def __init__(self, screen, pos):
        self.rect = pygame.Rect(pos, (50, 50))
        self.screen = screen
        self.frameNum = 0
        self.spritesheet = spritesheet('./Assets/Background/TX FX Flame.png')
        self.spritesheet.sheet = pygame.transform.scale(self.spritesheet.sheet, (300, 300))
        self.animation = []
        
        i = 0
        index_x = 0
        index_y = 0
        while i < 36:
            img = self.spritesheet.image_at((index_x*50, index_y*50, 50, 50), -1)
            self.animation.append(img)
            i+=1
            index_x += 1
            if index_x == 6:
                index_y += 1
                index_x = 0
        
        self.status = 'burning'
                
    def GetActiveFrame(self):
        """
        if self.status == 'burning':
            self.frameNum += 0.2
        else:
            self.frameNum += 0.03
            
        if self.status == 'burning':
            if self.frameNum >= 25:
                self.frameNum = 15
        else:
            if self.frameNum >= 36:
                self.frameNum = 35
        """
        self.frameNum += 0.25
        if self.frameNum >= 27:
            self.frameNum = 14
            
        return self.animation[int(self.frameNum)]
    
    def Update(self):
        if self.rect.right < 0 or self.rect.left > 1500: return
        frame = self.GetActiveFrame()
        self.screen.blit(frame, self.rect)
        
    def Move(self, x, y):
        self.rect.move_ip(x, y)
        

class VillageObject(pygame.sprite.Sprite):
    
    def __init__(self, sprite, pos, size, screen):
        self.sprite = sprite
        self.rect = pygame.Rect(pos, size)
        self.screen = screen
    
    def Update(self):
        self.screen.blit(self.sprite, self.rect)
        
    def Move(self, x, y):
        self.rect.move_ip(x, y)
        
class VillageObjects:
    
    def __init__(self) -> None:
        self.spritesheet = spritesheet('./Assets/Background/TX Village Props.png')
        
        #boxes
        self.box_1 = self.spritesheet.image_at((10, 0, 100, 80), -1) #1
        self.box_2 = self.spritesheet.image_at((110, 0, 80, 80), -1) #2
        self.box_3 = self.spritesheet.image_at((180, 0, 60, 80), -1) #3
        
        #archery target
        self.target = self.spritesheet.image_at((700, 20, 80, 60), -1) #4
        
        #pan
        self.pan = self.spritesheet.image_at((780, 0, 80, 80), -1) #5
        
        #cross
        self.cross = self.spritesheet.image_at((850, 0, 80, 80), -1) #6
        
        #lamp
        self.lamp_on = self.spritesheet.image_at((960, 0, 30, 30), -1) #7
        self.lamp_off = self.spritesheet.image_at((1000, 0, 30, 30), -1) #8
        self.col = self.spritesheet.image_at((935, 30, 30, 100), -1) #9 cây cột đèn
        self.row = self.spritesheet.image_at((970, 35, 50, 30), -1) #10 thanh ngang đèn
        
        #well
        self.well = self.spritesheet.image_at((20, 150, 100, 150), -1) #11
        
        #scarecrow
        
        #tree
        
        #grave
        
    def Generate(self, pos, type, screen):
        if type == 1:
            return VillageObject(self.box_1, pos, self.box_1.get_size(), screen)
        elif type == 2:
            return VillageObject(self.box_2, pos, self.box_2.get_size(), screen )
        elif type == 3:
            return VillageObject(self.box_3, pos, self.box_3.get_size(), screen )
        elif type == 4:
            return VillageObject(self.target, pos, self.target.get_size(), screen )
        elif type == 5:
            return VillageObject(self.pan, pos, self.pan.get_size(), screen )
        elif type == 6:
            return VillageObject(self.cross, pos, self.cross.get_size(), screen )
        elif type == 7:
            return VillageObject(self.lamp_on, pos, self.lamp_on.get_size(), screen )
        elif type == 8:
            return VillageObject(self.lamp_off, pos, self.lamp_off.get_size(), screen )
        elif type == 9:
            return VillageObject(self.col, pos, self.col.get_size(), screen )
        elif type == 10:
            return VillageObject(self.row, pos, self.row.get_size(), screen )
        elif type == 11:
             return VillageObject(self.well, pos, self.well.get_size(), screen )
        

    
        
        