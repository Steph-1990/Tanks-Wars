# Classe Enemy

import pygame
from Class_folder import rect_color

class Enemy(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def draw(self, surface):
        return pygame.draw.rect(surface, rect_color.RED, (self.x, self.y, 50, 50))



