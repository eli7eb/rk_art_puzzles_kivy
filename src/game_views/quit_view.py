import sys
import pygame
from src.game_views.views import View
# TODO add are you sure
class QuitView(View):
    # Dummy screen that just quits the game (after quitting screen has been shown)
    def __init__(self, screen,bg_color):
        View.__init__(self, screen,bg_color)

    def prepare(self):
        sys.exit()