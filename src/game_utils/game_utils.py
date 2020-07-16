import pygame
import random
from src.game_consts.game_constants import *
from src.ui_elements.grid_tile import Tile

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2
TEXT_COLOR = pygame.Color(255, 255, 255)
SCREEN_SPACER_SIZE = 5
# how many spacers vertical and horizontal for the three main containers in the screen
# vertically 3 left. between grid and drag tiles and right
# horizntally 3 top between grid and dashboard and bottom
SCREEN_SPACER_NUMBER_VER = 3
SCREEN_SPACER_NUMBER_HOR = 3
# count number of spaces in grid is calculated as number of tiles horizontally -1
# count number of spaces in grid is calculated as number of tiles vertically -1

class GameUtils:

    def __init__(self):
        self.done = False
        self.image = None
        # tile needs to fit in the screen 5 times in the horizontal directions with overheads
        # at least 5 tiles across: 4 grid and one to drag
        self.tile_size = (SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR * SCREEN_SPACER_SIZE) / 5
        self.grid_width = SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR * SCREEN_SPACER_SIZE - self.tile_size
        self.grid_height = SCREEN_HEIGHT - SCREEN_SPACER_NUMBER_VER * SCREEN_SPACER_SIZE

    def getRandomSearchValue(self):
        return random.choice(MOOD_IDEAS)
    # crop function
    # Set the cropping area with box=(left, upper, right, lower).
    # an_array = [[1, 2], [3, 4]]
    # rows = len(an_array) Find row and column length.
    # columns = len(an_array[0])
    # total_length = rows * columns. Compute total length.
    # print(total_length)
    def crop_image_to_array(self,image):
        self.image = image

        # TODO 4 tiles across depends on level
        w = 4
        # floor division
        h = int(SCREEN_HEIGHT // self.tile_size)

        tile_matrix = [[None for x in range(w)] for y in range(h)]

        print('array rows {} cols {}'.format(str(len(tile_matrix)), str(len(tile_matrix[0]))))

        for i in range(len(tile_matrix)):
            for j in range(len(tile_matrix[i])):
                print('i {} j {}'.format( str(i), str(j)))
                top = SCREEN_SPACER_SIZE + i*self.tile_size
                upper = SCREEN_SPACER_SIZE + j*self.tile_size
                right = SCREEN_SPACER_SIZE + i * self.tile_size + self.tile_size
                lower = SCREEN_SPACER_SIZE + j * self.tile_size + self.tile_size
                print('i %s j %s top % upper % right % lower %', str(i), str(j), str(top), str(upper), str(right),
                      str(lower))
                cropped = self.image.crop((top, upper, right, lower))
                # convert to pygame image

                # TODO generate tile class image, x,y, state : found, in pos
                mode = cropped.mode
                size = cropped.size
                data = cropped.tobytes()
                #
                py_image = pygame.image.fromstring(data, size, mode)
                # position is set in game view when the tile is displayed
                py_tile = Tile(py_image,self.tile_size,0,0,TILE_INVISIBLE)
                tile_matrix[i][j] = py_tile

        return tile_matrix

