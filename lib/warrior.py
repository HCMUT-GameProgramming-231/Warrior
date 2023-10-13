import pygame
from .spritesheet import spritesheet
import random

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
        self.currentFrameNums = 5
        
        self.status = 'fall'
        
        self.attacking = False
        
        self.current_height = 0
        self.tartget_height = self.current_height + 200
        self.jumping = False
        
        self.falling = True
        
        self.faint_delay = 2000
        self.faint_time = 0
        self.fainting = False
        
        self.stand_up = False
        
        self.quick_moving = False
        
        self.dashing = False
        self.attacking_2 = False
        
        self.direction = 'right'
        
        #w = 70 if attacking else 35
        self.rect = pygame.Rect(0, 0, 40, 100)
        self.rect.center = (100, 450)

        #speed
        self.move_speed = 150 
        self.quick_move_speed = 200
        self.dash_speed = 200
        self.jump_speed = 300
        
        self.isHoldingLeft = False
        self.isHoldingRight = False

        
    def Update(self, deltaTime, fps):
        
        if self.frameTime > 1000 / fps:
            frames_per_sprite = fps / self.currentFrameNums
            if self.attacking_2:
                self.frameIndex += 1.75 / frames_per_sprite
            else:
                self.frameIndex += 2 / frames_per_sprite
                
            self.frameTime = 0
        
        if self.frameIndex >= self.currentFrameNums:  
            if self.fainting :
                self.frameIndex = self.currentFrameNums -1
            elif self.falling:
                self.frameIndex = 2
            elif self.jumping:
                self.frameIndex = 0
            elif self.stand_up:
                self.stand_up = False
                self.ChangeStatus('stand')
            elif self.quick_moving:
                self.quick_moving = False
                self.ChangeStatus('stand')
            elif self.attacking:
                self.attacking = False
                if self.direction == "right":
                    self.rect.centerx -= 30
                else: 
                    self.rect.centerx += 50
                self.ChangeStatus('stand')
            elif self.attacking_2:
                self.attacking_2 = False
                if self.direction == "right":
                    self.rect.centerx -= 30
                else: 
                    self.rect.centerx += 50
                self.ChangeStatus('stand')
            elif self.dashing:
                self.dashing = False
                self.ChangeStatus('stand')
            else:
                self.frameIndex = self.frameIndex % self.currentFrameNums
        
        self.frameTime += deltaTime
         
        frame = self.GetActiveFrame()
        
        if self.attacking or self.attacking_2:
            self.rect.w = 60
        else:
            self.rect.w = 40

        
        rect = frame.get_rect()
        rect.center = self.rect.center
        
        if self.attacking or self.attacking_2:
            if self.direction == 'right':
                rect.centerx -= 30
            else:
                rect.centerx += 30
                
        
        if self.direction == 'right':      
            rect.centerx += 10
        else:
            rect.centerx -= 10

        
        
        if self.status == 'move' or self.status == 'dash' or self.status == 'quick_move':
            speed = self.move_speed if self.status == 'move' else self.dash_speed
            
            if self.direction == 'right':
                self.rect.centerx += speed * deltaTime / 1000
 
            else:
                self.rect.centerx -= speed * deltaTime / 1000
        
        if self.jumping:
            if self.jump_speed <= 0:
                self.jumping = False
                self.jump_speed = 0
                self.ChangeStatus('fall')

            else:
                self.rect.centery -= self.jump_speed * deltaTime / 1000
                self.jump_speed = self.jump_speed - 700 * deltaTime / 1000
                if self.isHoldingLeft:
                    self.rect.centerx -= self.move_speed * deltaTime / 1000
                elif self.isHoldingRight:
                    self.rect.centerx += self.move_speed * deltaTime / 1000
        
        if self.falling:
            self.rect.centery += self.jump_speed * deltaTime / 1000
            self.jump_speed  = self.jump_speed + 700 *deltaTime / 1000
            if self.jump_speed > 300: self.jump_speed = 300
            if self.isHoldingLeft:
                self.rect.centerx -= self.move_speed * deltaTime / 1000
            elif self.isHoldingRight:
                self.rect.centerx += self.move_speed * deltaTime / 1000

        #pygame.draw.rect(self.SCREEN, (0, 0, 255), rect)
        #pygame.draw.rect(self.SCREEN, (0, 255, 0), self.rect)
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

        
    
        
    def GetEvent(self, events : list):
        time = pygame.time.get_ticks()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        
        keystate = pygame.key.get_pressed()
        
        moving = False
        self.isHoldingLeft = False
        self.isHoldingRight = False
        if keystate[pygame.K_RIGHT]:
            moving = True
            self.isHoldingRight = True
            if not self.fainting and not self.attacking:
                self.direction = 'right' 
            self.ChangeStatus('move')
        
        if keystate[pygame.K_LEFT]:
            moving = True
            self.isHoldingLeft = True
            if not self.fainting and not self.attacking:
                self.direction = 'left' 
            self.ChangeStatus('move')
            
        if keystate[pygame.K_x]:
            moving = True
            r = random.randint(0, 10)
            if r > 3:
                self.ChangeStatus('attack')
            else:
                self.ChangeStatus('attack_2')
            
        if keystate[pygame.K_z]:
            moving = True
            self.ChangeStatus('quick_move')
        
        if keystate[pygame.K_UP]:
            moving = True
            self.ChangeStatus('jump')
            
        if keystate[pygame.K_c]:
            moving = True
            self.ChangeStatus('dash')
        
        """
        Update later: hanging, slipping, onground, climbing
        """
        
        if keystate[pygame.K_f]:
            moving = True
            self.faint_time = time
            self.ChangeStatus('faint', time)
        
        if self.fainting == True:

            if time - self.faint_time > self.faint_delay:
                self.fainting = False
                self.ChangeStatus('stand_up')
        
        if not moving:
            self.ChangeStatus('stand')
        
    def ChangeStatus(self, status : str, time = pygame.time.get_ticks()):
        if self.status == status:
            return
        
        if self.attacking_2:
            return
        
        if self.attacking:
            return
        
        if self.stand_up:
            return
        
        if self.quick_moving:
            if status == 'fall':
                self.quick_moving = False
            else:
                return
        
        if self.fainting:
            return
        
        if self.dashing:
            if status == 'fall':
                self.dashing = False
            else:
                return
        
        if self.jumping:
            #check xem có chạm đất k ở đây
            #if self.IsOnGround:
                #self.jumping = False
            #else
                return
        if self.falling:
            return
        
        self.frameIndex = 0
        self.status = status
        
        if status == 'move':
            self.currentFrameNums = self.action_num_frames['move']
            
        elif status =='stand':
            self.currentFrameNums = self.action_num_frames['stand']
            
        elif status == 'attack':
            self.attacking = True
            if self.direction == 'right':
                self.rect.centerx += 30
            else:
                self.rect.centerx -= 50
            self.currentFrameNums = self.action_num_frames['attack']
            
        elif status == 'jump':
            self.jumping = True
            self.jump_speed = 400
            self.currentFrameNums = self.action_num_frames['jump']   
            
        elif status == 'fall':
            self.falling = True
            self.currentFrameNums = self.action_num_frames['fall']
             
        elif status == 'faint':
            self.fainting = True
            self.currentFrameNums = self.action_num_frames['faint']
            
        elif status == 'stand_up':
            self.stand_up = True
            self.currentFrameNums = self.action_num_frames['stand_up']
            
        elif self.status == 'quick_move':
            self.quick_moving = True
            self.currentFrameNums = self.action_num_frames['quick_move']
            
        elif self.status == 'attack_2':
            self.attacking_2 = True
            if self.direction == 'right':
                self.rect.centerx += 30
            else:
                self.rect.centerx -= 50
            self.currentFrameNums = self.action_num_frames['attack_2']
            
        elif self.status == 'dash':
            self.dashing = True
            self.currentFrameNums = self.action_num_frames['dash']

        
    def IsColliding(self, ground : pygame.surface.Surface) -> (bool, str):
        if pygame.Rect.colliderect(self.rect, ground) and self.rect.y + self.rect.h - 10 <= ground.y \
            and self.rect.x + self.rect.w - 10 > ground.x and self.rect.x < ground.x + ground.w - 10:
                return (True, 'On')
        
        return (False, None)