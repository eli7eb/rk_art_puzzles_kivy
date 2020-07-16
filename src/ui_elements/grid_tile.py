# tile class
# all tile properties
import pygame
from pygame.locals import *


class Tile:
    def __init__(self,image,size,x_index,y_index,state):
        self.image = image
        self.size = size
        self.x_index = x_index
        self.y_index = y_index
        self.state = state
        self.x_pos = 0
        self.y_pos = 0
