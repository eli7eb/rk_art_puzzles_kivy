# play window
# draw screen
# grid
# buttom screen with place holders for current tiles
# main menu
# get user mood or not
# return will lead to load image interstate menu

import os, os.path
import pygame
from pathlib import Path
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
SCREEN_SPACER_SIZE = 5
# how many spacers vertical and horizontal
SCREEN_SPACER_NUMBER_VER = 3
SCREEN_SPACER_NUMBER_HOR = 2

titleFont = pygame.font.SysFont("comicsansmsttf", 60)
FONT = pygame.font.Font(None, 32)

def generate_random_color(self):
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

            art_tiles_obj = get_art_tiles.getArtImage()
            self.dashboard.set_title_info(art_dict)
            art_image = GetArtImage(art_tiles_obj, self.game_utils.grid_width, self.game_utils.grid_height)
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
    def prepare(self, mood_str):
        if mood_str == '':
            self.mood_str = self.game_utils.getRandomSearchValue()
        else:
            self.mood_str = mood_str

        self.top_drag_grid_x = SCREEN_SPACER_SIZE
        self.top_drag_grid_y = SCREEN_SPACER_SIZE
        self.dash_board_position = [4, 3]
        self.drag_tiles_position = [4, 3]

        self.grid_size = (self.game_utils.grid_width, self.game_utils.grid_height)

        self.puzzle_image, self.pil_image = self.getLoadedImage()

        self.tiles_grid = self.game_utils.crop_image_to_array(self.pil_image,self.level.tiles_hor,self.level.tiles_ver)
        # self.tiles_drag_grid = self.init_drag_tiles()
        total_size = len(self.tiles_grid) * len(self.tiles_grid[0])
        # number oh shown tiles is floor fifth og the whole
        number_tiles_displayed = int(total_size / 5)
        list_to_random = list(range(0, total_size))
        self.tiles_to_show = random.sample(list_to_random, k=number_tiles_displayed)
        self.draw_grid()

    # draw grid of rects around the tiles
    # last row is not the same size as the previous TODO fix it
    def draw_grid(self):
        width = len(self.tiles_grid[0])
        height = len(self.tiles_grid)
        block_size = self.game_utils.tile_size
        grid_color = generate_random_color(self)
        #self.logger.info("draw_grid width {} height {}".format(str(width),str(height)))

        for y in range(height):
            for x in range(width):
                row_spacer = SCREEN_SPACER_SIZE * y + SCREEN_SPACER_SIZE
                col_spacer = SCREEN_SPACER_SIZE * x + SCREEN_SPACER_SIZE
                # print('row_spacer {} col_spacer {}'.format(str(row_spacer), str(col_spacer)))

                x_pos = x * block_size + col_spacer
                y_pos = y * block_size + row_spacer

                rect = pygame.Rect(x_pos, y_pos, block_size, block_size)
                #self.logger.info("y {} x {} ".format(str(y_pos),str(x_pos)))
                pygame.draw.rect(self.screen, grid_color, rect,SCREEN_SPACER_SIZE)


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
        counter = 0

        self.logger.info('rows {} cols  {}'.format(str(len(self.tiles_grid)), str(len(self.tiles_grid[0]))))
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
                self.logger.info('y {} x {}'.format(str(y), str(x)))

                if (y % 2 == 0):
                     display_tile = col.transparant_image
                else:
                     display_tile = col.transparant_image
                # # TODO set the Tile object state
                # tile.y = y
                # tile.state = TILE_ON_BOARD_TEST
                #print('y {} x {}'.format(str(y), str(x)))
                self.screen.blit(display_tile, (y, x))
                # self.tiles_grid[col.y_index][col.x_index] = tile
                counter += 1

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
        print()

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
