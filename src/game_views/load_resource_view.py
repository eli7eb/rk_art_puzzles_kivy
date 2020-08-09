import random
import sys
import pygame
import os, os.path
import math

from pathlib import Path

from src.game_consts.game_constants import *
from src.game_views.views import View
from src.rk_communication.rk_http_requests import *
from src.ui_elements.grid_tile import Tile
from src.game_utils.game_logger import RkLogger

from src.game_consts.game_constants import SCREEN_SPACER_SIZE
# habdle all data load - remote and local
# data load is as follows:
# if remote is possible
# if mood string is not empty use this word to search otherwise get a random mood
# get list of images (art works) from RK
# choose the one - choose first the portrait ones and then from that list a random entry
# the image comes back in pieces - paste them together
# then cut in to squares
# the returned data is the list of squares (tiles)
# name and link of the art

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

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

# TODO add are you sure
class LoadingView(View):
    # Dummy screen that just quits the game (after quitting screen has been shown)
    def __init__(self, screen,bg_color,level):
        View.__init__(self, screen,bg_color)
        self.level = level

        # call the game utils to load the image from list of images returned
        # resize image
        # crop to tiles and resize them
        # 2 modes remote and locally when I need to test
    def getLoadedImage(self):
        remote = True
        if remote:
            search_art_obj = SearchArt(self.mood_str)
            # get a list of art works for this mood
            art_dict = search_art_obj.getImageList()
            # get one art piece
            get_art_tiles = GetArtTiles(art_dict)
            # at this stage I need to know the final image size
            art_tiles_obj = get_art_tiles.getArtImage()
            #self.dashboard.set_title_info(art_dict)
            art_image = GetArtImage(art_tiles_obj)
            pygame_image, pil_image = art_image.getBitmapFromTiles()
            return pygame_image, pil_image
        else:
            base_path = Path(__file__).parent.resolve()
            file_path = (base_path / "../assets/rk_background.png").resolve()
            local_pil_image = Image.open(file_path)

            local_pil_image = local_pil_image.convert('RGBA')
            local_pil_image = local_pil_image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
            data = local_pil_image.getdata()  # you'll get a list of tuples
            newData = []
            for a in data:
                a = a[:3]  # you'll get your tuple shorten to RGB
                a = a + (100,)  # change the 100 to any transparency number you like between (0,255)
                newData.append(a)
            local_pil_image.putdata(newData)  # you'll get your new img ready
            mode = local_pil_image.mode
            size = local_pil_image.size
            data = local_pil_image.tobytes()
            local_pygame_image = pygame.image.fromstring(data, size, mode)
            return local_pygame_image, local_pil_image

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

    def crop_image_to_array(self, image, tiles_hor, tiles_ver):
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

        w_index = int(math.ceil(width / chopsize))
        h_index = int(math.ceil(height / chopsize))
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
                # pil_image_rgba = pil_image_rgba.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
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

    def get_image_data(self):
        return self.tiles_grid

    def getRandomSearchValue(self):
        return random.choice(MOOD_IDEAS)

        # get image and tiles grid
    def prepare(self, mood_str, level):
        if mood_str == '':
            self.mood_str = self.getRandomSearchValue()
        else:
            self.mood_str = mood_str

        # self.top_drag_grid_x = SCREEN_SPACER_SIZE
        # self.top_drag_grid_y = SCREEN_SPACER_SIZE
        # self.dash_board_position = [4, 3]
        # self.drag_tiles_position = [4, 3]
        #
        # self.grid_size = (self.game_utils.grid_width, self.game_utils.grid_height)

        self.puzzle_image, self.pil_image = self.getLoadedImage()
        tile_tuple = self.fit_squares(self.pil_image, level.tiles_hor*level.tiles_ver)
        # size,num_cols,num_rows
        # crop to tiles and show

        self.tiles_grid = self.crop_image_to_array(self.pil_image, self.level.tiles_hor,
                                                              self.level.tiles_ver)
        # self.tiles_drag_grid = self.init_drag_tiles()
        # total_size = len(self.tiles_grid) * len(self.tiles_grid[0])
        # # number oh shown tiles is floor fifth og the whole
        # number_tiles_displayed = int(total_size / 5)
        # list_to_random = list(range(0, total_size))
        # self.tiles_to_show = random.sample(list_to_random, k=number_tiles_displayed)
        # self.draw_grid()

    def transition(self):
        return self.transitionToState
