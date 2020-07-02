import pygame
import sys
from pygame.locals import *

BACKGROUND_COLOR = pygame.Color(0, 0, 100)
TEXT_COLOR = pygame.Color(255, 255, 255)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2

VIEW_STATE_SPLASH = 0
VIEW_STATE_MENU = 1
VIEW_STATE_GAME_A = 2
VIEW_STATE_GAME_B = 3
VIEW_STATE_OPTIONS = 4
VIEW_STATE_QUITTING = 5
VIEW_STATE_QUIT = 6


###### BASE CLASS FOR VIEWS
class View:
    def __init__(self, screen):
        self.screen = screen

    # called when transitioning to this view
    def prepare(self):
        pass

    # handle events for this view
    def handleEvents(self):
        for event in pygame.event.get():
            pass

    # render this view
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)

    # returns a view id if the game should transition to another view, None else
    def transition(self):
        return None

    def __str__(self):
        return type(self).__name__


class TextView(View):
    # Displays a text on screen
    #
    # Shows text for 2 seconds then proceed to next view
    firstRender = True
    startTime = 0

    def __init__(self, screen, text, nextView):
        View.__init__(self, screen)
        self.text = text
        self.font = pygame.font.SysFont("comicsansmsttf", 40)
        self.textSurface = self.font.render(self.text, True, TEXT_COLOR)
        self.nextView = nextView

    def prepare(self):
        self.startTime = pygame.time.get_ticks()

    def render(self):
        textSize = self.font.size(self.text)
        textX = HALF_SCREEN_WIDTH - (textSize[0] / 2)
        textY = HALF_SCREEN_HEIGHT - (textSize[1] / 2)

        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.textSurface, [textX, textY])

    def transition(self):
        nextView = None
        if pygame.time.get_ticks() - self.startTime >= 2000:
            nextView = self.nextView
        return nextView

    def __str__(self):
        return "%s(\"%s\")" % (type(self).__name__, self.text)


class MenuView(View):
    # Displays the main menu

    titleText = "Game title"
    menuItems = ['Game A', 'Game B', 'Options', 'Quit']
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

    def __init__(self, screen):
        View.__init__(self, screen)

    def prepare(self):
        self.transitionToState = None

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
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
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(textSurface, [HALF_SCREEN_WIDTH - 150, HALF_SCREEN_HEIGHT - 150])
        self.renderMenuItems(self.screen, self.selectedItem)

    def transition(self):
        return self.transitionToState


class QuitView(View):
    # Dummy screen that just quits the game (after quitting screen has been shown)
    def __init__(self, screen):
        View.__init__(self, screen)

    def prepare(self):
        sys.exit()


######################### START OF PROGRAM

pygame.init()

titleFont = pygame.font.SysFont("comicsansmsttf", 60)
menuFont = pygame.font.SysFont("comicsansmsttf", 30)
menuSelectedFont = pygame.font.SysFont("comicsansmsttf", 30, True)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

views = { \
    VIEW_STATE_SPLASH: TextView(screen, "Nonexistant games presents", VIEW_STATE_MENU),
    VIEW_STATE_MENU: MenuView(screen),
    VIEW_STATE_GAME_A: TextView(screen, "Game A screen...", VIEW_STATE_MENU),
    VIEW_STATE_GAME_B: TextView(screen, "Game B screen...", VIEW_STATE_MENU),
    VIEW_STATE_OPTIONS: TextView(screen, "Game options screen", VIEW_STATE_MENU),
    VIEW_STATE_QUITTING: TextView(screen, "Bye bye!", VIEW_STATE_QUIT),
    VIEW_STATE_QUIT: QuitView(screen)
}

currentViewId = VIEW_STATE_SPLASH
currentViewState = views[currentViewId]
currentViewState.prepare()

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
