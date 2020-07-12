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
        art_image = GetArtImage(art_tiles_obj,self.grid_width,self.grid_height)
        bitmap_art_image = art_image.getBitmapFromTiles()
        return bitmap_art_image

    # tile needs to fit in the screen 5 times in the horizontal directions with overheads
    def calcualteTileSize(self):
        self.tile_size = (SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR*SCREEN_SPACER_SIZE) / 5
        print("tile size " + str(self.tile_size))

    def calculateGridSize(self):
        self.grid_width = SCREEN_WIDTH - SCREEN_SPACER_NUMBER_HOR*SCREEN_SPACER_SIZE
        self.grid_height = SCREEN_HEIGHT - SCREEN_SPACER_NUMBER_VER*SCREEN_SPACER_SIZE



    def prepare(self, mood_str):
        self.transitionToState = None
        self.mood_str = mood_str

        self.top_drag_grid_x = SCREEN_SPACER_SIZE
        self.top_drag_grid_y = SCREEN_SPACER_SIZE
        self.calcualteTileSize()
        self.calculateGridSize()
        self.puzzle_image = self.getLoadedImage()
        # display_surface = pygame.display.set_mode((self.grid_width, self.grid_height))





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


    def render(self):
       
        self.screen.blit(self.puzzle_image,(self.top_drag_grid_x, self.top_drag_grid_y))
        print("on screen")
        # self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        pygame.display.flip()

    def transition(self):
        return self.transitionToState
