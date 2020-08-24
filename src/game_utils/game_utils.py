import pygame
import random
import math

from PIL import Image

from src.game_consts.game_constants import *

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

