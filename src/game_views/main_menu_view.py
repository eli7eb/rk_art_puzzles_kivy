# main menu
# get user mood or not
# return will lead to load image interstate menu

import pygame
from pygame.locals import *
from src.game_views.views import View

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
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
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
                    print(self.text)
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
        self.textinput = InputBox(self.centerX, (self.centerY - 60), 140, 32)
        self.mood_str = ''
        self.mood_str_1 = ''
        View.__init__(self, screen,self.bg_color)

    def prepare(self):
        self.transitionToState = None

    def handleEvents(self):

        events = pygame.event.get()
        for event in events:
            print ("event type "+ str(event.type))
            if event.type == pygame.QUIT:
                exit()
            # handle the text input first
            self.textinput.handle_event(event)

            print("textinput '%s'" % self.textinput.text)
            print("before mood_str '%s'" % self.mood_str)
            print("before mood_str_1 '%s'" % self.mood_str_1)
            self.mood_str = self.textinput.text
            self.mood_str_1 = self.textinput.get_text()
            print("textinput '%s'" % self.textinput.text)
            print("mood_str '%s'" % self.mood_str)
            print("mood_str_1 '%s'" % self.mood_str_1)
            if event.type == pygame.QUIT:
                done = True


            if event.type == pygame.KEYDOWN:
                if event.key == K_DOWN:
                    self.selectedItem = (self.selectedItem + 1) % len(self.menuItems)
                if event.key == K_UP:
                    self.selectedItem = (self.selectedItem - 1) % len(self.menuItems)
                if event.key == K_RETURN:
                    # check to see if there is anything in the text
                    print("K_RETURN mood_str '%s'" % self.textinput.text)
                    print("K_RETURN clicked menu item '%s'" % self.menuItems[self.selectedItem])
                    self.transitionToState = self.MENU_ITEM_TO_VIEW_STATE[self.selectedItem]

    def renderMenuItems(self, screen, selectedItem):
        index = 0

        # screen = pygame.display.set_mode((1000, 200))
        clock = pygame.time.Clock()

        # Blit its surface onto the screen
        # Create TextInput-object


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

    def render(self):
        textSurface = titleFont.render(self.titleText, True, TEXT_COLOR)
        self.screen.fill(self.bg_color)
        self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        self.renderMenuItems(self.screen, self.selectedItem)
        self.textinput.update()
        self.textinput.draw(self.screen)
        pygame.display.flip()

    def transition(self):
        return self.transitionToState
