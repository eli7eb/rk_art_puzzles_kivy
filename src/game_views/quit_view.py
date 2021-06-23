import sys
import pygame
from src.game_views.views import View
# TODO add are you sure
class QuitView(View):
    # Dummy game_screens that just quits the game (after quitting game_screens has been shown)
    def __init__(self, screen,bg_color):
        View.__init__(self, screen,bg_color)

    def prepare(self):
        sys.exit()