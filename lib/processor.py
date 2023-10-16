import pygame
from .warrior import WarriorAnimation
from .background import Ground
from .camera import Camera
from .slime import Slimes, Slime
class Processor:
    
    def __init__(self, warrior : WarriorAnimation, ground : Ground, cam : Camera, slimes : Slimes) -> None:
        self.warrior = warrior
        self.ground = ground
        self.cam = cam
        self.slimes = slimes
        
        slime_pos = [[750, 300]]
        for pos in slime_pos:
            self.slimes.Generate(pos)
        
        self.timeFromBeginning = 0
        self.currentTime = 0
        self.DELTA = 0.01
        self.currentFrameTime = 0
        self.accumulator = 0
        
    def Update(self, fps, SCREEN):
        newTime = pygame.time.get_ticks()
        frameTime = (newTime - self.currentTime) / 1000
        if frameTime  > 1 / fps:
            frameTime = 1 / fps
            
        self.currentTime = newTime
        self.accumulator += frameTime
        
        while self.accumulator >= self.DELTA:
            #self.lastState = copy.copy(self)
            self.Intergrate(self.DELTA)
            self.timeFromBeginning += self.DELTA
            self.currentFrameTime += self.DELTA
            self.accumulator -= self.DELTA
        
      
        
        self.ground.Update()
        self.slimes.Update()
        self.warrior.Update(fps)
        
    def Intergrate(self, deltaTime):
        
        falling = True
        self.warrior.collide_left = False
        self.warrior.collide_right = False
        for gr in self.ground.map:
            
            if abs(gr[1].x - self.warrior.rect.x) > 100: continue
            if abs(gr[1].y - self.warrior.rect.y) > 100: continue


                
            ret, pos = self.warrior.IsColliding(gr)
            if ret:
                falling = False
                if pos == 'On':
                    if gr[-1] == 10 or gr[-1] == 9: continue
                    self.warrior.rect.bottom = gr[1].top
                    self.warrior.rect.y += 2
                    self.warrior.falling = False
                    if self.warrior.slipping:
                        self.warrior.slipping = False
                        if self.warrior.direction == 'right':
                            self.warrior.rect.x += 2
                        else: 
                            self.warrior.rect.x -= 2
                        
                    break
                    
                elif pos == 'Left':
                    if self.warrior.slipping : continue
                    self.warrior.collide_right = True
                    self.warrior.rect.right = gr[1].left + 1


                        
                elif pos == 'Right':
                    if self.warrior.slipping : continue
                    self.warrior.collide_left = True
                    self.warrior.rect.left = gr[1].right - 1
                    


                    
                elif pos == 'Down':
                    if self.warrior.slipping: continue
                    self.warrior.jumping = False
                    self.warrior.ChangeStatus('fall')
                        
                elif pos == 'TopLeft' or pos == 'TopRight':
                    if gr[-1] == 10 or gr[-1] == 9: continue
                    if self.warrior.jumping : continue

                    if pos == 'TopLeft':
                        self.warrior.rect.right = gr[1].left
                    else:
                        
                        self.warrior.rect.left = gr[1].right
                    self.warrior.rect.top = gr[1].top
                    self.warrior.rect.y += 5
                    self.warrior.ChangeStatus('hanging')


                elif pos == 'SlipLeft' or pos == 'SlipRight':
                    if self.warrior.slipping : continue
                    if self.warrior.standing : continue
                    if pos == 'SlipLeft':
                        self.warrior.rect.right = gr[1].left + 1
                    else:
                        self.warrior.rect.left = gr[1].right - 1
                    self.warrior.falling = False
                    self.warrior.ChangeStatus('slip')
                    
        
        if falling:
            self.warrior.dashing = False
            self.warrior.quick_moving = False
            self.warrior.ChangeStatus('fall')

        self.warrior.Intergrate(deltaTime)
        self.slimes.Intergrate(deltaTime)
        if self.warrior.rect.centerx > self.cam.begin_pos_x:
                speed = 200
                if self.warrior.dashing or self.warrior.quick_moving:
                    speed = 300
                self.warrior.move_speed = 0
                self.warrior.dash_speed = 0
                offset_x = int(speed * deltaTime)
                if (self.warrior.isHoldingRight or ( (self.warrior.dashing or self.warrior.quick_moving) and self.warrior.direction == 'right') ) and not self.warrior.collide_right:
                    self.ground.Move(-offset_x, 0)
                    self.slimes.Move(-offset_x, 0)
                    self.cam.begin_pos_x -= offset_x
                    self.cam.pos_x = self.warrior.rect.centerx
                if (self.warrior.isHoldingLeft or ( (self.warrior.dashing or self.warrior.quick_moving) and self.warrior.direction == 'left')) and not self.warrior.collide_left:
                    #print(self.warrior.rect.centerx, self.cam.begin_pos_x)
                    self.ground.Move(offset_x, 0)
                    self.slimes.Move(offset_x, 0)
                    self.cam.begin_pos_x += offset_x
                    self.cam.pos_x = self.warrior.rect.centerx
        else:
            self.warrior.move_speed = 200
            self.warrior.dash_speed = 300
            self.cam.pos_x = self.cam.begin_pos_x


            
            