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

levels = {
  "beginner" : {
    "width" : 440,
    "height" : 660,
    "num_tiles": 24
  },
  "intermid" : {
    "width" : 450,
    "height" : 630,
    "num_tiles": 35
  },
   "inter_1": {
     "width": 420,
     "height": 630,
     "num_tiles": 63
   },
   "inter_2": {
      "width": 450,
      "height": 630,
      "num_tiles": 35
   },
    "master" : {
    "width" : 450,
    "height" : 650,
    "num_tiles": 117
  }
}
LOADING_ART_TEXT_COLOR = pygame.Color(242, 214, 179, 95)

# count number of spaces in grid is calculated as number of tiles horizontally -1
# count number of spaces in grid is calculated as number of tiles vertically -1
# function to validate the cropsize
# values are first 2 are row,col on the left side
# last 2 are bottom right on the right side
# TODO if error exit game ? or find new image ?
def validate_crop_size(image,tile_size):
    w = abs(image.width - tile_size)
    h = abs(image.height - tile_size)
    if w > 5 or h > 5:
        return False
    return True


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
    def __init__(self, screen,bg_color,level_name):
        View.__init__(self, screen,bg_color)
        self.level_name = level_name
        self.level = levels[self.level_name]
        self.title = None
        self.long_title = None

    # call the game utils to load the image from list of images returned
    # resize image
    # crop to tiles and resize them
    # 2 modes remote and locally when I need to test
    # TODO when local make sure there is a title
    def getLoadedImage(self):
        remote = False
        if remote:
            search_art_obj = SearchArt(self.mood_str)
            # get a list of art works for this mood
            art_dict = search_art_obj.getImageList()
            # get one art piece
            get_art_tiles = GetArtTiles(art_dict)
            self.title = art_dict['title']
            self.long_title = art_dict['longTitle']
            # at this stage I need to know the final image size
            art_tiles_obj = get_art_tiles.getArtImage()
            #self.dashboard.set_title_info(art_dict)
            art_image = GetArtImage(art_tiles_obj,SCREEN_WIDTH, SCREEN_HEIGHT)
            pygame_image, pil_image = art_image.getBitmapFromTiles()
            return pygame_image, pil_image
        else:
            base_path = Path(__file__).parent.resolve()
            file_path = (base_path / "../assets/rk_background.png").resolve()
            local_pil_image = Image.open(file_path)
            self.title = 'girl at kitchen'
            self.long_title = 'vermeer girl at kitchen'

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

    def get_tile_blurred(self, py_image):
        pil_image_rgba = py_image.copy()
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
        return py_image_t




    # the squares need to be exactly the size to fit in the array
    # we need to decide which comes first the image size or the tiles size
    # on a beginner level I have 4 - 6
    # then 5 - 7
    # then 7 - 9
    def fit_squares(self):
        logger = RkLogger.__call__().get_logger()
        logger.info("fit_squares")
        im = self.pil_image
        num_tiles = self.level['num_tiles']
        width = im.width
        height = im.height

        px = math.ceil(math.sqrt(num_tiles * width / height))
        if math.floor(px * height / width) * px < num_tiles:
            sx = height / math.ceil(px * height / width)
        else:
            sx = width / px
        py = math.ceil(math.sqrt(num_tiles * height / width))
        if math.floor(py * width / height) * py < num_tiles:
            sy = width / math.ceil((width * py / height))
        else:
            sy = height / py
        # TODO get the number of cols and rows by deviding the width/size and height/size
        # return all as tuple
        size = int(max(sx, sy))
        num_cols = int(width / size)
        num_rows = int(height / size)
        return size, num_cols, num_rows

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
    def crop_image_to_array(self, tile_tuple):
        im = self.pil_image
        # TODO 4 tiles across depends on level
        width = int(im.width)
        height = int(im.height)
        chopsize = tile_tuple[0]

        num_cols = tile_tuple[1]
        num_rows = tile_tuple[2]

        tile_matrix = [[1] * num_cols for n in range(num_rows)]
        counter = 0

        for x0 in range(0, width, chopsize):
            for y0 in range(0, height, chopsize):
                box = (x0, y0,
                       x0 + chopsize if x0 + chopsize < width else width - 1,
                       y0 + chopsize if y0 + chopsize < height else height - 1)
                print('box {}'.format(box))

                cropped = im.crop(box)
                if validate_crop_size(cropped, chopsize):
                    mode = cropped.mode
                    size = cropped.size
                    data = cropped.tobytes()
                    py_image = pygame.image.fromstring(data, size, mode)

                    # position is set in game view when the tile is displayed
                    counter += 1
                    coords = getXYCoordinatesFromBox(box, chopsize)
                    print("coords {}".format(str(coords)))
                    # TODO fix this
                    py_image_t = py_image.copy() # self.get_tile_blurred(py_image)
                    py_tile = Tile(py_image, py_image_t, chopsize, x0, y0, coords, TILE_INVISIBLE)

                    tile_matrix[coords[0]][coords[1]] = py_tile
                    # img.crop(box).save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))
                else:
                    print('error on crop')


                # PIL for transparant copy

                # position is set in game view when the tile is displayed
                counter += 1
                coords = getXYCoordinatesFromBox(box, chopsize)

                py_tile = Tile(py_image, py_image_t, chopsize, x0, y0, coords, TILE_INVISIBLE)

                tile_matrix[coords[0]][coords[1]] = py_tile
                # img.crop(box).save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))


        return tile_matrix

    def get_image_data(self):
        return self.tiles_grid

    def get_image(self):
        return self.pil_image

    def get_image_info(self):
        return self.title, self.long_title

    def getRandomSearchValue(self):
        return random.choice(MOOD_IDEAS)

        # resize based on level
        # width needs to accomodate the scroller
        # height needs to accomodate the dashboard
        # validate that the size is divided by tile_size
    def image_resize(self, im):
        grid_size_percent = 85
        original_width = SCREEN_WIDTH - OUTER_BORDER_SIZE * 2 + INNER_BORDER_SIZE
        original_height = SCREEN_HEIGHT - OUTER_BORDER_SIZE * 2 + INNER_BORDER_SIZE
        # make the grid 80%

        im_width = self.level['width']  # int(original_width * (grid_size_percent / 100))
        im_height = self.level['height']  # int(original_height * (grid_size_percent / 100))
        im = im.resize((im_width, im_height), Image.LANCZOS)
        return im

        # get image and tiles grid
    def prepare(self, mood_str, level):
        if mood_str == '':
            self.mood_str = self.getRandomSearchValue()
        else:
            self.mood_str = mood_str
        self.transitionToState = None

        # self.top_drag_grid_x = SCREEN_SPACER_SIZE
        # self.top_drag_grid_y = SCREEN_SPACER_SIZE
        # self.dash_board_position = [4, 3]
        # self.drag_tiles_position = [4, 3]
        #
        # self.grid_size = (self.game_utils.grid_width, self.game_utils.grid_height)

        self.puzzle_image, im = self.getLoadedImage()
        self.pil_image = self.image_resize(im)
        tile_tuple = self.fit_squares()

        tile_size = tile_tuple[0]
        num_cols = tile_tuple[1]
        num_rows = tile_tuple[2]
        locations_matrix = [[1] * num_cols for n in range(num_rows)]
        #draw_border()
        #draw_grid_of_rects()



        self.tiles_grid = self.crop_image_to_array(tile_tuple)
        # self.tiles_drag_grid = self.init_drag_tiles()
        # total_size = len(self.tiles_grid) * len(self.tiles_grid[0])
        # # number oh shown tiles is floor fifth og the whole
        # number_tiles_displayed = int(total_size / 5)
        # list_to_random = list(range(0, total_size))
        # self.tiles_to_show = random.sample(list_to_random, k=number_tiles_displayed)
        # self.draw_grid()
        self.transitionToState = VIEW_STATE_GAME_A

    def render(self):
        self.loading_msg = 'LOADING ART'
        titleFont = pygame.font.SysFont("comicsansmsttf", 60)
        loading_str = titleFont.render(self.loading_msg, True, LOADING_ART_TEXT_COLOR)
        self.screen.fill(self.bg_color)
        self.screen.blit(loading_str, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])

    def transition(self):
        return self.transitionToState

    def clean(self):
        transparent = (127, 127, 127)
        self.screen.fill(transparent)
