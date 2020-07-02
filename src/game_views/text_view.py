import pygame
from src.game_views.views import View

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2
TEXT_COLOR = pygame.Color(255, 255, 255)

class TextView(View):
    # Displays a text on screen
    #
    # Shows text for 2 seconds then proceed to next view
    firstRender = True
    startTime = 0

    def __init__(self, screen, text, nextView, bg_color):
        View.__init__(self, screen, bg_color)
        self.text = text
        self.font = pygame.font.SysFont("comicsansmsttf", 40)
        self.textSurface = self.font.render(self.text, True, TEXT_COLOR)
        self.nextView = nextView
        self.bg_color = bg_color

    def prepare(self):
        self.startTime = pygame.time.get_ticks()

    def render(self):
        textSize = self.font.size(self.text)
        textX = HALF_SCREEN_WIDTH - (textSize[0] / 2)
        textY = HALF_SCREEN_HEIGHT - (textSize[1] / 2)

        self.screen.fill(self.bg_color)
        self.screen.blit(self.textSurface, [textX, textY])

    def transition(self):
        nextView = None
        if pygame.time.get_ticks() - self.startTime >= 2000:
            nextView = self.nextView
        return nextView

    def __str__(self):
        return "%s(\"%s\")" % (type(self).__name__, self.text)

