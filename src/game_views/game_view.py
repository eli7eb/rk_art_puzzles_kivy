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

class GameView(View):
    # Displays the main menu

    titleText = "RK_PUZZLES_GAME"
    centerX = HALF_SCREEN_WIDTH
    centerY = HALF_SCREEN_HEIGHT
    grid_image = None


    def __init__(self, screen,bg_color):
        self.bg_color = bg_color
        self.screen = screen

    def getLoadedImage(self):
        searchArtObj = SearchArt(self.mood_str)
        art_dict = searchArtObj.getImageList()
        getArtWorkObj = GetArtTiles(art_dict)
        art_tiles_obj = getArtWorkObj.getArtImage()
        art_image = GetArtImage(art_tiles_obj,self.game_utils.grid_width,self.game_utils.grid_height)
        pygame_image, pil_image = art_image.getBitmapFromTiles()
        return pygame_image, pil_image

    def getTilesGrid(self):
        print('getTilesGrid')
        self.tiles_grid = self.game_utils.crop_image_to_array(self.pil_image)
        # display_surface = pygame.display.set_mode((self.grid_width, self.grid_height))



    def prepare(self, mood_str, level):
        self.transitionToState = None
        # TODO generate an array to get random value from
        if mood_str == '':
            self.mood_str = 'hand'
        else:
            self.mood_str = mood_str
        self.level = level
        self.top_drag_grid_x = SCREEN_SPACER_SIZE
        self.top_drag_grid_y = SCREEN_SPACER_SIZE
        self.game_utils = GameUtils()
        self.game_utils.calculateTileSize()
        self.game_utils.calculateGridSize()
        self.puzzle_image, self.pil_image = self.getLoadedImage()

        self.getTilesGrid()

    def handleEvents(self):

        events = pygame.event.get()
        for event in events:
            print ("event type "+ str(event.type))
            if event.type == pygame.QUIT:
                exit()
            # handle the text input first
            #self.textinput.handle_event(event)
            #if event.type == pygame.QUIT:
            #    done = True

            # handle drag drop and locations

            # when ends : go back to main menu game over
            # self.transitionToState = self.MENU_ITEM_TO_VIEW_STATE[self.selectedItem]
    def display_tiles(self):
        print ('len to display %s',len(self.tiles_grid))

    def render(self):
        if self.level < LEVEL_MASTER:
            self.screen.blit(self.puzzle_image,(self.top_drag_grid_x, self.top_drag_grid_y))
        else:
            self.display_tiles()
        # self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        pygame.display.flip()

    def transition(self):
        return self.transitionToState
