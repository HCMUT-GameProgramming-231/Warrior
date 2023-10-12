import pygame
from .warrior import WarriorAnimation
from .background import Ground

class Processor:
    
    def __init__(self, warrior : WarriorAnimation, background : Ground) -> None:
        self.warrior = warrior
        self.background = background
        
    def process(self):
        if self.warrior.falling:
            bottom_ground = self.background.map[-1]
            for ground in bottom_ground:
                if len(ground) == 2 and self.warrior.IsOnGround(ground[1]):
                    self.warrior.falling = False
                    self.warrior.ChangeStatus('stand')
                    break