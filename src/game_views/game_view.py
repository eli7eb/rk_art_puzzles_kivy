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

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2
TEXT_COLOR = pygame.Color(255, 255, 255)


titleFont = pygame.font.SysFont("comicsansmsttf", 60)
FONT = pygame.font.Font(None, 32)

class GameView(View):
    # Displays the main menu

    titleText = "RK_PUZZLES_GAME"
    centerX = HALF_SCREEN_WIDTH
    centerY = HALF_SCREEN_HEIGHT

    def __init__(self, screen,bg_color):
        self.bg_color = bg_color
        View.__init__(self, screen,self.bg_color)

    def prepare(self, mood_str):
        self.transitionToState = None
        self.mood_str = mood_str

    def handleEvents(self):

        events = pygame.event.get()
        for event in events:
            print ("event type "+ str(event.type))
            if event.type == pygame.QUIT:
                exit()
            # handle the text input first
            self.textinput.handle_event(event)
            if event.type == pygame.QUIT:
                done = True

            # handle drag drop and locations

            # when ends : go back to main menu game over
            # self.transitionToState = self.MENU_ITEM_TO_VIEW_STATE[self.selectedItem]


    def render(self):
        textSurface = titleFont.render(self.titleText, True, TEXT_COLOR)
        self.screen.fill(self.bg_color)
        self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        pygame.display.flip()

    def transition(self):
        return self.transitionToState
