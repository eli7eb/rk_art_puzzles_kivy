import pygame

import sys
import time
import random


from src.game_consts.game_constants import LEVEL_BEGIN

pygame.font.init()
from pygame.locals import *
from src.game_views.load_resource_view import LoadingView
from src.game_views.text_view import TextView
from src.game_views.main_menu_view import MenuView
from src.game_views.quit_view import QuitView
from src.game_views.game_view import GameView
from src.game_consts.game_constants import *
from src.game_utils.game_logger import RkLogger
from src.game_consts.game_constants import *

# TODO make the players think before trying so reward on success at first attempt
# TODO and minus score on successive same tries
# TODO non equal tiles for next version



# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
pygame.display.set_caption("Puzzle")
level = levels[1]
# load resources


titleFont = pygame.font.SysFont("comicsansmsttf", 60)
menuFont = pygame.font.SysFont("comicsansmsttf", 30)
menuSelectedFont = pygame.font.SysFont("comicsansmsttf", 30, True)

BACKGROUND_COLOR = pygame.Color(121,136,145,57)
BACKGROUND_COLOR_LOADING = pygame.Color(40,67,90,35)

TEXT_COLOR = pygame.Color(255, 255, 255)
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
mood_str = ""

views = { \
    VIEW_STATE_SPLASH: TextView(screen, "RK games presents", VIEW_STATE_MENU,BACKGROUND_COLOR),
    VIEW_STATE_MENU: MenuView(screen,BACKGROUND_COLOR),
    VIEW_STATE_LOADING: LoadingView(screen, BACKGROUND_COLOR_LOADING, "intermid"),
    VIEW_STATE_GAME_A: GameView(screen, level),
    VIEW_STATE_GAME_B: TextView(screen, "Game B screen...", VIEW_STATE_MENU,BACKGROUND_COLOR),
    VIEW_STATE_OPTIONS: TextView(screen, "Game options screen", VIEW_STATE_MENU,BACKGROUND_COLOR),
    VIEW_STATE_QUITTING: TextView(screen, "Bye bye!", VIEW_STATE_QUIT,BACKGROUND_COLOR),
    VIEW_STATE_QUIT: QuitView(screen,BACKGROUND_COLOR)
}


def init_logger():
    logger = RkLogger.__call__().get_logger()
    logger.info("Hello, Logger")

init_logger()
currentViewId = VIEW_STATE_SPLASH
currentViewState = views[currentViewId]
currentViewState.prepare()
logger = RkLogger.__call__().get_logger()
logger.info("Showing %s" % currentViewState)

while True:

    currentViewState.handleEvents()
    currentViewState.render();

    pygame.display.flip()
    pygame.time.delay(100)

    nextViewId = currentViewState.transition()
    if nextViewId:
        logger.info("Transition from %s -> %s" % (currentViewState, views[nextViewId]))
        if currentViewId == VIEW_STATE_SPLASH:
            currentViewState.clean()
        elif currentViewId == VIEW_STATE_MENU:
            mood_str = currentViewState.textinput.get_text()
            currentViewState.clean()
        elif currentViewId == VIEW_STATE_LOADING:
            image_grid_data = currentViewState.get_image_grid()
            image_data = currentViewState.get_image()
            title,long_title = currentViewState.get_image_info()
            currentViewState.clean()

        currentViewId = nextViewId
        currentViewState = views[currentViewId]
        if currentViewId == VIEW_STATE_LOADING:
            currentViewState.prepare(mood_str,level)
        elif currentViewId == VIEW_STATE_GAME_A:
            currentViewState.prepare(image_grid_data, image_data, title, long_title)
        else:
            currentViewState.prepare()

def main():
    run = True
    FPS = 60
    lives = 5
    # make an object for all player info
    try_counter = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    clock = pygame.time.Clock()
    def redraw_window():
        # WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (SCREEN_WIDTH - level_label.get_width() - 10, 10))
        # draw the tiles
        # draw the input tiles bar
        # draw dashboard

        pygame.display.update()

        while run:
            clock.tick(FPS)
            redraw_window()

            # check for game complete
            # check time if level requires it
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            keys = pygame.key.get_pressed()
            # check for dragging state

    def draw_text(text, font, color, x, y):
        text_obj = font.render(text,1,color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x,y)
        screen.blit(text_obj,text_rect)

    def game():
        running = True
        while running:
            screen.fill((0, 0, 0))

            draw_text('game', font, (255, 255, 255), screen, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            mainClock.tick(60)


    def options():
        running = True
        while running:
            screen.fill((0, 0, 0))

            draw_text('options', font, (255, 255, 255), screen, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            mainClock.tick(60)


currentViewId = VIEW_STATE_SPLASH
currentViewState = views[currentViewId]
currentViewState.prepare()
init_logger()
print("Showing %s" % currentViewState)

while True:

    currentViewState.handleEvents()
    currentViewState.render();

    pygame.display.flip()
    pygame.time.delay(100)

    nextViewId = currentViewState.transition()
    if nextViewId:
        print("Transition from %s -> %s" % (currentViewState, views[nextViewId]))
        currentViewId = nextViewId
        currentViewState = views[currentViewId]
        currentViewState.prepare()
