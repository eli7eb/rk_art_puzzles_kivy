# tile class
# all tile properties
import pygame
from pygame.locals import *


class Tile:
    def __init__(self, image, transparant_image, size, row_pos, col_pos, coords, state):
        self.image = image
        self.transparant_image = transparant_image
        self.size = size
        self.x_pos = col_pos
        self.y_pos = row_pos
        self.coords = coords
        self.state = state
