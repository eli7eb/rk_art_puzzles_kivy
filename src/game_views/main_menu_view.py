# main menu
# get user mood or not
# return will lead to load image interstate menu
import os
import random
import pygame
from pygame.locals import *
from src.game_views.views import View
from src.game_utils.game_logger import RkLogger
from src.game_consts.game_constants import *

TEXT_COLOR = pygame.Color(255, 255, 255)
# display main menu and background
# let the user enter the mood or hit enter for random
# move to game view
# TODO options menu to let the user play with time limit or steps limit
# TODO about menu with links

# Background
bg_old_logo = pygame.image.load(os.path.join("assets", "Rijk_old_logo.png"))
#bg_logo = pygame.image.load(os.path.join("assets", "Rijk_logo.png"))
bg_logo = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Rijk_logo.png")), (int((SCREEN_WIDTH*80)/100), int(SCREEN_HEIGHT/6)))
titleFont = pygame.font.SysFont("comicsansmsttf", 60)
menuFont = pygame.font.SysFont("comicsansmsttf", 30)
menuSelectedFont = pygame.font.SysFont("comicsansmsttf", 30, True)
COLOR_INACTIVE = pygame.Color('azure2')
COLOR_ACTIVE = pygame.Color('azure1')

FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text != '':
                        logger = RkLogger.__call__().get_logger()
                        logger.info("mood entered "+self.text)
                    # self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text

class MenuView(View):
    # Displays the main menu

    titleText = "RK_PUZZLES"
    # TODO add the about menu when done
    # menuItems = ['Play', 'Options', 'About', 'Quit']

    menuItems = ['Play', 'Options', 'Quit']
    selectedItem = 0
    centerX = HALF_SCREEN_WIDTH
    centerY = HALF_SCREEN_HEIGHT

    MENU_LOADING = 0
    MENU_ITEM_OPTIONS = 1
    MENU_ITEM_QUIT = 2

    MENU_ITEM_TO_VIEW_STATE = {
        MENU_LOADING: VIEW_STATE_LOADING,
        MENU_ITEM_OPTIONS: VIEW_STATE_OPTIONS,
        MENU_ITEM_QUIT: VIEW_STATE_QUITTING,
    }

    def __init__(self, screen,bg_color):
        self.bg_color = bg_color
        self.textinput = InputBox(self.centerX, (self.centerY - 60), 140, 32)
        self.mood_str = ''
        self.mood_str_1 = ''
        self.loading_msg = ''
        View.__init__(self, screen,self.bg_color)

    def prepare(self):
        self.transitionToState = None

    def handleEvents(self):

        events = pygame.event.get()
        for event in events:
            logger = RkLogger.__call__().get_logger()
            logger.info("event type "+ str(event.type))
            if event.type == pygame.QUIT:
                exit()
            # handle the text input first
            self.textinput.handle_event(event)

            logger.info("textinput "+self.textinput.text)

            self.mood_str = self.textinput.text
            self.mood_str_1 = self.textinput.get_text()
            if event.type == pygame.QUIT:
                done = True


            if event.type == pygame.KEYDOWN:
                if event.key == K_DOWN:
                    self.selectedItem = (self.selectedItem + 1) % len(self.menuItems)
                if event.key == K_UP:
                    self.selectedItem = (self.selectedItem - 1) % len(self.menuItems)
                if event.key == K_RETURN:
                    # check to see if there is anything in the text
                    logger.info("K_RETURN mood_str "+self.textinput.text)
                    logger.info("K_RETURN clicked menu item "+self.menuItems[self.selectedItem])
                    # set loading message
                    if self.menuItems[self.selectedItem] == 'Play':
                        self.transitionToState = VIEW_STATE_LOADING
                    else:
                        self.transitionToState = self.MENU_ITEM_TO_VIEW_STATE[self.selectedItem]

    def renderMenuItems(self, screen, selectedItem):
        index = 0

        clock = pygame.time.Clock()


        for menuItemText in self.menuItems:
            textX = self.centerX - 100
            textY = self.centerY - 50 + (40 * index)

            if self.selectedItem == index:
                textSurface = menuSelectedFont.render(menuItemText, True, TEXT_COLOR)
                pygame.draw.circle(self.screen, TEXT_COLOR, (int(textX - 15), int(textY + 15)), 5)
            else:
                textSurface = menuFont.render(menuItemText, True, TEXT_COLOR)

            self.screen.blit(textSurface, [textX, textY])
            index += 1

    def generate_random_color(self):
        start = 0
        stop = 255
        # 798891
        red = random.randint(start, stop)
        green = random.randint(start, stop)
        blue = random.randint(start, stop)
        return pygame.Color(red,green,blue)

    def render(self):
        textSurface = titleFont.render(self.titleText, True, TEXT_COLOR)
        x = int(SCREEN_WIDTH/2 - ((SCREEN_WIDTH*80)/100)/2)
        self.screen.blit(bg_logo, ( x, 10))
        # when mood is entered change the display
        self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        self.renderMenuItems(self.screen, self.selectedItem)
        self.textinput.update()
        self.textinput.draw(self.screen)
        pygame.display.flip()

    def clean(self):
        transparent = (127, 127, 127)
        self.screen.fill(transparent)

    def transition(self):
        return self.transitionToState
