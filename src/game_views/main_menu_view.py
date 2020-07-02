import pygame
from pygame.locals import *
from src.game_views.views import View
from src.ui_elements.pygame_text_input import TextInput
VIEW_STATE_SPLASH = 0
VIEW_STATE_MENU = 1
VIEW_STATE_GAME_A = 2
VIEW_STATE_GAME_B = 3
VIEW_STATE_OPTIONS = 4
VIEW_STATE_QUITTING = 5
VIEW_STATE_QUIT = 6
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2
TEXT_COLOR = pygame.Color(255, 255, 255)


titleFont = pygame.font.SysFont("comicsansmsttf", 60)
menuFont = pygame.font.SysFont("comicsansmsttf", 30)
menuSelectedFont = pygame.font.SysFont("comicsansmsttf", 30, True)

class MenuView(View):
    # Displays the main menu

    titleText = "RK_PUZZLES"
    menuItems = ['Play', 'Options', 'About', 'Quit']
    selectedItem = 0
    centerX = HALF_SCREEN_WIDTH
    centerY = HALF_SCREEN_HEIGHT

    MENU_ITEM_GAME_A = 0
    MENU_ITEM_GAME_B = 1
    MENU_ITEM_OPTIONS = 2
    MENU_ITEM_QUIT = 3

    MENU_ITEM_TO_VIEW_STATE = {
        MENU_ITEM_GAME_A: VIEW_STATE_GAME_A,
        MENU_ITEM_GAME_B: VIEW_STATE_GAME_B,
        MENU_ITEM_OPTIONS: VIEW_STATE_OPTIONS,
        MENU_ITEM_QUIT: VIEW_STATE_QUITTING,
    }

    def __init__(self, screen,bg_color):
        self.bg_color = bg_color
        # Create TextInput-object
        self.textinput = TextInput()

        View.__init__(self, screen,self.bg_color)

    def prepare(self):
        self.transitionToState = None

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # handle return on the text input field for mood
            if self.textinput.update(pygame.event.get()):
                print(self.textinput.get_text())
            if event.type == pygame.KEYDOWN:
                if event.key == K_DOWN:
                    self.selectedItem = (self.selectedItem + 1) % len(self.menuItems)
                if event.key == K_UP:
                    self.selectedItem = (self.selectedItem - 1) % len(self.menuItems)
                if event.key == K_RETURN:
                    # print("clicked menu item '%s'" % self.menuItems[self.selectedItem])
                    self.transitionToState = self.MENU_ITEM_TO_VIEW_STATE[self.selectedItem]

    def renderMenuItems(self, screen, selectedItem):
        index = 0

        screen = pygame.display.set_mode((1000, 200))
        clock = pygame.time.Clock()

        # Blit its surface onto the screen
        self.screen.blit(self.textinput.get_surface(), (10, 10))

        for menuItemText in self.menuItems:
            textX = self.centerX - 100
            textY = self.centerY - 50 + (40 * index)
            if self.selectedItem == index:
                textSurface = menuSelectedFont.render(menuItemText, True, TEXT_COLOR)
                # pygame.draw.circle(self.screen, TEXT_COLOR, textX - 15, textY + 15, 5)
            else:
                textSurface = menuFont.render(menuItemText, True, TEXT_COLOR)
            self.screen.blit(textSurface, [textX, textY])
            index += 1

    def render(self):
        textSurface = titleFont.render(self.titleText, True, TEXT_COLOR)
        self.screen.fill(self.bg_color)
        self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        self.renderMenuItems(self.screen, self.selectedItem)

    def transition(self):
        return self.transitionToState
