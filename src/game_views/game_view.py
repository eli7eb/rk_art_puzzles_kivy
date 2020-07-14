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
        searchArtObj = SearchArt(self.mood_str)
        art_dict = searchArtObj.getImageList()
        getArtWorkObj = GetArtTiles(art_dict)
        art_tiles_obj = getArtWorkObj.getArtImage()
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
        self.dash_board_position = [4,3]
        self.drag_tiles_position = [4, 3]

        self.tile_size = self.game_utils.calculateTileSize()
        self.grid_size = self.game_utils.calculateGridSize()
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
        for i in range(len(self.tiles_grid)):
            for j in range(len(self.tiles_grid[i])):

                x = SCREEN_SPACER_SIZE*(i+1) + i * self.tile_size
                y = SCREEN_SPACER_SIZE*(j+1) + j * self.tile_size
                tile_object = self.tiles_grid[i][j]
                tile = tile_object.image
                tile_object.x = x
                tile_object.y = y
                tile_object.state = TILE_ON_BOARD_TEST
                self.screen.blit(tile, (x, y))
                print('row {} col {}'.format(str(x), str(y)))

                self.tiles_grid[i][j] = tile_object

    # get 4 random tiles which are not yet displayed
    # display vertically
    # add mouse drag actions
    def display_drag_tiles(self):
        print()

    # display game dashboard
    # time
    # tiles x of y
    # name of art and painter are shown as the player progresses
    def display_dash_board(self):
        print()


    def render(self):
        if self.level < LEVEL_MASTER:
            self.screen.blit(self.puzzle_image, (self.top_drag_grid_x, self.top_drag_grid_y))
        else:
            self.display_tiles()
            self.display_drag_tiles()
            self.display_dash_board()
        # self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        pygame.display.flip()

    def transition(self):
        return self.transitionToState
