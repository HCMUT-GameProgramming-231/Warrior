from .spritesheet import spritesheet
import pygame
import random

class Chest(pygame.sprite.Sprite):
    
    def __init__(self, screen, pos, animation):
        self.screen = screen
        self.rect = pygame.Rect(pos, (75, 75))
        self.status = 'closs'
        self.frameNum = 0
        self.animation = animation
        
    def Update(self):
        frame = self.GetActiveFrame()
        self.screen.blit(frame, self.rect)
    
    def GetActiveFrame(self):
        if self.status == 'close':
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
        print(self.spritesheet.sheet.get_size())
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
            return Chest(screen, pos, self.chest_1_animation)
        elif i == 1:
            return Chest(screen, pos, self.chest_2_animation)
        elif i == 2:
            return Chest(screen, pos, self.chest_3_animation)
        else:
            return Chest(screen, pos, self.chest_4_animation)
