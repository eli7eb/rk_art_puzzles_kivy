import pygame
import random
import math

from PIL import Image

from src.game_consts.game_constants import *
from src.ui_elements.grid_tile import Tile
from src.game_utils.game_logger import RkLogger

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
def validate_crop_size(width, height, tile_size, *values):
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
    logger = RkLogger.__call__().get_logger()
    logger.info("box {}".format(box))

    # find the middle point
    x = box[0] + tile_size/2
    y = box[1] + tile_size/2
    x_index = int(x/tile_size)
    y_index = int(y/tile_size)
    return y_index, x_index


class GameUtils:

    def __init__(self,  level):
        self.done = False
        self.image = None
        self.level = level
        # tile needs to 4/6 fit horizontally in the screen by level and one spare for the drag tiles scroller
        # vertically is 4/5 as we need space for the dashboard
        # at least 5 tiles across: 4 grid and one to drag

        tile_size_ver = (SCREEN_HEIGHT - SCREEN_HEIGHT/5 - SCREEN_SPACER_NUMBER_VER * SCREEN_SPACER_SIZE) / (self.level.tiles_ver)
        tile_size_hor = (SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR * SCREEN_SPACER_SIZE) / (self.level.tiles_hor+1)
        self.tile_size = tile_size_ver # (SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR * SCREEN_SPACER_SIZE) / (self.level.tiles_hor+1)
        self.grid_width = SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR * SCREEN_SPACER_SIZE - self.tile_size
        self.grid_height = SCREEN_HEIGHT - SCREEN_SPACER_NUMBER_VER * SCREEN_SPACER_SIZE - self.tile_size

    # crop PIL image from this class and outside classes
    def crop_image_PIL(self, image, left, upper, right, lower):
        cropped = image.crop((left, upper, right, lower))

        return cropped

    def getRandomSearchValue(self):
        return random.choice(MOOD_IDEAS)

    def fit_aquares(self):
        print()
        im_pth = "rk_background.png"
        # img = Image.open("rk_background.png")
        im = Image.open(im_pth)
        n = 12

        im = im.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
        width = im.width
        height = im.height
        px = math.ceil(math.sqrt(n * width / height))
        if math.floor(px * height / width) * px < n:
            sx = height / math.ceil(px * y / x)
        else:
            sx = width / px
        py = math.ceil(math.sqrt(n * height / width))
        if math.floor(py * width / height) * py < n:
            sy = width / math.ceil((width * py / height))
        else:
            sy = height / py
        return math.max(sx, sy)

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
    # create the tile object with image and image_transparent
    def crop_image_to_array(self, image,tiles_hor,tiles_ver):
        self.image = image

        # TODO 4 tiles across depends on level
        w = tiles_hor
        # floor division
        h = tiles_ver
        int(SCREEN_HEIGHT // self.tile_size)
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
                logger = RkLogger.__call__().get_logger()
                logger.info('box {}'.format(box))

                cropped = image.crop(box)
                mode = cropped.mode
                size = cropped.size
                data = cropped.tobytes()
                py_image = pygame.image.fromstring(data, size, mode)

                # PIL for transparant copy
                pil_image_rgba = cropped.copy()
                # test to save tiles
                # cropped.save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))

                pil_image_rgba = pil_image_rgba.convert('RGBA')
                #pil_image_rgba = pil_image_rgba.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
                data = pil_image_rgba.getdata()  # you'll get a list of tuples
                newData = []
                for a in data:
                    a = a[:3]  # you'll get your tuple shorten to RGB
                    a = a + (128,)  # change the 100 to any transparency number you like between (0,255)
                    newData.append(a)
                pil_image_rgba.putdata(newData)  # you'll get your new img ready
                mode_t = pil_image_rgba.mode
                size_t = pil_image_rgba.size
                data_t = pil_image_rgba.tobytes()
                py_image_t = pygame.image.fromstring(data_t, size_t, mode_t)
                # position is set in game view when the tile is displayed
                counter += 1
                coords = getXYCoordinatesFromBox(box, self.tile_size)

                py_tile = Tile(py_image, py_image_t, self.tile_size, x0, y0, coords, TILE_INVISIBLE)

                tile_matrix[coords[0]][coords[1]] = py_tile
                # img.crop(box).save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))

        return tile_matrix
