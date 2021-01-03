import pygame
import random
import math

from PIL import Image

from src.game_consts.game_constants import *
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
class GameUtilsSingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class GameUtils(metaclass=GameUtilsSingletonMeta):

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

    def generate_random_color(self):
        start = 0
        stop = 255

        red = random.randint(start, stop)
        green = random.randint(start, stop)
        blue = random.randint(start, stop)
        return pygame.Color(red, green, blue)

    def getRandomSearchValue(self):
        return random.choice(MOOD_IDEAS)

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


