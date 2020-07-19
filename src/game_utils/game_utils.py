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

    # crop PIL image from this class and outside classes
    def crop_image_PIL(self, image, upper, top, right, lower):
        cropped = image.crop((top, upper, right, lower))
        return cropped

    # crop function
    # Set the cropping area with box=(left, upper, right, lower).
    # an_array = [[1, 2], [3, 4]]
    # rows = len(an_array) Find row and column length.
    # columns = len(an_array[0])
    # total_length = rows * columns. Compute total length.
    # print(total_length)
    # cut the image to tiles and return them as two dimentianal array
    # im_crop = im.crop((100, 75, 300, 150))
    # calculate # tiles : regular and level specific
    # calculate per col and per line
    # validate that I am not out side the image size

    def crop_image_to_array(self, image):
        self.image = image

        # TODO 4 tiles across depends on level
        w = 4
        # floor division
        h = int(SCREEN_HEIGHT // self.tile_size)
        # build matrix for tiles
        # TODO this is for test - delete later
        grid = [[1] * 4 for n in range(6)]

        tile_matrix = [[1]*w for n in range(h)]
        tile_matrix[0] = [0, 1, 2, 3]
        tile_matrix[1] = [4, 5, 6, 7]
        tile_matrix[2] = [8,9,10,11]
        tile_matrix[3] = [12,13,14,15]
        tile_matrix[4] = [16,17,18,19]
        tile_matrix[5] = [20,21,22,23]

        # row is y col is x
        row_index = 0
        col_index = 0
        counter = 0
        for row in tile_matrix:
            for col in row:
                #print('x {} y {} value {}'.format(str(x), str(y), str(tile_matrix[x][y])))
                assert (2 + 2 == 5, "Houston we've got a problem")

                assert((row_index * self.tile_size) in range(0, w), "Top outside range")

                assert ((row_index * self.tile_size) in range(0, w), "Top outside range")

                assert ((row_index * self.tile_size) in range(0, w), "Top outside range")

                assert ((row_index * self.tile_size) in range(0, w), "Top outside range")

                top = row_index * self.tile_size
                upper = col_index * self.tile_size
                right = row_index * self.tile_size + self.tile_size
                lower = col_index * self.tile_size + self.tile_size
                #print('top {} upper {} right {} lower {}'.format(str(top), str(upper), str(right), str(lower)))
                #print('counter {}'.format(str(counter)))

                cropped = self.crop_image_PIL(self.image,top, upper, right, lower)
                # convert to pygame image
                mode = cropped.mode
                size = cropped.size
                data = cropped.tobytes()
                #
                py_image = pygame.image.fromstring(data, size, mode)
                # position is set in game view when the tile is displayed
                py_tile = Tile(py_image, self.tile_size, row_index, col_index, TILE_INVISIBLE)
                tile_matrix[row_index][col_index] = py_tile
                counter += 1
                col_index += 1
            row_index += 1
            col_index = 0

        return tile_matrix

