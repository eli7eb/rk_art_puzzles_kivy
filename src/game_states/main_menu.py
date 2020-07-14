import pygame
import os
from pygame.locals import *
import sys
from src.ui_elements.menu_button import MenuButton
# Background

class MainMenu:
    def __init__(self, win, width, height):
        self.done = False
        self.screen = win
        self.bg_width = width
        self.bg_height = height

    def draw(self):
        title_font = pygame.font.SysFont("comicsans", 70)
        run = True
        mainClock = pygame.time.Clock()
        while run:
            BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "rk_background.png")), (self.bg_width, self.bg_height))
            self.screen.blit(BG, (0, 0))
            title_label = title_font.render("Game Menu", 1, (255, 255, 255))
            font = pygame.font.SysFont(None, 20)
            # draw_text("Game Menu", font, (255, 255, 255), 20, 20)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            button_play = MenuButton("play")
            button_settings = pygame.Rect(50, 200, 200, 50)
            button_about = pygame.Rect(50, 300, 200, 50)
            if (button_about.collidepoint(mouse_x, mouse_y)):
                pass
            if (button_settings.collidepoint(mouse_x, mouse_y)):
                pass
            if (button_play.collidepoint(mouse_x, mouse_y)):
                pass
            mouse_click = False
            pygame.draw.rect(self.screen, (255, 0, 0), button_play)
            pygame.draw.rect(self.screen, (255, 0, 0), button_settings)
            pygame.draw.rect(self.screen, (255, 0, 0), button_about)

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    # TODO do not exit like this - make are you sure ? and save game stats
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            mainClock.tick(60)

    def transition(self):
        nextView = None
        if pygame.time.get_ticks() - self.startTime >= 2000:
            nextView = self.nextView
        # print loading message
        return nextView