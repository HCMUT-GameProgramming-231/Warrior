import pygame

class Camera:
    def __init__(self, pos_x, pos_y, pos_x_end, pos_y_end) -> None:
        self.begin_pos_x = pos_x
        self.begin_pos_y = pos_y
        self.end_pos_x = pos_x_end
        self.end_pos_y = pos_y_end
        
        self.pos_x = pos_x
        self.pos_y = pos_y