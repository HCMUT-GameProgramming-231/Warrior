import pygame
from .warrior import WarriorAnimation
from .background import Ground

class Processor:
    
    def __init__(self, warrior : WarriorAnimation, ground : Ground) -> None:
        self.warrior = warrior
        self.ground = ground
        
    def process(self):
        #falling
        falling = True
        for ground in self.ground.map:
            
            if len(ground) == 2:
                if abs(ground[1].x - self.warrior.rect.x) > 100:
                    continue
                if abs(ground[1].y - self.warrior.rect.y) > 100:
                    continue
            
                ret, pos = self.warrior.IsColliding(ground[1])
                if not ret: 
                    continue
                if pos == 'On':
                    falling = False
                    self.warrior.falling = False
                    break
                  
                
        if falling:
            self.warrior.ChangeStatus('fall')