# tile class
# all tile properties
import pygame
from pygame.locals import *


class Tile:
    def __init__(self,image,size,row_index,col_index,state):
        self.image = image
        self.size = size
        self.row_index = row_index
        self.col_index = col_index
        self.state = state
        self.x_pos = 0
        self.y_pos = 0
