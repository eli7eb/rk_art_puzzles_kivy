import pygame
import os
import sys
import time
import random
pygame.font.init()
from pygame.locals import *
from src.game_states.main_menu import MainMenu

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle")

# load resources
# constants
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle")
# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "rk_background.png")), (WIDTH, HEIGHT))

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    # make an object for all player info
    try_counter = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        # draw the tiles
        # draw the input tiles bar
        # draw dashboard

        pygame.display.update()

        while run:
            clock.tick(FPS)
            redraw_window()

            # check for game complete
            # check time if level requires it
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            keys = pygame.key.get_pressed()
            # check for dragging state

    def draw_text(text, font, color, x, y):
        text_obj = font.render(text,1,color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x,y)
        WIN.blit(text_obj,text_rect)

    def game():
        running = True
        while running:
            WIN.fill((0, 0, 0))

            draw_text('game', font, (255, 255, 255), WIN, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            mainClock.tick(60)


    def options():
        running = True
        while running:
            WIN.fill((0, 0, 0))

            draw_text('options', font, (255, 255, 255), WIN, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            mainClock.tick(60)

game_main_menu = MainMenu(WIN,WIDTH,HEIGHT)
game_main_menu.draw()