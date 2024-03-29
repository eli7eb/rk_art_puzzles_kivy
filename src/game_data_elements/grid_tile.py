# tile class
# all tile properties
import pygame
from pygame.locals import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, image,  size, pos, coords, state):
        super().__init__()
        self.image = image
        #self.transparant_image = transparant_image
        self.size = size
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.x = pos[0]
        self.y = pos[1]
        self.coords = coords
        self.state = state
        self.rect = self.image.get_rect(center=pos)
        # bullet position is according the player position
        self.rect.centerx = self.x_pos
        self.rect.bottom = self.y_pos
        self.speedy = -15
