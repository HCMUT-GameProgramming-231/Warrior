import pygame
from .spritesheet import spritesheet
import random
import copy

class WarriorAnimation(pygame.sprite.Sprite):
    
    def __init__(self, SCREEN):
        
        self.SCREEN = SCREEN
        
        self.spritesheet = spritesheet("./Assets/Warrior/Warrior_Sheet-Effect.png")
        self.spritesheet.sheet = pygame.transform.scale(self.spritesheet.sheet, (420, 850))
        
        #animation 
        #right direction
        self.stand_right = []
        self.move_right = [] 
        self.attack_right = []
        self.faint_right = []
        self.stand_up_right = []
        self.jump_right = []
        self.fall_right = [] 
        self.onground_right = []
        self.quick_move_right = []
        self.attack_2_right = []
        self.dash_right = []
        self.hanging_right = []
        self.slip_right = []
                
        #left direction
        self.stand_left = []
        self.move_left = [] 
        self.attack_left = []
        self.faint_left = []
        self.stand_up_left = []
        self.jump_left = []
        self.fall_left = [] 
        self.onground_left = []
        self.quick_move_left = []
        self.attack_2_left = []
        self.dash_left = []
        self.hanging_left = []
        self.slip_left = []
                
        
        #no direction
        self.climb = [] 
        
        #add animation 
        self.action_num_frames = {
            'stand' : 6,
            'move' : 8,
            'attack' : 12,
            'faint' : 11,
            'stand_up' : 4,
            'jump' : 3,
            'fall' : 5,
            'hanging' : 11,
            'slip' : 3,
            'onground' : 6,
            'quick_move' : 7,
            'attack_2' : 8,
            'dash' : 7,
            'climb' : 8
        }
        
        
        index_x = 0
        index_y = 0
        
        for key in self.action_num_frames.keys():
            num_frames = self.action_num_frames[key]
            for i in range(num_frames):
                img = self.spritesheet.image_at((index_x * 70, index_y * 50, 70, 50), -1)
                img = pygame.transform.scale(img, (100, 100))
                flipped_img = pygame.transform.flip(img, True, False)
                
                if key == 'stand':
                    self.stand_right += [img]
                    self.stand_left += [flipped_img]
                    
                elif key == 'move':
                    self.move_right += [img]
                    self.move_left += [flipped_img]
                    
                elif key == 'attack':
                    self.attack_right += [img]
                    self.attack_left += [flipped_img]
                    
                elif key == 'faint':
                    self.faint_right += [img]
                    self.faint_left += [flipped_img]
                    
                elif key == 'stand_up':
                    self.stand_up_left += [flipped_img]
                    self.stand_up_right += [img]
                    
                elif key == 'jump':
                    self.jump_right += [img]
                    self.jump_left += [flipped_img]
                
                elif key == 'fall':
                    self.fall_right += [img]
                    self.fall_left += [flipped_img]
                
                elif key == 'hanging':
                    self.hanging_right += [img]
                    self.hanging_left += [flipped_img]
                
                elif key == 'slip':
                    self.slip_left += [flipped_img]
                    self.slip_right += [img]
                
                elif key == 'onground':
                    self.onground_right += [img]
                    self.onground_left += [flipped_img]
                
                elif key == 'quick_move':
                    self.quick_move_right += [img]
                    self.quick_move_left += [flipped_img]
                
                elif key == 'attack_2':
                    self.attack_2_left += [flipped_img]
                    self.attack_2_right += [img]
                    
                elif key == 'dash':
                    self.dash_left += [flipped_img]
                    self.dash_right += [img]
                    
                else:
                    self.climb += [img]

                index_x += 1
                if index_x == 6:
                    index_x = 0
                    index_y += 1
        
        #init start status
        self.frameTime = 0
        self.frameIndex = 0
        self.currentFrameNums = 6
        
        self.status = 'stand'
        
        self.attacking = False
        
        self.current_height = 0
        self.jumping = False
        
        self.falling = False
        
        self.faint_delay = 2700
        self.faint_time = 0
        self.fainting = False
        self.standing = False
        self.hanging = False
        
        self.stand_up = False
        
        self.quick_moving = False
        
        self.dashing = False
        self.attacking_2 = False
        self.slipping = False
        self.falling_time = 0
        
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        
        self.direction = 'right'
        
        self.collide_left = False
        self.collide_right = False
        #w = 70 if attacking else 35
        self.rect = pygame.Rect(0, 0, 20, 80)
        self.rect.center = (200, 450)
        
        self.attack_range = pygame.Rect(0, 0, 40, 80)
        self.attack_time = 0
        #speed
        self.move_speed = 200
        self.quick_move_speed = 300
        self.dash_speed = 300
        self.jump_speed = 400
        self.slip_speed = 150
        
        self.jump_when_slip_time_left = 0
        self.jump_when_slip_time_right = 0
        self.jump_when_slipping_time = 0
        self.jump_delay = 1000
        
        self.isHoldingLeft = False
        self.isHoldingRight = False
        
        self.findHiddenChest = False
        self.find_time = 0
        
        self.maxHP = 2000
        self.curHP = 2000
        
        self.attacked_by = None
        
        self.timeFromBeginning = 0
        self.currentTime = 0
        self.DELTA = 0.01
        self.currentFrameTime = 0

        self.background_moving = False
        #self.lastState = None
        self.accumulator = 0
        
        self.attack_damage = 200
        self.attack_2_damage = 500
        self.dash_damage = 50
        
        self.attack_sound = pygame.mixer.Sound('./sound/sword-sound-1.mp3')
    
    def GetEvent(self, events):
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        
        self.standing = True
        self.isHoldingLeft = False
        self.isHoldingRight = False
        self.findHiddenChest = False
        time = pygame.time.get_ticks()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_g]:
            print(time - self.find_time)
            if time - self.find_time > 200:
                self.find_time = time
                self.findHiddenChest = True
        
        if keystate[pygame.K_RIGHT]:
            self.standing = False
            if not self.fainting and not self.attacking and not self.attacking_2 and not self.hanging and not self.dashing and not self.quick_moving\
                and not self.stand_up and not self.slipping and time - self.jump_when_slip_time_left > 500:
                self.direction = 'right' 
                self.isHoldingRight = True
            self.ChangeStatus('move')
        
        if keystate[pygame.K_LEFT]:
            self.standing = False
            if not self.fainting and not self.attacking and not self.attacking_2 and not self.hanging and not self.dashing and not self.quick_moving\
                and not self.stand_up and not self.slipping and time - self.jump_when_slip_time_right > 500:
                self.direction = 'left' 
                self.isHoldingLeft = True
            self.ChangeStatus('move')
        
        if keystate[pygame.K_x]:
            self.standing = False
            i = random.randint(1, 10)
            self.attack_time = time
            if i < 4:
                self.ChangeStatus('attack_2')
            else:
                self.ChangeStatus('attack')
                
        if keystate[pygame.K_z]:
            self.standing = False
            self.ChangeStatus('quick_move')
        
        if keystate[pygame.K_c]:
            self.standing = False
            self.ChangeStatus('dash')
        
        if keystate[pygame.K_UP]:
            if time - self.jump_when_slip_time_left > 100:
                self.standing = False
                self.ChangeStatus('jump')
        
        if keystate[pygame.K_q]:
            self.standing = False
            self.ChangeStatus('fall')
        
        
        if self.standing :
            self.ChangeStatus('stand')
    
    def ChangeStatus(self, status):
        if self.status == status:
            return

        if status == 'slip' and (self.status == 'move' or self.status == 'stand' or self.attacking or self.attacking_2 or self.fainting):
            return
        
        if self.attacking or self.attacking_2:
            return
        
        if self.quick_moving:
            if status != 'fall':
                return
        
        if self.dashing:
            if status != 'fall':
                return
        
        if self.slipping:
            if status == 'fall' or status == 'jump':
                self.slipping = False
                if self.direction == 'right':
                    self.rect.x += 5
                    self.jump_when_slip_time_right = pygame.time.get_ticks()
                else:
                    self.jump_when_slip_time_left = pygame.time.get_ticks()
                    self.rect.x -= 5
            else:
                return
        
        
        if self.jumping:
            if status == 'slip':
                self.jumping = False
            else:
                return
        
        if self.falling:
            if  status == 'hanging':
                self.falling = False
            else:
                return

        if self.fainting:
            return
        
        if self.stand_up:
            return
        
        if self.hanging:
            if status == 'jump':
                self.rect.y -= 10
                self.hanging = False
            else:
                return       
         
        if status == 'dash' and self.status != 'move': 
            return
        
        self.status = status
        self.frameIndex = 0
        
        if status == 'move':
            self.currentFrameNums = self.action_num_frames['move']
            
        elif status =='stand':
            self.currentFrameNums = self.action_num_frames['stand']
        elif status == 'attack':
            pygame.mixer.find_channel(True).play(self.attack_sound)
            self.attacking = True
            self.attack_range.top = self.rect.top
            if self.direction == 'right':
                self.attack_range.left = self.rect.right
            else: 
                self.attack_range.right = self.rect.left
            self.currentFrameNums = self.action_num_frames['attack']
        elif status == 'attack_2':
            pygame.mixer.find_channel(True).play(self.attack_sound)
            self.attacking_2 = True
            self.attack_range.top = self.rect.top
            if self.direction == 'right':
                self.attack_range.left = self.rect.right
            else: 
                self.attack_range.right = self.rect.left
            self.currentFrameNums = self.action_num_frames['attack_2']
        elif status == 'quick_move':
            self.quick_moving = True
            self.currentFrameNums = self.action_num_frames['quick_move']
        elif status == 'dash':
            self.dashing = True
            self.currentFrameNums = self.action_num_frames['dash']
        elif status == 'jump':
            self.jumping = True
            self.jump_speed = 400
            self.currentFrameNums = self.action_num_frames['jump']
        elif status == 'fall':
            self.falling_time = pygame.time.get_ticks()
            self.falling = True
            self.currentFrameNums = self.action_num_frames['fall']
        elif status == 'faint':
            self.fainting = True
            self.currentFrameNums = self.action_num_frames['faint']
        elif status == 'stand_up':
            self.stand_up = True
            self.currentFrameNums = self.action_num_frames['stand_up']
        elif status == 'hanging':
            self.hanging = True
            self.currentFrameNums = self.action_num_frames['hanging']
        elif status == 'slip':
            self.slipping = True
            self.jump_when_slip_time_left = pygame.time.get_ticks()
            self.direction = 'right' if self.direction == 'left' else 'left'
            self.currentFrameNums = self.action_num_frames['slip']
    
    def Update(self, fps):
        newTime = pygame.time.get_ticks()
            
        
        if self.currentFrameTime > 1 / fps:
            frames_per_sprite = fps / self.currentFrameNums
            if self.attacking_2:
                self.frameIndex += 1.75 / frames_per_sprite
            elif self.jumping or self.falling:
                self.frameIndex += 2 / frames_per_sprite
            elif self.slipping:
                self.frameIndex += 3 / frames_per_sprite
            else:
                self.frameIndex += 2 / frames_per_sprite
                
            self.currentFrameTime = 0
        
        if self.frameIndex >= self.currentFrameNums:
            self.frameIndex = self.frameIndex % self.currentFrameNums
            standing = True
            
            
            if self.attacking:
                self.attacking = False

            elif self.attacking_2:
                self.attacking_2 = False

            elif self.hanging:
                self.frameIndex = 2
            
            elif self.quick_moving:
                self.quick_moving =  False

            elif self.dashing:
                self.dashing = False
            
            elif self.jumping:
                self.frameIndex = 1
                
            elif self.falling:
                self.frameIndex = 2
            
            elif self.fainting:
                self.frameIndex = self.currentFrameNums - 1
                if newTime - self.faint_time > self.faint_delay:
                    self.fainting = False
                    standing = False
                    self.attacked_by = None
                    self.ChangeStatus('stand_up')
            
            elif self.status == 'move':
                standing = False
                    
            elif self.stand_up:
                self.stand_up = False
            
            if standing:
                self.ChangeStatus('stand')
            
            
            
            
        
        """
        alpha = self.accumulator / self.DELTA
        renderState = self  + self.lastState

        print(renderState.rect.centerx)
        renderState.Render()
        """
       
        self.Render()
        
    
        
    def Intergrate(self, deltaTime):
        
        self.timeFromBeginning += self.DELTA
        self.currentFrameTime += self.DELTA

        
        if self.status == 'move' or self.status == 'dash' or self.status == 'quick_move':
            speed = self.move_speed if self.status == 'move' else self.dash_speed
            if self.direction == 'right':
                self.rect.centerx += int(speed * deltaTime)
            else:
                self.rect.centerx -= int(speed * deltaTime)
                
        if self.status == 'jump':
            self.rect.centery -= int(self.jump_speed * deltaTime)
            self.jump_speed -= int(500 * deltaTime)
            
            if self.jump_speed <= 80:
                self.jump_speed = 0
                self.jumping = False
                self.ChangeStatus('fall')
                
            if self.isHoldingLeft:
                self.rect.centerx -= int(self.move_speed * deltaTime)
            elif self.isHoldingRight:
                self.rect.centerx += int(self.move_speed * deltaTime)
        
        if self.status == 'fall':
            self.rect.centery += int(self.jump_speed * deltaTime)
            self.jump_speed += int(500 * deltaTime)
            
            if self.jump_speed >= 400:
                self.jump_speed = 400

                
            if self.isHoldingLeft:
                self.rect.centerx -= int(self.move_speed * deltaTime)
            elif self.isHoldingRight:
                self.rect.centerx += int(self.move_speed * deltaTime)
        
        if self.status == 'slip':
             self.rect.centery += int(self.slip_speed * deltaTime)
                
            
        
        

    
    def Render(self):

        frame = self.GetActiveFrame()
        rect = frame.get_rect()
        rect.center = self.rect.center
        
        
        
        if self.direction == 'right':
            if self.slipping:
                rect.centerx -= 15
            else:
                rect.centerx += 10
        else:
            if self.slipping:
                rect.centerx += 12
            else:
                rect.centerx -= 10
            
        rect.centery -= 10
        
        #pygame.draw.rect(self.SCREEN, (255, 0, 0), rect)
        #pygame.draw.rect(self.SCREEN, (0, 255, 0), self.rect)
        #if self.attacking or self.attacking_2:
         #  pygame.draw.rect(self.SCREEN, (100, 200, 150), self.attack_range)
        HP_rect = pygame.Rect(self.rect.x - 20, self.rect.y - 10, self.curHP / self.maxHP * 60, 5)
        pygame.draw.rect(self.SCREEN, (255, 0, 0), HP_rect)
        if self.fainting:
            damage = 500 if self.attacked_by == 'slime'  else 2000
            text_surface = self.font.render(str(damage), False, (255, 0, 0))
            HP_rect.y -= 30
            self.SCREEN.blit(text_surface, HP_rect)
        self.SCREEN.blit(frame, rect)
            
        
    def GetActiveFrame(self) -> pygame.Rect:
        
        if self.status == 'stand':
            if self.direction == 'right':
                return self.stand_right[int(self.frameIndex)]
            return self.stand_left[int(self.frameIndex)]
        
        elif self.status == 'move':
            if self.direction == 'right':
                return self.move_right[int(self.frameIndex)]
            return self.move_left[int(self.frameIndex)]
        
        elif self.status == 'attack':
            if self.direction == 'right':
                return self.attack_right[int(self.frameIndex)]
            return self.attack_left[int(self.frameIndex)]
        
        elif self.status == 'jump':
            if self.direction == 'right':
                return self.jump_right[int(self.frameIndex)]
            return self.jump_left[int(self.frameIndex)]
        
        elif self.status =='fall':
            if self.direction == 'right':
                return self.fall_right[int(self.frameIndex)]
            return self.fall_left[int(self.frameIndex)]
        
        elif self.status == 'faint':
            if self.direction == 'right':
                return self.faint_right[int(self.frameIndex)]
            return self.faint_left[int(self.frameIndex)]
        
        elif self.status == 'stand_up':
            if self.direction == 'right':
                return self.stand_up_right[int(self.frameIndex)]
            return self.stand_up_left[int(self.frameIndex)]
        
        elif self.status == 'quick_move':
            if self.direction == 'right':
                return self.quick_move_right[int(self.frameIndex)]
            return self.quick_move_left[int(self.frameIndex)]
        
        elif self.status == 'attack_2':
            if self.direction == 'right':
                return self.attack_2_right[int(self.frameIndex)]
            return self.attack_2_left[int(self.frameIndex)]
        
        elif self.status == 'dash':
            if self.direction == 'right':
                return self.dash_right[int(self.frameIndex)]
            return self.dash_left[int(self.frameIndex)]
        
        elif self.status == 'hanging':
            if self.direction == 'right':
                return self.hanging_right[int(self.frameIndex)]
            return self.hanging_left[int(self.frameIndex)]
        
        elif self.status == 'slip':
            if self.direction == 'right':
                return self.slip_left[int(self.frameIndex)]
            return self.slip_right[int(self.frameIndex)]
        
    def IsColliding(self, block):
        
        rect = block[1]
        if self.rect.colliderect(rect):
            
            if self.rect.y + self.rect.h >= rect.y and self.rect.y + self.rect.h <= rect.y  + 10:
                return True, 'On'

            elif self.rect.y - (rect.y + rect.h) > -10:
               
                return True, 'Down'
            
            else:
                if self.rect.x + self.rect.w >= rect.x - 10 and self.rect.x <= rect.x:
                    if block[-1] == 9 or block[-1] == 10:
                        #print (self.rect.y - rect.y)
                        if self.rect.y - rect.y >= 0:
                            return True, 'SlipLeft'

                   # print (abs(self.rect.y - rect.y))
                    if abs(self.rect.y - rect.y) <= 5 and not self.jumping:
                        return True, 'TopLeft'

                    return True, 'Left'

                if self.rect.x <= rect.x + rect.w + 10:
                    if block[-1] == 9 or block[-1] == 10:
                         if self.rect.y - rect.y >= 0:
                            return True, 'SlipRight'

                    if abs(self.rect.y - rect.y) <= 5 and not self.jumping:
                       return True, 'TopRight'
                    return True, 'Right'
        

        return False, None
    
    def IsCollidingWithSlime(self, slime):
        slime_rect = slime.real_rect
        if slime.type == 'slime':
            if abs(self.rect.x - slime_rect.x) > 50 or self.attacking or self.attacking_2 or self.dashing or self.fainting: return False
            if self.rect.colliderect(slime_rect):
                return True
        else:
            if abs(self.rect.x - slime_rect.x) > 300 or self.attacking or self.attacking_2 or self.dashing or self.fainting: return False
            if self.rect.colliderect(slime_rect):
                return True

        
