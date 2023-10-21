from .spritesheet import spritesheet
import pygame
import random

class Chest(pygame.sprite.Sprite):
    
    def __init__(self, screen, pos, animation, hole, wall, type):
        self.screen = screen
        self.rect = pygame.Rect(pos, (75, 75))
        self.frameNum = 0
        self.animation = animation
        self.hole = hole
        self.wall = wall
        self.hole_rect = pygame.Rect(pos, (95, 95))
        
        self.hidden = True
        self.close = True
        
        if type == 0:
            self.hole_rect.x -= 15
            self.hole_rect.y += 5
        elif type == 1:
            self.hole_rect.x -= 15
            self.hole_rect.y += 5
        elif type == 2:
            self.hole_rect.x -= 23
            self.hole_rect.y += 5
        else:
            self.hole_rect.x -= 30
            self.hole_rect.y += 5
    
    def UnHidden(self, warrior_rect):
        if abs(self.rect.x - warrior_rect.x) > 50: return
        if self.rect.colliderect(warrior_rect):
            if self.hidden:
                self.hidden = False
            else:
                self.close = False
        
    
    def Move(self, x, y):
        self.rect.move_ip(x, y)
        self.hole_rect.move_ip(x, y)
        
    def Update(self):
        if self.hole_rect.right < 0 or self.rect.left > 1500: return
        frame = self.GetActiveFrame()
        self.screen.blit(self.hole, self.hole_rect)
        self.screen.blit(frame, self.rect)
        if self.hidden:
            self.screen.blit(self.wall, self.hole_rect)
    
    def GetActiveFrame(self):
        if self.close:
            return self.animation[0]
        else:
            self.frameNum += 0.1
            if self.frameNum >= 4:
                self.frameNum = 4
            return self.animation[int(self.frameNum)]
        
class Chests:
    def __init__(self):
        self.spritesheet = spritesheet('./Assets/Background/TX Chest Animation.png')
        self.spritesheet.sheet = pygame.transform.scale(self.spritesheet.sheet, (75 * 7, 75 * 8))
        
        wallsheet = spritesheet('./Assets/Background/TX Tileset Ground.png')
        self.hole = wallsheet.image_at((0, 125, 95, 100), -1)
        self.wall = wallsheet.image_at((330, 180, 95, 100))
        
        self.chest_1_animation = []
        self.chest_2_animation = []
        self.chest_3_animation = []
        self.chest_4_animation = []
        
        i = 0
        index_x = 0.1
        index_y = 0
        while i < 28:
            img = self.spritesheet.image_at((11 + i+ index_x * 65, index_y * 75, 60, 75), -1)
            if index_y == 0:
                self.chest_1_animation.append(img)
            elif index_y == 1:
                self.chest_2_animation.append(img)
            elif index_y == 2:
                self.chest_3_animation.append(img)
            else:
                self.chest_4_animation.append(img)
            
            index_x += 1
            if index_x >=  7:
                index_y += 1
                index_x = 0
                
            i += 1
    
    def Generate(self, screen , pos):
        i = random.randint(0, 3)
        if i == 0:
            return Chest(screen, pos, self.chest_1_animation, self.hole, self.wall, i)
        elif i == 1:
            return Chest(screen, pos, self.chest_2_animation, self.hole, self.wall, i)
        elif i == 2:
            return Chest(screen, pos, self.chest_3_animation, self.hole, self.wall, i)
        else:
            return Chest(screen, pos, self.chest_4_animation, self.hole, self.wall, i)
