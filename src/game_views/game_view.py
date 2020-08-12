# play window
# draw screen
# grid
# buttom screen with place holders for current tiles
# main menu
# get user mood or not
# return will lead to load image interstate menu

import os, os.path
import pygame

from pygame.locals import *
from src.game_views.views import View
from src.rk_communication.rk_http_requests import *
from src.game_consts.game_constants import *
from src.game_utils.game_utils import *
from src.ui_elements.dash_board import DashBoard
from src.game_utils.game_logger import RkLogger

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
TEXT_COLOR = pygame.Color(255, 255, 255)

# how many spacers vertical and horizontal
SCREEN_SPACER_NUMBER_VER = 3
SCREEN_SPACER_NUMBER_HOR = 2

titleFont = pygame.font.SysFont("comicsansmsttf", 60)
FONT = pygame.font.Font(None, 32)

def generate_random_color():
    start = 0
    stop = 255

    red = random.randint(start, stop)
    green = random.randint(start, stop)
    blue = random.randint(start, stop)
    return pygame.Color(red, green, blue)


# main game loop
# start in prepare function
# by bringing the puzzle image in one image and as grid tiles
# by level decide how and if to display it
# set the tile size
# implement drag and drop function
# implement game dashboard: score, time, number of tiles left etc
# dash board also has mood str and the RK result
# TODO add pause button
# TODO levels description
# first level show bg half transparent of image. then show a percentage of tiles. i.e. for 24 tiles show 6 then decrease.
# when hover on correct tile glow. then glow at finite number of times. when done issue a message you are now on your own
# show art for X seconds then dissapear before game start
# finite number of steps until game over
# button for info on art
# number of tiles per grid
# change of levels in options: you have set your level vs you have achieved your level
# text into locale
# number of tiles to drag is always number of rows
firstTimeGrid = False

class GameView(View):

    def __init__(self, screen, level):
        self.mood_str = None
        self.transitionToState = None
        self.screen = screen
        self.game_utils = GameUtils(level)
        self.level = level

        self.top_drag_grid_x = SCREEN_SPACER_SIZE
        self.top_drag_grid_y = SCREEN_SPACER_SIZE
        self.dash_board_position = [0, 0]
        self.drag_tiles_position = [0, 0]
        self.dashboard = DashBoard(self.screen, self.game_utils.grid_width, self.game_utils.grid_height, SCREEN_SPACER_SIZE)
        self.grid_size = None
        self.puzzle_image = None
        self.pil_image = None
        self.logger = RkLogger.__call__().get_logger()
        self.tiles_grid = None
        self.drag_tiles_grid = None
        self.tiles_to_show = None


    # create the drag grid
    # init with random tiles
    def init_drag_tiles(self):
        total_grid_size = int(self.level['tiles_ver'])*int(self.level['tiles_hor'])
        list_len = self.level['tiles_ver']
        index = 0
        list_index = random.sample(range(0, total_grid_size), int(self.level['tiles_ver']))
        while index < list_len:

            if len(self.drag_tiles_grid) == 0:
                self.level['tiles_ver']
        print()



    # get image and tiles grid
    def prepare(self, tile_grid, image,title, long_title):

        self.top_drag_grid_x = SCREEN_SPACER_SIZE
        self.top_drag_grid_y = SCREEN_SPACER_SIZE
        self.dash_board_position = [4, 3]
        self.drag_tiles_position = [4, 3]
        self.title = title
        self.long_title = long_title
        self.grid_size = (self.game_utils.grid_width, self.game_utils.grid_height)
        self.pil_image = image
        self.tiles_grid = tile_grid
        # self.tiles_drag_grid = self.init_drag_tiles()
        total_size = len(self.tiles_grid) * len(self.tiles_grid[0])
        self.num_rows = len(self.tiles_grid)
        self.num_cols = len(self.tiles_grid[0])
        self.locations_matrix = [[1] * self.num_cols for n in range(self.num_rows)]
        tile = tile_grid[0][0]
        self.tile_size = tile.size
        # number oh shown tiles is floor fifth og the whole
        number_tiles_displayed = int(total_size / 5)
        list_to_random = list(range(0, total_size))
        self.tiles_to_show = random.sample(list_to_random, k=number_tiles_displayed)
        self.draw_grid_of_rects()
        self.display_tiles()
        self.display_dash_board()

    # draw grid of rects around the tiles
    # last row is not the same size as the previous TODO fix it
    def draw_grid_of_rects(self):
        print('draw_grid_of_rects')
        width = self.pil_image.width
        height = self.pil_image.height

        grid_color = generate_random_color()
        # self.logger.info("draw_grid width {} height {}".format(str(width),str(height)))

        for y in range(self.num_rows):
            for x in range(self.num_cols):
                row_spacer = OUTER_BORDER_SIZE / 2 + SCREEN_SPACER_SIZE * y
                col_spacer = OUTER_BORDER_SIZE / 2 + SCREEN_SPACER_SIZE * x
                # print('row_spacer {} col_spacer {}'.format(str(row_spacer), str(col_spacer)))

                x_pos = int(x * self.tile_size + col_spacer)
                y_pos = int(y * self.tile_size + row_spacer)
                print('x_pos {} y_pos {}'.format(str(x_pos), str(y_pos)))
                self.locations_matrix[y][x] = (x_pos, y_pos)
                rect = pygame.Rect(x_pos, y_pos, self.tile_size, self.tile_size)
                # self.logger.info("y {} x {} ".format(str(y_pos),str(x_pos)))
                pygame.draw.rect(self.screen, grid_color, rect, SCREEN_SPACER_SIZE)



    def handleEvents(self):
        events = pygame.event.get()
        for event in events:
            #self.logger.info("event type " + str(event.type))
            if event.type == pygame.QUIT:
                exit()
            # handle the text input first
            # self.textinput.handle_event(event)
            # if event.type == pygame.QUIT:
            #    done = True

            # handle drag drop and locations

            # when ends : go back to main menu game over
            # self.transitionToState = self.MENU_ITEM_TO_VIEW_STATE[self.selectedItem]

    # display tiles on grid
    # i want a little space between the tiles
    # the first tile is on spacer
    # the second is spacer * row or col + 1
    def display_tiles(self):
        # check for grid tiles
        x = 0
        y = 0

        x_counter = 0
        y_counter = 0

        for row in self.tiles_grid:
            for col in row:
                # row_index is screen spacer and tile size times row
                #print('counter {} coords[0] {} coords[1] {}'.format(str(counter), str(col.coords[0]),
                #                                                 str(col.coords[1])))

                loc_tuple = self.locations_matrix[x_counter][y_counter]

                y = int(loc_tuple[0])
                x = int(loc_tuple[1])
                self.logger.info('y {} x {}'.format(str(y), str(x)))
                # # TODO set the Tile object state
                # tile.y = y
                # tile.state = TILE_ON_BOARD_TEST
                display_tile = col.image
                self.screen.blit(display_tile, (y, x))
                # self.tiles_grid[col.y_index][col.x_index] = tile
                y_counter += 1
                if y_counter > self.num_cols - 1:
                    y_counter = 0
            x_counter += 1

    # display only number of tiles as hints
    # get the number then get a set of random locations on grid to display
    # update the tile grid with tile status for these tiles
    def display_tiles_by_level(self):
        # check for grid tiles
        counter = 0
        print('')
        counter_col = 0
        # row is y col is x
        x = 0
        y = 0
        counter = 0

        for row in self.tiles_grid:
            for col in row:
                # row_index is screen spacer and tile size times row
                #print('counter {} coords[0] {} coords[1] {}'.format(str(counter), str(col.coords[0]),
                #                                                 str(col.coords[1])))

                row_spacer = SCREEN_SPACER_SIZE * col.coords[0] + SCREEN_SPACER_SIZE
                col_spacer = SCREEN_SPACER_SIZE * col.coords[1] + SCREEN_SPACER_SIZE
                #print('row_spacer {} col_spacer {}'.format(str(row_spacer), str(col_spacer)))

                x = col.x_pos + row_spacer
                y = col.y_pos + col_spacer
                if counter in self.tiles_to_show:
                    display_tile = col.image
                    self.screen.blit(display_tile, (y, x))
                # # TODO set the Tile object state
                # tile.y = y
                # tile.state = TILE_ON_BOARD_TEST
                #print('y {} x {}'.format(str(y), str(x)))

                # self.tiles_grid[col.y_index][col.x_index] = tile
                counter += 1


    # get 6 random tiles which are not yet displayed
    # display vertically
    # add mouse drag actions
    def display_test_tiles(self):
        grid = self.tiles_grid # [[1] * 4 for n in range(6)]

        x = 0
        y = 0
        w = 117
        print('display_test_tiles')
        for row in grid:
            for col in row:
                # TODO rect x,w,w,h
                x = col.x_pos
                y = col.y_pos
                #print('x {} y {}'.format(str(x), str(y)))
                pygame.draw.rect(self.screen, self.generate_random_color(), [x,y,w, w])
                pygame.display.update()
                x = x + w
            y = y + w
            x = 0

    # display game dashboard
    # time
    # tiles x of y
    # name of art and painter are shown as the player progresses
    def display_dash_board(self):
        self.dashboard.set_title_info(self.title,self.long_title)

    # start from random number of vertical tiles
    # get random
    # when one is placed on grid : de count
    # get a random from what is left by state of tile
    #
    def display_drag_tiles(self):
        print()

    def render(self):
        if self.level.id < LEVEL_MASTER:
            self.display_tiles()
            #self.screen.blit(self.puzzle_image, (self.top_drag_grid_x, self.top_drag_grid_y))
        else:
            #self.display_test_tiles()
            self.display_tiles()
            #self.display_drag_tiles()
        self.display_dash_board()
        self.display_drag_tiles()

    def transition(self):
        return self.transitionToState
