# play window
# draw screen
# grid
# buttom screen with place holders for current tiles
# main menu
# get user mood or not
# return will lead to load image interstate menu

import pygame
from pygame.locals import *
from src.game_views.views import View
from src.rk_communication.rk_http_requests import *
from src.game_consts.game_constants import *
from src.game_utils.game_utils import *

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2
TEXT_COLOR = pygame.Color(255, 255, 255)
SCREEN_SPACER_SIZE = 5
# how many spacers vertical and horizontal
SCREEN_SPACER_NUMBER_VER = 3
SCREEN_SPACER_NUMBER_HOR = 2

titleFont = pygame.font.SysFont("comicsansmsttf", 60)
FONT = pygame.font.Font(None, 32)


# main game loop
# start in prepare function
# by bringing the puzzle image in one image and as grid tiles
# by level decide how and if to display it
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

class GameView(View):
    # Displays the main menu

    titleText = "RK_PUZZLES_GAME"
    centerX = HALF_SCREEN_WIDTH
    centerY = HALF_SCREEN_HEIGHT
    grid_image = None

    def __init__(self, screen, bg_color):
        self.mood_str = None
        self.transitionToState = None
        self.bg_color = bg_color
        self.screen = screen
        self.game_utils = GameUtils()
        self.level = None
        self.top_drag_grid_x = SCREEN_SPACER_SIZE
        self.top_drag_grid_y = SCREEN_SPACER_SIZE
        self.dash_board_position = [0, 0]
        self.drag_tiles_position = [0, 0]

        self.tile_size = None
        self.grid_size = None
        self.puzzle_image = None
        self.pil_image = None

        self.tiles_grid = None

    # call the game utils to load the image from list of images returned
    # resize image
    # crop to tiles and resize them

    def getLoadedImage(self):
        search_art_obj = SearchArt(self.mood_str)
        art_dict = search_art_obj.getImageList()
        get_art_tiles = GetArtTiles(art_dict)
        art_tiles_obj = get_art_tiles.getArtImage()
        art_image = GetArtImage(art_tiles_obj, self.game_utils.grid_width, self.game_utils.grid_height)
        pygame_image, pil_image = art_image.getBitmapFromTiles()
        return pygame_image, pil_image

    # get image and tiles grid
    def prepare(self, mood_str, level):
        if mood_str == '':
            self.mood_str = self.game_utils.getRandomSearchValue()
        else:
            self.mood_str = mood_str

        self.level = level
        self.top_drag_grid_x = SCREEN_SPACER_SIZE
        self.top_drag_grid_y = SCREEN_SPACER_SIZE
        self.dash_board_position = [4, 3]
        self.drag_tiles_position = [4, 3]

        self.tile_size = self.game_utils.tile_size
        self.grid_size = (self.game_utils.grid_width, self.game_utils.grid_height)

        self.puzzle_image, self.pil_image = self.getLoadedImage()

        self.tiles_grid = self.game_utils.crop_image_to_array(self.pil_image)

    def handleEvents(self):

        events = pygame.event.get()
        for event in events:
            print("event type " + str(event.type))
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

        print('rows {} cols  {}'.format(str(len(self.tiles_grid)), str(len(self.tiles_grid[0]))))
        # calculte the Y positions
        col_positions = [SCREEN_SPACER_SIZE,
                         self.tile_size + 2 * SCREEN_SPACER_SIZE,
                         2 * self.tile_size + 3 * SCREEN_SPACER_SIZE,
                         3 * self.tile_size + 4 * SCREEN_SPACER_SIZE]
        counter_col = 0
        # row is y col is x
        x = 0
        y = 0
        counter = 0

        for row in self.tiles_grid:
            for col in row:
                # row_index is screen spacer and tile size times row
                row_spacer = SCREEN_SPACER_SIZE * col.coords[1]
                if row_spacer == 0:
                    row_spacer = SCREEN_SPACER_SIZE
                col_spacer = SCREEN_SPACER_SIZE * col.coords[0]
                if col_spacer == 0:
                    col_spacer = SCREEN_SPACER_SIZE
                x = col.x_pos + row_spacer
                y = col.y_pos + col_spacer
                display_tile = col.image
                # TODO set the Tile object state
                # tile.y = y
                # tile.state = TILE_ON_BOARD_TEST
                print('y {} x {}'.format(str(y), str(x)))
                self.screen.blit(display_tile, (y, x))

                # self.tiles_grid[col.y_index][col.x_index] = tile
                print('counter {}'.format(str(counter)))
                counter += 1


        print('end display tiles')

    def generate_random_color(self):
        start = 0
        stop = 255

        red = random.randint(start, stop)
        green = random.randint(start, stop)
        blue = random.randint(start, stop)
        return pygame.Color(red, green, blue)

    # get 6 random tiles which are not yet displayed
    # display vertically
    # add mouse drag actions
    def display_test_tiles(self):
        col_positions = [SCREEN_SPACER_SIZE,
                         self.tile_size + 2 * SCREEN_SPACER_SIZE,
                         2 * self.tile_size + 3 * SCREEN_SPACER_SIZE,
                         3 * self.tile_size + 4 * SCREEN_SPACER_SIZE]
        grid = self.tiles_grid # [[1] * 4 for n in range(6)]

        x = 0
        y = 0
        w = 117
        print('display_test_tiles')
        for row in grid:
            for col in row:
                # TODO rect x,w,w,h
                display_tile = col.image
                if col.row_index == 0:
                    row_spacer = SCREEN_SPACER_SIZE
                elif col.row_index == 1:
                    row_spacer = SCREEN_SPACER_SIZE*2
                elif col.row_index == 2:
                    row_spacer = SCREEN_SPACER_SIZE * 2 + SCREEN_SPACER_SIZE
                else:
                    row_spacer = SCREEN_SPACER_SIZE*col.row_index + SCREEN_SPACER_SIZE
                row_pos = col.row_index*col.size + row_spacer
                # col is one of 4 positions on grid
                col_pos = col_positions[col.col_index]
                # TODO set the Tile object state
                x = col_pos
                y = row_pos
                # tile.y = y
                # tile.state = TILE_ON_BOARD_TEST
                # self.screen.blit(display_tile, (x, y))
                print('x {} y {}'.format(str(x), str(y)))
                pygame.draw.rect(self.screen, self.generate_random_color(), [x,y,w, w])
                pygame.display.update()
                x = x + w
            y = y + w
            x = 0

        print()

    # display game dashboard
    # time
    # tiles x of y
    # name of art and painter are shown as the player progresses
    def display_dash_board(self):
        print()

    def display_drag_tiles(self):
        print()

    def render(self):
        if self.level < LEVEL_MASTER:
            self.screen.blit(self.puzzle_image, (self.top_drag_grid_x, self.top_drag_grid_y))
        else:
            #self.display_test_tiles()
            self.display_tiles()
            #self.display_drag_tiles()
            self.display_dash_board()
        # self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        # pygame.display.flip()

    def transition(self):
        return self.transitionToState
