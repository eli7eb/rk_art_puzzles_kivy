# vertical grid of X elements which are meant to be dragged to the main grid
# the tiles are shown in random order from a pool
# when one is placed on the main grid - a new one is generated randomply and put in the vertical grid
# and the counter is incremented
# once all tiles are placed the game is over
# the tiles can be dragged outside this grid and placed or not placed in the main grid
# if they are not placed they are put back in the drag grid
# check for collision with grid -
# display border when dragged


import os, os.path
import pygame


import pygame
from pygame.locals import *

TEXT_COLOR = pygame.Color(255, 255, 255)


class DragContainer:
    def __init__(self, screen, text_pos_x, text_pos_y, spacer_size):
        self.screen = screen
        self.text_pos_x = text_pos_x
        self.text_pos_y = text_pos_y
        self.spacer_size = spacer_size

    def prepare(self):
        self.font = pygame.font.SysFont("comicsansmsttf", 40)