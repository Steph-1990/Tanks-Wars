# Classe projectile

import pygame
from Class_folder import rect_color

class Projectile(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def draw(self, surface):
        return pygame.draw.rect(surface, rect_color.BLACK, (self.x, self.y, 10, 10))
