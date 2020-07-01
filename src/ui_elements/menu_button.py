# create and return a button to the menu
import pygame
from pygame.locals import *

GREY = (128, 128, 128)

# TODO , x, y, w, h, ic, ac, action=None

class MenuButton:
    def __init__(self,msg):
        self.done = False
        self.smallText = pygame.font.SysFont("comicsansms", 20)
        self.textSurf, self.textRect = self.text_objects(msg, self.smallText)

    # create button text and bg and action
    # text is in the center of the rect
    def text_objects(text, font):
        textSurface = font.render(text, True, GREY)
        return textSurface, textSurface.get_rect()


