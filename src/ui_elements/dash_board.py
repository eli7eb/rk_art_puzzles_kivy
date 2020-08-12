# dashboard class
# dashboard displays game status and info
# art work with link to more info
# tiles status how many left
# time passed
# round number
# player and leader board info

import pygame
from pygame.locals import *

TEXT_COLOR = pygame.Color(255, 255, 255)


class DashBoard:
    def __init__(self, screen, text_pos_x, text_pos_y, spacer_size):
        self.screen = screen
        self.text_pos_x = text_pos_x
        self.text_pos_y = text_pos_y
        self.spacer_size = spacer_size

    def prepare(self):
        self.font = pygame.font.SysFont("comicsansmsttf", 40)

    # art_dict.title and art_dict.longTitle
    # TODO set the title to fit in the correct space with new line - break the line
    def set_title_info(self, title, long_title):
        self.font = pygame.font.SysFont("comicsansmsttf", 20)
        self.textSurfaceTitle = self.font.render(title, True, TEXT_COLOR)
        self.screen.blit(self.textSurfaceTitle, [self.spacer_size, self.text_pos_y+30])
        self.textSurfaceLongTitle = self.font.render(long_title, True, TEXT_COLOR)
        self.screen.blit(self.textSurfaceLongTitle, [self.spacer_size, self.text_pos_y + 50])

    # play time tiles left to go
    # how many moves till now
    def set_play_time(self):
        self.font = pygame.font.SysFont("comicsansmsttf", 20)
        self.textSurfaceTitle = self.font.render('time and steps', True, TEXT_COLOR)
        self.screen.blit(self.textSurfaceTitle, [self.spacer_size, self.text_pos_y + 70])
# text_field_1 = TextField(90, 'TextField1')
# text_field_2 = TextField(90, 'TextField2')
# text_field_3 = TextField(90, 'TextField3')
# h_stack = HStack([text_field_1, text_field_2, text_field_3])
# v_stack = VStack([text_field_1, text_field_2, text_field_3])
# text_field_2.set_content('Field2')