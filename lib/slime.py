from .spritesheet import spritesheet
import pygame
import os
import random

class Slime:
    def __init__(self, animation, pos):
        self.animation = animation
        self.rect = pygame.Rect(pos, (100, 100))
        self.pos = pos
        self.status = ['stand','move', 'jump', 'fall']
        self.direction = 'left'
        self.moving = True
        self.jumping = False
        self.falling = False
        self.current_status = 'move'
        self.x_lower = pos[0] - 150
        self.x_upper = pos[0] + 150
        self.frameNum = 0
    
    def GetActiveFrame(self):
        if self.current_status == 'stand' or self.current_status == 'move':
            if self.direction == 'left':
                return self.animation[int(self.frameNum)][1]
            else:
                return self.animation[int(self.frameNum)][0]
        if self.current_status == 'fall':
            if self.direction == 'left':
                return self.animation[2][1]
            else:
                return self.animation[2][0]
        if self.current_status == 'jump':
            if self.direction == 'left':
                return self.animation[3][1]
            else:
                return self.animation[3][0]
            
    def Intergrate(self, deltaTime):
        print(self.rect.x, self.x_lower)
        if self.moving:
            if self.direction == 'left':
                self.rect.centerx -= 100 * deltaTime
            else:
                self.rect.centerx += 100 * deltaTime
            
            if self.rect.x <= self.x_lower:
                self.direction = 'right'
            elif self.rect.x >= self.x_upper:
                self.direction = 'left'
                
    def Update(self): 
        if self.current_status == 'move' or self.current_status == 'stand':
            self.frameNum += 0.05
            if self.frameNum >= 2:
                self.frameNum = 0
                
    def Move(self, x, y):
        self.rect.move_ip(x, y)
        self.pos[0] += x
        self.x_lower = self.pos[0] - 150
        self.x_upper = self.pos[0] + 150
        
    
class Slimes:
    def __init__(self, screen):
        self.screen = screen
        directory = './Assets/Slime'
        self.slimes_sprite = []
        for name in os.listdir(directory):
            f = os.path.join(directory, name)
            for other_name in os.listdir(f):
                slime_type = os.path.join(f, other_name)
                temp = []
                for sprite in os.listdir(slime_type):
                    sprite_path = os.path.join(slime_type, sprite)
                    slime_right = pygame.transform.scale(pygame.image.load(sprite_path), (100, 100))
                    slime_left = pygame.transform.flip(slime_right, True, False)
                    temp += [(slime_right, slime_left)]
                self.slimes_sprite += [temp]
        
        self.slimes = []
    
    def Generate(self, pos):
        i = random.randint(0, len(self.slimes_sprite) - 3)
        self.slimes.append(Slime(self.slimes_sprite[i], pos))
        
    def Update(self):
        for slime in self.slimes:
            slime.Update()
            frame = slime.GetActiveFrame()
            self.screen.blit(frame, slime.rect)
            
    def Intergrate(self, deltaTime):
        for slime in self.slimes:
            slime.Intergrate(deltaTime)
            
    def Move(self, x, y):
        for slime in self.slimes:
            slime.Move(x, y)