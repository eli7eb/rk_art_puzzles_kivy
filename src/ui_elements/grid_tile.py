# tile class
# all tile properties
import pygame
from pygame.locals import *


class Tile:
    def __init__(self,image,size,x,y,state):
        self.image = image
        self.size = size
        self.x = x
        self.y = y
        self.state = state
        print('tile')
