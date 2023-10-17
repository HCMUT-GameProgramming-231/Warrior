from .spritesheet import spritesheet
import pygame
import os
import random

class Slime:
    def __init__(self, animation, pos):
        self.animation = animation
        self.rect = pygame.Rect(pos, (100, 100))
        self.real_rect = pygame.Rect(pos, (70, 40))
        self.pos = pos
        self.direction = 'left'
        self.moving = True
        self.being_hit = False
        self.jumping = False
        self.falling = False
        self.detectWarrior = False
        self.x_lower = pos[0] - 150
        self.x_upper = pos[0] + 150
        self.frameNum = 0
        self.jump_speed = 200
    
    def GetActiveFrame(self):
        if self.falling:
            if self.direction == 'left':
                return self.animation[2][1]
            else:
                return self.animation[2][0]
        if self.jumping:
            if self.direction == 'left':
                return self.animation[3][1]
            else:
                return self.animation[3][0]
        if self.moving:
            if self.direction == 'left':
                return self.animation[int(self.frameNum)][1]
            else:
                return self.animation[int(self.frameNum)][0]
    
    def IsCollidingWithBlock(self, block):
        rect = block[1]
        
        if abs(self.real_rect.x - rect.x) > 70: return False, None
        
        if self.real_rect.colliderect(rect):
            if self.real_rect.y + self.real_rect.h <= rect.y + 20:
                return True, 'On'
            
            if self.real_rect.x <= rect.x + rect.w + 10 and self.real_rect.x + self.rect.w >= rect.x + rect.w:
                return True, 'Left'
            
            if self.real_rect.right >= rect.left + 10:
                return True, 'Right'
            
        return False, None
    
    def IsCollidingWithWarrior(self, warrior_rect):
        pass
    
    def Intergrate(self, deltaTime):

        if self.moving and not self.being_hit:
            if self.direction == 'left':
                self.rect.centerx -= 100 * deltaTime
            else:
                self.rect.centerx += 100 * deltaTime
        
        if self.jumping:
            self.rect.y -= self.jump_speed * deltaTime
            self.jump_speed -= 600 * deltaTime
            if self.jump_speed <= 0:
                self.jump_speed = 0
                self.jumping = False
                self.falling = True
        
        elif self.falling:
            self.rect.y += self.jump_speed * deltaTime
            self.jump_speed += 600 * deltaTime
            if self.jump_speed >= 200:
                self.jump_speed = 200

                
        if not self.falling and not self.jumping and not self.detectWarrior:
            
            if self.rect.x <= self.x_lower:
                self.direction = 'right'
            elif self.rect.x >= self.x_upper:
                self.direction = 'left'
        
        self.real_rect.center = self.rect.center
            
                
    def Update(self): 
        if self.moving:
            self.frameNum += 0.05
            if self.frameNum >= 2:
                self.frameNum = 0
                
    def UpdatePos(self):
        self.x_lower = self.pos[0] - 150
        self.x_upper = self.pos[0] + 150
                
    def Move(self, x, y):
        self.rect.move_ip(x, y)
        self.pos[0] += x
        self.UpdatePos()
        
    
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
            #pygame.draw.rect(self.screen, (255, 0, 120), slime.rect)
            #pygame.draw.rect(self.screen, (255, 170, 120), slime.real_rect)
            self.screen.blit(frame, slime.rect)
            
    def Intergrate(self, deltaTime):
        for slime in self.slimes:
            slime.Intergrate(deltaTime)
            
    def Move(self, x, y):
        for slime in self.slimes:
            slime.Move(x, y)