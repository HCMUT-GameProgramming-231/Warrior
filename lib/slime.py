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
        self.attacked_time = 0
        self.maxHP = 1000
        self.curHP = 1000
        self.back_speed = 100
        self.being_hit_left = False
        self.being_hit_right = False
        self.damage_rect = pygame.Rect(self.real_rect)
        self.hit_by_dash = False
        self.hit_by_attack = False
        self.hit_by_attack_2 = False
        self.font = pygame.font.SysFont('Comic Sans MS', 25)
        self.collide_left = False
        self.collide_right = False
        self.dead = False
        self.temp_dead = False
        self.dead_time = 0
        self.damage = 500
        self.type = 'slime'
        self.damage_taken = 0

        
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
    
    def IsBeingAttacked(self, attack_range, time, type):
        if self.temp_dead : return
        
        pos = self.real_rect.x - attack_range.x
        if abs(pos) > 50: 
            return False

        if self.real_rect.colliderect(attack_range):
            if not self.being_hit and time - self.attacked_time > 0.7:
                self.attacked_time = time
                self.being_hit = True
                self.jumping = True
                if type == 'dash':
                    self.back_speed = 400
                    self.hit_by_dash = True
                else: 
                    self.back_speed = 100
                    if type == 'attack':
                        self.hit_by_attack = True
                    else:
                        self.hit_by_attack_2 = True
                if attack_range.centerx <= self.real_rect.centerx:
                    self.direction = 'left'
                    self.being_hit_left = True
                else:
                    self.direction = 'right'
                    self.being_hit_right = True

                return True
        
        return False
    
    def DetectWarrior(self, warrior_rect):
        if self.temp_dead: return False
        if abs(warrior_rect.x - self.real_rect.x) > 300: 
            self.detectWarrior = False
            return False
 
        if self.direction == 'right' and warrior_rect.x - self.real_rect.x > 0:
            self.detectWarrior = True
            self.jumping = True if not self.falling else False
            return True
        elif self.direction == 'left' and self.rect.x - warrior_rect.x > 0:
            self.detectWarrior = True
            self.jumping = True if not self.falling else False
            return True
        
        return False
    
    def Intergrate(self, deltaTime, time):
        if self.temp_dead:
            #print(time - self.dead_time)
            if time - self.dead_time >= 1: self.dead = True
            return
        
        if self.curHP <= 0:
            self.temp_dead = True
            self.dead_time = time
            return
        
        if self.being_hit:
            self.damage_rect.centery = self.real_rect.centery - 50
            self.damage_rect.centerx = self.real_rect.centerx + 20
        
        if time - self.attacked_time > 0.7:
            self.being_hit = False
            self.being_hit_left = False
            self.being_hit_right = False
            self.hit_by_attack = False
            self.hit_by_dash = False
            self.hit_by_attack_2 = False

            
        if self.being_hit_left and not self.collide_right:
            self.rect.centerx += self.back_speed * deltaTime
        
        elif self.being_hit_right and not self.collide_left:
            self.rect.centerx -= self.back_speed * deltaTime    
        
            
        elif self.moving:
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
 
class Boss(Slime):
     
    def __init__(self, animation, pos):
         super().__init__(animation, pos)
         for ani in self.animation:
             ani[0] = pygame.transform.scale(ani[0], (200, 200))
             ani[1] = pygame.transform.scale(ani[1], (200, 200))
             
         self.rect = pygame.Rect(pos, (200, 200))
         self.real_rect = pygame.Rect((pos, (150, 80)))
         self.type = 'boss'
         self.maxHP = 5000
         self.curHP = 5000
         self.damage = 1000
         self.jump_speed = 200
         
    
    def IsCollidingWithBlock(self, block):
        rect = block[1]
        
        if abs(self.real_rect.x - rect.x) > 300: return False, None
        
        if self.real_rect.colliderect(rect):
            if self.real_rect.y + self.real_rect.h <= rect.y + 20:
                return True, 'On'
            
            if self.real_rect.x <= rect.x + rect.w + 10 and self.real_rect.x + self.rect.w >= rect.x + rect.w:
                return True, 'Left'
            
            if self.real_rect.right >= rect.left + 10:
                return True, 'Right'
            
        return False, None
    
    def GetActiveFrame(self):
        if self.temp_dead:
            if self.direction == 'left':
                return self.animation[2][1]
            else:
                return self.animation[2][0]
        if self.falling:
            if self.direction == 'left':
                return self.animation[0][1]
            else:
                return self.animation[0][0]
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
    
    def IsBeingAttacked(self, attack_range, time, type):
        if self.temp_dead : return
        
        pos = self.real_rect.x - attack_range.x
        if abs(pos) > 200: 
            return False

        if self.real_rect.colliderect(attack_range):
            if not self.being_hit and time - self.attacked_time > 0.7:
                self.attacked_time = time
                self.being_hit = True
                self.jumping = True
                if type == 'dash':
                    self.back_speed = 400
                    self.hit_by_dash = True
                else: 
                    self.back_speed = 100
                    if type == 'attack':
                        self.hit_by_attack = True
                    else:
                        self.hit_by_attack_2 = True
                if attack_range.centerx <= self.real_rect.centerx:
                    self.direction = 'left'
                    self.being_hit_left = True
                else:
                    self.direction = 'right'
                    self.being_hit_right = True
                
                
                return True
        
        return False
    
    def Intergrate(self, deltaTime, time):
            
        if self.temp_dead:
            #print(time - self.dead_time)
            if time - self.dead_time >= 1: self.dead = True
            return
        
        if self.curHP <= 0:
            self.temp_dead = True
            self.dead_time = time
            return
        
        if self.being_hit:
            self.damage_rect.centery = self.real_rect.centery - 50
            self.damage_rect.centerx = self.real_rect.centerx + 20
        
        if time - self.attacked_time > 0.7:
            self.being_hit = False
            self.being_hit_left = False
            self.being_hit_right = False
            self.hit_by_attack = False
            self.hit_by_dash = False
            self.hit_by_attack_2 = False

            
        if self.being_hit_left and not self.collide_right:
            self.rect.centerx += self.back_speed * deltaTime
        
        elif self.being_hit_right and not self.collide_left:
            self.rect.centerx -= self.back_speed * deltaTime    
        
            
        elif self.moving:
            if self.direction == 'left':
                self.rect.centerx -= 200 * deltaTime
            else:
                self.rect.centerx += 200 * deltaTime
        
        if self.jumping:
            self.rect.y -= self.jump_speed * deltaTime
            self.jump_speed -= 700 * deltaTime
            if self.jump_speed <= 0:
                self.jump_speed = 0
                self.jumping = False
                self.falling = True
        
        elif self.falling:
            self.rect.y += self.jump_speed * deltaTime
            self.jump_speed += 700 * deltaTime
            if self.jump_speed >= 200:
                self.jump_speed = 200

                
        if not self.falling and not self.jumping and not self.detectWarrior:
            
            if self.rect.x <= self.x_lower:
                self.direction = 'right'
            elif self.rect.x >= self.x_upper:
                self.direction = 'left'
        
        self.real_rect.center = self.rect.center
                
    
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
                    temp += [[slime_right, slime_left]]
                self.slimes_sprite += [temp]
        
        self.slimes = []
    
    def Generate(self, pos):
        i = random.randint(0, len(self.slimes_sprite) - 3)
        self.slimes.append(Slime(self.slimes_sprite[i], pos))
    
    def GenerateBos(self, pos):
        i = random.randint(1, 2)
        self.slimes.append(Boss(self.slimes_sprite[-i], pos))
    
    def Update(self, time):
        for slime in self.slimes:
            slime.Update()
            if slime.real_rect.right < 0 or slime.real_rect.left > 1500: continue
            frame = slime.GetActiveFrame()
            #pygame.draw.rect(self.screen, (255, 0, 120), slime.rect)
            #pygame.draw.rect(self.screen, (255, 170, 120), slime.real_rect)
            if slime.being_hit and not slime.temp_dead:
                if slime.type == 'slime':
                    text_surface = slime.font.render(str(slime.damage_taken), False, (255, 0, 0))
                    self.screen.blit(text_surface, slime.damage_rect)
                else:
                    text_surface = slime.font.render(str(slime.damage_taken), False, (255, 0, 0))
                    self.screen.blit(text_surface, slime.damage_rect)
            HP = pygame.Rect(slime.real_rect.x, slime.real_rect.y - 25, slime.curHP/slime.maxHP * 150, 10) if slime.type == 'boss'\
                else pygame.Rect(slime.rect.x + 10, slime.rect.y + 15, slime.curHP/slime.maxHP * 80, 5)
            pygame.draw.rect(self.screen, (255, 0, 0), HP)  
            self.screen.blit(frame, slime.rect)
            
    def Intergrate(self, deltaTime, time):
        for slime in self.slimes:
            slime.Intergrate(deltaTime, time)
            
    def Move(self, x, y):
        for slime in self.slimes:
            slime.Move(x, y)