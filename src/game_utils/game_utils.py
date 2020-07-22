import pygame
import random
import math
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
# function to validate the cropsize
# values are first 2 are row,col on the left side
# last 2 are bottom right on the right side
# TODO if error exit game ? or find new image ?
def validete_crop_size(width, height, tile_size, *values):
    x = 0
    y = 0
    left = values[0]
    upper = values[1]
    right = values[2]
    lower = values[3]

    if right < left:
        left, right = right, left

    if lower < upper:
        lower, upper = upper, lower



    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)
    # assert ((row_index * self.tile_size) in range(0, w), "Top outside range")


# from box and image size get the x y coodinates in the grid
def getXYCoordinatesFromBox(box, tile_size):
    print (box)
    # find the middle point
    x = box[0] + tile_size/2
    y = box[1] + tile_size/2
    x_index = int(x/tile_size)
    y_index = int(y/tile_size)
    return y_index, x_index


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
    def crop_image_PIL(self, image, left, upper, right, lower):
        cropped = image.crop((left, upper, right, lower))

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
    # calculate where I am on the grid by dividing the box to the grid

    def crop_image_to_array(self, image):
        self.image = image

        # TODO 4 tiles across depends on level
        w = 4
        # floor division
        h = int(SCREEN_HEIGHT // self.tile_size)
        # build matrix for tiles
        width = int(self.image.width)
        height = int(self.image.height)
        chopsize = int(self.tile_size)

        w_index = int(math.ceil(width/chopsize))
        h_index = int(math.ceil(height/chopsize))
        tile_matrix = [[1] * w_index for n in range(h_index)]
        w_counter = 0
        h_counter = 0
        counter = 0
        infile = 'in.jpg'
        for x0 in range(0, width, chopsize):
            for y0 in range(0, height, chopsize):
                box = (x0, y0,
                       x0 + chopsize if x0 + chopsize < width else width - 1,
                       y0 + chopsize if y0 + chopsize < height else height - 1)
                print('box {}'.format(box))
                cropped = image.crop(box)
                cropped.save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))
                mode = cropped.mode
                size = cropped.size
                data = cropped.tobytes()
                #
                py_image = pygame.image.fromstring(data, size, mode)
                # position is set in game view when the tile is displayed
                counter+=1
                if (h_index > 7 or w_index > 4):
                    print ('error')
                coords = getXYCoordinatesFromBox(box, self.tile_size)
                py_tile = Tile(py_image, self.tile_size, x0, y0, coords, TILE_INVISIBLE)

                tile_matrix[coords[0]][coords[1]] = py_tile
                # img.crop(box).save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))




        # row is y col is x

        # counter = 0
        # for row in tile_matrix:
        #     for col in row:
        #         # print('x {} y {} value {}'.format(str(x), str(y), str(tile_matrix[x][y])))
        #
        #         left = row_index * self.tile_size
        #         upper = col_index * self.tile_size
        #         right = row_index * self.tile_size + self.tile_size
        #         lower = col_index * self.tile_size + self.tile_size
        #         print('left {} upper {} right {} lower {}'.format(str(left), str(upper), str(right), str(lower)))
        #         validete_crop_size(self.image.width, self.image.height, self.tile_size, *(left, upper, right, lower))
        #         print('row_index {} col_index {} counter {}'.format(str(row_index), str(col_index), str(counter)))
        #
        #         # print('top {} upper {} right {} lower {}'.format(str(top), str(upper), str(right), str(lower)))
        #         # print('counter {}'.format(str(counter)))
        #
        #         cropped = self.crop_image_PIL(self.image, left, upper, right, lower)
        #         # convert to pygame image
        #         mode = cropped.mode
        #         size = cropped.size
        #         data = cropped.tobytes()
        #         #
        #         py_image = pygame.image.fromstring(data, size, mode)
        #         # position is set in game view when the tile is displayed
        #         py_tile = Tile(py_image, self.tile_size, row_index, col_index, TILE_INVISIBLE)
        #         tile_matrix[row_index][col_index] = py_tile
        #         counter += 1
        #         col_index += 1
        #     row_index += 1
        #     col_index = 0

        return tile_matrix
