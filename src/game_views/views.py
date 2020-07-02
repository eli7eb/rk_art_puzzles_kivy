import pygame

class View:
    def __init__(self, screen, bg_color):
        self.screen = screen
        self.bg_color = bg_color

    # called when transitioning to this view
    def prepare(self):
        pass

    # handle events for this view
    def handleEvents(self):
        for event in pygame.event.get():
            pass

    # render this view
    def render(self):
        self.screen.fill(self.bg_color)

    # returns a view id if the game should transition to another view, None else
    def transition(self):
        return None

    def __str__(self):
        return type(self).__name__
