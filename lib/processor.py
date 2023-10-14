import pygame
from .warrior import WarriorAnimation
from .background import Ground

class Processor:
    
    def __init__(self, warrior : WarriorAnimation, ground : Ground) -> None:
        self.warrior = warrior
        self.ground = ground
        
        self.timeFromBeginning = 0
        self.currentTime = 0
        self.DELTA = 0.01
        self.currentFrameTime = 0
        self.accumulator = 0
        
    def Update(self, fps):
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
        self.warrior.Update(fps)
        
    def Intergrate(self, deltaTime):
        
        falling = True
        collideLeft = False
        collideRight = False
        for gr in self.ground.map:
            
            if abs(gr[1].x - self.warrior.rect.x) > 100: continue
            if abs(gr[1].y - self.warrior.rect.y) > 100: continue
        
            
            if len(gr) == 4:
                
                ret, pos = self.warrior.IsColliding(gr)
                if ret:
                    falling = False
                    if pos == 'On':
                        self.warrior.rect.bottom = gr[1].top
                        self.warrior.rect.y += 2
                        self.warrior.falling = False
                        pass
                    
                    elif pos == 'Left':
                        collideLeft = True
                        self.warrior.collide_left = True
                        self.warrior.move_speed = 0
                        self.warrior.dash_speed = 0
                        
                    elif pos == 'Right':
                        collideRight = True
                        self.warrior.collide_right = True
                        self.warrior.move_speed = 0
                        self.warrior.dash_speed = 0
                    
                    elif pos == 'Down':
                        self.warrior.jumping = False
                        self.warrior.ChangeStatus('fall')
                        
                    elif pos == 'TopLeft' or pos == 'TopRight':
                        self.warrior.ChangeStatus('hanging')

        
        if falling:
            self.warrior.ChangeStatus('fall')
            
        if not collideLeft:
            self.warrior.collide_left = False
        
        if not collideRight:
            self.warrior.collide_right = False
        
        self.warrior.Intergrate(deltaTime)