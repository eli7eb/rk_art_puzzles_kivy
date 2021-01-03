import pygame
from kivy.app import App
from kivy.uix.widget import Widget

# main class for the tiles grid
# based on level draw which part(s) of the grid
from src.game_utils.game_logger import RkLogger
from src.game_utils.game_utils import GameUtils
from src.game_consts.game_constants import *

class GameTilesGrid (Widget):
    def build(self):
        self.draw_tiles()

    def draw_tiles(self):
        with self.canvas:
            pass

    def draw_grid_of_rects(self,*args):
        logger = RkLogger.__call__().get_logger()
        logger.info('draw_grid_of_rects')
        # TODO width = im.width
        # TODO height = im.height
        for arg in args:
            logger.info("rk_callback {}".format(args))

        # grid_color = GameUtils.generate_random_color()
        # # self.logger.info("draw_grid width {} height {}".format(str(width),str(height)))
        #
        # for y in range(num_rows):
        #     for x in range(num_cols):
        #         row_spacer = OUTER_BORDER_SIZE / 2 + SCREEN_SPACER_SIZE * y
        #         col_spacer = OUTER_BORDER_SIZE / 2 + SCREEN_SPACER_SIZE * x
        #         # print('row_spacer {} col_spacer {}'.format(str(row_spacer), str(col_spacer)))
        #
        #         x_pos = int(x * tile_size + col_spacer)
        #         y_pos = int(y * tile_size + row_spacer)
        #         print('x_pos {} y_pos {}'.format(str(x_pos), str(y_pos)))
        #         locations_matrix[y][x] = (x_pos, y_pos)
        #         rect = pygame.Rect(x_pos, y_pos, tile_size, tile_size)
        #         # self.logger.info("y {} x {} ".format(str(y_pos),str(x_pos)))
        #         pygame.draw.rect(gameDisplay, grid_color, rect, SCREEN_SPACER_SIZE)
        # print('end')

