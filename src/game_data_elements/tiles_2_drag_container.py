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
from pygame.locals import *


class DragContainer:
    def __init__(self, screen, pos_x, spacer_size):
        print ('DragContainer')

        self.screen = screen
        self.x_pos = pos_x
        self.spacer_size = spacer_size

    def draw_border(self):
        print('draw_border')

    def prepare(self):
        #self.font = pygame.font.SysFont("comicsansmsttf", 40)
        print('prepare')

    def display_tiles_in_container(self,tiles_list):
        print('display_tiles_in_container')
        # display the tiles vertically
        x = self.x_pos + self.spacer_size
        y = self.spacer_size
        for tile in tiles_list:
            # calculate x y pos
            # get the image
            print('')
            # increment y pos by tile size + spacer size
            display_tile = tile.image
            self.screen.blit(display_tile, (x, y))
            y += tile.size + self.spacer_size